<script lang="ts">
  import { Avatar } from "@skeletonlabs/skeleton";
</script>

<div class="flex gap-2">
  <Avatar
    initials="B"
    width="w-12"
    rounded="rounded-xl"
    class="h-fit min-w-12"
  />
  <div class="card p-4 space-y-2 variant-glass-primary">
    <header class="flex items-center">
      <p class="font-bold">Bot</p>
      &nbsp;
      <small class="opacity-50">(typing)</small>
    </header>
    <p class="whitespace-pre-wrap px-24 aph" />
  </div>
</div>
