from services.db_service import db
from bson import ObjectId


def get_all_states():
    return list(db["states"].find({}, {"_id": 0}))



def insert_overdose_record(data):
    db["overdose_deaths"].insert_one({
        "year": int(data["year"]),
        "month": data["month"],
        "state": {
            "name": data["state_name"],
            "code": data["state_code"]
        },
        "indicator": data["indicator"],
        "no_of_deaths": float(data["no_of_deaths"])
    })



def update_overdose_record(record_id, updated_data):
    """
    Update an overdose death record based on its ObjectId.
    """
    db["overdose_deaths"].update_one(
        {"_id": ObjectId(record_id)},
        {"$set": {
            "no_of_deaths": float(updated_data["no_of_deaths"])
        }}
    )


def delete_overdose_records(criteria):
    """
    Delete overdose death records matching the provided filter criteria.
    """
    query = {}
    if criteria.get("state"):
        query["state.name"] = criteria["state"]
    if criteria.get("month"):
        query["month"] = criteria["month"]
    if criteria.get("indicator"):
        query["indicator"] = criteria["indicator"]

    db["overdose_deaths"].delete_many(query)


def create_user(email, hashed_password, role):
    """
    Create a new user in the user_login collection.
    Checks if email already exists before inserting.
    """
    existing_user = db["user_login"].find_one({"email": email})
    if existing_user:
        raise ValueError("User with this email already exists.")
    
    db["user_login"].insert_one({
        "email": email,
        "password": hashed_password,
        "role": role
    })

from services.db_service import db

def find_conflicting_record(data):
    return db["overdose_deaths"].find_one({
        "year": int(data["year"]),
        "month": data["month"],
        "state.name": data["state_name"],
        "indicator": data["indicator"]
    })

