import { derived, get, writable } from "svelte/store";
import { browser } from '$app/environment';
import { PUBLIC_API_URL } from "$env/static/public";
import { camelizedFetch } from "$lib/utils/fetchWrappers";

type State = {
  accessToken?: string;
  tokenType?: string;
};

class AuthStore {
  isLoggedInStore;

  private store;
  private SESSION_STORAGE_KEY = 'auth';

  constructor() {
    this.store = writable(this.storedState);
    this.isLoggedInStore = derived(this.store, store =>
      Boolean(store.accessToken),
    );
  }

  get accessToken() {
    return get(this.store).accessToken;
  }

  get tokenType() {
    return get(this.store).tokenType;
  }

  get isLoggedIn() {
    return get(this.isLoggedInStore);
  }

  private get storedState(): State {
    if (!browser) {
      return {};
    }

    const stored = sessionStorage.getItem(this.SESSION_STORAGE_KEY);
    return stored ? JSON.parse(stored) : {};
  }

  async getAuthURL() {
    const { ok, data } = await camelizedFetch<{ authorizationUrl: string }>(
      `${PUBLIC_API_URL}/auth/spotify/authorize`,
    );

    if (!ok || !data?.authorizationUrl) {
      throw new Error(`Failed to fetch authURL`);
    }

    return data.authorizationUrl;
  }

  async getToken() {
    const { ok, data } = await camelizedFetch<State, { detail: string }>(
      window.location.href.replace(window.location.origin, PUBLIC_API_URL),
    )

    if (!ok) {
      throw new Error(`Failed to fetch token`, { cause: data?.detail });
    }

    if (!data) {
      throw new Error('Invalid API response');
    }

    sessionStorage.setItem(this.SESSION_STORAGE_KEY, JSON.stringify(data));
    this.store.set(data);
  }
}

export const authStore = new AuthStore();
