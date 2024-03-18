import firebase_admin
from firebase_admin import credentials, firestore, auth

firebase_cred = credentials.Certificate("app/_firebase/firebase.json")
firebase_app = firebase_admin.initialize_app(firebase_cred, {}) if not firebase_admin._apps else firebase_admin.get_app()

firestore_db = firestore.client(firebase_app)
firebase_auth = auth


def ensure_firebase_app():
    global firebase_app
    global firestore_db
    if not firebase_admin._apps:
        firebase_app = firebase_admin.initialize_app(firebase_cred, {})
        firestore_db = firestore.client(firebase_app)
