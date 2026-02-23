<script>
  import { Eye, Pen, Book } from 'lucide-svelte'

  let {
    msg,
    showTime = false,
    showAvatar = false,
    formatTime,
  } = $props()
</script>

<div class="msg-enter flex gap-2 items-end">
  <!-- Avatar -->
  {#if showAvatar}
    <img src="/src/lib/assets/mini-profile.png" alt="Ushio Noa" class="w-7 h-7 rounded-full object-cover shrink-0" />
  {:else}
    <div class="w-7 shrink-0"></div>
  {/if}
  
  <div class="flex flex-col items-start max-w-[85%]">
    <!-- Text bubble -->
    <div class="msg-bubble-noa rounded-[18px] rounded-bl-[4px] px-4 py-2.5 text-sm leading-relaxed w-full">
      {msg.content}
    </div>

    <!-- Stats card -->
    {#if msg.stats}
      <div class="stats-card w-full mt-2 bg-white border border-nord-5 rounded-2xl overflow-hidden">
        <div class="stats-grid grid grid-cols-3 divide-x divide-nord-5">
          {#each msg.stats as stat}
            <div class="stat-item flex flex-col items-center py-4 px-3 gap-1.5">
              <div class="text-nord-3">
                {#if stat.icon === 'eye'}
                  <Eye size={18} />
                {:else if stat.icon === 'pen'}
                  <Pen size={18} />
                {:else if stat.icon === 'book'}
                  <Book size={18} />
                {/if}
              </div>
              <span class="text-[11px] text-nord-3">{stat.label}</span>
              <span class="text-lg font-semibold text-nord-0 leading-none">{stat.value}</span>
            </div>
          {/each}
        </div>
      </div>
    {/if}

    <!-- Image grid -->
    {#if msg.images}
      <div class="w-full mt-2 bg-nord-0 rounded-2xl overflow-hidden p-1">
        <p class="text-white text-xs px-3 pt-2 pb-1.5 opacity-80">Here are the photos:</p>
        <div class="grid grid-cols-3 gap-1">
          {#each msg.images as _, imgIdx}
            <div class="relative aspect-[4/3] bg-nord-2 rounded-lg overflow-hidden
              {imgIdx === 0 ? 'col-span-2 row-span-2 aspect-square' : ''}">
              <div class="absolute inset-0 bg-gradient-to-br
                {imgIdx === 0 ? 'from-nord-3 to-nord-1' : imgIdx === 1 ? 'from-nord-2 to-nord-3' : imgIdx === 2 ? 'from-nord-13/30 to-nord-2' : 'from-nord-1 to-nord-3'}
                flex items-center justify-center">
                {#if imgIdx === msg.images.length - 1 && msg.images.length > 3}
                  <span class="text-white text-lg font-semibold">3+</span>
                {:else}
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-white/40" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909M3.75 21h16.5A2.25 2.25 0 0022.5 18.75V5.25A2.25 2.25 0 0020.25 3H3.75A2.25 2.25 0 001.5 5.25v13.5A2.25 2.25 0 003.75 21z"/>
                  </svg>
                {/if}
              </div>
            </div>
          {/each}
        </div>
      </div>
    {/if}

    {#if showTime}
      <span class="text-[11px] text-nord-3/70 mt-1 px-1">{formatTime(msg.time)}</span>
    {/if}
  </div>
</div>
