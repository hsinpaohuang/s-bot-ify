<script lang="ts">
  import { Avatar, type PopupSettings } from "@skeletonlabs/skeleton";
  // @ts-expect-error no type definitions available for this package
  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  import { faArrowRightFromBracket } from '@fortawesome/free-solid-svg-icons';
	import Popup from "$lib/components/Popup.svelte";
	import { userInfoStore, type UserInfo } from "$lib/stores/userInfoStore";
	import { authStore } from "$lib/stores/authStore";

  const popupSettings: PopupSettings = {
    event: 'click',
    target: 'avatar-popup',
    placement: 'bottom-end',
    middleware: { offset: { mainAxis: 12, crossAxis: -12 } },
  };

  let userInfo: UserInfo;
  userInfoStore.subscribe(state => {
    userInfo = state;
  });

  $: isUserInfoLoaded = Boolean(userInfo.displayName);
  $: initials = userInfo.displayName || 'Y'; // Y === you;

  authStore.isLoggedInStore.subscribe(async isLoggedIn => {
    if (!isLoggedIn) {
      return;
    }

    await userInfoStore.load();
  });
</script>

{#if isUserInfoLoaded}
  <Popup
    settings={popupSettings}
    arrowClass="-ml-4"
    cardWidth="w-48"
    as="button"
    type="button"
    class="btn-icon"
  >
    <Avatar src={userInfo.avatar} {initials} rounded="rounded-xl" />

    <ul class="list flex flex-col gap-1" slot="popup-card">
      <li class="flex">
        <Avatar src={userInfo.avatar} {initials} width="w-8" rounded="rounded-lg" />
        <span>
          {userInfo.displayName}
        </span>
      </li>
      <li class="cursor-pointer">
        <FontAwesomeIcon
          icon={faArrowRightFromBracket}
          class="w-8 text-xl -scale-x-100"
        />
        <span class="logout-text">Logout</span>
      </li>
    </ul>
  </Popup>
{/if}


<style>
  .logout-text {
    @apply text-error-400;
  }

  :global(html.dark .logout-text) {
    @apply text-error-500;
  }
</style>
