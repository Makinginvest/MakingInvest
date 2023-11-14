import firebase_admin
from firebase_admin import credentials, messaging, firestore, auth

firebase_cred = credentials.Certificate("app/a_firebase/firebase.json")
firebase_app = firebase_admin.initialize_app(firebase_cred, {}) if not firebase_admin._apps else firebase_admin.get_app()

firestore_db = firestore.client(firebase_app)
firebase_auth = auth
