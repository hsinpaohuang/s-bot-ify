import type { Writable } from "svelte/store";

export type SpotifyPaginatedResponse = {
  hasMore: boolean;
  offset: number;
}

export type SpotifyPaginatedState = {
  hasMore: boolean;
}

export abstract class SpotifyPaginatedStore<T extends SpotifyPaginatedState> {
  protected abstract store: Writable<T>;
  protected abstract offset: number;

  protected abstract get length(): number;
  protected abstract get hasMore(): boolean;

  abstract fetchNext(): Promise<void>;
}
