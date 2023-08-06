"""
Sitemap Connection
==================
"""
from typing import List, Optional, Union

from requests import Response

from deepcrawl.api import ApiConnection
from deepcrawl.api.api_endpoints import get_api_endpoint

from .sitemap import DeepCrawlCrawlSitemap, DeepCrawlProjectSitemap


class SitemapConnection(ApiConnection):
    """
    PROJECT SITEMAP
        * endpoint: /accounts/{account_id}/projects/{project_id}/sitemaps
        * http methods: GET, POST
        * methods: get_project_sitemaps, create_project_sitemap

        - endpoint: /accounts/{account_id}/projects/{project_id}/sitemaps/{sitemap_code}
        - http methods: PATCH, DELETE
        - methods: update_project_sitemap, delete_project_sitemap

    CRAWL SITEMAP
        * endpoint: /accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/sitemaps
        * http methods: GET
        * methods: get_crawl_sitemaps

        - endpoint: /accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/sitemaps/{sitemap_code}
        - http methods: GET
        - methods: get_crawl_sitemap
    """

    """
    PROJECT SITEMAP
    """

    def get_project_sitemaps(
        self, account_id: Union[int, str], project_id: Union[int, str], filters: Optional[dict] = None, **kwargs
    ) -> List[DeepCrawlProjectSitemap]:
        """
        Get project sitemaps

        >>> connection.get_project_sitemaps(0, 1)
        [xSbcfwBTi, aWimWxmnc]

        :param account_id: account id
        :type account_id: int or str
        :param project_id: project id
        :type project_id: int or str
        :param filters: filters
        :type filters: dict
        :param kwargs: extra arguments, like pagination ones
        :type kwargs: dict
        :return: list of project sitemaps
        :rtype: list
        """
        endpoint_url = get_api_endpoint(
            endpoint='project_sitemaps', account_id=account_id, project_id=project_id)
        sitemaps = self.get_paginated_data(url=endpoint_url, method='get', filters=filters, **kwargs)
        list_of_sitemaps = []
        for sitemap in sitemaps:
            list_of_sitemaps.append(
                DeepCrawlProjectSitemap(
                    account_id=account_id, project_id=project_id, sitemap_data=sitemap)
            )
        return list_of_sitemaps

    def create_project_sitemap(
        self, account_id: Union[int, str], project_id: Union[int, str], sitemap_data: dict
    ) -> DeepCrawlProjectSitemap:
        """
        Create project sitemap

        .. code-block::

            sitemap_data = {
                "url": "http://www.example.com/sitemap3.xml",
                "parent": null,
                "links_out": null,
                "level": null,
                "enabled": true,
                "type": "custom",
                "status": "valid",
                "new": true
            }

        >>> connection.create_project_sitemap(0, 1, sitemap_data)
        xSbcfwBTi

        :param account_id: account id
        :type account_id: int or str
        :param project_id: project id
        :type project_id: int or str
        :param sitemap_data: sitemap configuration
        :type sitemap_data: dict
        :return: Project sitemap instance
        :rtype: DeepCrawlProjectSitemap
        """
        endpoint_url = get_api_endpoint(endpoint='project_sitemaps', account_id=account_id, project_id=project_id)
        response = self.dc_request(url=endpoint_url, method='post', json=sitemap_data)
        return DeepCrawlProjectSitemap(account_id=account_id, project_id=project_id, sitemap_data=response.json())

    def update_project_sitemap(
            self, account_id: Union[int, str], project_id: Union[int, str], sitemap_code: str, sitemap_data: dict
    ) -> DeepCrawlProjectSitemap:
        """
        Update project sitemap

        >>> connection.update_project_sitemap(0, 1, sitemap_data)
        xSbcfwBTi

        :param account_id: account id
        :type account_id: int or str
        :param project_id: project id
        :type project_id: int or str
        :param sitemap_code: sitemap code
        :type sitemap_code: str
        :param sitemap_data: sitemap configuration
        :type sitemap_data: dict
        :return: Updated project sitemap
        :rtype: DeepCrawlProjectSitemap
        """
        endpoint_url = get_api_endpoint(
            endpoint='project_sitemap',
            account_id=account_id, project_id=project_id, sitemap_code=sitemap_code
        )
        response = self.dc_request(url=endpoint_url, method='patch', json=sitemap_data)
        return DeepCrawlProjectSitemap(account_id=account_id, project_id=project_id, sitemap_data=response.json())

    def delete_project_sitemap(
            self, account_id: Union[int, str], project_id: Union[int, str], sitemap_code: str
    ) -> Response:
        """
        Delete project sitemap

        >>> response = connection.delete_project_sitemap(0, 1, "xSbcfwBTi")
        >>> response.status_code
        204

        :param account_id: account id
        :type account_id: int or str
        :param project_id: project id
        :type project_id: int or str
        :param sitemap_code: sitemap code
        :type sitemap_code: str
        :return: HTTP 204 No Content
        :rtype: Response
        """
        endpoint_url = get_api_endpoint(
            endpoint='project_sitemap',
            account_id=account_id, project_id=project_id, sitemap_code=sitemap_code
        )
        return self.dc_request(url=endpoint_url, method='delete')

    """
    CRAWL SITEMAP
    """

    def get_crawl_sitemaps(
        self, account_id: Union[int, str], project_id: Union[int, str], crawl_id: Union[int, str],
        filters: Optional[dict] = None, **kwargs
    ) -> List[DeepCrawlCrawlSitemap]:
        """
        Get crawl sitemaps

        >>> connection.get_crawl_sitemaps(0, 1, 2)
        [xSbcfwBTi, aWimWxmnc]

        :param account_id: account id
        :type account_id: int or str
        :param project_id: project id
        :type project_id: int or str
        :param crawl_id: crawl id
        :type crawl_id: int or str
        :param filters: filters
        :type filters: dict
        :param kwargs: extra arguments, like pagination ones
        :type kwargs: dict
        :return: list of crawl sitemaps
        :rtype: list
        """
        endpoint_url = get_api_endpoint(
            endpoint='crawl_sitemaps', account_id=account_id, project_id=project_id, crawl_id=crawl_id)
        sitemaps = self.get_paginated_data(url=endpoint_url, method='get', filters=filters, **kwargs)
        list_of_sitemaps = []
        for sitemap in sitemaps:
            list_of_sitemaps.append(
                DeepCrawlCrawlSitemap(
                    account_id=account_id, project_id=project_id, crawl_id=crawl_id, sitemap_data=sitemap)
            )
        return list_of_sitemaps

    def get_crawl_sitemap(
            self, account_id: Union[int, str], project_id: Union[int, str], crawl_id: Union[int, str],
            sitemap_code: str
    ) -> DeepCrawlCrawlSitemap:
        """
        Get crawl sitemap

        >>> connection.get_crawl(0, 1, 3, "xSbcfwBTi")
        xSbcfwBTi

        :param account_id: account id
        :type account_id: int or str
        :param project_id: project id
        :type project_id: int or str
        :param crawl_id: project id
        :type crawl_id: int or str
        :param sitemap_code: sitemap code
        :type sitemap_code: str
        :return: Requested crawl sitemap
        :rtype: DeepCrawlCrawlSitemap
        """
        endpoint_url = get_api_endpoint(
            endpoint='crawl_sitemap',
            account_id=account_id, project_id=project_id, crawl_id=crawl_id, sitemap_code=sitemap_code
        )
        response = self.dc_request(url=endpoint_url, method='get')
        return DeepCrawlCrawlSitemap(
            account_id=account_id, project_id=project_id, crawl_id=crawl_id, sitemap_data=response.json()
        )
