"""
Datasource
==========
"""

from typing import List, Optional

import deepcrawl
from deepcrawl.report_templates.report_template import DeepCrawlReportTemplate
from deepcrawl.utils import ImmutableAttributesMixin

datasource_extra_fields = (
    'report_templates',
)

datasource_immutable_fields = (
    "code",
    "column_types",
    "version",

    "_href",
    "_report_templates_href",
    "_metrics_href"
)

datasource_fields = datasource_extra_fields + datasource_immutable_fields


class DeepCrawlDatasource(ImmutableAttributesMixin):
    """
    Datasource
    """

    __slots__ = datasource_fields
    mutable_attributes = datasource_extra_fields

    def __init__(self, datasource_data: dict):
        self.code = datasource_data.get("code")
        self.column_types = datasource_data.get("column_types")
        self.version = datasource_data.get("version")

        self.report_templates = []

        self._href = datasource_data.get("_href")
        self._report_templates_href = datasource_data.get(
            "_report_templates_href")
        self._metrics_href = datasource_data.get("_metrics_href")

        super(DeepCrawlDatasource, self).__init__()

    def __repr__(self) -> str:
        return self.code

    def __str__(self) -> str:
        return self.code

    def load_datasource_report_templates(
        self, connection: 'deepcrawl.DeepCrawlConnection' = None, filters: Optional[dict] = None, **kwargs
    ) -> List[DeepCrawlReportTemplate]:
        """
        Load report templates in curent instance

        >>> self.load_report_templates()
        [duplicate_content, duplicate_titles]
        >>> self.report_templates
        [duplicate_content, duplicate_titles]

        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: list of report templates
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.report_templates = connection.get_datasource_report_templates(
            self.code, filters=filters, **kwargs)
        return self.report_templates

    def get_datasource_report_templates(
        self, use_cache: bool = True,
        connection: 'deepcrawl.DeepCrawlConnection' = None, filters: Optional[dict] = None, **kwargs
    ) -> List[DeepCrawlReportTemplate]:
        """
        Get datasource report templates

        * use_cache=True > get_datasource_report_templates will return cached report templates changes or will do a call to DeepCrawl if report_templates attribute is empty.
        * use_cache=False > get_datasource_report_templates will call DeepCrawl api and will override report_templates attribute.

        >>> self.get_datasource_report_templates()
        [duplicate_content, duplicate_titles]

        :param use_cache:
        :type use_cache: bool
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: list of datasource report templates
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if self.report_templates and use_cache:
            return self.report_templates
        return self.load_datasource_report_templates(connection=connection, filters=filters, **kwargs)
