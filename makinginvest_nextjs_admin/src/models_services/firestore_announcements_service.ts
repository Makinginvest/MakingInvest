import axios from 'axios';
import { addDoc, collection, deleteDoc, doc, getDoc, getDocs, limit, query, serverTimestamp, setDoc, updateDoc, orderBy } from 'firebase/firestore';
import { authClient, firestoreClient } from '../_firebase/firebase_client';
import { AnnouncementModel } from '../models/model.announcement';
import { apiGetUser } from './firestore_user_service';

/* ------------------------------ NOTE Announcement ----------------------------- */
export async function apiCreateAnnouncement(x: AnnouncementModel) {
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to create announcements.');

    const jsonWebToken = await authClient.currentUser?.getIdToken(true);
    await addDoc(collection(firestoreClient, 'announcements'), { ...AnnouncementModel.toJson(x), timestampCreated: serverTimestamp() });
    await apiAggregateAnnouncements();
    await axios.post(`/api/notifications`, { title: x.title, body: x.body, jsonWebToken });
    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiUpdateAnnouncement(id: string, announcement: AnnouncementModel) {
  const _announcement = { ...AnnouncementModel.toJson(announcement), timestampUpdated: serverTimestamp() };
  delete _announcement.timestampCreated;

  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to update announcements.');

    await updateDoc(doc(firestoreClient, 'announcements', id), { ..._announcement });
    await apiAggregateAnnouncements();

    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiGetAnnouncement(id: string) {
  try {
    const announcement = await getDoc(doc(firestoreClient, 'announcements', id));
    if (!announcement.data()) return null;
    return AnnouncementModel.fromJson({ ...announcement.data(), id: announcement.id });
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiGetAnnouncements(amt: number = 50) {
  try {
    const announcements = await getDocs(query(collection(firestoreClient, 'announcements'), orderBy('timestampCreated', 'desc'), limit(amt)));
    return announcements.docs.map((videoLesson) => {
      return AnnouncementModel.fromJson({ ...videoLesson.data(), id: videoLesson.id });
    });
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiDeleteAnnouncement(id: string) {
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to create announcements.');

    await deleteDoc(doc(firestoreClient, 'announcements', id));
    await apiAggregateAnnouncements();
    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiAggregateAnnouncements(): Promise<boolean> {
  try {
    const signals = await apiGetAnnouncements(50);

    const data = signals.map((signal) => {
      return AnnouncementModel.toJson(signal);
    });

    console.log(data);

    await setDoc(doc(firestoreClient, 'announcementsAggr', 'announcementsAggr'), { data, timestampUpdated: serverTimestamp() });

    return true;
  } catch (error: any) {
    console.log(error);
    throw new Error(error.message);
  }
}
