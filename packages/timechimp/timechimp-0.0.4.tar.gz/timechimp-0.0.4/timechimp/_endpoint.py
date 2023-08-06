"""Module containing TimeChimp API endpoints
TimeChimp API doc: https://api.timechimp.com/
"""
HOSTNAME = "https://api.timechimp.com"

DEFAULT_VERSION = "1"
VERSION_ENDPOINT = "/".join([HOSTNAME, "v{version}"])

CUSTOMERS_ENDPOINT = "/".join([VERSION_ENDPOINT, "customers"])
EXPENSES_ENDPOINT = "/".join([VERSION_ENDPOINT, "expenses"])
INVOICES_ENDPOINT = "/".join([VERSION_ENDPOINT, "invoices"])
MILEAGE_ENDPOINT = "/".join([VERSION_ENDPOINT, "mileage"])
PROJECTS_ENDPOINT = "/".join([VERSION_ENDPOINT, "projects"])
PROJECT_NOTES_ENDPOINT = "/".join([VERSION_ENDPOINT, "projectnotes"])
PROJECT_TASKS_ENDPOINT = "/".join([VERSION_ENDPOINT, "projecttasks"])
PROJECT_USERS_ENDPOINT = "/".join([VERSION_ENDPOINT, "projectusers"])
TAGS_ENDPOINT = "/".join([VERSION_ENDPOINT, "tags"])
TASKS_ENDPOINT = "/".join([VERSION_ENDPOINT, "tasks"])
TIME_ENDPOINT = "/".join([VERSION_ENDPOINT, "time"])
USERS_ENDPOINT = "/".join([VERSION_ENDPOINT, "users"])
USER_CONTRACTS_ENDPOINT = "/".join([VERSION_ENDPOINT, "userContracts"])
