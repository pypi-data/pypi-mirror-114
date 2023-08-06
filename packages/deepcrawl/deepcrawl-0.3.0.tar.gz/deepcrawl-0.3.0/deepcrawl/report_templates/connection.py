"""
Report Templates Connection
===========================
"""
from typing import List, Optional, Union

from deepcrawl.api import ApiConnection
from deepcrawl.api.api_endpoints import get_api_endpoint

from .datasource import DeepCrawlDatasource
from .report_template import DeepCrawlReportTemplate


class ReportTemplatesConnection(ApiConnection):
    """
    REPORT TEMPLATES

        * endpoint: /report_templates
        * http methods: GET
        * methods: get_report_templates

        - endpoint: /datasources/{datasource_code}/report_templates
        - http methods: GET
        - methods: get_datasource_report_templates

        * endpoint: /datasources/{datasource_code}/report_templates/{report_template_id}
        * http methods: GET
        * methods: get_datasource_report_template

    DATASOURCES
        * endpoint: /datasources
        * http methods: GET
        * methods: get_datasources

        - endpoint: /datasources/{datasource_code}
        - http methods: GET
        - methods: get_datasource
    """

    def get_datasources(self, filters: Optional[dict] = None, **kwargs) -> List[DeepCrawlDatasource]:
        """
        Get datasources

        >>> connection.get_datasources()
        [crawl_duplicate_urls, crawl_hreflangs]

        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :return: List of report templates
        :rtype: list
        """
        request_url: str = get_api_endpoint("datasources")
        datasources_data: List[dict] = self.get_paginated_data(
            request_url, method='get', filters=filters, **kwargs
        )
        list_of_datasources = []
        for template in datasources_data:
            list_of_datasources.append(DeepCrawlDatasource(template))
        return list_of_datasources

    def get_datasource(self, datasource_code: str) -> DeepCrawlDatasource:
        """
        Get datasource

        >>> connection.get_datasource('crawl_duplicate_urls')
        crawl_duplicate_urls

        :param datasource_code: datasource code
        :type datasource_code: str
        :return: Requested datasources
        :rtype: DeepCrawlDatasource
        """
        request_url: str = get_api_endpoint(
            "datasource", datasource_code=datasource_code)
        response = self.dc_request(url=request_url, method='get')
        return DeepCrawlDatasource(response.json())

    def get_report_templates(self, filters: Optional[dict] = None, **kwargs) -> List[DeepCrawlReportTemplate]:
        """
        Get report templates

        >>> connection.get_report_templates()
        [duplicate_content, duplicate_titles]

        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :return: List of report templates
        :rtype: list
        """
        request_url: str = get_api_endpoint("report_templates")
        report_templates_data: List[dict] = self.get_paginated_data(
            request_url, method='get', filters=filters, **kwargs
        )
        list_of_templates = []
        for template in report_templates_data:
            list_of_templates.append(DeepCrawlReportTemplate(template))
        return list_of_templates

    def get_datasource_report_templates(
        self, datasource_code: str, filters: Optional[dict] = None, **kwargs
    ) -> List[DeepCrawlReportTemplate]:
        """
        Get datasource report templates

        >>> connection.datasource_report_templates(datasource_code)
        [duplicate_content, duplicate_titles]

        :param datasource_code: datasource code
        :type datasource_code: str
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :return: List of report templates
        :rtype: list
        """
        request_url: str = get_api_endpoint(
            "datasource_report_templates", datasource_code=datasource_code)
        report_templates_data: List[dict] = self.get_paginated_data(
            request_url, method='get', filters=filters, **kwargs
        )
        list_of_templates = []
        for template in report_templates_data:
            list_of_templates.append(DeepCrawlReportTemplate(template))
        return list_of_templates

    def get_datasource_report_template(
        self, datasource_code: str, report_template_id: Union[int, str]
    ) -> DeepCrawlReportTemplate:
        """
        Get datasource report template

        >>> connection.get_datasource_report_template('crawl_duplicate_urls', 1)
        duplicate_content

        :param datasource_code: datasource code
        :type datasource_code: str
        :param report_template_id: report template id
        :type report_template_id: int or str
        :return: Requested report template
        :rtype: DeepCrawlReportTemplate
        """
        request_url: str = get_api_endpoint(
            "datasource_report_template",
            datasource_code=datasource_code, report_template_id=report_template_id
        )
        response = self.dc_request(url=request_url, method='get')
        return DeepCrawlReportTemplate(response.json())
