type I_APP_MODE = 'DEV' | 'PROD';

export const APP_MODE: I_APP_MODE = 'PROD';

export const APP_NAME = 'MakingInvest';

export const firebaseConfigClient = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
  measurementId: process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID
};

export const STRIPE_MONTHLY_PRODUCT_TEST = process.env.NEXT_PUBLIC_STRIPE_MONTHLY_PRODUCT_TEST as string;
export const STRIPE_YEARLY_PRODUCT_TEST = process.env.NEXT_PUBLIC_STRIPE_YEARLY_PRODUCT_TEST as string;

export const STRIPE_MONTHLY_PRODUCT_LIVE = process.env.NEXT_PUBLIC_STRIPE_MONTHLY_PRODUCT_LIVE as string;
export const STRIPE_YEARLY_PRODUCT_LIVE = process.env.NEXT_PUBLIC_STRIPE_YEARLY_PRODUCT_LIVE as string;

export const USE_LIVE_STRIPE_API = false;
