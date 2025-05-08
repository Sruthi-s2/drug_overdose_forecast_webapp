from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
from werkzeug.security import generate_password_hash


# MongoDB connection (replace with your URI if needed)
client = MongoClient("mongodb+srv://Sruthi:wWtlUgwBCAO9iWz9@drug-overdose-cluster.hhbelb5.mongodb.net/")
db = client["drug_overdose_db"]

# # User details
# email = "sruthilayaganji.19@gmail.com"
# password = "Sruthi@123"
# role = "admin"

# # Hash the password
# hashed_pw = generate_password_hash(password)

# # Prepare the document
# user_doc = {
#     "email": email,
#     "password": hashed_pw,
#     "role": role
# }

# # Insert into user_login collection
# result = db["user_login"].insert_one(user_doc)

# print("✅ Admin user inserted with ID:", result.inserted_id)



db.states.insert_many([
  { "name": "Alabama", "code": "AL" },
  { "name": "Alaska", "code": "AK" },
  { "name": "Arizona", "code": "AZ" },
  { "name": "Arkansas", "code": "AR" },
  { "name": "California", "code": "CA" },
  { "name": "Colorado", "code": "CO" },
  { "name": "Connecticut", "code": "CT" },
  { "name": "Delaware", "code": "DE" },
  { "name": "Florida", "code": "FL" },
  { "name": "Georgia", "code": "GA" },
  { "name": "Hawaii", "code": "HI" },
  { "name": "Idaho", "code": "ID" },
  { "name": "Illinois", "code": "IL" },
  { "name": "Indiana", "code": "IN" },
  { "name": "Iowa", "code": "IA" },
  { "name": "Kansas", "code": "KS" },
  { "name": "Kentucky", "code": "KY" },
  { "name": "Louisiana", "code": "LA" },
  { "name": "Maine", "code": "ME" },
  { "name": "Maryland", "code": "MD" },
  { "name": "Massachusetts", "code": "MA" },
  { "name": "Michigan", "code": "MI" },
  { "name": "Minnesota", "code": "MN" },
  { "name": "Mississippi", "code": "MS" },
  { "name": "Missouri", "code": "MO" },
  { "name": "Montana", "code": "MT" },
  { "name": "Nebraska", "code": "NE" },
  { "name": "Nevada", "code": "NV" },
  { "name": "New Hampshire", "code": "NH" },
  { "name": "New Jersey", "code": "NJ" },
  { "name": "New Mexico", "code": "NM" },
  { "name": "New York", "code": "NY" },
  { "name": "North Carolina", "code": "NC" },
  { "name": "North Dakota", "code": "ND" },
  { "name": "Ohio", "code": "OH" },
  { "name": "Oklahoma", "code": "OK" },
  { "name": "Oregon", "code": "OR" },
  { "name": "Pennsylvania", "code": "PA" },
  { "name": "Rhode Island", "code": "RI" },
  { "name": "South Carolina", "code": "SC" },
  { "name": "South Dakota", "code": "SD" },
  { "name": "Tennessee", "code": "TN" },
  { "name": "Texas", "code": "TX" },
  { "name": "Utah", "code": "UT" },
  { "name": "Vermont", "code": "VT" },
  { "name": "Virginia", "code": "VA" },
  { "name": "Washington", "code": "WA" },
  { "name": "West Virginia", "code": "WV" },
  { "name": "Wisconsin", "code": "WI" },
  { "name": "Wyoming", "code": "WY" }
]);

