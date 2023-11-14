import axios from 'axios';
import { addDoc, collection, deleteDoc, doc, getDoc, getDocs, query, serverTimestamp, setDoc, updateDoc, where } from 'firebase/firestore';
import { SignalModel } from '../models/model.signal';
import { authClient, firestoreClient } from '../_firebase/firebase_client';
import { apiGetUser } from './firestore_user_service';

/* ------------------------------- NOTE SIGNALS ------------------------------ */

interface ISignalForm {
  id?: string;
  signal?: SignalModel;
  sendNotification?: boolean;
  dbPath: string;
  isClosed?: boolean;
}
export async function apiCreateSignal({ signal, sendNotification, dbPath = 'signalsCrypto' }: ISignalForm): Promise<boolean> {
  if (!signal) throw new Error('No signal provided!');
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to create signals.');

    const jsonWebToken = await authClient.currentUser?.getIdToken(true);

    await addDoc(collection(firestoreClient, dbPath), {
      ...SignalModel.toJson(signal),
      timestampCreated: serverTimestamp(),
      timestampUpdated: serverTimestamp(),
      timestampLastAutoCheck: serverTimestamp()
    });

    await apiAggregateSignals({ dbPath });

    if (sendNotification) await axios.post(`/api/notifications`, { title: 'Signal', body: `New ${signal.symbol} signal added`, jsonWebToken });
    return true;
  } catch (error: any) {
    console.log(error);
    throw new Error(error.message);
  }
}

export async function apiUpdateSignal({
  id,
  signal,
  sendNotification,
  dbPath = 'signalsCrypto',
  isClosed = false
}: ISignalForm): Promise<boolean> {
  if (!id) throw new Error('No id provided!');
  if (!signal) throw new Error('No signal provided!');

  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to create signals.');

    const jsonWebToken = await authClient.currentUser?.getIdToken(true);

    const signal_json = SignalModel.toJson(signal);
    delete signal_json.timestampLastAutoCheck;

    if (!isClosed) {
      await updateDoc(doc(firestoreClient, dbPath, id), { ...SignalModel.toJson(signal_json), timestampUpdated: serverTimestamp() });
      if (sendNotification)
        await axios.post(`/api/notifications`, { title: 'Signal', body: `${signal.symbol} Signal updated added`, jsonWebToken });
    }

    if (isClosed) {
      await updateDoc(doc(firestoreClient, dbPath, id), {
        ...SignalModel.toJson(signal_json),
        isClosedManual: true,
        isClosedAuto: false,
        isClosed: true,
        timestampClosed: serverTimestamp()
      });
      if (sendNotification)
        await axios.post(`/api/notifications`, { title: 'Signal', body: `${signal.symbol} Signal closed closed`, jsonWebToken });
    }

    await apiAggregateSignals({ dbPath });

    return true;
  } catch (error: any) {
    console.log(error);
    throw new Error(error.message);
  }
}

export async function apiUpdateSignalCloseManually({ id, sendNotification, dbPath = 'signalsCrypto', signal }: ISignalForm): Promise<boolean> {
  if (!id) throw new Error('No id provided!');
  if (!signal) throw new Error('No signal provided!');

  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to create signals.');

    const jsonWebToken = await authClient.currentUser?.getIdToken(true);

    await updateDoc(doc(firestoreClient, dbPath, id), {
      ...SignalModel.toJson(signal),
      isClosedManual: true,
      isClosedAuto: false,
      isClosed: true,
      timestampClosed: serverTimestamp()
    });

    if (sendNotification) await axios.post(`/api/notifications`, { title: 'Signal', body: 'Signal closed added', jsonWebToken });
    return true;
  } catch (error: any) {
    console.log(error);
    throw new Error(error.message);
  }
}

export async function apiGetSignal({ id, dbPath }: ISignalForm): Promise<SignalModel | null> {
  if (!id) throw new Error('No id provided!');
  try {
    const x = await getDoc(doc(firestoreClient, dbPath, id));
    if (!x.data()) return null;
    return SignalModel.fromJson({ ...x.data(), id: x.id });
  } catch (error) {
    console.log(error);
    return null;
  }
}

export async function apiGetSignalsOpen({ dbPath }: { dbPath: string }): Promise<SignalModel[]> {
  try {
    const x = await getDocs(query(collection(firestoreClient, dbPath), where('isClosed', '==', false)));
    return x.docs.map((doc) => SignalModel.fromJson({ ...doc.data(), id: doc.id }));
  } catch (error) {
    console.log(error);
    return [];
  }
}

export async function apiDeleteSignal({ id, dbPath }: ISignalForm): Promise<boolean> {
  if (!id) throw new Error('No id provided!');
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to delete signals.');

    await deleteDoc(doc(firestoreClient, dbPath, id));
    await apiAggregateSignals({ dbPath });

    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiAggregateSignals({ dbPath }: { dbPath: string }): Promise<boolean> {
  try {
    const signals = await apiGetSignalsOpen({ dbPath });
    const data = signals.map((signal) => {
      return SignalModel.toJson(signal);
    });

    let docPath = 'crypto';
    if (dbPath === 'signalsForex') docPath = 'forex';
    if (dbPath === 'signalsStocks') docPath = 'stocks';

    const hasData = data.length > 0;

    await setDoc(doc(firestoreClient, 'signalsAggrOpen', docPath), { data, hasData, timestampUpdated: serverTimestamp() }, { merge: true });

    return true;
  } catch (error: any) {
    console.log(error);
    throw new Error(error.message);
  }
}
