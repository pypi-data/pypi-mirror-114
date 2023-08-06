"""
Accounts Users Connection
=========================
"""
from typing import List, Optional, Type, Union

from requests import Response

from deepcrawl.accounts import DeepCrawlAccount
from deepcrawl.accounts_users.user import DeepCrawlUser
from deepcrawl.api import ApiConnection
from deepcrawl.api.api_endpoints import get_api_endpoint


class AccountsUsersConnection(ApiConnection):
    """
    ACCOUNT USERS

        * endpoint: /users/{uid}/accounts
        * http methods: GET
        * methods: get_user_accounts

        - endpoint: /users/{uid}/accounts/{account_id}
        - http methods: PUT, DELETE
        - methods: update_user_account, delete_user_account

        * endpoint: /accounts/{account_id}/users
        * http methods: GET, POST
        * methods: get_account_users, create_account_user

        - endpoint: /accounts/{account_id}/users/{uid}
        - http methods: GET, DELETE
        - methods: get_account_user, delete_account_user
    """

    """
    ACCOUNTS USERS
    """

    def get_user_accounts(
            self, uid: Union[int, str], filters: Optional[dict] = None, **kwargs
    ) -> List[DeepCrawlAccount]:
        """
        Get all accounts associated with the user

         >>> connection.get_user_accounts(1)
         [[0] DeepCrawlAccount,
         [1] DeepCrawlAccount]

        :param uid: user id
        :type uid: int
        :param filters: filters
        :type filters: dict
        :param kwargs: extra arguments, like pagination ones
        :type kwargs: dict
        :return: List of accounts
        :rtype: list
        """
        endpoint_url: str = get_api_endpoint(endpoint='user_accounts', uid=uid)
        accounts: List[dict] = self.get_paginated_data(url=endpoint_url, method='get', filters=filters, **kwargs)
        list_of_accounts = []
        for account in accounts:
            list_of_accounts.append(
                DeepCrawlAccount(account_data=account)
            )
        return list_of_accounts

    def add_user_to_account(
            self, uid: Union[int, str], account_id: Union[int, str]
    ) -> Response:
        """
        Add user to account

        >>> response = connection.add_user_account(1, 0)
        >>> response.status_code
        204

        :param uid: user id
        :type uid: int
        :param account_id: account id
        :type account_id: int
        :return: Http response
        :rtype: Response
        """
        endpoint_url: str = get_api_endpoint(endpoint='user_account', uid=uid, account_id=account_id)
        return self.dc_request(url=endpoint_url, method='put')

    def delete_user_account(self, uid: Union[int, str], account_id: Union[int, str]) -> Type[NotImplementedError]:
        """
        Delete user account

        >>> response = connection.delete_user_account(1, 0)
        >>> response.status_code
        204

        :param uid: user id
        :type uid: int or str
        :param account_id: account id
        :type account_id: int or str
        :return: NotImplementedError
        :rtype: NotImplementedError
        """
        return NotImplementedError
        # endpoint_url: str = get_api_endpoint(endpoint='user_account', uid=uid, account_id=account_id)
        # return self.dc_request(url=endpoint_url, method='delete')

    def get_account_users(
            self, account_id: Union[int, str], filters: Optional[dict] = None, **kwargs
    ) -> List[DeepCrawlUser]:
        """
        Get the users associated with an account

        >>> connection.get_account_users(0)
        [FirstName1 LastName1 email1@localhost.com,
        FirstName2 LastName2 email2@localhost.com]

        :param account_id: account id
        :type account_id: int or str
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :return: list of users
        :rtype: list
        """
        endpoint_url: str = get_api_endpoint(endpoint='account_users', account_id=account_id)
        users: List[dict] = self.get_paginated_data(url=endpoint_url, method='get', filters=filters, **kwargs)
        list_of_users = []
        for user in users:
            list_of_users.append(
                DeepCrawlUser(user_data=user)
            )
        return list_of_users

    def create_account_user(self, account_id: Union[int, str], user_data: dict) -> Type[NotImplementedError]:
        """
        Create an user for an account

        .. code-block::

            user_data = {}  # TODO

        >>> connnection.create_account_user(account_id, user_data)

        :param account_id: account id
        :type account_id: int or str
        :param user_data: user configuration
        :type user_data: dict
        :return: NotImplementedError
        :rtype: NotImplementedError
        """
        return NotImplementedError
        # endpoint_url: str = get_api_endpoint(endpoint='account_users', account_id=account_id)
        # response = self.dc_request(url=endpoint_url, method="post", json=user_data)
        # return DeepCrawlUser(user_data=response.json())

    def get_account_user(self, account_id: Union[int, str], uid: Union[int, str]) -> DeepCrawlUser:
        """
        Get a user using the account id and user id

        >>> connection.get_account_user(1, 1)
        FirstName1 LastName1 email1@localhost.com

        :param account_id: account id
        :type account_id: int or str
        :param uid: user id
        :type uid: int or str
        :return: The requested user or 404
        :rtype: DeepCrawlUser
        """
        endpoint_url: str = get_api_endpoint(endpoint='account_user', account_id=account_id, uid=uid)
        response = self.dc_request(url=endpoint_url, method="get")
        return DeepCrawlUser(user_data=response.json())

    def remove_account_user(self, account_id: Union[int, str], uid: Union[int, str]) -> Response:
        """
        Remove user from account

        >>> response = connection.remove_account_user(1, 0)
        >>> response.status_code
        204

        :param account_id: account id
        :type account_id: int or str
        :param uid: user id
        :type uid: int or str
        :return: Http response
        :rtype: Response
        """
        endpoint_url: str = get_api_endpoint(endpoint='account_user', account_id=account_id, uid=uid)
        return self.dc_request(url=endpoint_url, method='delete')

    """
    USERS
    """

    def create_user(self, user_data: dict) -> DeepCrawlUser:
        """
        Create user

        .. code-block::

            user_data = {
                "email": "email1@localhost.com",
                "name_first": "FirstName1",
                "name_last": "LastName1",
                "password": "uuqueek4OoX8thuos0Zai1nieChohW3"
            }

        >>> connection.create_user(user_data)
        FirstName1 LastName1 email1@localhost.com

        :param user_data: user data
        :type user_data: dict
        :return: Created user
        :rtype: DeepCrawlUser
        """
        endpoint_url: str = get_api_endpoint(endpoint='users')
        response = self.dc_request(url=endpoint_url, method='post', json=user_data)
        return DeepCrawlUser(user_data=response.json())

    def user_resend(self, uid: Union[int, str]) -> Response:
        """
        Resend

        >>> connection.user_resend(1)

        :param uid: user id
        :type uid: int or str
        :return:  Http response
        :rtype: Response
        """
        endpoint_url: str = get_api_endpoint(endpoint='user_resend', uid=uid)
        return self.dc_request(url=endpoint_url, method="post")

    def user_set_password(self, uid, user_data: dict) -> Response:
        """
        Set user password

        .. code-block::

            user_data = {
                "name_first": "FirstName1",
                "name_last": "LastName1",
                "password": "uuqueek4OoX8thuos0Zai1nieChohW3"
            }

        >>> connection.user_set_password(1, user_data)

        :param uid: user id
        :type uid: int or str
        :param user_data: user data
        :type user_data: dict
        :return:  Http response
        :rtype:  Response
        """
        endpoint_url = get_api_endpoint(endpoint="user_set_password", uid=uid)
        return self.dc_request(url=endpoint_url, method='patch', json=user_data)
