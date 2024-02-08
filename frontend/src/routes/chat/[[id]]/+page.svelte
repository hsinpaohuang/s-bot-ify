<script lang="ts">
	import SideMenu from "./components/SideMenu.svelte";
	import ChatFeed from "./components/ChatFeed.svelte";
	import MessageInput from "./components/MessageInput.svelte";
	import { sideMenuStore } from "$lib/stores/sideMenuStore";

	let isMenuOpen: boolean;
  sideMenuStore.subscribe(({ isOpen }) => {
    isMenuOpen = isOpen;
  });
</script>

<div class="w-full h-full flex">
	<div
		class="z-[1] transition-transform lg:translate-x-0"
		class:-translate-x-[100vw]={!isMenuOpen}
	>
		<SideMenu />
	</div>
	<div
		class="flex flex-col h-full w-full transition-[margin-left] lg:ml-0"
		class:-ml-[100vw]={!isMenuOpen}
	>
		<ChatFeed />
		<MessageInput />
	</div>
</div>

<style>
	/* required to have input stay at bottom of page */
	:global(#page-content) {
		@apply h-full;
	}
</style>
