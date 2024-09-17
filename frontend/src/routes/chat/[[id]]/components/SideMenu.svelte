<script lang="ts">
  import { onDestroy } from "svelte";
  import { AppRail, AppRailAnchor, Avatar, type PopupSettings } from "@skeletonlabs/skeleton";
  import { page } from "$app/stores";
	import { afterNavigate } from "$app/navigation";
	import Popup from "$lib/components/Popup.svelte";
  import { sideMenuStore } from "$lib/stores/sideMenuStore";
	import PlaylistMenu from "./PlaylistMenu.svelte";
	import { playlistsStore, type Playlist, placeholders } from "../stores/playlistsStore";
	import { intersectionObserver } from "$lib/utils/intersectionObserverAction";

  sideMenuStore.setHasSideMenu(true);
  onDestroy(() => {
    sideMenuStore.setHasSideMenu(false);
  });

  afterNavigate(nav => {
    sideMenuStore.setIsOpen(!nav.to?.params?.id);
  });


  let playlists: Playlist[];
  let hasMore = true;
  playlistsStore.subscribe(state => {
    playlists = state.playlists;
    hasMore = state.hasMore;
  });

  $: selectedPlaylist = playlists.find(({ id }) => id === $page.params.id);

  function popupSettings(id: string): PopupSettings {
    return {
      event: 'hover',
      target: `playlistPopup-${id}`,
      placement: 'right',
    };
  }

  async function fetchNext(e: CustomEvent<boolean>) {
    if (!e.detail) {
      return;
    }

    await playlistsStore.fetchNext();
  }
</script>

<aside class="flex h-full w-screen lg:w-auto shadow-[7px_0_15px_0_rgb(0,0,0,0.12)]">
  <AppRail
    width="w-16"
    height="h-auto"
    class="no-scrollbar pt-4 z-10 shadow-[7px_0_15px_0_rgb(0,0,0,0.12)]"
    regionDefault="flex flex-col"
  >
    {#each playlists as playlist}
      <AppRailAnchor
        href="/chat/{playlist.id}"
        selected={$page.url.pathname === `/chat/${playlist.id}`}
      >
        <Popup
          settings={popupSettings(playlist.id)}
          class="flex justify-center [&>*]:pointer-events-none"
          role="button"
          tabindex="0"
        >
          <Avatar
            src={playlist.icon ?? undefined}
            initials={playlist.name}
            width="w-12"
            rounded="rounded-xl"
          />
          <span slot="popup-card">{playlist.name}</span>
        </Popup>
      </AppRailAnchor>
    {/each}
    {#if hasMore}
      <div
        use:intersectionObserver
        on:intersect={fetchNext}
      />
      {#each placeholders as placeholder}
        <AppRailAnchor>
          <Popup
            settings={popupSettings(String(placeholder))}
            class="flex justify-center [&>*]:pointer-events-none"
            role="button"
            tabindex="0"
          >
            <Avatar
              initials=" "
              width="w-12"
              rounded="rounded-xl"
            />
            <span slot="popup-card">Loading...</span>
          </Popup>
        </AppRailAnchor>
      {/each}
    {/if}
      <!-- TODO: add create button -->
  </AppRail>
  <PlaylistMenu title={selectedPlaylist?.name} />
</aside>
