from ..clients.httpClient import HttpClient
from ..clients.metaApi.metaApiWebsocket_client import MetaApiWebsocketClient
from ..metaApi.provisioningProfileApi import ProvisioningProfileApi
from ..clients.metaApi.provisioningProfile_client import ProvisioningProfileClient
from ..metaApi.metatraderAccountApi import MetatraderAccountApi
from ..clients.metaApi.metatraderAccount_client import MetatraderAccountClient
from ..clients.metaApi.packetLogger import PacketLoggerOpts
from ..clients.errorHandler import ValidationException
from ..metaApi.connectionRegistry import ConnectionRegistry
from .metatraderDemoAccountApi import MetatraderDemoAccountApi
from ..clients.metaApi.synchronizationThrottler import SynchronizationThrottlerOpts
from ..clients.metaApi.metatraderDemoAccount_client import MetatraderDemoAccountClient
from ..clients.metaApi.historicalMarketData_client import HistoricalMarketDataClient
from ..clients.optionsValidator import OptionsValidator
from .latencyMonitor import LatencyMonitor
from ..clients.metaApi.expertAdvisor_client import ExpertAdvisorClient
import re
from typing import Optional
from ..metaApi.models import format_error
from typing_extensions import TypedDict


class RetryOpts(TypedDict):
    """Request retry options."""
    retries: Optional[int]
    """Maximum amount of request retries, default value is 5."""
    minDelayInSeconds: Optional[float]
    """Minimum delay in seconds until request retry, default value is 1."""
    maxDelayInSeconds: Optional[float]
    """Maximum delay in seconds until request retry, default value is 30."""
    subscribeCooldownInSeconds: Optional[float]
    """Time to disable new subscriptions for """


class EventProcessingOpts(TypedDict):
    """Options for processing websocket client events."""
    sequentialProcessing: Optional[bool]
    """An option to process synchronization events after finishing previous ones."""


class MetaApiOpts(TypedDict):
    """MetaApi options"""
    application: Optional[str]
    """Application id."""
    domain: Optional[str]
    """Domain to connect to, default is agiliumtrade.agiliumtrade.ai."""
    requestTimeout: Optional[float]
    """Timeout for socket requests in seconds."""
    connectTimeout: Optional[float]
    """Timeout for connecting to server in seconds."""
    packetOrderingTimeout: Optional[float]
    """Packet ordering timeout in seconds."""
    historicalMarketDataRequestTimeout: Optional[float]
    """Timeout for historical market data client in seconds."""
    demoAccountRequestTimeout: Optional[float]
    """Timeout for demo account requests in seconds."""
    packetLogger: Optional[PacketLoggerOpts]
    """Packet logger options."""
    enableLatencyMonitor: Optional[bool]
    """An option to enable latency tracking."""
    enableLatencyTracking: Optional[bool]
    """An option to enable latency tracking."""
    synchronizationThrottler: Optional[SynchronizationThrottlerOpts]
    """Options for synchronization throttler."""
    retryOpts: Optional[RetryOpts]
    """Options for request retries."""
    eventProcessing: Optional[EventProcessingOpts]
    """Options for processing events."""
    useSharedClientApi: Optional[bool]
    """Option to use a shared server."""


class MetaApi:
    """MetaApi MetaTrader API SDK"""

    def __init__(self, token: str, opts: MetaApiOpts = None):
        """Inits MetaApi class instance.

        Args:
            token: Authorization token.
            opts: Application options.
        """
        validator = OptionsValidator()
        opts: MetaApiOpts = opts or {}
        application = opts['application'] if 'application' in opts else 'MetaApi'
        domain = opts['domain'] if 'domain' in opts else 'agiliumtrade.agiliumtrade.ai'
        request_timeout = validator.validate_non_zero(opts['requestTimeout'] if 'requestTimeout' in opts else None,
                                                      60, 'requestTimeout')
        historical_market_data_request_timeout = validator.validate_non_zero(
            opts['historicalMarketDataRequestTimeout'] if 'historicalMarketDataRequestTimeout' in opts else None, 240,
            'historicalMarketDataRequestTimeout')
        connect_timeout = validator.validate_non_zero(opts['connectTimeout'] if 'connectTimeout' in opts else None, 60,
                                                      'connectTimeout')
        packet_ordering_timeout = validator.validate_non_zero(
            opts['packetOrderingTimeout'] if 'packetOrderingTimeout' in opts else None, 60, 'packetOrderingTimeout')
        retry_opts = opts['retryOpts'] if 'retryOpts' in opts else {}
        packet_logger = opts['packetLogger'] if 'packetLogger' in opts else {}
        synchronization_throttler = opts['synchronizationThrottler'] if 'synchronizationThrottler' in opts else {}
        demo_account_request_timeout = validator.validate_non_zero(
            opts['demoAccountRequestTimeout'] if 'demoAccountRequestTimeout' in opts else None, 240,
            'demoAccountRequestTimeout')
        event_processing = opts['eventProcessing'] if 'eventProcessing' in opts else {}
        use_shared_client_api = opts['useSharedClientApi'] if 'useSharedClientApi' in opts else False
        if not re.search(r"[a-zA-Z0-9_]+", application):
            raise ValidationException('Application name must be non-empty string consisting ' +
                                      'from letters, digits and _ only')
        http_client = HttpClient(request_timeout, retry_opts)
        historical_market_data_http_client = HttpClient(historical_market_data_request_timeout, retry_opts)
        demo_account_http_client = HttpClient(demo_account_request_timeout, retry_opts)
        self._metaApiWebsocketClient = MetaApiWebsocketClient(
            http_client, token, {'application': application, 'domain': domain, 'requestTimeout': request_timeout,
                                 'connectTimeout': connect_timeout, 'packetLogger': packet_logger,
                                 'packetOrderingTimeout': packet_ordering_timeout,
                                 'synchronizationThrottler': synchronization_throttler,
                                 'eventProcessing': event_processing, 'retryOpts': retry_opts,
                                 'useSharedClientApi': use_shared_client_api})
        self._provisioningProfileApi = ProvisioningProfileApi(ProvisioningProfileClient(http_client, token, domain))
        self._connectionRegistry = ConnectionRegistry(self._metaApiWebsocketClient, application)
        historical_market_data_client = HistoricalMarketDataClient(historical_market_data_http_client, token, domain)
        self._metatraderAccountApi = MetatraderAccountApi(MetatraderAccountClient(http_client, token, domain),
                                                          self._metaApiWebsocketClient, self._connectionRegistry,
                                                          ExpertAdvisorClient(http_client, token, domain),
                                                          historical_market_data_client)
        self._metatraderDemoAccountApi = MetatraderDemoAccountApi(MetatraderDemoAccountClient(
            demo_account_http_client, token, domain))
        if ('enableLatencyTracking' in opts and opts['enableLatencyTracking']) or ('enableLatencyMonitor' in opts and
                                                                                   opts['enableLatencyMonitor']):
            self._latencyMonitor = LatencyMonitor()
            self._metaApiWebsocketClient.add_latency_listener(self._latencyMonitor)

    @property
    def provisioning_profile_api(self) -> ProvisioningProfileApi:
        """Returns provisioning profile API.

        Returns:
            Provisioning profile API.
        """
        return self._provisioningProfileApi

    @property
    def metatrader_account_api(self) -> MetatraderAccountApi:
        """Returns MetaTrader account API.

        Returns:
            MetaTrader account API.
        """
        return self._metatraderAccountApi

    @property
    def metatrader_demo_account_api(self) -> MetatraderDemoAccountApi:
        """Returns MetaTrader demo account API.

        Returns:
            MetaTrader demo account API.
        """
        return self._metatraderDemoAccountApi

    @property
    def latency_monitor(self) -> LatencyMonitor:
        """Returns MetaApi application latency monitor.

        Returns:
            Latency monitor.
        """
        return self._latencyMonitor

    def format_error(self, err: Exception):
        """Formats and outputs metaApi errors with additional information.

        Args:
            err: Exception to process.
        """
        return format_error(err)

    def close(self):
        """Closes all clients and connections"""
        self._metaApiWebsocketClient.remove_latency_listener(self._latencyMonitor)
        self._metaApiWebsocketClient.close()
