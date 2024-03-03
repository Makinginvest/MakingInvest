import { doc, getDoc, setDoc } from 'firebase/firestore';
import { StripeModel } from '../models/model.stripe';
import { authClient, firestoreClient } from '../_firebase/firebase_client';
import { apiGetUser } from './firestore_user_service';

export async function apiUpdateStripe(x: StripeModel): Promise<boolean | null> {
  let smtp = { ...StripeModel.toJson(x) };
  delete smtp.id;

  const fbUser = authClient.currentUser;
  const user = await apiGetUser(fbUser!.uid);

  if (!user) throw new Error('No user found!');
  if (!user.isSuperAdmin) throw new Error('You are not authorized to update Stripe settings.');

  try {
    await setDoc(doc(firestoreClient, 'appControlsPrivate', 'stripe'), { ...smtp }, { merge: true });
    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiGetStripe(): Promise<StripeModel | null> {
  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);

    if (!user) return null;

    if (!user.isSuperAdmin)
      return StripeModel.fromJson({
        id: '',
        stripeTestKey: 'XXXXXXXXXXXXXXXXXXXXXXX',
        stripeLiveKey: 'XXXXXXXXXXXXXXXXXXXXXXX',
        stripeMonthlyProductTest: 'XXXXXXXXXXXXXXXXXXXXXXX',
        stripeYearlyProductTest: 'XXXXXXXXXXXXXXXXXXXXXXX',
        stripeMonthlyProductLive: 'XXXXXXXXXXXXXXXXXXXXXXX',
        stripeYearlyProductLive: 'XXXXXXXXXXXXXXXXXXXXXXX',
        isStripeKeyLive: false
      });

    const smtp = await getDoc(doc(firestoreClient, 'appControlsPrivate', 'stripe'));
    return StripeModel.fromJson({ ...smtp.data(), id: smtp.id });
  } catch (error) {
    return null;
  }
}
