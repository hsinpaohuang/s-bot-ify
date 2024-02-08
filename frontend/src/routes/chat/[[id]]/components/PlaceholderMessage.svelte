<script lang="ts">
  import { Avatar } from "@skeletonlabs/skeleton";
	import { randomElement } from "$lib/utils/randomElement";

  export let bot: boolean;

  $: cardColor = bot ? 'variant-glass-primary' : 'variant-glass-tertiary';

  // random number of lines with random horizontal padding for placeholders
  const placeholderLines = Array.from(
    { length: Math.ceil(Math.random() * 3) },
    () => randomElement(
      ['w-24', 'w-28', 'w-32', 'w-36', 'w-40', 'w-48', 'w-52', 'w-56'],
    ),
  );
</script>

<div class="flex gap-2" class:flex-row-reverse={!bot}>
  <Avatar
    initials=" "
    width="w-12"
    rounded="rounded-xl"
    class="apa min-w-12 h-fit"
  />
  <div class="card p-4 space-y-2 {cardColor}">
    <header class="flex items-center">
      <p class="aph px-6 !h-4" />
      &nbsp;
      <small class="aph px-12 !h-4" />
    </header>
    {#each placeholderLines as width}
      <p class="aph {width} !h-4" />
    {/each}
  </div>
</div>
