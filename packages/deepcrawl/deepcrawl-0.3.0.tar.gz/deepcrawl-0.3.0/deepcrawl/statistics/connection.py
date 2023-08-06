"""
Statistics Connection
=====================
"""
from typing import List, Optional, Union

from deepcrawl.api import ApiConnection
from deepcrawl.api.api_endpoints import get_api_endpoint
from deepcrawl.statistics.statistic import DeepCrawlCrawlStatistic, DeepCrawlIssueStatistic, DeepCrawlReportStatistic


class StatisticConnection(ApiConnection):
    """
    REPORT STATISTIC

        * endpoint: accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/statistics
        * http methods: GET
        * methods: get_report_statistics

        - endpoint: accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/statistics/{statistic_type}
        - http methods: GET
        - methods: get_report_statistic

    CRAWL STATISTIC

        * endpoint: accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/statistics
        * http methods: GET
        * methods: get_crawl_statistics

        - endpoint: accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/statistics/{statistic_type}
        - http methods: GET
        - methods: get_crawl_statistic

    ISSUE STATISTIC

        * endpoint: accounts/{account_id}/projects/{project_id}/issues/{issue_id}/statistics
        * http methods: GET
        * methods: get_issue_statistics

        - endpoint: accounts/{account_id}/projects/{project_id}/issues/{issue_id}/statistics/{statistic_type}
        - http methods: GET
        - methods: get_issue_statistic
    """

    """
    REPORT
    """

    def get_report_statistics(
            self, account_id: Union[int, str], project_id: Union[int, str], crawl_id: Union[int, str],
            report_id: str, filters: Optional[dict] = None, **kwargs
    ) -> List[DeepCrawlReportStatistic]:
        """
        Get report statistics

        >>> connection.get_report_statistics(1, 2, 3, "duplicate_body_content:basic")
        [Template 29 Trend, Template 30 Trend]

        :param account_id: account id
        :type account_id: int or str
        :param project_id: project id
        :type project_id: int or str
        :param crawl_id: crawl id
        :type crawl_id: int or str
        :param report_id: report id
        :type report_id: str
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :return: List of report statistics
        :rtype: list
        """
        request_url: str = get_api_endpoint(
            "report_statistics",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id, report_id=report_id
        )
        statistics_response: List[dict] = self.get_paginated_data(request_url, method='get', filters=filters, **kwargs)

        list_of_statistics = []
        for statistic in statistics_response:
            list_of_statistics.append(DeepCrawlReportStatistic(
                account_id=account_id, project_id=project_id, crawl_id=crawl_id, report_id=report_id,
                statistic_data=statistic
            ))
        return list_of_statistics

    def get_report_statistic(
            self, account_id: Union[int, str], project_id: Union[int, str], crawl_id: Union[int, str],
            report_id: str, statistic_type: str
    ) -> DeepCrawlReportStatistic:
        """
        Get report statistic

        >>> connection.get_report_statistics(1, 2, 3, "duplicate_body_content:basic", "report_trend")
        Template 29 Trend

        :param account_id: account id
        :type account_id: int or str
        :param project_id: project id
        :type project_id: int or str
        :param crawl_id: crawl id
        :type crawl_id: int or str
        :param report_id: report id
        :type report_id: str
        :param statistic_type: statistic type
        :type statistic_type: str
        :return: Requested statistic
        :rtype: DeepCrawlReportStatistic
        """
        request_url: str = get_api_endpoint(
            "report_statistic",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id, report_id=report_id,
            statistic_type=statistic_type
        )
        response = self.dc_request(url=request_url, method='get')
        return DeepCrawlReportStatistic(
            account_id=account_id, project_id=project_id, crawl_id=crawl_id, report_id=report_id,
            statistic_data=response.json()
        )

    """
    CRAWLS
    """

    def get_crawl_statistics(
            self, account_id: Union[int, str], project_id: Union[int, str], crawl_id: Union[int, str],
            filters: Optional[dict] = None, **kwargs
    ) -> List[DeepCrawlCrawlStatistic]:
        """
        Get crawl statistics

        >>> connection.get_crawl_statistics(1, 2, 3)
        [URL Breakdown, Web Crawl Depth]

        :param account_id: account id
        :type account_id: int or str
        :param project_id: project id
        :type project_id: int or str
        :param crawl_id: crawl id
        :type crawl_id: int or str
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :return: List of crawl statistics
        :rtype: list
        """
        request_url: str = get_api_endpoint(
            "crawl_statistics", account_id=account_id, project_id=project_id, crawl_id=crawl_id
        )
        statistics_response: List[dict] = self.get_paginated_data(request_url, method='get', filters=filters, **kwargs)

        list_of_statistics = []
        for statistic in statistics_response:
            list_of_statistics.append(DeepCrawlCrawlStatistic(
                account_id=account_id, project_id=project_id, crawl_id=crawl_id,
                statistic_data=statistic
            ))
        return list_of_statistics

    def get_crawl_statistic(
            self, account_id: Union[int, str], project_id: Union[int, str], crawl_id: Union[int, str],
            statistic_type: str
    ) -> DeepCrawlCrawlStatistic:
        """
        Get crawl statistic

        >>> connection.get_crawl_statistic(1, 2, 3, "url_breakdown")
        URL Breakdown

        :param account_id: account id
        :type account_id: int or str
        :param project_id: project id
        :type project_id: int or str
        :param crawl_id: crawl id
        :type crawl_id: int or str
        :param statistic_type: statistic type
        :type statistic_type: str
        :return: Requested statistic
        :rtype: DeepCrawlCrawlStatistic
        """
        request_url: str = get_api_endpoint(
            "crawl_statistic",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id, statistic_type=statistic_type
        )
        response = self.dc_request(url=request_url, method='get')
        return DeepCrawlCrawlStatistic(
            account_id=account_id, project_id=project_id, crawl_id=crawl_id, statistic_data=response.json()
        )

    """
    ISSUES
    """

    def get_issue_statistics(
            self, account_id: Union[int, str], project_id: Union[int, str], issue_id: Union[int, str],
            filters: Optional[dict] = None, **kwargs
    ) -> List[DeepCrawlIssueStatistic]:
        """
        Get issue statistics

        >>> connection.get_issue_statistics(1, 2, 3)
        [Recent Issue Trend, Recent Issue Trend]

        :param account_id: account id
        :type account_id: int or str
        :param project_id: project id
        :type project_id: int or str
        :param issue_id: issue id
        :type issue_id: int or str
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :return: List of issue statistics
        :rtype: list
        """
        request_url: str = get_api_endpoint(
            "issue_statistics", account_id=account_id, project_id=project_id, issue_id=issue_id
        )
        statistics_response: List[dict] = self.get_paginated_data(request_url, method='get', filters=filters, **kwargs)

        list_of_statistics = []
        for statistic in statistics_response:
            list_of_statistics.append(DeepCrawlIssueStatistic(
                account_id=account_id, project_id=project_id, issue_id=issue_id,
                statistic_data=statistic
            ))
        return list_of_statistics

    def get_issue_statistic(
            self, account_id: Union[int, str], project_id: Union[int, str], issue_id: Union[int, str],
            statistic_type: str
    ) -> DeepCrawlIssueStatistic:
        """
        Get issue statistic

        >>> connection.get_issue_statistic(1, 2, 3, "url_breakdown")
        Recent Issue Trend

        :param account_id: account id
        :type account_id: int or str
        :param project_id: project id
        :type project_id: int or str
        :param issue_id: issue id
        :type issue_id: int or str
        :param statistic_type: statistic type
        :type statistic_type: str
        :return: Requested statistic
        :rtype: DeepCrawlIssueStatistic
        """
        request_url: str = get_api_endpoint(
            "issue_statistic",
            account_id=account_id, project_id=project_id, issue_id=issue_id, statistic_type=statistic_type
        )
        response = self.dc_request(url=request_url, method='get')
        return DeepCrawlIssueStatistic(
            account_id=account_id, project_id=project_id, issue_id=issue_id, statistic_data=response.json()
        )
