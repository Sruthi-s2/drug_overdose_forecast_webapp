from repository.admin_repo import (
    insert_overdose_record,
    update_overdose_record,
    delete_overdose_records,
    create_user
)
from werkzeug.security import generate_password_hash
from repository.admin_repo import get_all_states
from repository.admin_repo import find_conflicting_record, insert_overdose_record



def fetch_states_for_admin():
    return get_all_states()


def call_insert_record(data):
    
    existing = find_conflicting_record(data)
    if existing:
        raise Exception("A record with the same Year, Month, State, and Indicator already exists.")

    return insert_overdose_record(data)


def call_update_record(record_id, update_data):
    """
    Updates an existing overdose death record by ID.
    """
    return update_overdose_record(record_id, update_data)


def call_delete_records(criteria):
    """
    Deletes overdose death records matching the given filter criteria.
    """
    return delete_overdose_records(criteria)


def call_create_user(email, password, role):
    """
    Creates a new user with a hashed password and assigned role.
    """
    hashed_password = generate_password_hash(password)
    return create_user(email, hashed_password, role)




