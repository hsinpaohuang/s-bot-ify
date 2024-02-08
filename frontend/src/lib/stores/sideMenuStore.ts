import { writable } from "svelte/store";

function createSideMenuStore() {
  const { subscribe, update } = writable({
    hasSideMenu: false,
    isOpen: false,
  });

  return {
    subscribe,
    toggleOpen() {
      update(state => ({ ...state, isOpen: !state.isOpen }));
    },
    setIsOpen(isOpen: boolean) {
      update(state => ({ ...state, isOpen }));
    },
    setHasSideMenu(hasSideMenu: boolean) {
      update(state => ({ ...state, hasSideMenu, }));
    },
  };
}

export const sideMenuStore = createSideMenuStore();
