import { authedFetch } from "$lib/utils/fetchWrappers";
import { sleep } from "$lib/utils/sleep";
import { get, writable } from "svelte/store";

export type Message = {
  id?: string;
  bot: boolean;
  timestamp: number;
  content: string;
}

type State = {
  messages: Message[];
  isSending: boolean;
  hasMore: boolean;
  isFetching: boolean;
  lastAddedMsgPos: 'top' | 'bottom' | null;
}

// TODO: replace with real chat feed
// const timestamp = Intl.DateTimeFormat().format();
const timestamp = Date.now() / 1000;
const fakeChatFeed: Message[] = [
  {
    id: '1',
    bot: true,
    timestamp,
    content: 'Test Message 1',
  },
  {
    id: '2',
    bot: false,
    timestamp,
    content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec turpis metus, porta sagittis rhoncus id, pharetra quis arcu. Maecenas in nisi a tortor consequat efficitur sit amet eget dui. Quisque scelerisque condimentum euismod. Fusce tristique diam ut ligula euismod, at fringilla risus elementum. Nam ultricies convallis mollis. Etiam varius in metus vel hendrerit. Proin elementum lectus vitae sapien eleifend, id ullamcorper urna varius. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed consectetur tincidunt augue, sit amet ultrices ipsum suscipit et. Etiam vulputate condimentum dignissim. Nam vitae congue mauris.',
  },
  {
    id: '1',
    bot: true,
    timestamp,
    content: 'Fusce elementum aliquet magna nec luctus. Donec sed vehicula mi. Morbi nec justo aliquam, feugiat dolor ac, pulvinar sapien. Integer iaculis venenatis scelerisque. Nulla quis eleifend quam. Curabitur volutpat leo non erat elementum, eget sollicitudin tortor dignissim. Vivamus pharetra, felis sed rhoncus blandit, lorem dui volutpat dui, quis pharetra quam libero hendrerit magna. Aenean in mi vitae turpis tristique dictum. Praesent quam neque, consectetur lobortis lacus a, eleifend consequat erat. Sed tempor blandit augue sollicitudin pulvinar. Aenean ut elit dui. Suspendisse eros risus, pharetra a scelerisque id, congue non augue.',
  },
  {
    id: '2',
    bot: false,
    timestamp,
    content: 'Test Message 2',
  },
  {
    id: '3',
    bot: true,
    timestamp,
    content: 'Duis ultricies, dui euismod rhoncus placerat, erat nibh sodales leo, a eleifend arcu lectus vulputate tellus. Aenean tellus quam, finibus non justo non, rutrum posuere ipsum. Donec sollicitudin lectus id elit posuere, quis vulputate urna laoreet. Vivamus tempor, libero eget tincidunt laoreet, nisi lectus consectetur nibh, non fermentum risus felis ac urna. Praesent odio erat, tincidunt sed malesuada at, ultrices ullamcorper nisi. Integer auctor mi urna, quis viverra ipsum mattis nec. Pellentesque vitae rutrum nisl. Nam vulputate ligula vel quam venenatis, nec imperdiet odio sodales. Nunc nec diam vel magna facilisis mattis.',
  },
  {
    id: '4',
    bot: false,
    timestamp,
    content: 'Test Message 4',
  },
  {
    id: '5',
    bot: true,
    timestamp,
    content: 'Test Message 5',
  },
  {
    id: '6',
    bot: false,
    timestamp,
    content: 'Test Message 6',
  },
  {
    id: '7',
    bot: true,
    timestamp,
    content: 'Test Message 7',
  },
  {
    id: '8',
    bot: false,
    timestamp,
    content: 'Test Message 8',
  },
];

class ChatFeedStore {
  subscribe;
  FIXED_ARTIFICAL_DELAY = 1000;

  private store;
  private id = '';

  constructor() {
    this.store = writable<State>({
      messages: [],
      isSending: false,
      hasMore: true,
      isFetching: false,
      lastAddedMsgPos: null,
    });
    this.subscribe = this.store.subscribe;
  }

  get length() {
    return get(this.store).messages.length;
  }

  private get hasMore() {
    return get(this.store).hasMore;
  }

  private get lastChatID() {
    return get(this.store).messages[0]?.id;
  }

  private get randomArtificialDelay() {
    return this.FIXED_ARTIFICAL_DELAY + Math.random() * 1000;
  }

  async fetchNewChat(id: string) {
    if (id === this.id) {
      return;
    }

    this.id = id;

    this.store.update(state => {
      state.isFetching = true;
      return state;
    });

    try {
      const res = await authedFetch<Message[]>(`/playlists/${id}/chat`);
      if (!res || !res.ok || !res.data) {
        throw new Error('Failed to fetch Chat history');
      }

      this.store.update(({ isSending }) => ({
        messages: res.data,
        isSending,
        hasMore: res.data.length > 0,
        isFetching: false,
        lastAddedMsgPos: 'bottom',
      }));
    } catch (e) {
      this.store.update(state => ({
        ...state,
        isSending: false,
        hasMore: false,
        isFetching: false,
      }));

      throw e;
    }
  }

  async fetchPrevious() {
    if (!this.hasMore || !this.lastChatID) {
      return;
    }

    const params = new URLSearchParams();
    params.append('before', this.lastChatID);

    this.store.update(state => {
      state.isFetching = true;
      return state;
    });

    try {
      const res = await authedFetch<Message[]>(`/playlists/${this.id}/chat?${params}`);
      if (!res || !res.ok || !res.data) {
        throw new Error('Failed to fetch Chat history');
      }

      this.store.update(state => {
        state.messages = res.data.concat(state.messages);
        state.hasMore = res.data.length !== 0;
        state.lastAddedMsgPos = 'top';
        return state;
      });

      await sleep(500);

      this.store.update(state => {
        state.isFetching = false;
        return state;
      });
    } catch (e) {
      this.store.update(state => {
        state.hasMore = false;
        state.isFetching = false;
        return state;
      });

      throw e;
    }
  }

  async send(message: string) {
    const newMessage: Message = {
      bot: false,
      timestamp: Date.now() / 1000,
      content: message,
    };

    // optimistic update
    this.store.update(state => {
      state.messages.push(newMessage);
      state.lastAddedMsgPos = 'bottom';
      return state;
    });

    await sleep(this.randomArtificialDelay);

    this.store.update(state => {
      state.isSending = true;
      return state;
    });

    try {
      const res = await authedFetch<Message>(`/playlists/${this.id}/chat`, {
        method: 'POST',
        body: JSON.stringify({ content: message }),
      });

      if (!res?.ok || !res.data) {
        throw new Error('Failed to fetch Chat history');
      }

      this.store.update(state => {
        state.messages.push(res.data);
        state.isSending = false;
        return state;
      });
    } catch (e) {
      this.store.update(state => {
        state.isSending = false;
        return state;
      });

      throw e;
    }
  }
}

export const chatFeedStore = new ChatFeedStore();

export const placeholders = [
  { bot: false },
  { bot: true },
  { bot: false },
  { bot: true },
  { bot: false },
  { bot: true },
]
