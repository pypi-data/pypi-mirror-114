"""
Statistic
=========
"""
from typing import Union

from deepcrawl.utils import ImmutableAttributesMixin

statistic_extra_fields = (
    'id',
    'account_id',
    'project_id'
)

statistic_immutable_fields = statistic_extra_fields + (
    'statistics_type',
    'title',
    'argument_title',
    'argument_type',
    'data',
    '_href',
    '_account_href',
    '_project_href'
)


class DeepCrawlStatisticBase(ImmutableAttributesMixin):
    mutable_attributes = []

    def __init__(self, account_id: Union[int, str], project_id: Union[int, str], statistic_data: dict):
        # relations
        self.account_id = account_id
        self.project_id = project_id

        self.statistics_type = statistic_data['statistics_type']
        self.title = statistic_data['title']
        self.argument_title = statistic_data['argument_title']
        self.argument_type = statistic_data['argument_type']
        self.data = statistic_data['data']
        self._href = statistic_data['_href']
        self._account_href = statistic_data['_account_href']
        self._project_href = statistic_data['_project_href']

        super(DeepCrawlStatisticBase, self).__init__()

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


report_statistic_immutable_fields = statistic_immutable_fields + (
    'crawl_id',
    'report_id',
    '_crawl_href',
    '_report_href',
    '_report_href_alt',
)


class DeepCrawlReportStatistic(DeepCrawlStatisticBase):
    """
    Report statistic class
    """
    __slots__ = report_statistic_immutable_fields
    mutable_attributes = []

    def __init__(
            self, account_id: Union[int, str], project_id: Union[int, str], crawl_id: Union[int, str], report_id: str,
            statistic_data: dict
    ):
        # relations
        self.crawl_id = crawl_id
        self.report_id = report_id

        self._crawl_href = statistic_data['_crawl_href']
        self._report_href = statistic_data['_report_href']
        self._report_href_alt = statistic_data['_report_href_alt']

        super(DeepCrawlReportStatistic, self).__init__(account_id, project_id, statistic_data)

    @property
    def to_dict_immutable_fields(self) -> dict:
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in report_statistic_immutable_fields}


crawl_statistic_immutable_fields = statistic_immutable_fields + (
    'crawl_id',
    '_crawl_href',
)


class DeepCrawlCrawlStatistic(DeepCrawlStatisticBase):
    """
    Crawl statistic class
    """
    __slots__ = crawl_statistic_immutable_fields
    mutable_attributes = []

    def __init__(
            self, account_id: Union[int, str], project_id: Union[int, str], crawl_id: Union[int, str],
            statistic_data: dict
    ):
        # relations
        self.crawl_id = crawl_id

        self._crawl_href = statistic_data['_crawl_href']

        super(DeepCrawlCrawlStatistic, self).__init__(account_id, project_id, statistic_data)

    @property
    def to_dict_immutable_fields(self) -> dict:
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in crawl_statistic_immutable_fields}


issue_statistic_immutable_fields = statistic_immutable_fields + (
    'issue_id',
    '_issue_href',
)


class DeepCrawlIssueStatistic(DeepCrawlStatisticBase):
    """
    Issue statistic class
    """
    __slots__ = issue_statistic_immutable_fields
    mutable_attributes = []

    def __init__(
            self, account_id: Union[int, str], project_id: Union[int, str], issue_id: Union[int, str],
            statistic_data: dict
    ):
        # relations
        self.crawl_id = issue_id
        self._issue_href = statistic_data['_issue_href']

        super(DeepCrawlIssueStatistic, self).__init__(account_id, project_id, statistic_data)

    @property
    def to_dict_immutable_fields(self) -> dict:
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in issue_statistic_immutable_fields}
