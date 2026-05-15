from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "advisor_ai_secret_key"

ALGORITHM = "HS256"

# -----------------------------
# MOCK USERS
# -----------------------------
users_db = {
    "advisor_user": {
        "password": "advisor123",
        "role": "advisor"
    },
    "compliance_user": {
        "password": "compliance123",
        "role": "compliance"
    },
    "admin_user": {
        "password": "admin123",
        "role": "admin"
    }
}


# -----------------------------
# AUTHENTICATE USER
# -----------------------------
def authenticate_user(username, password):

    user = users_db.get(username)

    if not user:
        return None

    if user["password"] != password:
        return None

    return user


# -----------------------------
# CREATE JWT TOKEN
# -----------------------------
def create_access_token(data):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=2)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt