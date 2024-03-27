import type { Writable } from "svelte/store";

export type PaginatedResponse = {
  hasMore: boolean;
  offset: number;
}

export abstract class PaginatedStore {
  abstract hasMore: boolean;

  protected abstract store: Writable<unknown>;
  protected abstract offset: number;

  protected abstract get length(): number;

  abstract fetchNext(): Promise<void>;
}
