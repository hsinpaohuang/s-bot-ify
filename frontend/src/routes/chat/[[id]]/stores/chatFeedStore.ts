import { authedFetch } from "$lib/utils/fetchWrappers";
import { sleep } from "$lib/utils/sleep";
import { get, writable } from "svelte/store";

export type Message = {
  id?: string;
  bot: boolean;
  timeStamp: string;
  content: string;
}

type ChatResponse = {
  history: Message[];
}

type State = {
  messages: Message[];
  isSending: boolean;
  hasMore: boolean;
}

// TODO: replace with real chat feed
const timeStamp = Intl.DateTimeFormat().format();
const fakeChatFeed: Message[] = [
  {
    id: '1',
    bot: true,
    timeStamp,
    content: 'Test Message 1',
  },
  {
    id: '2',
    bot: false,
    timeStamp,
    content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec turpis metus, porta sagittis rhoncus id, pharetra quis arcu. Maecenas in nisi a tortor consequat efficitur sit amet eget dui. Quisque scelerisque condimentum euismod. Fusce tristique diam ut ligula euismod, at fringilla risus elementum. Nam ultricies convallis mollis. Etiam varius in metus vel hendrerit. Proin elementum lectus vitae sapien eleifend, id ullamcorper urna varius. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed consectetur tincidunt augue, sit amet ultrices ipsum suscipit et. Etiam vulputate condimentum dignissim. Nam vitae congue mauris.',
  },
  {
    id: '1',
    bot: true,
    timeStamp,
    content: 'Fusce elementum aliquet magna nec luctus. Donec sed vehicula mi. Morbi nec justo aliquam, feugiat dolor ac, pulvinar sapien. Integer iaculis venenatis scelerisque. Nulla quis eleifend quam. Curabitur volutpat leo non erat elementum, eget sollicitudin tortor dignissim. Vivamus pharetra, felis sed rhoncus blandit, lorem dui volutpat dui, quis pharetra quam libero hendrerit magna. Aenean in mi vitae turpis tristique dictum. Praesent quam neque, consectetur lobortis lacus a, eleifend consequat erat. Sed tempor blandit augue sollicitudin pulvinar. Aenean ut elit dui. Suspendisse eros risus, pharetra a scelerisque id, congue non augue.',
  },
  {
    id: '2',
    bot: false,
    timeStamp,
    content: 'Test Message 2',
  },
  {
    id: '3',
    bot: true,
    timeStamp,
    content: 'Duis ultricies, dui euismod rhoncus placerat, erat nibh sodales leo, a eleifend arcu lectus vulputate tellus. Aenean tellus quam, finibus non justo non, rutrum posuere ipsum. Donec sollicitudin lectus id elit posuere, quis vulputate urna laoreet. Vivamus tempor, libero eget tincidunt laoreet, nisi lectus consectetur nibh, non fermentum risus felis ac urna. Praesent odio erat, tincidunt sed malesuada at, ultrices ullamcorper nisi. Integer auctor mi urna, quis viverra ipsum mattis nec. Pellentesque vitae rutrum nisl. Nam vulputate ligula vel quam venenatis, nec imperdiet odio sodales. Nunc nec diam vel magna facilisis mattis.',
  },
  {
    id: '4',
    bot: false,
    timeStamp,
    content: 'Test Message 4',
  },
  {
    id: '5',
    bot: true,
    timeStamp,
    content: 'Test Message 5',
  },
  {
    id: '6',
    bot: false,
    timeStamp,
    content: 'Test Message 6',
  },
  {
    id: '7',
    bot: true,
    timeStamp,
    content: 'Test Message 7',
  },
  {
    id: '8',
    bot: false,
    timeStamp,
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

    const res = await authedFetch<ChatResponse>(`/playlists/${id}/chat`);
    if (!res || !res.ok || !res.data) {
      throw new Error('Failed to fetch Chat history');
    }

    const { history } = res.data;

    this.store.update(({ isSending }) => ({
      messages: history,
      isSending,
      hasMore: history.length !== 0,
    }));
  }

  async fetchPrevious() {
    if (!this.hasMore || !this.lastChatID) {
      return;
    }

    const params = new URLSearchParams();
    params.append('before', this.lastChatID);

    const res = await authedFetch<ChatResponse>(`/playlists/${this.id}/chat?${params}`);
    if (!res || !res.ok || !res.data) {
      throw new Error('Failed to fetch Chat history');
    }

    const { history } = res.data;

    this.store.update(({ messages, isSending }) => ({
      messages: messages.concat(history),
      isSending,
      hasMore: history.length !== 0,
    }));
  }

  async send(message: string) {
    const newMessage: Message = {
      bot: false,
      timeStamp: Intl.DateTimeFormat().format(),
      content: message,
    };

    // optimistic update
    this.store.update(({ messages, hasMore }) => ({
      messages: [...messages, newMessage],
      isSending: true,
      hasMore,
    }));

    await sleep(this.randomArtificialDelay);

    // TODO: replace with send message
    await sleep(this.FIXED_ARTIFICAL_DELAY);
    const response = fakeChatFeed[0]

    this.store.update(({ messages, hasMore }) => ({
      messages: [...messages, response],
      isSending: false,
      hasMore,
    }));
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
