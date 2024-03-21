<!-- TODO: check if user has logged in -->

<script lang="ts">
	import { ProgressRadial } from '@skeletonlabs/skeleton';
  // @ts-expect-error no type definitions available for this package
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  import { faSpotify } from '@fortawesome/free-brands-svg-icons';
  import { faArrowUpRightFromSquare } from '@fortawesome/free-solid-svg-icons';
  import { authStore } from '$lib/stores/authStore';

  let isAuthing = false;

  async function redirectToSpotifyOAuth() {
    isAuthing = true;
    window.location.assign(await authStore.getAuthURL());
  }
</script>

<div class="flex flex-col justify-center items-center h-full gap-8">
  <p class="text-2xl">
    Log in With Spotify to Get Started
  </p>
  <button
    class="btn spotify-button"
    on:click={redirectToSpotifyOAuth}
  >
    <FontAwesomeIcon icon={faSpotify} class="text-2xl" />
    <span>Log in with Spotify</span>
    {#if isAuthing}
      <ProgressRadial width="w-6" />
    {:else}
      <FontAwesomeIcon icon={faArrowUpRightFromSquare} class="text-sm" />
    {/if}
  </button>
</div>

<style>
  .spotify-button {
    background-color: #1DB954;
  }
</style>
