import axios from 'axios';
import { get, getDatabase, push, ref, remove, set, update } from 'firebase/database';
import { SignalModel } from '../models/model.signal';
import { convertToDate } from '../utils/convert_to_date';
import { authClient } from '../_firebase/firebase_client';
import { apiGetUser } from './firestore_user_service';

/* ------------------------------- NOTE SIGNALS ------------------------------ */
export async function apiCreateSignalRealtimeDB(x: SignalModel, sendNotification: boolean) {
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to create signals.');

    const jsonWebToken = await authClient.currentUser?.getIdToken(true);

    const db = getDatabase();
    const newSignalRef = push(ref(db, 'signalsOpen'));
    await set(newSignalRef, { ...SignalModel.toJsonRealtimeDB(x) });
    if (sendNotification) await axios.post(`/api/notifications`, { title: 'Signal', body: 'New signal added', jsonWebToken });
    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiUpdateSignalRealtimeDB(id: string, x: SignalModel, sendNotification: boolean) {
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to create signals.');

    const jsonWebToken = await authClient.currentUser?.getIdToken(true);

    const db = getDatabase();
    await update(ref(db, `signalsOpen/${id}`), { ...SignalModel.toJsonRealtimeDB(x) });
    if (sendNotification) await axios.post(`/api/notifications`, { title: 'Signal', body: 'Signal updated added', jsonWebToken });
    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiDeleteSignalRealtimeDB(id: string, sendNotification?: boolean) {
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to create signals.');

    const db = getDatabase();
    await remove(ref(db, `signalsOpen/${id}`));

    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiGetSignalRealtimeDB(id: string): Promise<SignalModel | null> {
  try {
    const db = getDatabase();
    const s = await get(ref(db, `signalsOpen/${id}`));
    if (s.exists()) {
      const childKey = s.key;
      const childData = s.val();

      const signal = SignalModel.fromJson({
        ...childData,
        id: childKey,
        timestampCreated: convertToDate(childData.timestampCreated),
        timestampUpdated: convertToDate(childData.timestampUpdated),
        entryDate: convertToDate(childData.entryDate),
        entryTime: convertToDate(childData.entryTime),
        entryDateTime: convertToDate(childData.entryDateTime),
        stopLossDate: convertToDate(childData.stopLossDate),
        stopLossTime: convertToDate(childData.stopLossTime),
        stopLossDateTime: convertToDate(childData.stopLossDateTime),
        takeProfit1Date: convertToDate(childData.takeProfit1Date),
        takeProfit1Time: convertToDate(childData.takeProfit1Time),
        takeProfit1DateTime: convertToDate(childData.takeProfit1DateTime),
        takeProfit2Date: convertToDate(childData.takeProfit2Date),
        takeProfit2Time: convertToDate(childData.takeProfit2Time),
        takeProfit2DateTime: convertToDate(childData.takeProfit2DateTime),
        takeProfit3Date: convertToDate(childData.takeProfit3Date),
        takeProfit3Time: convertToDate(childData.takeProfit3Time),
        takeProfit3DateTime: convertToDate(childData.takeProfit3DateTime)
      });
      return signal;
    }

    return null;
  } catch (error: any) {
    throw new Error(error.message);
  }
}
