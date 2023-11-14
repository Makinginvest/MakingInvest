import axios from 'axios';
import { addDoc, collection, deleteDoc, doc, getDoc, getDocs, limit, orderBy, query, serverTimestamp, setDoc, updateDoc } from 'firebase/firestore';
import { authClient, firestoreClient } from '../_firebase/firebase_client';
import { OfferingModel } from '../models/model.offering';
import { apiGetUser } from './firestore_user_service';

/* ------------------------------ NOTE Offering ----------------------------- */
export async function apiCreateOffering(x: OfferingModel) {
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to create offerings.');

    const jsonWebToken = await authClient.currentUser?.getIdToken(true);
    await addDoc(collection(firestoreClient, 'offerings'), { ...OfferingModel.toJson(x), timestampCreated: serverTimestamp() });
    await apiAggregateOfferings();
    await axios.post(`/api/notifications`, { title: x.title, body: x.body, jsonWebToken });
    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiUpdateOffering(id: string, offering: OfferingModel) {
  const _announcement = { ...OfferingModel.toJson(offering), timestampUpdated: serverTimestamp() };
  delete _announcement.timestampCreated;

  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to update offerings.');

    await updateDoc(doc(firestoreClient, 'offerings', id), { ..._announcement });
    await apiAggregateOfferings();

    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiGetOffering(id: string) {
  try {
    const offering = await getDoc(doc(firestoreClient, 'offerings', id));
    if (!offering.data()) return null;
    return OfferingModel.fromJson({ ...offering.data(), id: offering.id });
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiGetOfferings(amt: number = 50) {
  try {
    const offerings = await getDocs(query(collection(firestoreClient, 'offerings'), orderBy('timestampCreated', 'desc'), limit(amt)));
    return offerings.docs.map((videoLesson) => {
      return OfferingModel.fromJson({ ...videoLesson.data(), id: videoLesson.id });
    });
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiDeleteOffering(id: string) {
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to create offerings.');

    await deleteDoc(doc(firestoreClient, 'offerings', id));
    await apiAggregateOfferings();
    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiAggregateOfferings(): Promise<boolean> {
  try {
    const signals = await apiGetOfferings(50);

    const data = signals.map((signal) => {
      return OfferingModel.toJson(signal);
    });

    await setDoc(doc(firestoreClient, 'offeringsAggr', 'offeringsAggr'), { data, timestampUpdated: serverTimestamp() });

    return true;
  } catch (error: any) {
    console.log(error);
    throw new Error(error.message);
  }
}
