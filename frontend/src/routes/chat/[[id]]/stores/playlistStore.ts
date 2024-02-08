import { sleep } from "$lib/utils/sleep";
import { writable } from "svelte/store";

export type Song = {
  id: string;
  title: string;
  authors: string;
  icon: string;
}

type State = {
  id?: string;
  songs: Song[];
}

const fakeSongs: Song[] = [
  {
    id: '1',
    title: 'Song fhdjksahfd hsajkfhdsjkalhfjkd sahfjk hsajkfl',
    icon: '(icon)',
    authors: 'fjdsklajfdklfdhsa hfjdksahfjdhs h  hfjdslah jhs kahjkfdlas h'
  },
  {
    id: '2',
    title: 'Song 2',
    icon: '(icon)',
    authors: 'Author1'
  },
  {
    id: '3',
    title: 'Song 3',
    icon: '(icon)',
    authors: 'Author1'
  },
  {
    id: '4',
    title: 'Song 4',
    icon: '(icon)',
    authors: 'Author1'
  },
  {
    id: '5',
    title: 'Song 5',
    icon: '(icon)',
    authors: 'Author1'
  },
  {
    id: '6',
    title: 'Song 6',
    icon: '(icon)',
    authors: 'Author1'
  },
  {
    id: '6',
    title: 'Song 6',
    icon: '(icon)',
    authors: 'Author1'
  },
  {
    id: '6',
    title: 'Song 6',
    icon: '(icon)',
    authors: 'Author1'
  },
  {
    id: '6',
    title: 'Song 6',
    icon: '(icon)',
    authors: 'Author1'
  },
  {
    id: '6',
    title: 'Song 6',
    icon: '(icon)',
    authors: 'Author1'
  },
  {
    id: '6',
    title: 'Song 6',
    icon: '(icon)',
    authors: 'Author1'
  },
  {
    id: '6',
    title: 'Song 6',
    icon: '(icon)',
    authors: 'Author1'
  },
  {
    id: '6',
    title: 'Song 6',
    icon: '(icon)',
    authors: 'Author1'
  },
  {
    id: '6',
    title: 'Song 6',
    icon: '(icon)',
    authors: 'Author1'
  },
  {
    id: '6',
    title: 'Song 6',
    icon: '(icon)',
    authors: 'Author1'
  },
];

class PlaylistStore {
  private set;

  subscribe;

  constructor() {
    const { subscribe, set } = writable<State>({ songs: [] });
    this.subscribe = subscribe;
    this.set = set;
  }

  async fetchPlaylist(newID: string) {
    await sleep(1000);

    // TODO: replace with real songs
    this.set({ id: newID, songs: fakeSongs });
  }
}

export const playlistStore = new PlaylistStore();

export const placeholders = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
