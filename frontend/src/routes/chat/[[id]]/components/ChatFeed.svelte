<script lang="ts">
  import { tick } from "svelte";
	import { afterNavigate } from "$app/navigation";
	import { sleep } from "$lib/utils/sleep";
  import { chatFeedStore, placeholders, type Message } from "../stores/chatFeedStore";
  import ChatMessage from "./ChatMessage.svelte";
  import PlaceholderMessage from "./PlaceholderMessage.svelte";
  import BotTyping from './BotTyping.svelte';

  let chatFeedRef: HTMLDivElement;

  let chatFeed: Message[];
  let isResponding: boolean;
  chatFeedStore.subscribe(async({ messages, isSending }) => {
    chatFeed = messages;
    if (isSending) {
      await sleep(chatFeedStore.FIXED_ARTIFICAL_DELAY);
    }
    isResponding = isSending;
  });

  // scroll to bottom when new message is appended to chat
  $: {
    const lastID = chatFeed[chatFeed.length - 1]?.id;
    tick().then(() => {
      chatFeedRef.scrollTo({
        top: chatFeedRef.scrollHeight,
        behavior: isResponding || !lastID ? 'smooth' : 'instant',
      });
    });
  }

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
