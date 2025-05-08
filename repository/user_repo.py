from services.db_service import db

def find_user_by_email(email: str):
    user = db['user_login'].find_one({"email": email})
    if user:
        print(user)
        return {
            "email": user.get("email"),
            "password": user.get("password"),
            "role": user.get("role")  
        }
    return None

def create_user(email, hashed_password, role):
    existing = db["user_login"].find_one({"email": email})
    if existing:
        raise Exception("A user with this email already exists.")

    db["user_login"].insert_one({
        "email": email,
        "password": hashed_password,
        "role": role
    })
        
 
def get_filtered_users(email=None, role=None):
    query = {}
    if email:
        query['email'] = {"$regex": email, "$options": "i"}
    if role:
        query['role'] = role
    return list(db["user_login"].find(query, {"password": 0}))
   
def delete_user_by_emails(emails):
    db["user_login"].delete_many({"email": {"$in": emails}})