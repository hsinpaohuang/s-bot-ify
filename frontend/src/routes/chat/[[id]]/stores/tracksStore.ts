import { get, writable } from "svelte/store";
import {
  SpotifyPaginatedStore,
  type SpotifyPaginatedResponse,
  type SpotifyPaginatedState,
} from "$lib/utils/paginatedStore";
import { authedFetch } from "$lib/utils/fetchWrappers";

export type Track = {
  id: string;
  name: string;
  artists: string;
  icon: string;
}

type GetTracksReponse = SpotifyPaginatedResponse & { tracks: Track[]; };

type State = SpotifyPaginatedState & { tracks: Track[] };

const defaultState = { tracks: [], hasMore: true };

class TracksStore extends SpotifyPaginatedStore<State> {
  subscribe;

  protected store;
  protected offset = 0;

  private _id: string;

  constructor() {
    super();

    this.store = writable<State>(defaultState);
    this.subscribe = this.store.subscribe;
    this._id = '';
  }

  protected get length() {
    return get(this.store).tracks.length;
  }

  protected get hasMore() {
    return get(this.store).hasMore;
  }

  set id(newID: string) {
    this._id = newID;
    this.resetState();
  }

  async fetchNext() {
    if (!this.hasMore) {
      return;
    }

    const params = new URLSearchParams();
    if (this.length) {
      params.append('offset', String(this.offset));
    }

    const res = await authedFetch<GetTracksReponse>(
      `/playlists/${this._id}/tracks?${params}`,
    );
    if (!res || !res.ok || !res.data) {
      throw new Error('Failed to fetch playlists');
    }

    const { hasMore, offset, tracks } = res.data;

    this.offset = offset + tracks.length;
    this.store.update(({ tracks: stateTracks }) => ({
      tracks: stateTracks.concat(tracks),
      hasMore,
    }));
  }

  private resetState() {
    this.offset = 0;
    this.store.set(defaultState);
  }
}

export const tracksStore = new TracksStore();

export const placeholders = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
