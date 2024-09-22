<script lang="ts">
  import { Avatar } from "@skeletonlabs/skeleton";
	import type { Message } from "../stores/chatFeedStore";

  export let message: Message;


  $: sender = message.bot ? 'Bot' : 'You';

  $: cardColor = message.bot
    ? 'variant-glass-primary'
    : 'variant-glass-tertiary';
</script>

<div class="flex gap-2" class:flex-row-reverse={!message.bot}>
  <Avatar
    initials={sender[0]}
    width="w-12"
    rounded="rounded-xl"
    class="h-fit min-w-12"
  />
  <div class="card p-4 space-y-2 {cardColor}">
    <header class="flex items-center">
      <p class="font-bold">{sender}</p>
      &nbsp;
      <small class="opacity-50">@ {message.timestamp}</small>
    </header>
    <p class="whitespace-pre-wrap">{message.content}</p>
  </div>
</div>
