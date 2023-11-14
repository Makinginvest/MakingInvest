import { limit, query, serverTimestamp, setDoc, updateDoc, where } from 'firebase/firestore';
import { addDoc, collection, deleteDoc, doc, getDoc, getDocs } from 'firebase/firestore';
import { PostModel } from '../models/model.post';
import { authClient, firestoreClient } from '../_firebase/firebase_client';
import { apiGetUser } from './firestore_user_service';

export async function apiCreatePost(x: PostModel): Promise<boolean> {
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to update links settings.');

    const qName = query(collection(firestoreClient, 'posts'), where('name', '==', x.title));
    const qSlug = query(collection(firestoreClient, 'posts'), where('slug', '==', x.slug));

    const qNameSnapshot = await getDocs(qName);
    const qSlugSnapshot = await getDocs(qSlug);

    if (qNameSnapshot.size > 0 || qSlugSnapshot.size > 0) {
      throw new Error('Post name or slug already exists');
    }

    await addDoc(collection(firestoreClient, 'posts'), {
      ...PostModel.toJson(x),
      timestampCreated: serverTimestamp(),
      timestampUpdated: serverTimestamp()
    });

    await apiAggregatePosts();

    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiUpdatePost(id: string, x: PostModel): Promise<boolean> {
  let post = { ...PostModel.toJson(x), timestampUpdated: serverTimestamp() };
  delete post.timestampCreated;
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to update links settings.');

    await updateDoc(doc(firestoreClient, 'posts', id), { ...post });
    await apiAggregatePosts();

    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiGetPost(id: string): Promise<PostModel | null> {
  try {
    const post = await getDoc(doc(firestoreClient, 'posts', id));
    if (!post.data()) return null;
    return PostModel.fromJson({
      ...post.data(),
      id: post.id
    });
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiGetPosts() {
  try {
    const posts = await getDocs(query(collection(firestoreClient, 'posts'), where('status', '==', 'Published'), limit(50)));
    return posts.docs.map((videoLesson) => {
      return PostModel.fromJson({ ...videoLesson.data(), id: videoLesson.id });
    });
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiDeletePost(id: string): Promise<boolean> {
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to update links settings.');

    await deleteDoc(doc(firestoreClient, 'posts', id));
    await apiAggregatePosts();

    return true;
  } catch (error: any) {
    console.log(error);
    throw new Error(error.message);
  }
}

export async function apiAggregatePosts(): Promise<boolean> {
  try {
    const signals = await apiGetPosts();

    const data = signals.map((signal) => {
      return PostModel.toJson(signal);
    });

    await setDoc(doc(firestoreClient, 'postsAggr', 'postsAggr'), { data, timestampUpdated: serverTimestamp() });

    return true;
  } catch (error: any) {
    console.log(error);
    throw new Error(error.message);
  }
}
