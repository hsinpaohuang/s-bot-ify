<script lang="ts">
	import { popup, type PopupSettings } from "@skeletonlabs/skeleton";

  export let as = 'div';
  export let settings: PopupSettings;
  export let cardWidth = '';
  export let arrowClass = '';
</script>

<div
  class="card {cardWidth} shadow-xl p-2 variant-filled"
  data-popup={settings.target}
>
  <slot name="popup-card" />
  <div class="arrow variant-filled {arrowClass}" />
</div>

<svelte:element this={as} use:popup={settings} {...$$props}>
  <slot />
</svelte:element>
