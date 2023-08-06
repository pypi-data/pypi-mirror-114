"""
Issues
======
"""

from typing import List, Optional, Union

import deepcrawl
from deepcrawl.statistics.statistic import DeepCrawlIssueStatistic
from deepcrawl.utils import ImmutableAttributesMixin, safe_string_to_datetime

issue_extra_fields = (
    'id',
    'account_id',
    'project_id',
    'statistics'
)

issue_mutable_fields = issue_extra_fields + (
    'title',
    'assigned_to',
    'deadline_at',
    'description',
    'dismissed',
    'filters',
    'fixed_at',
    'priority',
    'identified',
    'remaining',
    'report_type',
    'discovered_at',
    'report_template',
)

issue_immutable_fields = (
    'created_at',
    'trend',
    'site_primary',
    '_account_href',
    '_project_href',
    '_recent_issue_trend_href',
    '_report_template_href',
    '_report_type_href',
    '_href',
    '_issue_notes_href',
    '_statistics_href',
    '_crawls_finished_last_href',
    '_reports_last_href',
    '_reports_last_href_alt',
    '_reports_last_report_rows_href',
    '_reports_identified_href',
    '_reports_identified_href_alt',
    '_reports_identified_report_rows_href'
)

issue_fields = issue_mutable_fields + issue_immutable_fields


class DeepCrawlIssue(ImmutableAttributesMixin):
    """
    Issues Class
    """
    __slots__ = issue_fields

    mutable_attributes = issue_mutable_fields

    def __init__(self, account_id: Union[int, str], project_id: Union[int, str], issue_data: dict):
        self.id = issue_data.get('_href', "").split('/')[-1]
        self.account_id = account_id
        self.project_id = project_id
        self.statistics = []

        self.title = issue_data.get('title')
        self.assigned_to = issue_data.get('assigned_to')
        self.deadline_at = issue_data.get('deadline_at')
        self.description = issue_data.get('description')
        self.dismissed = issue_data.get('dismissed')
        self.filters = issue_data.get('filters')
        self.fixed_at = issue_data.get('fixed_at')
        self.priority = issue_data.get('priority')
        self.identified = issue_data.get('identified')
        self.remaining = issue_data.get('remaining')
        self.report_type = issue_data.get('report_type')
        self.discovered_at = issue_data.get('discovered_at')
        self.report_template = issue_data.get('report_template')

        self.created_at = safe_string_to_datetime(issue_data.get('created_at'))
        self.trend = issue_data.get('trend')
        self.site_primary = issue_data.get('site_primary')
        self._account_href = issue_data.get('_account_href')
        self._project_href = issue_data.get('_project_href')
        self._recent_issue_trend_href = issue_data.get('_recent_issue_trend_href')
        self._report_template_href = issue_data.get('_report_template_href')
        self._report_type_href = issue_data.get('_report_type_href')
        self._href = issue_data.get('_href')
        self._issue_notes_href = issue_data.get('_issue_notes_href')
        self._statistics_href = issue_data.get('_statistics_href')
        self._crawls_finished_last_href = issue_data.get('_crawls_finished_last_href')
        self._reports_last_href = issue_data.get('_reports_last_href')
        self._reports_last_href_alt = issue_data.get('_reports_last_href_alt')
        self._reports_last_report_rows_href = issue_data.get('_reports_last_report_rows_href')
        self._reports_identified_href = issue_data.get('_reports_identified_href')
        self._reports_identified_href_alt = issue_data.get('_reports_identified_href_alt')
        self._reports_identified_report_rows_href = issue_data.get('_reports_identified_report_rows_href')

        super(DeepCrawlIssue, self).__init__()

    def __repr__(self) -> str:
        return f"[{self.account_id} {self.project_id} {self.id}] {self.title}"

    def __str__(self) -> str:
        return f"[{self.account_id} {self.project_id} {self.id}] {self.title}"

    @property
    def to_dict_mutable_fields(self) -> dict:
        """
        :return: dictionary with the mutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in issue_mutable_fields}

    @property
    def to_dict_immutable_fields(self) -> dict:
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in issue_immutable_fields}

    def load_statistics(
            self, connection: 'deepcrawl.DeepCrawlConnection' = None, filters: Optional[dict] = None, **kwargs
    ) -> List[DeepCrawlIssueStatistic]:
        """
        Loads statistics into current instance

        >>> self.load_statistics()
        [Recent Issue Trend, Recent Issue Trend]
        >>> self.statistics
        [Recent Issue Trend, Recent Issue Trend]

        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: list of statistics
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.statistics = connection.get_issue_statistics(
            self.account_id, self.project_id, self.id, filters=filters, **kwargs
        )
        return self.statistics

    """
    CRAWL STATISTICS
    """

    def get_issue_statistic(
            self, statistic_type: str, connection: 'deepcrawl.DeepCrawlConnection' = None
    ) -> DeepCrawlIssueStatistic:
        """
        Get issue statistic

        >>> self.get_issue_statistic('url_breakdown')
        Recent Issue Trend

        :param statistic_type: statistic type
        :type statistic_type: str
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: Requested statistic
        :rtype: DeepCrawlIssueStatistic
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.get_issue_statistic(
            self.account_id, self.project_id, self.id, statistic_type
        )

    def get_issue_statistics(
            self, use_cache: bool = True,
            connection: 'deepcrawl.DeepCrawlConnection' = None, filters: Optional[dict] = None, **kwargs
    ) -> List[DeepCrawlIssueStatistic]:
        """
        Get issue statistics

        * use_cache=True > get_issue_statistics will return cached statistics or will do a call to DeepCrawl if statistics attribute is empty.
        * use_cache=False > get_issue_statistics will call DeepCrawl api and will override statistics attribute.

        >>> self.get_issue_statistics()
        [Recent Issue Trend, Recent Issue Trend]

        :param use_cache:
        :type use_cache: bool
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: List of statistics
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if self.statistics and use_cache:
            return self.statistics
        return self.load_statistics(connection=connection, filters=filters, **kwargs)
