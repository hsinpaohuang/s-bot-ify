<script lang="ts">
  import { Avatar, type PopupSettings } from "@skeletonlabs/skeleton";
	import Popup from "./Popup.svelte";

  const popupSettings: PopupSettings = {
    event: 'click',
    target: 'avatar-popup',
    placement: 'bottom-end',
    middleware: { offset: { mainAxis: 12, crossAxis: -12 } },
  };
</script>

<Popup
  settings={popupSettings}
  arrowClass="-ml-4"
  cardWidth="w-48"
  as="button"
  type="button"
  class="btn-icon"
>
  <Avatar rounded="rounded-xl" />

  <ul class="list" slot="popup-card">
    <li>
      <span class="logout-text">Logout</span>
    </li>
  </ul>
</Popup>

<style>
  .logout-text {
    @apply text-error-400;
  }

  :global(html.dark .logout-text) {
    @apply text-error-500;
  }
</style>
