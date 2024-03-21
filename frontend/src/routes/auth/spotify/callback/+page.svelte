<script lang="ts">
	import { onMount } from "svelte";
	import { getToastStore } from "@skeletonlabs/skeleton";
  import { authStore } from "$lib/stores/authStore";
	import { goto, preloadCode } from "$app/navigation";

  onMount(async () => {
    try {
      await preloadCode('/');
      await authStore.getToken();
      goto('/chat');
    } catch (e) {
      const error = e as Error;
      const toastStore = getToastStore();
      toastStore.trigger({
        message: error.cause
          ? error.message
          : 'Failed to login. Please try again by refreshing the page later.',
        background: 'variant-filled-error',
      });

      console.error(e);
    }
  });
</script>

