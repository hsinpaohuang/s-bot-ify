<script lang="ts">
  import { tick, beforeUpdate, afterUpdate } from "svelte";
	import { afterNavigate } from "$app/navigation";
  import { chatFeedStore, placeholders, type Message } from "../stores/chatFeedStore";
  import ChatMessage from "./ChatMessage.svelte";
  import PlaceholderMessage from "./PlaceholderMessage.svelte";
  import BotTyping from './BotTyping.svelte';
	import LoadPrevChat from "./LoadPrevChat.svelte";

  let chatFeedRef: HTMLDivElement;

  let chatFeed: Message[] = [];
  let isResponding: boolean;
  let lastPos: 'top' | 'bottom' | null = null;
  chatFeedStore.subscribe(async({ messages, isSending, lastAddedMsgPos }) => {
    chatFeed = messages;
    isResponding = isSending;
    lastPos = lastAddedMsgPos;
  });

  // scroll to bottom when new message is appended to chat
  async function scrollToBottom() {
    await tick();

    chatFeedRef.scrollTo({
      top: chatFeedRef.scrollHeight,
      behavior: 'smooth',
    });
  }

  $: if (isResponding) {
    scrollToBottom();
  }

  let prevHeight = 0;
  beforeUpdate(() => {
    if (!chatFeed.length) {
      return;
    }

    prevHeight = chatFeedRef.scrollHeight;
  });

  afterUpdate(() => {
    if (!chatFeed.length) {
      return;
    }

    if (lastPos === 'top') {
      const currHeight = chatFeedRef.scrollHeight;
      const diff = currHeight - prevHeight;
      if (diff === 0) {
        return;
      }

      chatFeedRef.scrollBy({ top: diff, behavior: 'instant' });
    } else if (lastPos === 'bottom') {
      scrollToBottom();
    }
  });

  let fetching: Promise<void>;

  afterNavigate(nav => {
    const id = nav.to?.params?.id;
    if (!id) {
      return;
    }

    fetching = chatFeedStore.fetchNewChat(id);
  });
</script>

<div
  bind:this={chatFeedRef}
  class="flex flex-col gap-4 flex-1 overflow-y-auto px-3 py-6"
>
  {#await fetching}
    {#each placeholders as { bot }}
      <PlaceholderMessage {bot} />
    {/each}
  {:then _}
    <LoadPrevChat />

    {#each chatFeed as message}
      <ChatMessage {message} />
    {/each}
    {#if chatFeed.length === 0}
      <!-- TODO: Fix this message -->
      <span class="text-center">(No messages)</span>
    {/if}
    {#if isResponding}
      <BotTyping />
    {/if}
  {:catch}
    <span class="text-center">
      Sorry, something went wrong. Please try again later.
    </span>
  {/await}
</div>
