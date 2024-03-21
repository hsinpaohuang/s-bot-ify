import { get, readonly, writable } from "svelte/store";
import { PUBLIC_API_URL } from "$env/static/public";

class AuthStore {
  set;
  store;
  private _store;

  constructor() {
    this._store = writable({ accessToken: '', tokenType: '' });
    this.store = readonly(this._store);
    this.set = this._store.set;
  }

  get accessToken() {
    return get(this._store).accessToken;
  }

  get tokenType() {
    return get(this._store).tokenType;
  }

  async getAuthURL() {
   const url = await fetch(`${PUBLIC_API_URL}/auth/spotify/authorize`);
    const { authorization_url: authURL }: { authorization_url: string }
      = await url.json();

    return authURL;
  }

  async getToken() {
    const registerResponse = await fetch(
      window.location.href.replace(window.location.origin, PUBLIC_API_URL),
    )

    const registerData = await registerResponse.json();

    if (!registerResponse.ok) {
      const { detail }: { detail: string } = registerData;
      throw new Error(`Failed to fetch token`, { cause: detail });
    }

    const {
      access_token: accessToken,
      token_type: tokenType
    }: {
      access_token: string;
      token_type: string
    } = registerData;

    this.set({ accessToken, tokenType });
  }
}

export const authStore = new AuthStore();
