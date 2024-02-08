import { sleep } from "$lib/utils/sleep";
import { writable } from "svelte/store";

export type Message = {
  id?: string;
  bot: boolean;
  timeStamp: string;
  content: string;
}

type State = {
  messages: Message[];
  isSending: boolean;
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

  private update;
  private id = '';

  constructor() {
    const { subscribe, update } = writable<State>({
      messages: [],
      isSending: false,
    });
    this.subscribe = subscribe;
    this.update = update;
  }

  private get randomArtificialDelay() {
    return this.FIXED_ARTIFICAL_DELAY + Math.random() * 1000;
  }

  async fetchNewChat(id: string) {
    this.id = id;

    // TODO: replace with real chat
    await sleep(this.FIXED_ARTIFICAL_DELAY);
    const newChat = fakeChatFeed;

    this.update(({ isSending }) => ({ messages: newChat, isSending }));
  }

  async fetchPrevious() {
    // TODO: replace with real previous chat
    await sleep(this.FIXED_ARTIFICAL_DELAY);
    const prevChat = fakeChatFeed;

    this.update(({ messages, isSending }) => ({
      messages: prevChat.concat(messages),
      isSending,
    }));
  }

  async send(message: string) {
    const newMessage: Message = {
      bot: false,
      timeStamp: Intl.DateTimeFormat().format(),
      content: message,
    };

    // optimistic update
    this.update(({ messages }) => ({
      messages: [...messages, newMessage],
      isSending: true,
    }));

    await sleep(this.randomArtificialDelay);

    // TODO: replace with send message
    await sleep(this.FIXED_ARTIFICAL_DELAY);
    const response = fakeChatFeed[0]

    this.update(({ messages }) => ({
      messages: [...messages, response],
      isSending: false,
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
