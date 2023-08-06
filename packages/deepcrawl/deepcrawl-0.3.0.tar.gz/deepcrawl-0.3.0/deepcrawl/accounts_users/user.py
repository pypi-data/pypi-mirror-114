"""
User Account
============
"""
from typing import List, Optional

import deepcrawl
from deepcrawl.accounts import DeepCrawlAccount
from deepcrawl.utils import ImmutableAttributesMixin

user_extra_fields = (
    "id",
    "user_accounts",
)

user_mutable_fields = (
    'email',
    'name_first',
    'name_last',
    'username',
    'v1_migrating_at',
    'v1_migrated_at',
    'v1_projects_count',
    'v1_projects_migrated',
    'permissions',
    'overall_limit_levels_max',
    'overall_limit_pages_max',
    'password_login_enabled',
    'password_set',
    'sso_client_id',
    'sso_user_id',
    'terms_agreed',
    'confirmed',
    'beta',
    'beta_features_disabled',
    'limit_levels_max',
    'limit_pages_max',
    'email_validated_at',
    'created_at',
    'last_login_at',
    'v1_beta_at'
)

user_immutable_fields = (
    '_role_href',
    '_href',
    '_google_connections_href',
    '_google_analytics_connections_href',
    '_google_analytics_views_href',
    '_adobe_connections_href',
    '_adobe_analytics_report_suites_href',
    '_google_search_console_views_href',
    '_accounts_href',
    '_api_tokens_href',
    '_account_user_href',
    '_vendors_href'
)

user_fields = user_extra_fields + user_mutable_fields + user_immutable_fields


class DeepCrawlUser(ImmutableAttributesMixin):
    """
    User class
    """
    __slots__ = user_fields

    mutable_attributes = user_mutable_fields

    def __init__(self, user_data: dict):
        self.id = user_data.get('id')
        self.user_accounts = []

        self.email = user_data.get('email')
        self.name_first = user_data.get('name_first')
        self.name_last = user_data.get('name_last')
        self.username = user_data.get('username')
        self.v1_migrating_at = user_data.get('v1_migrating_at')
        self.v1_migrated_at = user_data.get('v1_migrated_at')
        self.v1_projects_count = user_data.get('v1_projects_count')
        self.v1_projects_migrated = user_data.get('v1_projects_migrated')
        self.permissions = user_data.get('permissions')
        self.overall_limit_levels_max = user_data.get('overall_limit_levels_max')
        self.overall_limit_pages_max = user_data.get('overall_limit_pages_max')
        self.password_login_enabled = user_data.get('password_login_enabled')
        self.password_set = user_data.get('password_set')
        self.sso_client_id = user_data.get('sso_client_id')
        self.sso_user_id = user_data.get('sso_user_id')
        self.terms_agreed = user_data.get('terms_agreed')
        self.confirmed = user_data.get('confirmed')
        self.beta = user_data.get('beta')
        self.beta_features_disabled = user_data.get('beta_features_disabled')
        self.limit_levels_max = user_data.get('limit_levels_max')
        self.limit_pages_max = user_data.get('limit_pages_max')
        self.email_validated_at = user_data.get('email_validated_at')
        self.created_at = user_data.get('created_at')
        self.last_login_at = user_data.get('last_login_at')
        self.v1_beta_at = user_data.get('v1_beta_at')
        self._role_href = user_data.get('_role_href')
        self._href = user_data.get('_href')
        self._google_connections_href = user_data.get('_google_connections_href')
        self._google_analytics_connections_href = user_data.get('_google_analytics_connections_href')
        self._google_analytics_views_href = user_data.get('_google_analytics_views_href')
        self._adobe_connections_href = user_data.get('_adobe_connections_href')
        self._adobe_analytics_report_suites_href = user_data.get('_adobe_analytics_report_suites_href')
        self._google_search_console_views_href = user_data.get('_google_search_console_views_href')
        self._accounts_href = user_data.get('_accounts_href')
        self._api_tokens_href = user_data.get('_api_tokens_href')
        self._account_user_href = user_data.get('_account_user_href')
        self._vendors_href = user_data.get('_vendors_href')

        super(DeepCrawlUser, self).__init__()

    def __repr__(self) -> str:
        return f"{self.name_first} {self.name_last} {self.email}"

    def __str__(self) -> str:
        return f"{self.name_first} {self.name_last} {self.email}"

    @property
    def to_dict_mutable_fields(self) -> dict:
        """
        :return: dictionary with the mutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in user_mutable_fields}

    @property
    def to_dict_immutable_fields(self) -> dict:
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in user_immutable_fields}

    def load_user_accounts(
            self, connection: 'deepcrawl.DeepCrawlConnection' = None, filters: Optional[dict] = None, **kwargs
    ) -> List[DeepCrawlAccount]:
        """
        Loads user accounts into current instance

        >>> self.load_user_accounts()
         [[0] DeepCrawlAccount, [1] DeepCrawlAccount]
        >>> self.user_accounts
        [[0] DeepCrawlAccount, [1] DeepCrawlAccount]

        :param filters: filters dict
        :type filters: dict
        :param kwargs: pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: list of user accounts
        :rtype: list
        :return:
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.user_accounts: List[DeepCrawlAccount] = connection.get_user_accounts(self.id, filters=filters, **kwargs)
        return self.user_accounts

    def get_user_accounts(
            self, use_cache: bool = True,
            connection: 'deepcrawl.DeepCrawlConnection' = None, filters: Optional[dict] = None, **kwargs
    ) -> List[DeepCrawlAccount]:
        """
        Get user accounts

        * use_cache=True > get_user_accounts will return cached user_accounts or will do a call to DeepCrawl if user_accounts attribute is empty.
        * use_cache=False > get_user_accounts will call DeepCrawl api and will override user_accounts attribute.

        >>> self.get_user_accounts()
        [[0] DeepCrawlAccount, [1] DeepCrawlAccount]

        :param use_cache:
        :type use_cache: bool
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :param filters: filters dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :return: list of user accounts
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if use_cache and self.user_accounts:
            return self.user_accounts
        return self.load_user_accounts(connection=connection, filters=filters, **kwargs)
