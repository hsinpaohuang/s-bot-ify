<script lang="ts">
  import type { PopupSettings } from '@skeletonlabs/skeleton';
  // @ts-expect-error no type definitions available for this package
  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
  import { faCircleQuestion } from '@fortawesome/free-solid-svg-icons';
  import { page } from '$app/stores';
	import Popup from '$lib/components/Popup.svelte';
	import { chatFeedStore } from '../stores/chatFeedStore';

  let currentMessage = '';
  let numRows = 1;

  $: isInputDisabled = !$page.params.id;
  $: isSendButtonDisabled = isInputDisabled || currentMessage === '';

  const inputHintPopup: PopupSettings = {
    event: 'hover',
    target: 'inputHintPopup',
    placement: 'top-end',
    middleware: { offset: { mainAxis: 24 } },
  };

  /**
   * check if shift + enter is pressed
   *
   * if yes, submit the message
   */
  function onInput({ key, shiftKey }: KeyboardEvent) {
    numRows = Math.min((currentMessage.match(/\n/g)?.length || 0) + 1, 5);

    if (!(key === 'Enter' && shiftKey)) {
      return;
    }

    sendMessage();
  }

  function sendMessage() {
    chatFeedStore.send(currentMessage);
    currentMessage = '';
    numRows = 1;
  }
</script>

<div class="flex items-center gap-1 bg-surface-500/30 p-4 shadow-[0_-7px_15px_0_rgb(0,0,0,0.12)]">
  <div class="input-group input-group-divider grid-cols-[1fr_auto] rounded-container-token">
    <textarea
      bind:value={currentMessage}
      class="bg-transparent border-0 ring-0 p-2"
      placeholder="Write a message..."
      rows={numRows}
      disabled={isInputDisabled}
      on:keyup={onInput}
    />
    <button
      class="variant-filled-primary disabled:variant-filled-surface disabled:cursor-not-allowed"
      disabled={isSendButtonDisabled}
      on:click={sendMessage}
    >
      Send
    </button>
  </div>
  <Popup
    settings={inputHintPopup}
    arrowClass="ml-0.5"
    cardWidth="w-auto"
    class="pl-2"
  >
    <FontAwesomeIcon icon={faCircleQuestion} class="text-xl text-surface-300" />

    <p slot="popup-card">Press shift + enter to send</p>
  </Popup>
</div>
