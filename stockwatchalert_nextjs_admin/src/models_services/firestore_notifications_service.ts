import axios from 'axios';
import { addDoc, collection, deleteDoc, doc, serverTimestamp } from 'firebase/firestore';
import { NotificationModel } from '../models/model.notification';
import { authClient, firestoreClient } from '../_firebase/firebase_client';
import { apiGetUser } from './firestore_user_service';

/* ------------------------------ NOTE NOTIFICATION -------------------------- */
export async function apiCreateNotification(notification: NotificationModel) {
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to create announcements.');

    const jsonWebToken = await authClient.currentUser?.getIdToken(true);

    await addDoc(collection(firestoreClient, 'notifications'), {
      ...NotificationModel.toJson(notification),
      timestampCreated: serverTimestamp()
    });
    await axios.post(`/api/notifications`, { title: notification.title, body: notification.body, jsonWebToken });
    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiDeleteNotification(id: string) {
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to create notifications.');

    await deleteDoc(doc(firestoreClient, 'notifications', id));
    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}
