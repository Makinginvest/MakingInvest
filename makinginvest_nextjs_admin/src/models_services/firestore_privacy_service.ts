import { doc, getDoc, setDoc } from 'firebase/firestore';
import { PrivacyModel } from '../models/model.privacy';
import { authClient, firestoreClient } from '../_firebase/firebase_client';
import { apiGetUser } from './firestore_user_service';

export async function apiUpdatePrivacy(x: PrivacyModel): Promise<boolean> {
  let terms = { ...PrivacyModel.toJson(x) };
  delete terms.id;

  const fbUser = authClient.currentUser;
  const user = await apiGetUser(fbUser!.uid);
  if (!user) throw new Error('No user found!');
  if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to update privacy settings.');
  try {
    await setDoc(doc(firestoreClient, 'appControlsPublic', 'privacy'), { ...terms }, { merge: true });
    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiGetPrivacy(): Promise<PrivacyModel | null> {
  try {
    const smtp = await getDoc(doc(firestoreClient, 'appControlsPublic', 'privacy'));
    return PrivacyModel.fromJson({ ...smtp.data(), id: smtp.id });
  } catch (error) {
    return null;
  }
}
