<script lang="ts">
  import { Avatar } from "@skeletonlabs/skeleton";
	import { page } from "$app/stores";
	import { randomElement } from "$lib/utils/randomElement";
  import { intersectionObserver } from "$lib/utils/intersectionObserverAction";
  import {
    placeholders,
    tracksStore,
    type Track,
  } from "../stores/tracksStore";

  export let title: string | undefined;

  let tracks: Track[];
  let hasMore = true;
  tracksStore.subscribe(state => {
    tracks = state.tracks;
    hasMore = state.hasMore;
  });

  async function fetchNext(e: CustomEvent<boolean>) {
    if (!e.detail) {
      return;
    }

    await tracksStore.fetchNext();
  }

  $: id = $page.params.id;
  $: {
    tracksStore.id = $page.params.id;
  }

  const validPaddings = ['w-12', 'w-14', 'w-16', 'w-20', 'w-24', 'w-28', 'w-32', 'w-36'];
</script>

<section
  class="lg:w-[30vw] bg-surface-100-800-token pb-4 overflow-y-auto text-nowrap flex-1"
>
  {#if !id}
    <span class="flex justify-center items-center h-full">
      👈 Select a playlist to get started
    </span>
  {:else}
    <div class="bg-surface-100-800-token sticky top-0 z-[1] py-4 px-3">
      <p class="text-2xl font-bold px-2">
        {#if title}
          {title}
        {:else}
          &nbsp;
        {/if}
      </p>
    </div>
    <hr class="mx-3">
    <dl class="list-dl px-3">
      {#each tracks as track}
        <div class="w-full">
          <span>
            <Avatar
              src={track.icon}
              initials={track.id}
              width="w-9"
              rounded="rounded-lg"
            />
          </span>
          <span class="overflow-x-hidden">
            <dt class="text-ellipsis whitespace-nowrap overflow-x-hidden">
              {track.name}
            </dt>
            <dd class="text-sm opacity-50 text-ellipsis whitespace-nowrap overflow-x-hidden">
              {track.artists}
            </dd>
          </span>
        </div>
      {/each}
      {#if hasMore}
        <div
          use:intersectionObserver
          on:intersect={fetchNext}
        />
        {#each placeholders as _}
          <div class="w-full">
            <span>
              <Avatar
                initials=" "
                width="w-9"
                rounded="rounded-lg"
                class="apa"
              />
            </span>
            <span class="overflow-x-hidden">
              <dt class="text-ellipsis whitespace-nowrap overflow-x-hidden aph {randomElement(validPaddings)} my-1 !h-4" />
              <dd class="text-sm !opacity-50 text-ellipsis whitespace-nowrap overflow-x-hidden aph {randomElement(validPaddings)} my-1 !h-3" />
            </span>
          </div>
        {/each}
      {:else if !hasMore && tracks.length === 0}
          <p class="flex justify-center pt-8">
            (This playlist does not have any songs)
          </p>
      {/if}
    </dl>
  {/if}
</section>
