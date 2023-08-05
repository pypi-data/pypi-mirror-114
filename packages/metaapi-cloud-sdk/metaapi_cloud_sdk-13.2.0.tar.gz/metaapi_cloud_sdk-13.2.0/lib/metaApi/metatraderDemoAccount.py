from ..clients.metaApi.metatraderDemoAccount_client import MetatraderDemoAccountDto


class MetatraderDemoAccount:
    """Implements a MetaTrader demo account entity."""

    def __init__(self, data: MetatraderDemoAccountDto):
        """Inits a MetaTrader demo account entity.

        Args:
            data: MetaTrader demo account data.
        """
        self._data = data

    @property
    def login(self) -> str:
        """Returns account login.

        Returns:
            Account login.
        """
        return self._data['login']

    @property
    def password(self) -> str:
        """Returns account password.

        Returns:
            Account password.
        """
        return self._data['password']

    @property
    def server_name(self) -> str:
        """Returns account server name.

        Returns:
            Account server name.
        """
        return self._data['serverName']

    @property
    def investor_password(self) -> str:
        """Returns account investor password.

        Returns:
            Account investor password.
        """
        return self._data['investorPassword']
