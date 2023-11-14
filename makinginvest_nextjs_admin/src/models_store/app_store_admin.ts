import create from 'zustand';

type State = {
  subscriptions: any;
  openDrawer: boolean;

  toggleDrawer: () => void;
};

export const useAppStore = create<State>((set) => ({
  subscriptions: {},
  openDrawer: false,

  toggleDrawer: () => set((state) => ({ openDrawer: !state.openDrawer }))
}));
