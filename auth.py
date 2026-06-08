import pyrebase
from firebase_config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()

def sign_up(email, password):
    try:
        user = auth.create_user_with_email_and_password(
            email,
            password
        )
        return user
    except Exception as e:
        print(e)
        return None

def sign_in(email, password):
    try:
        user = auth.sign_in_with_email_and_password(
            email,
            password
        )
        return user
    except Exception as e:
        print(e)
        return None