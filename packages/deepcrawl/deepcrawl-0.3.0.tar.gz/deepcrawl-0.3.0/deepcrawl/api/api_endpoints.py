from deepcrawl.exceptions import InvalidDcUrl

DC_BASE_URL = "https://api.deepcrawl.com/"

ENDPOINTS = {
    # auth
    "session": "sessions",

    # Users
    "users": "users",
    "user_resend": "users/{uid}/resend",
    "user_set_password": "users/{uid}/set_password",

    # Accounts
    "account": "accounts/{account_id}",
    "accounts": "accounts",

    # Account Users
    "user_account": "users/{uid}/accounts/{account_id}",
    "user_accounts": "users/{uid}/accounts",
    "account_user": "accounts/{account_id}/users/{uid}",
    "account_users": "accounts/{account_id}/users",

    # Projects
    "project": "accounts/{account_id}/projects/{project_id}",
    "projects": "accounts/{account_id}/projects",
    "project_upload": "accounts/{account_id}/projects/{project_id}/uploads/{project_upload_id}",
    "project_uploads": "accounts/{account_id}/projects/{project_id}/uploads",
    "project_upload_types": "project_upload_types",
    "project_upload_type": "project_upload_types/{project_upload_type_code}",

    "majestic": "accounts/{account_id}/projects/{project_id}/majestic_configuration",

    "issue": "accounts/{account_id}/projects/{project_id}/issues/{issue_id}",
    "issues": "accounts/{account_id}/projects/{project_id}/issues",

    # Crawls
    "crawl": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}",
    "crawls": "accounts/{account_id}/projects/{project_id}/crawls",

    "crawl_schedule": "accounts/{account_id}/projects/{project_id}/schedules/{schedule_id}",
    "crawl_schedules": "accounts/{account_id}/projects/{project_id}/schedules",

    # Reports
    "report": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}",
    "reports": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports",
    "reports_changes": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/changes",

    "report_row": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/"
                  "report_rows/{report_row_id}",
    "report_rows": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/"
                   "report_rows",

    # Downloads
    "crawl_downloads": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/downloads",
    "report_download": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/"
                       "downloads/{report_download_id}",
    "report_downloads": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/"
                        "downloads",

    # Statistics
    "report_statistics": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/"
                         "statistics",
    "report_statistic": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/"
                        "statistics/{statistic_type}",
    "crawl_statistics": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/statistics",
    "crawl_statistic": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/statistics/{statistic_type}",
    "issue_statistics": "accounts/{account_id}/projects/{project_id}/issues/{issue_id}/statistics",
    "issue_statistic": "accounts/{account_id}/projects/{project_id}/issues/{issue_id}/statistics/{statistic_type}",

    # Report templates
    "report_templates": "report_templates",
    "datasources": "datasources",
    "datasource": "datasources/{datasource_code}",
    "datasource_report_templates": "datasources/{datasource_code}/report_templates",
    "datasource_report_template": "datasources/{datasource_code}/report_templates/{report_template_id}",

    # Sitemaps
    "project_sitemaps": "accounts/{account_id}/projects/{project_id}/sitemaps",
    "project_sitemap": "accounts/{account_id}/projects/{project_id}/sitemaps/{sitemap_code}",
    "crawl_sitemaps": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/sitemaps",
    "crawl_sitemap": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/sitemaps/{sitemap_code}",
}


def get_api_endpoint(endpoint: str, **kwargs) -> str:
    """
    >>> get_api_endpoint("report", account_id=1, project_id=2, crawl_id=3, report_id=4)
    """

    try:
        return f"{DC_BASE_URL}{ENDPOINTS.get(endpoint).format(**kwargs)}"
    except Exception:
        raise InvalidDcUrl("Invalid url name or invalid kwargs send.")
