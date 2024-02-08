<script lang="ts">
  import { Avatar } from "@skeletonlabs/skeleton";
	import { page } from "$app/stores";
	import { randomElement } from "$lib/utils/randomElement";
  import { placeholders, playlistStore, type Song } from "../stores/playlistStore";

  export let title: string | undefined;

  let songs: Song[];
  playlistStore.subscribe(state => {
    songs = state.songs;
  });

  $: id = $page.params.id;
  $: fetching = id && playlistStore.fetchPlaylist(id);

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
    <div class="bg-surface-100-800-token sticky top-0 z-[1] py-4 px-3 shadow-[0_7px_15px_0_rgb(0,0,0,0.12)]">
      <p class="text-2xl font-bold px-2">
        {#if title}
          {title}
        {:else}
          &nbsp;
        {/if}
      </p>
    </div>
    <dl class="list-dl px-3">
      {#await fetching}
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
      {:then}
        {#each songs as song}
          <div class="w-full">
            <span>
              <Avatar initials={song.id} width="w-9" rounded="rounded-lg" />
            </span>
            <span class="overflow-x-hidden">
              <dt class="text-ellipsis whitespace-nowrap overflow-x-hidden">
                {song.title}
              </dt>
              <dd class="text-sm opacity-50 text-ellipsis whitespace-nowrap overflow-x-hidden">
                {song.authors}
              </dd>
            </span>
          </div>
        {/each}
      {:catch}
        Could not retrieve plalist at this time. Please try again later.
      {/await}
    </dl>
  {/if}
</section>
