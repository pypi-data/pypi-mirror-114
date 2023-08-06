"""
Report Template
===============
"""

from deepcrawl.utils import ImmutableAttributesMixin

report_template_extra_fields = (
    "id",
)

report_immutable_fields = report_template_extra_fields + (
    "code",
    "category",
    "datasource_code",
    "description",
    "name",
    "position",
    "report_types",
    "summary",
    "total_sign",
    "change_sign",
    "total_weight",
    "change_weight",
    "metrics_grouping",
    "metric_types",
    "download_output_types",
    "tags",
    "_datasource_href",
    "_href",
)


class DeepCrawlReportTemplate(ImmutableAttributesMixin):
    """
    Report Template class
    """
    __slots__ = report_immutable_fields
    mutable_attributes = []

    def __init__(self, report_template_data: dict):
        self.id = report_template_data.get('_href', "").split('/')[-1]

        self.code = report_template_data.get("code")
        self.category = report_template_data.get("category")
        self.datasource_code = report_template_data.get("datasource_code")
        self.description = report_template_data.get("description")
        self.name = report_template_data.get("name")
        self.position = report_template_data.get("position")
        self.report_types = report_template_data.get("report_types")
        self.summary = report_template_data.get("summary")
        self.total_sign = report_template_data.get("total_sign")
        self.change_sign = report_template_data.get("change_sign")
        self.total_weight = report_template_data.get("total_weight")
        self.change_weight = report_template_data.get("change_weight")
        self.metrics_grouping = report_template_data.get("metrics_grouping")
        self.metric_types = report_template_data.get("metric_types")
        self.download_output_types = report_template_data.get(
            "download_output_types")
        self.tags = report_template_data.get("tags")
        self._datasource_href = report_template_data.get("_datasource_href")
        self._href = report_template_data.get("_href")

        super(DeepCrawlReportTemplate, self).__init__()

    def __repr__(self) -> str:
        return self.code

    def __str__(self) -> str:
        return self.code
