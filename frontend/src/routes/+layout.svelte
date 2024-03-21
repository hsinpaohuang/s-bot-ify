<script lang="ts">
	import '../app.postcss';
	import { AppShell, AppBar, LightSwitch, Toast, initializeStores } from '@skeletonlabs/skeleton';
	import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	// @ts-expect-error no type definitions available for this package
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
	import { config } from '@fortawesome/fontawesome-svg-core';
	import '@fortawesome/fontawesome-svg-core/styles.css';
	import { faBars } from '@fortawesome/free-solid-svg-icons';
	import AvatarButton from '$lib/components/AvatarButton.svelte';
	import { sideMenuStore } from '$lib/stores/sideMenuStore';

	// for fontawesome
	config.autoAddCss = false;

	// skeleton setups
	initializeStores();
	storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });


	let hasMobileSideMenu: boolean;
	sideMenuStore.subscribe(({ hasSideMenu }) => {
		hasMobileSideMenu = hasSideMenu;
	});
</script>

<Toast />

<!-- App Shell -->
<AppShell>
	<AppBar slot="header" shadow="shadow-lg">
		<div slot="lead" class="flex items-center gap-4">
			{#if hasMobileSideMenu}
				<button
					type="button"
					class="pt-1"
					on:click={sideMenuStore.toggleOpen}
				>
					<FontAwesomeIcon
						icon={faBars}
						class="text-xl lg:!hidden cursor-pointer"
					/>
				</button>
			{/if}
			<strong class="text-xl uppercase select-none">S-bot-ify</strong>
		</div>
		<svelte:fragment slot="trail">
			<LightSwitch />
			<AvatarButton />
		</svelte:fragment>
	</AppBar>
	<!-- Page Route Content -->
	<slot />
</AppShell>
