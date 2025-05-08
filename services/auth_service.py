from werkzeug.security import check_password_hash
from repository.user_repo import find_user_by_email

def authenticate_user(email: str, password: str):
    user = find_user_by_email(email)
    if user and check_password_hash(user['password'], password):
        print(user)
        return user
    return None

