import * as admin from 'firebase-admin';

export const firebaseConfigServer = {
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
  privateKey: process.env.FIREBASE_PRIVATE_KEY!.replace(/\\n/g, '\n')
};

const app = getApp();

let authAdmin: admin.auth.Auth;
let firestoreAdmin: admin.firestore.Firestore;

authAdmin = admin.auth(app);
firestoreAdmin = admin.firestore(app);

function getApp() {
  if (admin.apps.length > 0) return admin.apps[0]!;

  return admin.initializeApp({
    credential: admin.credential.cert(firebaseConfigServer)
  });
}

export { firestoreAdmin, authAdmin };
