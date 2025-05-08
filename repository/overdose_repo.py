from services.db_service import db
from bson import ObjectId


def query_records(filters):
    query = {}
    if filters.get("year") is not None:
        query["year"] = filters["year"]
    if filters.get("month"):
        query["month"] = filters["month"]
    if filters.get("state"):
        query["state.name"] = filters["state"]
    if filters.get("indicator"):
        query["indicator"] = filters["indicator"]

    limit = filters.get("limit", 8)
    cursor = db["overdose_deaths"].find(query).limit(limit)

    records = []
    for doc in cursor:
        records.append({
            "year": doc.get("year"),
            "month": doc.get("month"),
            "state": doc.get("state", {}).get("name"),
            "indicator": doc.get("indicator"),
            "no_of_deaths": doc.get("no_of_deaths")
        })
    return records


def fetch_filter_options():
    collection = db["overdose_deaths"]

    years = sorted(collection.distinct("year"))
    months = sorted(collection.distinct("month"))
    states = sorted(collection.distinct("state.name"))
    indicators = sorted(collection.distinct("indicator"))

    return {
        "years": years,
        "months": months,
        "states": states,
        "indicators": indicators
    }



def find_single_record(filters):
    query = {
        "year": filters["year"],
        "month": filters["month"],
        "state.name": filters["state"],
        "indicator": filters["indicator"]
    }

    return db["overdose_deaths"].find_one(query)

def update_overdose_record(record_id, updated_data):
    return db["overdose_deaths"].update_one(
        {"_id": ObjectId(record_id)},
        {"$set": updated_data}
    )
    

def find_conflicting_record(updated_data, current_id):
    return db["overdose_deaths"].find_one({
        "_id": {"$ne": ObjectId(current_id)},
        "year": updated_data["year"],
        "month": updated_data["month"],
        "state.name": updated_data["state"]["name"],
        "indicator": updated_data["indicator"],
        "no_of_deaths": updated_data["no_of_deaths"]
    })
    
def find_records_for_deletion(filter_query):
    return list(db["overdose_deaths"].find(filter_query))



def delete_overdose_records(filter_criteria):
    return db["overdose_deaths"].delete_many(filter_criteria)

from bson import ObjectId

def delete_by_ids(id_list):
    object_ids = [ObjectId(i) for i in id_list]
    return db["overdose_deaths"].delete_many({"_id": {"$in": object_ids}})


def get_overdose_records_by_filters(indicator=None, years=None, states=None, months=None):
    query = {}
    if indicator:
        query["indicator"] = indicator
    if years:
        query["year"] = {"$in": years}
    if states:
        query["state.name"] = {"$in": states}
    if months:
        query["month"] = {"$in": months}

    return list(db["overdose_deaths"].find(query))



