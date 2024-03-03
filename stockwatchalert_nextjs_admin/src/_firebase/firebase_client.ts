import { Auth, getAuth, User } from '@firebase/auth';
import { Firestore, getFirestore } from '@firebase/firestore';
import { getApps, initializeApp } from 'firebase/app';
import { FirebaseStorage, getStorage } from 'firebase/storage';
import { getAnalytics, Analytics } from 'firebase/analytics';
import { firebaseConfigClient } from '../constants/app_constants';
import { getDatabase, push, ref, set } from 'firebase/database';

let authClient: Auth;
let firestoreClient: Firestore;
let storageClient: FirebaseStorage;
let analyticsClient: Analytics;
let realtimeDbClient: any;

export async function initializeFirebaseClient(): Promise<boolean> {
  if (getApps.length !== 0) return false;

  const app = initializeApp(firebaseConfigClient);
  analyticsClient = getAnalytics(app);
  authClient = getAuth();
  firestoreClient = getFirestore();
  storageClient = getStorage();
  realtimeDbClient = getDatabase();

  return Promise.resolve(true);
}

export async function listenAuthStateChange(): Promise<User | null> {
  return new Promise((resolve, reject) => {
    const unsubscribe = authClient.onAuthStateChanged((user) => {
      unsubscribe();
      resolve(user);
    });
  });
}

export { authClient, firestoreClient, storageClient, analyticsClient, realtimeDbClient };
