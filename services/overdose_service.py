from repository.overdose_repo import query_records, fetch_filter_options

def fetch_records(filters):
    return query_records(filters)

def get_filter_options():
    return fetch_filter_options()


