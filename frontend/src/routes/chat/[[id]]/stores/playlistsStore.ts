import { authedFetch } from "$lib/utils/fetchWrappers";
import { get, writable } from "svelte/store";

export type Playlist = {
  id: string;
  name: string;
  icon: string | null;
}

type GetPlaylistResponse = {
  hasMore: boolean;
  offset: number;
  playlists: Playlist[];
}

class PlaylistsStore {
  subscribe;
  hasMore = true;

  private store;
  private offset = 0;

  constructor() {
    this.store = writable<Playlist[]>([]);
    this.subscribe = this.store.subscribe;
  }

  private get length() {
    return get(this.store).length;
  }

  async fetchNext() {
    if (!this.hasMore) {
      return;
    }

    const params = new URLSearchParams();
    if (this.length) {
      params.append('offset', String(this.offset + this.length));
    }

    const res = await authedFetch<GetPlaylistResponse>(`/playlists?${params}`);
    if (!res || !res.ok || !res.data) {
      throw new Error('Failed to fetch playlists');
    }

    const { hasMore, offset, playlists } = res.data;

    this.hasMore = hasMore;
    this.offset = offset;
    this.store.update(state => state.concat(playlists));
  }
}

export const playlistsStore = new PlaylistsStore();

export const placeholders = [0, 1, 2, 3, 4];
