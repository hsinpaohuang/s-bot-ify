import { sleep } from "$lib/utils/sleep";
import { writable } from "svelte/store";

export type Playlist = {
  id: string;
  title: string;
  icon: string;
}

export const fakePlaylists: Playlist[] = [
  {
    id: '1',
    icon: '(icon)',
    title: 'Tile 1',
  },
  {
    id: '2',
    icon: '(icon)',
    title: 'Tile 2',
  },
  {
    id: '3',
    icon: '(icon)',
    title: 'Tile 3',
  },
  {
    id: '4',
    icon: '(icon)',
    title: 'Tile 4',
  },
  {
    id: '5',
    icon: '(icon)',
    title: 'Tile 5',
  },
];

class PlaylistsStore {
  private set;

  subscribe;

  constructor() {
    const { subscribe, set } = writable<Playlist[]>([]);
    this.subscribe = subscribe;
    this.set = set;
  }

  async fetchPlaylists() {
    await sleep(1000);

    // TODO: replace with real playlists
    this.set(fakePlaylists);
  }
}

export const playlistsStore = new PlaylistsStore();

export const placeholders = [0, 1, 2, 3, 4];
