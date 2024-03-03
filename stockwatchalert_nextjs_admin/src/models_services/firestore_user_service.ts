import { doc, getDoc, serverTimestamp, updateDoc } from 'firebase/firestore';
import { AuthUserModel } from '../models/model.authuser';
import { authClient, firestoreClient } from '../_firebase/firebase_client';

export async function apiUpdateUser(id: string, x: AuthUserModel): Promise<boolean> {
  let authUser = {
    isAdmin: x.isAdmin,
    isSuperAdmin: x.isSuperAdmin,
    subIsLifetime: x.subIsLifetime,
    subIsLifetimeExpirationDateTime: x.subIsLifetimeExpirationDateTime,
    username: x.username,
    profileImage: x.profileImage,
    timestampUpdated: serverTimestamp()
  };

  try {
    const fbUser = authClient.currentUser;
    const user = await apiGetUser(fbUser!.uid);
    if (!user) throw new Error('No user found!');
    if (!user.isSuperAdmin && !user.isAdmin) throw new Error('You are not authorized to update users.');

    await updateDoc(doc(firestoreClient, 'users', id), { ...authUser });
    return true;
  } catch (error: any) {
    throw new Error(error.message);
  }
}

export async function apiGetUser(id: string): Promise<AuthUserModel | null> {
  try {
    const user = await getDoc(doc(firestoreClient, 'users', id));
    if (!user.data()) return null;
    return AuthUserModel.fromJson({
      ...user.data(),
      id: user.id,
      timestampCreated: user.data()!.timestampCreated?.toDate(),
      timestampUpdated: user.data()!.timestampUpdated?.toDate(),
      subIsLifetimeExpirationDateTime: user.data()!.subIsLifetimeExpirationDateTime?.toDate(),
      subRevenueCatBillingIssueDetectedAt: user.data()!.subRevenueCatBillingIssueDetectedAt?.toDate(),
      subRevenueCatOriginalPurchaseDate: user.data()!.subRevenueCatOriginalPurchaseDate?.toDate(),
      subRevenueCatLatestPurchaseDate: user.data()!.subRevenueCatLatestPurchaseDate?.toDate(),
      subRevenueCatExpirationDate: user.data()!.subRevenueCatExpirationDate?.toDate(),
      subRevenueCatUnsubscribeDetectedAt: user.data()!.subRevenueCatUnsubscribeDetectedAt?.toDate(),
      subStripeStart: user.data()!.subStripeStart?.toDate(),
      subStripeEnd: user.data()!.subStripeEnd?.toDate(),
      subSubscriptionEndDate: user.data()!.subSubscriptionEndDate?.toDate()
    });
  } catch (error) {
    return null;
  }
}
