import { authClient, firestoreClient } from '../_firebase/firebase_client';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, User, sendPasswordResetEmail } from 'firebase/auth';
import { doc, serverTimestamp, setDoc } from 'firebase/firestore';
import { AppControlsPublicModel } from '../models/model.app_controls';
import { apiUpdateAppControlsPublic } from './firestore_appcontrols_service';

export async function signinWithEmail(email: string, password: string): Promise<User | null> {
  email.trim().toLowerCase();
  try {
    const res = await signInWithEmailAndPassword(authClient, email, password);
    return res.user;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function resetPassword(email: string): Promise<boolean> {
  email.trim().toLowerCase();

  try {
    const res = await sendPasswordResetEmail(authClient, email);
    return true;
  } catch (error) {
    throw error;
  }
}

export async function createSuperAdminUserWithEmail(email: string, password: string): Promise<User | undefined> {
  try {
    email.trim().toLowerCase();
    const res = await createUserWithEmailAndPassword(authClient, email, password);
    if (res) {
      await setDoc(
        doc(firestoreClient, 'users', res.user.uid),
        {
          name: '',
          email: res.user.email,
          isNotificationsEnabled: true,
          isAdmin: true,
          isSuperAdmin: true,
          subIsLifetime: true,
          timestampUpdated: serverTimestamp(),
          timestampCreated: serverTimestamp(),
          roles: ['admin', 'superadmin']
        },
        { merge: true }
      );

      const appInfoModel = new AppControlsPublicModel();
      await apiUpdateAppControlsPublic(appInfoModel);
      await setDoc(doc(firestoreClient, 'appControlsPrivate', 'appControlsPrivate'), { isSuperAdminConfigured: true }, { merge: true });

      return res.user;
    }
  } catch (error) {
    throw error;
  }
}
export async function signOut(): Promise<void> {
  try {
    await authClient.signOut();
  } catch (error) {
    throw error;
  }
}
