from ..clients.metaApi.synchronizationListener import SynchronizationListener
from ..clients.metaApi.reconnectListener import ReconnectListener
from ..clients.metaApi.metaApiWebsocket_client import MetaApiWebsocketClient
from .terminalState import TerminalState
from .connectionHealthMonitor import ConnectionHealthMonitor
from .memoryHistoryStorage import MemoryHistoryStorage
from .metatraderAccountModel import MetatraderAccountModel
from .connectionRegistryModel import ConnectionRegistryModel
from .historyStorage import HistoryStorage
from ..clients.timeoutException import TimeoutException
from .models import random_id, format_error, MetatraderSymbolSpecification, MetatraderAccountInformation, \
    MetatraderPosition, MetatraderOrder, MetatraderHistoryOrders, MetatraderDeals, MetatraderTradeResponse, \
    MetatraderSymbolPrice, MarketTradeOptions, PendingTradeOptions, MarketDataSubscription, MarketDataUnsubscription, \
    MetatraderCandle, MetatraderTick, MetatraderBook, StopOptions
from datetime import datetime, timedelta
from typing import Coroutine, List, Optional, Dict
from typing_extensions import TypedDict
from functools import reduce
import pytz
import asyncio


class MetaApiConnectionDict(TypedDict):
    instanceIndex: int
    ordersSynchronized: dict
    dealsSynchronized: dict
    shouldSynchronize: Optional[str]
    synchronizationRetryIntervalInSeconds: float
    synchronized: bool
    lastDisconnectedSynchronizationId: Optional[str]
    lastSynchronizationId: Optional[str]
    disconnected: bool


class SynchronizationOptions(TypedDict):
    instanceIndex: Optional[int]
    """Index of an account instance to ensure synchronization on, default is to wait for the first instance to
    synchronize."""
    applicationPattern: Optional[str]
    """Application regular expression pattern, default is .*"""
    synchronizationId: Optional[str]
    """synchronization id, last synchronization request id will be used by default"""
    timeoutInSeconds: Optional[float]
    """Wait timeout in seconds, default is 5m."""
    intervalInMilliseconds: Optional[float]
    """Interval between account reloads while waiting for a change, default is 1s."""


class MetaApiConnection(SynchronizationListener, ReconnectListener):
    """Exposes MetaApi MetaTrader API connection to consumers."""

    def __init__(self, websocket_client: MetaApiWebsocketClient, account: MetatraderAccountModel,
                 history_storage: HistoryStorage or None, connection_registry: ConnectionRegistryModel,
                 history_start_time: datetime = None):
        """Inits MetaApi MetaTrader Api connection.

        Args:
            websocket_client: MetaApi websocket client.
            account: MetaTrader account id to connect to.
            history_storage: Local terminal history storage. By default an instance of MemoryHistoryStorage
            will be used.
            history_start_time: History start sync time.
        """
        super().__init__()
        self._websocketClient = websocket_client
        self._account = account
        self._closed = False
        self._connection_registry = connection_registry
        self._history_start_time = history_start_time
        self._terminalState = TerminalState()
        self._historyStorage = history_storage or MemoryHistoryStorage(account.id)
        self._healthMonitor = ConnectionHealthMonitor(self)
        self._websocketClient.add_synchronization_listener(account.id, self)
        self._websocketClient.add_synchronization_listener(account.id, self._terminalState)
        self._websocketClient.add_synchronization_listener(account.id, self._historyStorage)
        self._websocketClient.add_synchronization_listener(account.id, self._healthMonitor)
        self._websocketClient.add_reconnect_listener(self, account.id)
        self._subscriptions = {}
        self._stateByInstanceIndex = {}
        self._synchronized = False
        self._synchronizationListeners = []

    def get_account_information(self) -> 'Coroutine[asyncio.Future[MetatraderAccountInformation]]':
        """Returns account information (see
        https://metaapi.cloud/docs/client/websocket/api/readTradingTerminalState/readAccountInformation/).

        Returns:
            A coroutine resolving with account information.
        """
        return self._websocketClient.get_account_information(self._account.id)

    def get_positions(self) -> 'Coroutine[asyncio.Future[List[MetatraderPosition]]]':
        """Returns positions (see
        https://metaapi.cloud/docs/client/websocket/api/readTradingTerminalState/readPositions/).

        Returns:
            A coroutine resolving with array of open positions.
        """
        return self._websocketClient.get_positions(self._account.id)

    def get_position(self, position_id: str) -> 'Coroutine[asyncio.Future[MetatraderPosition]]':
        """Returns specific position (see
        https://metaapi.cloud/docs/client/websocket/api/readTradingTerminalState/readPosition/).

        Args:
            position_id: Position id.

        Returns:
            A coroutine resolving with MetaTrader position found.
        """
        return self._websocketClient.get_position(self._account.id, position_id)

    def get_orders(self) -> 'Coroutine[asyncio.Future[List[MetatraderOrder]]]':
        """Returns open orders (see
        https://metaapi.cloud/docs/client/websocket/api/readTradingTerminalState/readOrders/).

        Returns:
            A coroutine resolving with open MetaTrader orders.
        """
        return self._websocketClient.get_orders(self._account.id)

    def get_order(self, order_id: str) -> 'Coroutine[asyncio.Future[MetatraderOrder]]':
        """Returns specific open order (see
        https://metaapi.cloud/docs/client/websocket/api/readTradingTerminalState/readOrder/).

        Args:
            order_id: Order id (ticket number).

        Returns:
            A coroutine resolving with metatrader order found.
        """
        return self._websocketClient.get_order(self._account.id, order_id)

    def get_history_orders_by_ticket(self, ticket: str) -> 'Coroutine[MetatraderHistoryOrders]':
        """Returns the history of completed orders for a specific ticket number (see
        https://metaapi.cloud/docs/client/websocket/api/retrieveHistoricalData/readHistoryOrdersByTicket/).

        Args:
            ticket: Ticket number (order id).

        Returns:
            A coroutine resolving with request results containing history orders found.
        """
        return self._websocketClient.get_history_orders_by_ticket(self._account.id, ticket)

    def get_history_orders_by_position(self, position_id: str) -> 'Coroutine[MetatraderHistoryOrders]':
        """Returns the history of completed orders for a specific position id (see
        https://metaapi.cloud/docs/client/websocket/api/retrieveHistoricalData/readHistoryOrdersByPosition/)

        Args:
            position_id: Position id.

        Returns:
            A coroutine resolving with request results containing history orders found.
        """
        return self._websocketClient.get_history_orders_by_position(self._account.id, position_id)

    def get_history_orders_by_time_range(self, start_time: datetime, end_time: datetime, offset: int = 0,
                                         limit: int = 1000) -> 'Coroutine[MetatraderHistoryOrders]':
        """Returns the history of completed orders for a specific time range (see
        https://metaapi.cloud/docs/client/websocket/api/retrieveHistoricalData/readHistoryOrdersByTimeRange/)

        Args:
            start_time: Start of time range, inclusive.
            end_time: End of time range, exclusive.
            offset: Pagination offset, default is 0.
            limit: Pagination limit, default is 1000.

        Returns:
            A coroutine resolving with request results containing history orders found.
        """
        return self._websocketClient.get_history_orders_by_time_range(self._account.id, start_time, end_time,
                                                                      offset, limit)

    def get_deals_by_ticket(self, ticket: str) -> 'Coroutine[MetatraderDeals]':
        """Returns history deals with a specific ticket number (see
        https://metaapi.cloud/docs/client/websocket/api/retrieveHistoricalData/readDealsByTicket/).

        Args:
            ticket: Ticket number (deal id for MT5 or order id for MT4).

        Returns:
            A coroutine resolving with request results containing deals found.
        """
        return self._websocketClient.get_deals_by_ticket(self._account.id, ticket)

    def get_deals_by_position(self, position_id) -> 'Coroutine[MetatraderDeals]':
        """Returns history deals for a specific position id (see
        https://metaapi.cloud/docs/client/websocket/api/retrieveHistoricalData/readDealsByPosition/).

        Args:
            position_id: Position id.

        Returns:
            A coroutine resolving with request results containing deals found.
        """
        return self._websocketClient.get_deals_by_position(self._account.id, position_id)

    def get_deals_by_time_range(self, start_time: datetime, end_time: datetime, offset: int = 0,
                                limit: int = 1000) -> 'Coroutine[MetatraderDeals]':
        """Returns history deals with for a specific time range (see
        https://metaapi.cloud/docs/client/websocket/api/retrieveHistoricalData/readDealsByTimeRange/).

        Args:
            start_time: Start of time range, inclusive.
            end_time: End of time range, exclusive.
            offset: Pagination offset, default is 0.
            limit: Pagination limit, default is 1000.

        Returns:
            A coroutine resolving with request results containing deals found.
        """
        return self._websocketClient.get_deals_by_time_range(self._account.id, start_time, end_time, offset, limit)

    def remove_history(self, application: str = None) -> Coroutine:
        """Clears the order and transaction history of a specified account so that it can be synchronized from scratch
        (see https://metaapi.cloud/docs/client/websocket/api/removeHistory/).

        Args:
            application: Application to remove history for.

        Returns:
            A coroutine resolving when the history is cleared.
        """
        asyncio.create_task(self._historyStorage.clear())
        return self._websocketClient.remove_history(self._account.id, application)

    def remove_application(self):
        """Clears the order and transaction history of a specified application and removes application (see
        https://metaapi.cloud/docs/client/websocket/api/removeApplication/).

        Returns:
            A coroutine resolving when the history is cleared and application is removed.
        """
        asyncio.create_task(self._historyStorage.clear())
        return self._websocketClient.remove_application(self._account.id)

    def create_market_buy_order(self, symbol: str, volume: float, stop_loss: float or StopOptions = None,
                                take_profit: float or StopOptions = None,
                                options: MarketTradeOptions = None) -> \
            'Coroutine[asyncio.Future[MetatraderTradeResponse]]':
        """Creates a market buy order (see https://metaapi.cloud/docs/client/websocket/api/trade/).

        Args:
            symbol: Symbol to trade.
            volume: Order volume.
            stop_loss: Optional stop loss price.
            take_profit: Optional take profit price.
            options: Optional trade options.

        Returns:
            A coroutine resolving with trade result.

        Raises:
            TradeException: On trade error, check error properties for error code details.
        """
        trade_params = {'actionType': 'ORDER_TYPE_BUY', 'symbol': symbol, 'volume': volume,
                        **self._generate_stop_options(stop_loss=stop_loss, take_profit=take_profit)}
        trade_params.update(options or {})
        return self._websocketClient.trade(self._account.id, trade_params)

    def create_market_sell_order(self, symbol: str, volume: float, stop_loss: float or StopOptions = None,
                                 take_profit: float or StopOptions = None,
                                 options: MarketTradeOptions = None) -> \
            'Coroutine[asyncio.Future[MetatraderTradeResponse]]':
        """Creates a market sell order (see https://metaapi.cloud/docs/client/websocket/api/trade/).

        Args:
            symbol: Symbol to trade.
            volume: Order volume.
            stop_loss: Optional stop loss price.
            take_profit: Optional take profit price.
            options: Optional trade options.

        Returns:
            A coroutine resolving with trade result.

        Raises:
            TradeException: On trade error, check error properties for error code details.
        """
        trade_params = {'actionType': 'ORDER_TYPE_SELL', 'symbol': symbol, 'volume': volume,
                        **self._generate_stop_options(stop_loss=stop_loss, take_profit=take_profit)}
        trade_params.update(options or {})
        return self._websocketClient.trade(self._account.id, trade_params)

    def create_limit_buy_order(self, symbol: str, volume: float, open_price: float,
                               stop_loss: float or StopOptions = None,
                               take_profit: float or StopOptions = None, options: PendingTradeOptions = None) -> \
            'Coroutine[asyncio.Future[MetatraderTradeResponse]]':
        """Creates a limit buy order (see https://metaapi.cloud/docs/client/websocket/api/trade/).

        Args:
            symbol: Symbol to trade.
            volume: Order volume.
            open_price: Order limit price.
            stop_loss: Optional stop loss price.
            take_profit: Optional take profit price.
            options: Optional trade options.

        Returns:
            A coroutine resolving with trade result.

        Raises:
            TradeException: On trade error, check error properties for error code details.
        """
        trade_params = {'actionType': 'ORDER_TYPE_BUY_LIMIT', 'symbol': symbol, 'volume': volume,
                        'openPrice': open_price,
                        **self._generate_stop_options(stop_loss=stop_loss, take_profit=take_profit)}
        trade_params.update(options or {})
        return self._websocketClient.trade(self._account.id, trade_params)

    def create_limit_sell_order(self, symbol: str, volume: float, open_price: float,
                                stop_loss: float or StopOptions = None,
                                take_profit: float or StopOptions = None, options: PendingTradeOptions = None) -> \
            'Coroutine[asyncio.Future[MetatraderTradeResponse]]':
        """Creates a limit sell order (see https://metaapi.cloud/docs/client/websocket/api/trade/).

        Args:
            symbol: Symbol to trade.
            volume: Order volume.
            open_price: Order limit price.
            stop_loss: Optional stop loss price.
            take_profit: Optional take profit price.
            options: Optional trade options.

        Returns:
            A coroutine resolving with trade result.

        Raises:
            TradeException: On trade error, check error properties for error code details.
        """
        trade_params = {'actionType': 'ORDER_TYPE_SELL_LIMIT', 'symbol': symbol, 'volume': volume,
                        'openPrice': open_price,
                        **self._generate_stop_options(stop_loss=stop_loss, take_profit=take_profit)}
        trade_params.update(options or {})
        return self._websocketClient.trade(self._account.id, trade_params)

    def create_stop_buy_order(self, symbol: str, volume: float, open_price: float,
                              stop_loss: float or StopOptions = None,
                              take_profit: float or StopOptions = None, options: PendingTradeOptions = None) -> \
            'Coroutine[asyncio.Future[MetatraderTradeResponse]]':
        """Creates a stop buy order (see https://metaapi.cloud/docs/client/websocket/api/trade/).

        Args:
            symbol: Symbol to trade.
            volume: Order volume.
            open_price: Order limit price.
            stop_loss: Optional stop loss price.
            take_profit: Optional take profit price.
            options: Optional trade options.

        Returns:
            A coroutine resolving with trade result.

        Raises:
            TradeException: On trade error, check error properties for error code details.
        """
        trade_params = {'actionType': 'ORDER_TYPE_BUY_STOP', 'symbol': symbol, 'volume': volume,
                        'openPrice': open_price,
                        **self._generate_stop_options(stop_loss=stop_loss, take_profit=take_profit)}
        trade_params.update(options or {})
        return self._websocketClient.trade(self._account.id, trade_params)

    def create_stop_sell_order(self, symbol: str, volume: float, open_price: float,
                               stop_loss: float or StopOptions = None,
                               take_profit: float or StopOptions = None, options: PendingTradeOptions = None) -> \
            'Coroutine[asyncio.Future[MetatraderTradeResponse]]':
        """Creates a stop sell order (see https://metaapi.cloud/docs/client/websocket/api/trade/).

        Args:
            symbol: Symbol to trade.
            volume: Order volume.
            open_price: Order limit price.
            stop_loss: Optional stop loss price.
            take_profit: Optional take profit price.
            options: Optional trade options.

        Returns:
            A coroutine resolving with trade result.

        Raises:
            TradeException: On trade error, check error properties for error code details.
        """
        trade_params = {'actionType': 'ORDER_TYPE_SELL_STOP', 'symbol': symbol, 'volume': volume,
                        'openPrice': open_price,
                        **self._generate_stop_options(stop_loss=stop_loss, take_profit=take_profit)}
        trade_params.update(options or {})
        return self._websocketClient.trade(self._account.id, trade_params)

    def create_stop_limit_buy_order(self, symbol: str, volume: float, open_price: float, stop_limit_price: float,
                                    stop_loss: float or StopOptions = None, take_profit: float or StopOptions = None,
                                    options: PendingTradeOptions = None):
        """Creates a stop limit buy order (see https://metaapi.cloud/docs/client/websocket/api/trade/).

        Args:
            symbol: Symbol to trade.
            volume: Order volume.
            open_price: Order limit price.
            stop_limit_price: The limit order price for the stop limit order.
            stop_loss: Optional stop loss price.
            take_profit: Optional take profit price.
            options: Optional trade options.

        Returns:
            A coroutine resolving with trade result.

        Raises:
            TradeException: On trade error, check error properties for error code details.
        """
        trade_params = {'actionType': 'ORDER_TYPE_BUY_STOP_LIMIT', 'symbol': symbol, 'volume': volume,
                        'openPrice': open_price, 'stopLimitPrice': stop_limit_price,
                        **self._generate_stop_options(stop_loss=stop_loss, take_profit=take_profit)}
        trade_params.update(options or {})
        return self._websocketClient.trade(self._account.id, trade_params)

    def create_stop_limit_sell_order(self, symbol: str, volume: float, open_price: float, stop_limit_price: float,
                                     stop_loss: float or StopOptions = None, take_profit: float or StopOptions = None,
                                     options: PendingTradeOptions = None):
        """Creates a stop limit sell order (see https://metaapi.cloud/docs/client/websocket/api/trade/).

        Args:
            symbol: Symbol to trade.
            volume: Order volume.
            open_price: Order limit price.
            stop_limit_price: The limit order price for the stop limit order.
            stop_loss: Optional stop loss price.
            take_profit: Optional take profit price.
            options: Optional trade options.

        Returns:
            A coroutine resolving with trade result.

        Raises:
            TradeException: On trade error, check error properties for error code details.
        """
        trade_params = {'actionType': 'ORDER_TYPE_SELL_STOP_LIMIT', 'symbol': symbol, 'volume': volume,
                        'openPrice': open_price, 'stopLimitPrice': stop_limit_price,
                        **self._generate_stop_options(stop_loss=stop_loss, take_profit=take_profit)}
        trade_params.update(options or {})
        return self._websocketClient.trade(self._account.id, trade_params)

    def modify_position(self, position_id: str, stop_loss: float or StopOptions = None,
                        take_profit: float or StopOptions = None) -> \
            'Coroutine[asyncio.Future[MetatraderTradeResponse]]':
        """Modifies a position (see https://metaapi.cloud/docs/client/websocket/api/trade/).

        Args:
            position_id: Position id to modify.
            stop_loss: Optional stop loss price.
            take_profit: Optional take profit price.

        Returns:
            A coroutine resolving with trade result.

        Raises:
            TradeException: On trade error.
        """
        trade_params = {'actionType': 'POSITION_MODIFY', 'positionId': position_id,
                        **self._generate_stop_options(stop_loss=stop_loss, take_profit=take_profit)}
        return self._websocketClient.trade(self._account.id, trade_params)

    def close_position_partially(self, position_id: str, volume: float, options: MarketTradeOptions = None) -> \
            'Coroutine[asyncio.Future[MetatraderTradeResponse]]':
        """Partially closes a position (see https://metaapi.cloud/docs/client/websocket/api/trade/).

        Args:
            position_id: Position id to modify.
            volume: Volume to close.
            options: Optional trade options.

        Returns:
            A coroutine resolving with trade result.

        Raises:
            TradeException: On trade error, check error properties for error code details.
        """
        trade_params = {'actionType': 'POSITION_PARTIAL', 'positionId': position_id, 'volume': volume}
        trade_params.update(options or {})
        return self._websocketClient.trade(self._account.id, trade_params)

    def close_position(self, position_id: str, options: MarketTradeOptions = None) -> \
            'Coroutine[asyncio.Future[MetatraderTradeResponse]]':
        """Fully closes a position (see https://metaapi.cloud/docs/client/websocket/api/trade/).

        Args:
            position_id: Position id to modify.
            options: Optional trade options.

        Returns:
            A coroutine resolving with trade result.

        Raises:
            TradeException: On trade error, check error properties for error code details.
        """
        trade_params = {'actionType': 'POSITION_CLOSE_ID', 'positionId': position_id}
        trade_params.update(options or {})
        return self._websocketClient.trade(self._account.id, trade_params)

    def close_by(self, position_id: str, opposite_position_id: str, options: MarketTradeOptions = None) -> \
            'Coroutine[asyncio.Future[MetatraderTradeResponse]]':
        """Fully closes a position (see https://metaapi.cloud/docs/client/websocket/api/trade/).

        Args:
            position_id: Position id to close by opposite position.
            opposite_position_id: Opposite position id to close.
            options: Optional trade options.

        Returns:
            A coroutine resolving with trade result.

        Raises:
            TradeException: On trade error, check error properties for error code details.
        """
        trade_params = {'actionType': 'POSITION_CLOSE_BY', 'positionId': position_id,
                        'closeByPositionId': opposite_position_id}
        trade_params.update(options or {})
        return self._websocketClient.trade(self._account.id, trade_params)

    def close_positions_by_symbol(self, symbol: str, options: MarketTradeOptions = None) -> \
            'Coroutine[asyncio.Future[MetatraderTradeResponse]]':
        """Closes positions by a symbol (see https://metaapi.cloud/docs/client/websocket/api/trade/).

        Args:
            symbol: Symbol to trade.
            options: Optional trade options.

        Returns:
            A coroutine resolving with trade result.

        Raises:
            TradeException: On trade error, check error properties for error code details.
        """
        trade_params = {'actionType': 'POSITIONS_CLOSE_SYMBOL', 'symbol': symbol}
        trade_params.update(options or {})
        return self._websocketClient.trade(self._account.id, trade_params)

    def modify_order(self, order_id: str, open_price: float, stop_loss: float or StopOptions = None,
                     take_profit: float or StopOptions = None) -> \
            'Coroutine[asyncio.Future[MetatraderTradeResponse]]':
        """Modifies a pending order (see https://metaapi.cloud/docs/client/websocket/api/trade/).

        Args:
            order_id: Order id (ticket number).
            open_price: Order stop price.
            stop_loss: Optional stop loss price.
            take_profit: Optional take profit price.

        Returns:
            A coroutine resolving with trade result.

        Raises:
            TradeException: On trade error, check error properties for error code details.
        """
        trade_params = {'actionType': 'ORDER_MODIFY', 'orderId': order_id, 'openPrice': open_price,
                        **self._generate_stop_options(stop_loss=stop_loss, take_profit=take_profit)}
        return self._websocketClient.trade(self._account.id, trade_params)

    def cancel_order(self, order_id: str) -> \
            'Coroutine[asyncio.Future[MetatraderTradeResponse]]':
        """Cancels order (see https://metaapi.cloud/docs/client/websocket/api/trade/).

        Args:
            order_id: Order id (ticket number).

        Returns:
            A coroutine resolving with trade result.

        Raises:
            TradeException: On trade error, check error properties for error code details.
        """
        return self._websocketClient.trade(self._account.id, {'actionType': 'ORDER_CANCEL', 'orderId': order_id})

    def reconnect(self) -> Coroutine:
        """Reconnects to the Metatrader terminal (see https://metaapi.cloud/docs/client/websocket/api/reconnect/).

        Returns:
            A coroutine which resolves when reconnection started.
        """
        return self._websocketClient.reconnect(self._account.id)

    async def synchronize(self, instance_index: str) -> Coroutine:
        """Requests the terminal to start synchronization process.
        (see https://metaapi.cloud/docs/client/websocket/synchronizing/synchronize/).

        Args:
            instance_index: Instance index.

        Returns:
            A coroutine which resolves when synchronization started.
        """
        instance = self.get_instance_number(instance_index)
        host = self.get_host_name(instance_index)
        starting_history_order_time = \
            datetime.utcfromtimestamp(max(((self._history_start_time and self._history_start_time.timestamp()) or 0),
                                      (await self._historyStorage.last_history_order_time(instance))
                                          .timestamp())).replace(tzinfo=pytz.UTC)
        starting_deal_time = \
            datetime.utcfromtimestamp(max(((self._history_start_time and self._history_start_time.timestamp()) or 0),
                                      (await self._historyStorage.last_deal_time(instance)).timestamp()))\
            .replace(tzinfo=pytz.UTC)
        synchronization_id = random_id()
        self._get_state(instance_index)['lastSynchronizationId'] = synchronization_id
        return await self._websocketClient.synchronize(self._account.id, instance, host, synchronization_id,
                                                       starting_history_order_time, starting_deal_time)

    async def initialize(self):
        """Initializes meta api connection"""
        await self._historyStorage.initialize()

    async def subscribe(self):
        """Initiates subscription to MetaTrader terminal.

        Returns:
            A coroutine which resolves when subscription is initiated.
        """
        if not self._closed:
            self._websocketClient.ensure_subscribe(self._account.id)

    async def subscribe_to_market_data(self, symbol: str, subscriptions: List[MarketDataSubscription] = None,
                                       instance_index: int = None, timeout_in_seconds: float = None) -> Coroutine:
        """Subscribes on market data of specified symbol (see
        https://metaapi.cloud/docs/client/websocket/marketDataStreaming/subscribeToMarketData/).

        Args:
            symbol: Symbol (e.g. currency pair or an index).
            subscriptions: Array of market data subscription to create or update. Please note that this feature is
            not fully implemented on server-side yet.
            instance_index: Instance index.
            timeout_in_seconds: Timeout to wait for prices in seconds, default is 30.

        Returns:
            Promise which resolves when subscription request was processed.
        """
        self._subscriptions[symbol] = {'subscriptions': subscriptions or None}
        await self._websocketClient.subscribe_to_market_data(self._account.id, instance_index, symbol, subscriptions)
        return await self.terminal_state.wait_for_price(symbol, timeout_in_seconds)

    def unsubscribe_from_market_data(self, symbol: str, subscriptions: List[MarketDataUnsubscription] = None,
                                     instance_index: int = None) -> Coroutine:
        """Unsubscribes from market data of specified symbol (see
        https://metaapi.cloud/docs/client/websocket/marketDataStreaming/subscribeToMarketData/).

        Args:
            symbol: Symbol (e.g. currency pair or an index).
            subscriptions: Array of subscriptions to cancel.
            instance_index: Instance index.

        Returns:
            Promise which resolves when subscription request was processed.
        """
        if not subscriptions:
            if symbol in self._subscriptions:
                del self._subscriptions[symbol]
        elif symbol in self._subscriptions:
            self._subscriptions[symbol]['subscriptions'] = list(filter(
                lambda s: not next((s2 for s2 in subscriptions if s['type'] == s2['type']), None),
                self._subscriptions[symbol]['subscriptions']))
            if not len(self._subscriptions[symbol]['subscriptions']):
                del self._subscriptions[symbol]
        return self._websocketClient.unsubscribe_from_market_data(self._account.id, instance_index, symbol,
                                                                  subscriptions)

    async def on_subscription_downgraded(self, instance_index: str, symbol: str,
                                         updates: List[MarketDataSubscription] or None = None,
                                         unsubscriptions: List[MarketDataUnsubscription] or None = None):
        """Invoked when subscription downgrade has occurred.

        Args:
            instance_index: Index of an account instance connected.
            symbol: Symbol to update subscriptions for.
            updates: Array of market data subscription to update.
            unsubscriptions: Array of subscriptions to cancel.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        subscriptions = self._subscriptions[symbol] if symbol in self._subscriptions else None
        if unsubscriptions and len(unsubscriptions):
            if subscriptions:
                for subscription in unsubscriptions:
                    subscriptions = list(filter(lambda s: s['type'] == subscription['type'], subscriptions))
            asyncio.create_task(self.unsubscribe_from_market_data(symbol, unsubscriptions))
        if updates and len(updates):
            if subscriptions:
                for subscription in updates:
                    for s in list(filter(lambda s: s['type'] == subscription['type'], subscriptions)):
                        s['intervalInMilliiseconds'] = subscription['intervalInMilliseconds']
            asyncio.create_task(self.subscribe_to_market_data(symbol, updates))
        if subscriptions and (not len(subscriptions)):
            del self._subscriptions[symbol]

    @property
    def subscribed_symbols(self) -> List[str]:
        """Returns list of the symbols connection is subscribed to.

        Returns:
            List of the symbols connection is subscribed to.
        """
        return list(self._subscriptions.keys())

    def subscriptions(self, symbol) -> List[MarketDataSubscription]:
        """Returns subscriptions for a symbol.

        Args:
            symbol: Symbol to retrieve subscriptions for.

        Returns:
            List of market data subscriptions for the symbol.
        """
        return self._subscriptions[symbol]['subscriptions'] if symbol in self._subscriptions else []

    def get_symbols(self) -> 'Coroutine[asyncio.Future[List[str]]]':
        """Retrieves available symbols for an account (see
        https://metaapi.cloud/docs/client/websocket/api/retrieveMarketData/readSymbols/).

        Returns:
            A coroutine which resolves when symbols are retrieved.
        """
        return self._websocketClient.get_symbols(self._account.id)

    def get_symbol_specification(self, symbol: str) -> 'Coroutine[asyncio.Future[MetatraderSymbolSpecification]]':
        """Retrieves specification for a symbol (see
        https://metaapi.cloud/docs/client/websocket/api/retrieveMarketData/readSymbolSpecification/).

        Args:
            symbol: Symbol to retrieve specification for.

        Returns:
            A coroutine which resolves when specification MetatraderSymbolSpecification is retrieved.
        """
        return self._websocketClient.get_symbol_specification(self._account.id, symbol)

    def get_symbol_price(self, symbol) -> 'Coroutine[asyncio.Future[MetatraderSymbolPrice]]':
        """Retrieves latest price for a symbol (see
        https://metaapi.cloud/docs/client/websocket/api/retrieveMarketData/readSymbolPrice/).

        Args:
            symbol: Symbol to retrieve price for.

        Returns:
            A coroutine which resolves when price MetatraderSymbolPrice is retrieved.
        """
        return self._websocketClient.get_symbol_price(self._account.id, symbol)

    def get_candle(self, symbol: str, timeframe: str) -> 'Coroutine[asyncio.Future[MetatraderCandle]]':
        """Retrieves latest candle for a symbol and timeframe (see
        https://metaapi.cloud/docs/client/websocket/api/retrieveMarketData/readCandle/).

        Args:
            symbol: Symbol to retrieve candle for.
            timeframe: Defines the timeframe according to which the candle must be generated. Allowed values for
            MT5 are 1m, 2m, 3m, 4m, 5m, 6m, 10m, 12m, 15m, 20m, 30m, 1h, 2h, 3h, 4h, 6h, 8h, 12h, 1d, 1w, 1mn.
            Allowed values for MT4 are 1m, 5m, 15m 30m, 1h, 4h, 1d, 1w, 1mn.

        Returns:
            A coroutine which resolves when candle is retrieved.
        """
        return self._websocketClient.get_candle(self._account.id, symbol, timeframe)

    def get_tick(self, symbol: str) -> 'Coroutine[asyncio.Future[MetatraderTick]]':
        """Retrieves latest tick for a symbol (see
        https://metaapi.cloud/docs/client/websocket/api/retrieveMarketData/readTick/).

        Args:
            symbol: Symbol to retrieve tick for.

        Returns:
            A coroutine which resolves when tick is retrieved.
        """
        return self._websocketClient.get_tick(self._account.id, symbol)

    def get_book(self, symbol: str) -> 'Coroutine[asyncio.Future[MetatraderBook]]':
        """Retrieves latest order book for a symbol (see
        https://metaapi.cloud/docs/client/websocket/api/retrieveMarketData/readBook/).

        Args:
            symbol: Symbol to retrieve order book for.

        Returns:
            A coroutine which resolves when order book is retrieved.
        """
        return self._websocketClient.get_book(self._account.id, symbol)

    def save_uptime(self, uptime: Dict):
        """Sends client uptime stats to the server.

        Args:
            uptime: Uptime statistics to send to the server.

        Returns:
            A coroutine which resolves when uptime statistics is submitted.
        """
        return self._websocketClient.save_uptime(self._account.id, uptime)

    @property
    def terminal_state(self) -> TerminalState:
        """Returns local copy of terminal state.

        Returns:
            Local copy of terminal state.
        """
        return self._terminalState

    @property
    def history_storage(self) -> HistoryStorage:
        """Returns local history storage.

        Returns:
            Local history storage.
        """
        return self._historyStorage

    def add_synchronization_listener(self, listener):
        """Adds synchronization listener.

        Args:
            listener: Synchronization listener to add.
        """
        self._synchronizationListeners.append(listener)
        self._websocketClient.add_synchronization_listener(self._account.id, listener)

    def remove_synchronization_listener(self, listener):
        """Removes synchronization listener for specific account.

        Args:
            listener: Synchronization listener to remove.
        """
        self._synchronizationListeners = list(filter(lambda l: l != listener, self._synchronizationListeners))
        self._websocketClient.remove_synchronization_listener(self._account.id, listener)

    async def on_connected(self, instance_index: str, replicas: int):
        """Invoked when connection to MetaTrader terminal established.

        Args:
            instance_index: Index of an account instance connected.
            replicas: Number of account replicas launched.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        key = random_id(32)
        state = self._get_state(instance_index)
        state['shouldSynchronize'] = key
        state['synchronizationRetryIntervalInSeconds'] = 1
        state['synchronized'] = False
        asyncio.create_task(self._ensure_synchronized(instance_index, key))
        indices = []
        for i in range(replicas):
            indices.append(i)
        for key in list(self._stateByInstanceIndex.keys()):
            e = self._stateByInstanceIndex[key]
            if self.get_instance_number(e['instanceIndex']) not in indices:
                del self._stateByInstanceIndex[key]

    async def on_disconnected(self, instance_index: str):
        """Invoked when connection to MetaTrader terminal terminated.

        Args:
            instance_index: Index of an account instance connected.

        Returns:
             A coroutine which resolves when the asynchronous event is processed.
        """
        state = self._get_state(instance_index)
        state['lastDisconnectedSynchronizationId'] = state['lastSynchronizationId']
        state['lastSynchronizationId'] = None
        state['shouldSynchronize'] = None
        state['synchronized'] = False
        state['disconnected'] = True

    async def on_deal_synchronization_finished(self, instance_index: str, synchronization_id: str):
        """Invoked when a synchronization of history deals on a MetaTrader account have finished.

        Args:
            instance_index: Index of an account instance connected.
            synchronization_id: Synchronization request id.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        state = self._get_state(instance_index)
        state['dealsSynchronized'][synchronization_id] = True

    async def on_order_synchronization_finished(self, instance_index: str, synchronization_id: str):
        """Invoked when a synchronization of history orders on a MetaTrader account have finished.

        Args:
            instance_index: Index of an account instance connected.
            synchronization_id: Synchronization request id.

        Returns:
             A coroutine which resolves when the asynchronous event is processed
        """
        state = self._get_state(instance_index)
        state['ordersSynchronized'][synchronization_id] = True

    async def on_account_information_updated(self, instance_index: str,
                                             account_information: MetatraderAccountInformation):
        """Invoked when MetaTrader position is updated.

        Args:
            instance_index: Index of an account instance connected.
            account_information: Updated MetaTrader position.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        async def subscribe_task(symbol):
            try:
                instance = self.get_instance_number(instance_index)
                await self.subscribe_to_market_data(symbol, self._subscriptions[symbol]['subscriptions'],
                                                    instance)
            except Exception as err:
                print(f'[{datetime.now().isoformat()}] MetaApi websocket client for account ' + self.account.id +
                      ':' + str(instance_index) + ' failed to resubscribe to symbol ' + symbol, format_error(err))

        for symbol in self.subscribed_symbols:
            if not self._terminalState.price(symbol):
                asyncio.create_task(subscribe_task(symbol))

    async def on_reconnected(self):
        """Invoked when connection to MetaApi websocket API restored after a disconnect.

        Returns:
            A coroutine which resolves when connection to MetaApi websocket API restored after a disconnect.
        """
        self._stateByInstanceIndex = {}

    async def on_stream_closed(self, instance_index: str):
        """Invoked when a stream for an instance index is closed.

        Args:
            instance_index: Index of an account instance connected.

        Returns:
            A coroutine which resolves when the asynchronous event is processed.
        """
        if instance_index in self._stateByInstanceIndex:
            del self._stateByInstanceIndex[instance_index]

    async def is_synchronized(self, instance_index: str, synchronization_id: str = None) -> bool:
        """Returns flag indicating status of state synchronization with MetaTrader terminal.

        Args:
            instance_index: Index of an account instance connected.
            synchronization_id: Optional synchronization request id, last synchronization request id will be used.

        Returns:
            A coroutine resolving with a flag indicating status of state synchronization with MetaTrader terminal.
        """
        def reducer_func(acc, s: MetaApiConnectionDict):
            if instance_index is not None and s['instanceIndex'] != instance_index:
                return acc
            nonlocal synchronization_id
            synchronization_id = synchronization_id or s['lastSynchronizationId']
            synchronized = synchronization_id in s['ordersSynchronized'] and \
                bool(s['ordersSynchronized'][synchronization_id]) and \
                synchronization_id in s['dealsSynchronized'] and \
                bool(s['dealsSynchronized'][synchronization_id])
            return acc or synchronized
        return reduce(reducer_func, self._stateByInstanceIndex.values(), False) if \
            len(self._stateByInstanceIndex.values()) else False

    async def wait_synchronized(self, opts: SynchronizationOptions = None):
        """Waits until synchronization to MetaTrader terminal is completed.

        Args:
            opts: Synchronization options.

        Returns:
            A coroutine which resolves when synchronization to MetaTrader terminal is completed.

        Raises:
            TimeoutException: If application failed to synchronize with the terminal within timeout allowed.
        """
        start_time = datetime.now()
        opts = opts or {}
        instance_index = opts['instanceIndex'] if 'instanceIndex' in opts else None
        synchronization_id = opts['synchronizationId'] if 'synchronizationId' in opts else None
        timeout_in_seconds = opts['timeoutInSeconds'] if 'timeoutInSeconds' in opts else 300
        interval_in_milliseconds = opts['intervalInMilliseconds'] if 'intervalInMilliseconds' in opts else 1000
        application_pattern = opts['applicationPattern'] if 'applicationPattern' in opts \
            else ('CopyFactory.*|RPC' if self._account.application == 'CopyFactory' else 'RPC')
        synchronized = await self.is_synchronized(instance_index, synchronization_id)
        while not synchronized and (start_time + timedelta(seconds=timeout_in_seconds) > datetime.now()):
            await asyncio.sleep(interval_in_milliseconds / 1000)
            synchronized = await self.is_synchronized(instance_index, synchronization_id)
        state = None
        if instance_index is None:
            for s in self._stateByInstanceIndex.values():
                if await self.is_synchronized(s['instanceIndex'], synchronization_id):
                    state = s
                    instance_index = s['instanceIndex']
        else:
            state = next((s for s in self._stateByInstanceIndex if s['instanceIndex'] == instance_index), None)
        if not synchronized:
            raise TimeoutException('Timed out waiting for MetaApi to synchronize to MetaTrader account ' +
                                   self._account.id + ', synchronization id ' +
                                   (synchronization_id or (bool(state) and state['lastSynchronizationId']) or
                                    (bool(state) and state['lastDisconnectedSynchronizationId']) or 'None'))
        time_left_in_seconds = max(0, timeout_in_seconds - (datetime.now() - start_time).total_seconds())
        await self._websocketClient.wait_synchronized(self._account.id, self.get_instance_number(instance_index),
                                                      application_pattern, time_left_in_seconds)

    async def close(self):
        """Closes the connection. The instance of the class should no longer be used after this method is invoked."""
        if not self._closed:
            self._stateByInstanceIndex = {}
            await self._websocketClient.unsubscribe(self._account.id)
            self._websocketClient.remove_synchronization_listener(self._account.id, self)
            self._websocketClient.remove_synchronization_listener(self._account.id, self._terminalState)
            self._websocketClient.remove_synchronization_listener(self._account.id, self._historyStorage)
            self._websocketClient.remove_synchronization_listener(self._account.id, self._healthMonitor)
            for listener in self._synchronizationListeners:
                self._websocketClient.remove_synchronization_listener(self._account.id, listener)
            self._websocketClient.remove_reconnect_listener(self)
            self._connection_registry.remove(self._account.id)
            self._healthMonitor.stop()
            self._closed = True

    @property
    def synchronized(self) -> bool:
        """Returns synchronization status.

        Returns:
            Synchronization status.
        """
        return True in list(map(lambda s: s['synchronized'], self._stateByInstanceIndex.values()))

    @property
    def account(self) -> MetatraderAccountModel:
        """Returns MetaApi account.

        Returns:
            MetaApi account.
        """
        return self._account

    @property
    def health_monitor(self) -> ConnectionHealthMonitor:
        """Returns connection health monitor instance.

        Returns:
            Connection health monitor instance.
        """
        return self._healthMonitor

    def _generate_stop_options(self, stop_loss, take_profit):
        trade = {}
        if isinstance(stop_loss, int) or isinstance(stop_loss, float):
            trade['stopLoss'] = stop_loss
        elif stop_loss:
            trade['stopLoss'] = stop_loss['value']
            trade['stopLossUnits'] = stop_loss['units']
        if isinstance(take_profit, int) or isinstance(take_profit, float):
            trade['takeProfit'] = take_profit
        elif take_profit:
            trade['takeProfit'] = take_profit['value']
            trade['takeProfitUnits'] = take_profit['units']
        return trade

    async def _ensure_synchronized(self, instance_index: str, key):
        state = self._get_state(instance_index)
        if state and not self._closed:
            try:
                synchronization_result = await self.synchronize(instance_index)
                if synchronization_result:
                    state['synchronized'] = True
                    state['synchronizationRetryIntervalInSeconds'] = 1
            except Exception as err:
                print(f'[{datetime.now().isoformat()}] MetaApi websocket client for account ' + self.account.id +
                      ':' + str(instance_index) + ' failed to synchronize', format_error(err))
                if state['shouldSynchronize'] == key:

                    async def restart_ensure_sync():
                        await asyncio.sleep(state['synchronizationRetryIntervalInSeconds'])
                        await self._ensure_synchronized(instance_index, key)
                    asyncio.create_task(restart_ensure_sync())
                    state['synchronizationRetryIntervalInSeconds'] = \
                        min(state['synchronizationRetryIntervalInSeconds'] * 2, 300)

    def _get_state(self, instance_index: str) -> MetaApiConnectionDict:
        if instance_index not in self._stateByInstanceIndex:
            self._stateByInstanceIndex[instance_index] = {
                'instanceIndex': instance_index,
                'ordersSynchronized': {},
                'dealsSynchronized': {},
                'shouldSynchronize': None,
                'synchronizationRetryIntervalInSeconds': 1,
                'synchronized': False,
                'lastDisconnectedSynchronizationId': None,
                'lastSynchronizationId': None,
                'disconnected': False
            }
        return self._stateByInstanceIndex[instance_index]
