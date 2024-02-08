<script lang="ts">
  import { onDestroy } from "svelte";
  import { AppRail, AppRailAnchor, Avatar, type PopupSettings } from "@skeletonlabs/skeleton";
  import { page } from "$app/stores";
	import { afterNavigate } from "$app/navigation";
	import Popup from "$lib/components/Popup.svelte";
  import { sideMenuStore } from "$lib/stores/sideMenuStore";
	import PlaylistMenu from "./PlaylistMenu.svelte";
	import { playlistsStore, type Playlist, placeholders } from "../stores/playlistsStore";

  sideMenuStore.setHasSideMenu(true);
  onDestroy(() => {
    sideMenuStore.setHasSideMenu(false);
  });

  afterNavigate(nav => {
    sideMenuStore.setIsOpen(!nav.to?.params?.id);
  });

  $: fetching = playlistsStore.fetchPlaylists();

  let playlists: Playlist[];
  playlistsStore.subscribe(state => {
    playlists = state;
  });

  $: selectedPlaylist = playlists.find(({ id }) => id === $page.params.id);

  function popupSettings(id: string): PopupSettings {
    return {
      event: 'hover',
      target: `playlistPopup-${id}`,
      placement: 'right',
    };
  }
</script>

<aside class="flex h-full w-screen lg:w-auto shadow-[7px_0_15px_0_rgb(0,0,0,0.12)]">
  <AppRail width="w-16" class="pt-4 z-10 shadow-[7px_0_15px_0_rgb(0,0,0,0.12)]">
    {#await fetching}
      {#each placeholders as _}
        <AppRailAnchor>
          <div class="flex justify-center">
            <Avatar
              initials=" "
              width="w-12"
              rounded="rounded-xl"
              class="apa"
            />
          </div>
        </AppRailAnchor>
      {/each}
    {:then}
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
            <Avatar initials={playlist.id} width="w-12" rounded="rounded-xl" />

            <span slot="popup-card">{playlist.title}</span>
          </Popup>
        </AppRailAnchor>
      {/each}
      <!-- TODO: add create button -->
    {/await}
  </AppRail>
  <PlaylistMenu title={selectedPlaylist?.title} />
</aside>
