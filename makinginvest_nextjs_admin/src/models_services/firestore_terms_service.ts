import { doc, getDoc, setDoc } from 'firebase/firestore';
import { APP_MODE } from '../constants/app_constants';
import { TermsModel } from '../models/model.terms';
import { authClient, firestoreClient } from '../_firebase/firebase_client';
import { apiGetUser } from './firestore_user_service';

export async function apiUpdateTerms(x: TermsModel): Promise<boolean> {
  let terms = { ...TermsModel.toJson(x) };
  delete terms.id;

  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to update terms settings.');

    await setDoc(doc(firestoreClient, 'appControlsPublic', 'terms'), { ...terms }, { merge: true });
    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiGetTerms(): Promise<TermsModel | null> {
  try {
    const smtp = await getDoc(doc(firestoreClient, 'appControlsPublic', 'terms'));
    return TermsModel.fromJson({ ...smtp.data(), id: smtp.id });
  } catch (error) {
    return null;
  }
}
