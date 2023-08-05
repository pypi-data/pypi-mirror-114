from ..clients.metaApi.synchronizationListener import SynchronizationListener
from .models import MetatraderAccountInformation, MetatraderPosition, MetatraderOrder, \
    MetatraderSymbolSpecification, MetatraderSymbolPrice
import functools
from typing import List, Dict, Optional
from typing_extensions import TypedDict
import asyncio
from datetime import datetime


class TerminalStateDict(TypedDict):
    connected: bool
    connectedToBroker: bool
    accountInformation: Optional[dict]
    positions: List[dict]
    orders: List[dict]
    specifications: List[dict]
    specificationsBySymbol: dict
    pricesBySymbol: dict
    completedOrders: dict
    removedPositions: dict
    ordersInitialized: bool
    positionsInitialized: bool
    lastUpdateTime: float


class TerminalState(SynchronizationListener):
    """Responsible for storing a local copy of remote terminal state."""

    def __init__(self):
        """Inits the instance of terminal state class"""
        super().__init__()
        self._stateByInstanceIndex = {}
        self._waitForPriceResolves = {}

    @property
    def connected(self) -> bool:
        """Returns true if MetaApi has connected to MetaTrader terminal.

        Returns:
            Whether MetaApi has connected to MetaTrader terminal.
        """
        return True in list(map(lambda instance: instance['connected'], self._stateByInstanceIndex.values()))

    @property
    def connected_to_broker(self) -> bool:
        """Returns true if MetaApi has connected to MetaTrader terminal and MetaTrader terminal is connected to broker

        Returns:
             Whether MetaApi has connected to MetaTrader terminal and MetaTrader terminal is connected to broker
        """
        return True in list(map(lambda instance: instance['connectedToBroker'], self._stateByInstanceIndex.values()))

    @property
    def account_information(self) -> MetatraderAccountInformation:
        """Returns a local copy of account information.

        Returns:
            Local copy of account information.
        """
        return self._get_best_state()['accountInformation']

    @property
    def positions(self) -> List[MetatraderPosition]:
        """Returns a local copy of MetaTrader positions opened.

        Returns:
            A local copy of MetaTrader positions opened.
        """
        return self._get_best_state()['positions']

    @property
    def orders(self) -> List[MetatraderOrder]:
        """Returns a local copy of MetaTrader orders opened.

        Returns:
            A local copy of MetaTrader orders opened.
        """
        return self._get_best_state()['orders']

    @property
    def specifications(self) -> List[MetatraderSymbolSpecification]:
        """Returns a local copy of symbol specifications available in MetaTrader trading terminal.

        Returns:
             A local copy of symbol specifications available in MetaTrader trading terminal.
        """
        return self._get_best_state()['specifications']

    def specification(self, symbol: str) -> MetatraderSymbolSpecification:
        """Returns MetaTrader symbol specification by symbol.

        Args:
            symbol: Symbol (e.g. currency pair or an index).

        Returns:
            MetatraderSymbolSpecification found or undefined if specification for a symbol is not found.
        """
        state = self._get_best_state()
        return state['specificationsBySymbol'][symbol] if \
            (symbol in state['specificationsBySymbol']) else None

    def price(self, symbol: str) -> MetatraderSymbolPrice:
        """Returns MetaTrader symbol price by symbol.

        Args:
            symbol: Symbol (e.g. currency pair or an index).

        Returns:
            MetatraderSymbolPrice found or undefined if price for a symbol is not found.
        """
        state = self._get_best_state()
        return state['pricesBySymbol'][symbol] if \
            (symbol in state['pricesBySymbol']) else None

    async def wait_for_price(self, symbol: str, timeout_in_seconds: float = 30):
        """Waits for price to be received.

        Args:
            symbol: Symbol (e.g. currency pair or an index).
            timeout_in_seconds: Timeout in seconds, default is 30.

        Returns:
            A coroutine resolving with price or undefined if price has not been received.
        """
        self._waitForPriceResolves[symbol] = self._waitForPriceResolves[symbol] if symbol in \
            self._waitForPriceResolves else []
        if self.price(symbol) is None:
            future = asyncio.Future
            self._waitForPriceResolves[symbol].append(future)
            await asyncio.wait_for(future, timeout=timeout_in_seconds)

        return self.price(symbol)

    async def on_connected(self, instance_index: str, replicas: int):
        """Invoked when connection to MetaTrader terminal established.

        Args:
            instance_index: Index of an account instance connected.
            replicas: Number of account replicas launched.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        self._get_state(instance_index)['connected'] = True

    async def on_disconnected(self, instance_index: str):
        """Invoked when connection to MetaTrader terminal terminated.

        Args:
            instance_index: Index of an account instance connected.

        Returns:
             A coroutine which resolves when the asynchronous event is processed.
        """
        state = self._get_state(instance_index)
        state['connected'] = False
        state['connectedToBroker'] = False

    async def on_broker_connection_status_changed(self, instance_index: str, connected: bool):
        """Invoked when broker connection status have changed.

        Args:
            instance_index: Index of an account instance connected.
            connected: Is MetaTrader terminal is connected to broker.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        self._get_state(instance_index)['connectedToBroker'] = connected

    async def on_synchronization_started(self, instance_index: str):
        """Invoked when MetaTrader terminal state synchronization is started.

        Args:
            instance_index: Index of an account instance connected.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        state = self._get_state(instance_index)
        state['accountInformation'] = None
        state['positions'] = []
        state['orders'] = []
        state['specifications'] = []
        state['specificationsBySymbol'] = {}
        state['pricesBySymbol'] = {}
        state['completedOrders'] = {}
        state['removedPositions'] = {}
        state['ordersInitialized'] = False
        state['positionsInitialized'] = False

    async def on_account_information_updated(self, instance_index: str,
                                             account_information: MetatraderAccountInformation):
        """Invoked when MetaTrader position is updated.

        Args:
            instance_index: Index of an account instance connected.
            account_information: Updated MetaTrader position.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        self._get_state(instance_index)['accountInformation'] = account_information

    async def on_positions_replaced(self, instance_index: str, positions: List[MetatraderPosition]):
        """Invoked when the positions are replaced as a result of initial terminal state synchronization.

        Args:
            instance_index: Index of an account instance connected.
            positions: Updated array of positions.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        state = self._get_state(instance_index)
        state['positions'] = positions
        state['removedPositions'] = {}
        state['positionsInitialized'] = True

    async def on_position_updated(self, instance_index: str, position: MetatraderPosition):
        """Invoked when MetaTrader position is updated.

        Args:
            instance_index: Index of an account instance connected.
            position: Updated MetaTrader position.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        state = self._get_state(instance_index)
        is_exists = False
        for i in range(len(state['positions'])):
            if state['positions'][i]['id'] == position['id']:
                state['positions'][i] = position
                is_exists = True
                break
        if (not is_exists) and (position['id'] not in state['removedPositions']):
            state['positions'].append(position)

    async def on_position_removed(self, instance_index: str, position_id: str):
        """Invoked when MetaTrader position is removed.

        Args:
            instance_index: Index of an account instance connected.
            position_id: Removed MetaTrader position id.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        state = self._get_state(instance_index)
        position = next((p for p in state['positions'] if p['id'] == position_id), None)
        if position is None:
            for key in state['removedPositions']:
                e = state['removedPositions'][key]
                if e + 5 * 60 < datetime.now().timestamp():
                    del state['removedPositions'][key]
            state['removedPositions'][position_id] = datetime.now().timestamp()
        else:
            state['positions'] = list(filter(lambda p: p['id'] != position_id, state['positions']))

    async def on_orders_replaced(self, instance_index: str, orders: List[MetatraderOrder]):
        """Invoked when the orders are replaced as a result of initial terminal state synchronization.

        Args:
            instance_index: Index of an account instance connected.
            orders: Updated array of orders.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        state = self._get_state(instance_index)
        state['orders'] = orders
        state['completedOrders'] = {}
        state['ordersInitialized'] = True

    async def on_order_updated(self, instance_index: str, order: MetatraderOrder):
        """Invoked when MetaTrader order is updated.

        Args:
            instance_index: Index of an account instance connected.
            order: Updated MetaTrader order.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        state = self._get_state(instance_index)
        is_exists = False
        for i in range(len(state['orders'])):
            if state['orders'][i]['id'] == order['id']:
                state['orders'][i] = order
                is_exists = True
                break
        if (not is_exists) and (order['id'] not in state['completedOrders']):
            state['orders'].append(order)

    async def on_order_completed(self, instance_index: str, order_id: str):
        """Invoked when MetaTrader order is completed (executed or canceled).

        Args:
            instance_index: Index of an account instance connected.
            order_id: Completed MetaTrader order id.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        state = self._get_state(instance_index)
        order = next((p for p in state['orders'] if p['id'] == order_id), None)
        if order is None:
            for key in list(state['completedOrders'].keys()):
                e = state['completedOrders'][key]
                if e + 5 * 60 < datetime.now().timestamp():
                    del state['completedOrders'][key]
            state['completedOrders'][order_id] = datetime.now().timestamp()
        else:
            state['orders'] = list(filter(lambda o: o['id'] != order_id, state['orders']))

    async def on_symbol_specifications_updated(self, instance_index: str,
                                               specifications: List[MetatraderSymbolSpecification],
                                               removed_symbols: List[str]):
        """Invoked when a symbol specifications were updated.

        Args:
            instance_index: Index of an account instance connected.
            specifications: Updated MetaTrader symbol specification.
            removed_symbols: Removed symbols.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        state = self._get_state(instance_index)
        for specification in specifications:
            for i in range(len(state['specifications'])):
                if state['specifications'][i]['symbol'] == specification['symbol']:
                    state['specifications'][i] = specification
                    break
            else:
                state['specifications'].append(specification)
            state['specificationsBySymbol'][specification['symbol']] = specification
        state['specifications'] = list(filter(lambda s: s['symbol'] not in removed_symbols, state['specifications']))
        for symbol in removed_symbols:
            if symbol in state['specificationsBySymbol']:
                del state['specificationsBySymbol'][symbol]

    async def on_symbol_prices_updated(self, instance_index: str, prices: List[MetatraderSymbolPrice],
                                       equity: float = None, margin: float = None, free_margin: float = None,
                                       margin_level: float = None, account_currency_exchange_rate: float = None):
        """Invoked when prices for several symbols were updated.

        Args:
            instance_index: Index of an account instance connected.
            prices: Updated MetaTrader symbol prices.
            equity: Account liquidation value.
            margin: Margin used.
            free_margin: Free margin.
            margin_level: Margin level calculated as % of equity/margin.
            account_currency_exchange_rate: Current exchange rate of account currency into USD.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        state = self._get_state(instance_index)
        state['lastUpdateTime'] = max(map(lambda p: p['time'].timestamp(), prices)) if len(prices) else 0
        prices_initialized = False
        if prices:
            for price in prices:
                state['pricesBySymbol'][price['symbol']] = price
                positions = list(filter(lambda p: p['symbol'] == price['symbol'], state['positions']))
                other_positions = list(filter(lambda p: p['symbol'] != price['symbol'], state['positions']))
                orders = list(filter(lambda o: o['symbol'] == price['symbol'], state['orders']))
                prices_initialized = True
                for position in other_positions:
                    if position['symbol'] in state['pricesBySymbol']:
                        p = state['pricesBySymbol'][position['symbol']]
                        if 'unrealizedProfit' not in position:
                            self._update_position_profits(position, p)
                    else:
                        prices_initialized = False
                for position in positions:
                    self._update_position_profits(position, price)
                for order in orders:
                    order['currentPrice'] = price['ask'] if (order['type'] == 'ORDER_TYPE_BUY' or
                                                             order['type'] == 'ORDER_TYPE_BUY_LIMIT' or
                                                             order['type'] == 'ORDER_TYPE_BUY_STOP' or
                                                             order['type'] == 'ORDER_TYPE_BUY_STOP_LIMIT') else \
                        price['bid']
                price_resolves = self._waitForPriceResolves[price['symbol']] if price['symbol'] in \
                    self._waitForPriceResolves else []
                if len(price_resolves):
                    resolve: asyncio.Future
                    for resolve in price_resolves:
                        if not resolve.done():
                            resolve.set_result(True)
                    del self._waitForPriceResolves[price['symbol']]
        if state['accountInformation']:
            if state['positionsInitialized'] and prices_initialized:
                if state['accountInformation']['platform'] == 'mt5':
                    state['accountInformation']['equity'] = equity if equity is not None else \
                        state['accountInformation']['balance'] + \
                        functools.reduce(lambda a, b: a + round((b['unrealizedProfit'] if 'unrealizedProfit' in b and
                                                                 b['unrealizedProfit'] is not None
                                                                 else 0) * 100) / 100 +
                                         round((b['swap'] if 'swap' in b and b['swap'] is not None
                                                else 0) * 100) / 100, state['positions'], 0)
                else:
                    state['accountInformation']['equity'] = equity if equity is not None else \
                        state['accountInformation']['balance'] + \
                        functools.reduce(
                        lambda a, b: a + round((b['swap'] if 'swap' in b and b['swap'] is not None
                                                else 0) * 100) / 100 +
                        round((b['commission'] if 'commission' in b and b['commission'] is not None
                               else 0) * 100) / 100 +
                        round((b['unrealizedProfit'] if 'unrealizedProfit' in b and b['unrealizedProfit'] is not None
                               else 0) * 100) / 100,
                            state['positions'], 0)
                state['accountInformation']['equity'] = round(state['accountInformation']['equity'] * 100) / 100
            else:
                state['accountInformation']['equity'] = equity if equity else (
                    state['accountInformation']['equity'] if 'equity' in state['accountInformation'] else None)
            state['accountInformation']['margin'] = margin if margin else (
                state['accountInformation']['margin'] if 'margin' in state['accountInformation'] else None)
            state['accountInformation']['freeMargin'] = free_margin if free_margin else (
                state['accountInformation']['freeMargin'] if 'freeMargin' in state['accountInformation'] else None)
            state['accountInformation']['marginLevel'] = margin_level if free_margin else (
                state['accountInformation']['marginLevel'] if 'marginLevel' in state['accountInformation'] else None)

    async def on_stream_closed(self, instance_index: str):
        """Invoked when a stream for an instance index is closed.

        Args:
            instance_index: Index of an account instance connected.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        if instance_index in self._stateByInstanceIndex:
            del self._stateByInstanceIndex[instance_index]

    def _update_position_profits(self, position: Dict, price: Dict):
        specification = self.specification(position['symbol'])
        if specification:
            multiplier = pow(10, specification['digits'])
            if 'profit' in position:
                position['profit'] = round(position['profit'] * multiplier) / multiplier
            if 'unrealizedProfit' not in position or 'realizedProfit' not in position:
                position['unrealizedProfit'] = (1 if (position['type'] == 'POSITION_TYPE_BUY') else -1) * \
                                               (position['currentPrice'] - position['openPrice']) * \
                                               position['currentTickValue'] * position['volume'] / \
                                               specification['tickSize']
                position['unrealizedProfit'] = round(position['unrealizedProfit'] * multiplier) / multiplier
                position['realizedProfit'] = position['profit'] - position['unrealizedProfit']
            new_position_price = price['bid'] if (position['type'] == 'POSITION_TYPE_BUY') else price['ask']
            is_profitable = (1 if (position['type'] == 'POSITION_TYPE_BUY') else -1) * (new_position_price -
                                                                                        position['openPrice'])
            current_tick_value = price['profitTickValue'] if (is_profitable > 0) else price['lossTickValue']
            unrealized_profit = (1 if (position['type'] == 'POSITION_TYPE_BUY') else -1) * \
                                (new_position_price - position['openPrice']) * current_tick_value * \
                position['volume'] / specification['tickSize']
            unrealized_profit = round(unrealized_profit * multiplier) / multiplier
            position['unrealizedProfit'] = unrealized_profit
            position['profit'] = position['unrealizedProfit'] + position['realizedProfit']
            position['profit'] = round(position['profit'] * multiplier) / multiplier
            position['currentPrice'] = new_position_price
            position['currentTickValue'] = current_tick_value

    def _get_state(self, instance_index: str) -> TerminalStateDict:
        if str(instance_index) not in self._stateByInstanceIndex:
            self._stateByInstanceIndex[str(instance_index)] = self._construct_terminal_state()
        return self._stateByInstanceIndex[str(instance_index)]

    def _construct_terminal_state(self) -> TerminalStateDict:
        return {
            'connected': False,
            'connectedToBroker': False,
            'accountInformation': None,
            'positions': [],
            'orders': [],
            'specifications': [],
            'specificationsBySymbol': {},
            'pricesBySymbol': {},
            'completedOrders': {},
            'removedPositions': {},
            'ordersInitialized': False,
            'positionsInitialized': False,
            'lastUpdateTime': 0
        }

    def _get_best_state(self) -> TerminalStateDict:
        result = None
        max_update_time = None
        for state in self._stateByInstanceIndex.values():
            if max_update_time is None or max_update_time < state['lastUpdateTime']:
                max_update_time = state['lastUpdateTime']
                result = state
        return result or self._construct_terminal_state()
