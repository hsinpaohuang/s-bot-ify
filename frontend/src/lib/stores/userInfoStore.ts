import { authedFetch } from "$lib/utils/fetchWrappers";
import { writable } from "svelte/store";

export type UserInfo = {
  avatar?: string;
  displayName: string;
}

class UserInfoStore {
  subscribe;

  private store;

  constructor() {
    this.store = writable<UserInfo>({ displayName: '' });
    this.subscribe = this.store.subscribe;
  }

  async load() {
    const res = await authedFetch<UserInfo>('/users/me');

    if (!res?.ok || !res.data) {
      throw new Error('Failed to fetch user info', { cause: res?.data });
    }

    this.store.set(res.data);
  }
}

export const userInfoStore = new UserInfoStore();
