<script lang="ts">
	import { onMount, tick } from "svelte";
	import { sleep } from "$lib/utils/sleep";
  import { chatFeedStore, placeholders } from "../stores/chatFeedStore";
	import PlaceholderMessage from "./PlaceholderMessage.svelte";

  let hasMore = true;
  let isFetching = false;
  let observeTarget: HTMLDivElement;
  let isIntersecting = false;

  const observer = new IntersectionObserver(entries => {
    isIntersecting = Boolean(entries[0]?.isIntersecting);
  });

  chatFeedStore.subscribe(state => {
    hasMore = state.hasMore;
    isFetching = state.isFetching;

    if (!hasMore) {
      observer.disconnect();
      window.scrollTo(0, 0);
      return;
    }
  });

  $: if (hasMore && !isFetching && isIntersecting) {
    tick().then(() => {
      if (!isIntersecting) {
        return;
      }

      chatFeedStore.fetchPrevious();
    })
  }

  onMount(async () => {
    await sleep(1000);

    if (!observeTarget) {
      return;
    }

    observer.observe(observeTarget);
  });
</script>

<div bind:this={observeTarget}>
  {#if hasMore}
    {#each placeholders as { bot }}
      <PlaceholderMessage {bot} />
    {/each}
  {:else}
  <p class="text-center pb-4">
    (This is the beginning of the conversation)
  </p>
  {/if}
</div>
