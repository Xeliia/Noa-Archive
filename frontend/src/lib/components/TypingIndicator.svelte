<div class="msg-enter flex gap-2 items-end">
  <img src="/src/lib/assets/mini-profile.png" alt="Ushio Noa" class="w-7 h-7 rounded-full object-cover shrink-0" />
  <div class="flex flex-col items-start">
    <div class="msg-bubble-noa rounded-[18px] rounded-bl-[4px] px-4 py-3">
      <div class="flex gap-1 items-center">
        {#each [0, 1, 2] as i}
          <span class="dot-bounce block w-2 h-2 rounded-full bg-white/70"
            style="animation-delay: {i * 0.15}s"></span>
        {/each}
      </div>
    </div>
    <span class="text-[11px] text-nord-3/70 mt-1 px-1">Noa is typing...</span>
  </div>
</div>
