import { get, writable } from "svelte/store";
import { authedFetch } from "$lib/utils/fetchWrappers";
import {
  PaginatedStore,
  type PaginatedResponse,
} from "$lib/utils/paginatedStore";

export type Playlist = {
  id: string;
  name: string;
  icon: string | null;
}

type GetPlaylistResponse = PaginatedResponse & { playlists: Playlist[]; };

class PlaylistsStore extends PaginatedStore {
  subscribe;
  hasMore = true;

  protected store;
  protected offset = 0;

  constructor() {
    super();

    this.store = writable<Playlist[]>([]);
    this.subscribe = this.store.subscribe;
  }

  protected get length() {
    return get(this.store).length;
  }

  async fetchNext() {
    if (!this.hasMore) {
      return;
    }

    const params = new URLSearchParams();
    if (this.length) {
      params.append('offset', String(this.offset));
    }

    const res = await authedFetch<GetPlaylistResponse>(`/playlists?${params}`);
    if (!res || !res.ok || !res.data) {
      throw new Error('Failed to fetch playlists');
    }

    const { hasMore, offset, playlists } = res.data;

    this.hasMore = hasMore;
    this.offset = offset + playlists.length;
    this.store.update(state => state.concat(playlists));
  }
}

export const playlistsStore = new PlaylistsStore();

export const placeholders = [0, 1, 2, 3, 4];
