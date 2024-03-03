import { addDoc, collection, deleteDoc, doc, getDoc, getDocs } from 'firebase/firestore';
import { limit, query, serverTimestamp, setDoc, updateDoc, where } from 'firebase/firestore';
import { VideoLessonModel } from '../models/model.video_lesson';
import { authClient, firestoreClient } from '../_firebase/firebase_client';
import { apiGetUser } from './firestore_user_service';

export async function apiCreateVideoLesson(x: VideoLessonModel): Promise<boolean> {
  let videoLession = { ...VideoLessonModel.toJson(x) };
  delete videoLession.id;

  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to update videos.');

    await addDoc(collection(firestoreClient, 'videoLessons'), { ...videoLession });
    await apiAggregateVideoLessons();

    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiUpdateVideoLesson(id: string, x: VideoLessonModel): Promise<boolean> {
  let videoLesson = { ...VideoLessonModel.toJson(x), timestampUpdated: serverTimestamp() };
  delete videoLesson.timestampCreated;
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to update videos.');

    await updateDoc(doc(firestoreClient, 'videoLessons', id), { ...videoLesson });
    await apiAggregateVideoLessons();

    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiGetVideoLesson(id: string): Promise<VideoLessonModel | null> {
  try {
    const videoLession = await getDoc(doc(firestoreClient, 'videoLessons', id));
    if (!videoLession.data()) return null;
    return VideoLessonModel.fromJson({
      ...videoLession.data(),
      id: videoLession.id
    });
  } catch (error) {
    return null;
  }
}

export async function apiGetVideoLessons(): Promise<VideoLessonModel[]> {
  try {
    const videoLessons = await getDocs(query(collection(firestoreClient, 'videoLessons'), where('status', '==', 'Published'), limit(50)));
    return videoLessons.docs.map((videoLesson) => {
      return VideoLessonModel.fromJson({ ...videoLesson.data(), id: videoLesson.id });
    });
  } catch (error) {
    return [];
  }
}

export async function apiDeleteVideoLesson(id: string): Promise<boolean> {
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to update videos.');

    await deleteDoc(doc(firestoreClient, 'videoLessons', id));
    await apiAggregateVideoLessons();

    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiAggregateVideoLessons(): Promise<boolean> {
  try {
    const signals = await apiGetVideoLessons();

    const data = signals.map((signal) => {
      return VideoLessonModel.toJson(signal);
    });

    await setDoc(doc(firestoreClient, 'videoLessonsAggr', 'videoLessonsAggr'), { data, timestampUpdated: serverTimestamp() });

    return true;
  } catch (error: any) {
    console.log(error);
    throw new Error(error.message);
  }
}
