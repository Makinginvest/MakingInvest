import { doc, getDoc, setDoc } from 'firebase/firestore';
import { SMTPModel } from '../models/model.smtp';
import { authClient, firestoreClient } from '../_firebase/firebase_client';
import { apiGetUser } from './firestore_user_service';

export async function apiUpdateSMTP(x: SMTPModel): Promise<boolean | null> {
  let smtp = { ...SMTPModel.toJson(x) };
  delete smtp.id;

  const fbUser = authClient.currentUser;
  const user = await apiGetUser(fbUser!.uid);
  if (!user) throw new Error('No user found!');
  if (!user.isSuperAdmin) throw new Error('You are not authorized to update smtp settings.');

  try {
    await setDoc(doc(firestoreClient, 'appControlsPrivate', 'smtp'), { ...smtp }, { merge: true });
    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiGetSMTP(): Promise<SMTPModel | null> {
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);

    if (!user) return null;

    if (!user.isSuperAdmin)
      return SMTPModel.fromJson({
        id: '',
        password: 'XXXXXXXXXXXXXXXXXXXXXXX',
        host: 'XXXXXXXXXXXXXXXXXXXXXXX',
        port: 'XXXXXXXXXXXXXXXXXXXXXXX',
        email: 'XXXXXXXXXXXXXXXXXXXXXXX'
      });

    const smtp = await getDoc(doc(firestoreClient, 'appControlsPrivate', 'smtp'));
    return SMTPModel.fromJson({ ...smtp.data(), id: smtp.id });
  } catch (error) {
    return null;
  }
}
