import { get, writable } from "svelte/store";
import { authedFetch } from "$lib/utils/fetchWrappers";
import {
  SpotifyPaginatedStore,
  type SpotifyPaginatedResponse,
  type SpotifyPaginatedState,
} from "$lib/utils/paginatedStore";

export type Playlist = {
  id: string;
  name: string;
  icon: string | null;
}

type GetPlaylistResponse = SpotifyPaginatedResponse & { playlists: Playlist[]; };

type State = SpotifyPaginatedState & {
  playlists: Playlist[];
}
class PlaylistsStore extends SpotifyPaginatedStore<State> {
  subscribe;

  protected offset = 0;
  protected store;

  constructor() {
    super();

    this.store = writable<State>({ hasMore: true, playlists: [] });
    this.subscribe = this.store.subscribe;
  }

  protected get length() {
    return get(this.store).playlists.length;
  }

  protected get hasMore() {
    return get(this.store).hasMore;
  }

  async fetchNext() {
    if (!this.hasMore) {
      return;
    }

    const params = new URLSearchParams();
    if (this.length) {
      params.append('offset', String(this.offset));
    }

    try {
      const res = await authedFetch<GetPlaylistResponse>(`/playlists?${params}`);
      if (!res || !res.ok || !res.data) {
        throw new Error('Failed to fetch playlists');
      }

      const { hasMore, offset, playlists } = res.data;

      this.offset = offset + playlists.length;
      this.store.update(({ playlists: statePlaylist }) => ({
        playlists: statePlaylist.concat(playlists),
        hasMore,
      }));
    } catch (e) {
      this.store.update(state => {
        state.hasMore = false;
        return state;
      });

      throw e;
    }

  }
}

export const playlistsStore = new PlaylistsStore();

export const placeholders = [0, 1, 2, 3, 4];
