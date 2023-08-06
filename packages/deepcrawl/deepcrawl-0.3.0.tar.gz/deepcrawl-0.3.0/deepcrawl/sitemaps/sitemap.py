"""
Sitemap
=======
"""

from typing import Union

from requests import Response

import deepcrawl
from deepcrawl.utils import ImmutableAttributesMixin

project_sitemap_extra_fields = (
    "sitemap_code",
    "account_id",
    "project_id"
)

project_sitemap_mutable_fields = (
    "url",
    "enabled",
    "status",
    "type",
    "level",
    "links_out",
    "children",
)

project_sitemap_immutable_fields = (
    "_href",
)

project_sitemap_fields = project_sitemap_extra_fields + project_sitemap_mutable_fields + \
    project_sitemap_immutable_fields


class DeepCrawlProjectSitemap(ImmutableAttributesMixin):
    """
    Project sitemap class
    """
    __slots__ = project_sitemap_fields
    mutable_attributes = project_sitemap_extra_fields + project_sitemap_mutable_fields

    def __init__(self, account_id: Union[int, str], project_id: Union[int, str], sitemap_data: dict):
        self.account_id = account_id
        self.project_id = project_id

        self.sitemap_code = sitemap_data.get('_href', "").split('/')[-1]
        self.url = sitemap_data.get("url")
        self.enabled = sitemap_data.get("enabled")
        self.status = sitemap_data.get("status")
        self.type = sitemap_data.get("type")
        self.level = sitemap_data.get("level")
        self.links_out = sitemap_data.get("links_out")
        self.children = sitemap_data.get("children")
        self._href = sitemap_data.get("_href")

        super().__init__()

    def __str__(self) -> str:
        return self.sitemap_code

    def __repr__(self) -> str:
        return self.sitemap_code

    def update(
            self, sitemap_data: dict, connection: 'deepcrawl.DeepCrawlConnection' = None
    ) -> 'deepcrawl.sitemaps.DeepCrawlProjectSitemap':
        """
        Update project sitemap instance

        >>> self.update(crawl_data)
        xSbcfwBTi

        :param sitemap_data: crawl configuration
        :type sitemap_data: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: Updated project sitemap
        :rtype: DeepCrawlProjectSitemap
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        sitemap = connection.update_project_sitemap(self.account_id, self.project_id, self.sitemap_code, sitemap_data)
        for key in project_sitemap_mutable_fields:
            setattr(self, key, getattr(sitemap, key))
        return self

    def delete(self, connection: 'deepcrawl.DeepCrawlConnection' = None) -> Response:
        """
        Delete current project sitemap instance

        >>> response = self.delete()
        >>> response.status_code
        204

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: HTTP 204 No Content
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        response = connection.delete_project_sitemap(self.account_id, self.project_id, self.sitemap_code)
        del self
        return response

crawl_sitemap_extra_fields = (
    "sitemap_code",
    "account_id",
    "project_id",
    "crawl_id"
)


crawl_sitemap_immutable_fields = crawl_sitemap_extra_fields + (
    "status",
    "level",
    "links_out",
    "parent",
    "parent_digest",
    "child",
    "child_digest",
    "_href",
    "_account_href",
    "_project_href",
    "_crawl_href"
)


class DeepCrawlCrawlSitemap(ImmutableAttributesMixin):
    """
    Crawl sitemap class
    """
    __slots__ = crawl_sitemap_immutable_fields
    mutable_attributes = []

    def __init__(
        self, account_id: Union[int, str], project_id: Union[int, str], crawl_id: Union[int, str], sitemap_data: dict
    ):
        self.account_id = account_id
        self.project_id = project_id
        self.crawl_id = crawl_id

        self.sitemap_code = sitemap_data.get('_href', "").split('/')[-1]
        self.status = sitemap_data.get("status")
        self.level = sitemap_data.get("level")
        self.links_out = sitemap_data.get("links_out")
        self.parent = sitemap_data.get("parent")
        self.parent_digest = sitemap_data.get("parent_digest")
        self.child = sitemap_data.get("child")
        self.child_digest = sitemap_data.get("child_digest")
        self._href = sitemap_data.get("_href")
        self._account_href = sitemap_data.get("_account_href")
        self._project_href = sitemap_data.get("_project_href")
        self._crawl_href = sitemap_data.get("_crawl_href")

        super().__init__()

    def __str__(self) -> str:
        return self.sitemap_code

    def __repr__(self) -> str:
        return self.sitemap_code
