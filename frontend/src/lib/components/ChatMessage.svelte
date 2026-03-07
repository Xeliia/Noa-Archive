<script>
  import miniProfile from '../assets/mini-profile.png'

  let {
    msg,
    showTime = false,
    showAvatar = false,
    showSeen = false,
    formatTime,
  } = $props()
</script>

{#if msg.role === 'user'}
  <div class="msg-enter flex flex-col items-end">
    <div class="msg-bubble-user max-w-[78%] px-4 py-2.5 text-sm leading-relaxed whitespace-pre-wrap rounded-[18px] rounded-br-[4px]">
      {msg.content}
    </div>
    {#if showTime || showSeen}
      <div class="flex items-center gap-1.5 mt-1 px-1">
        {#if showTime}
          <span class="text-[11px] text-nord-3/70">{formatTime(msg.time)}</span>
        {/if}
        {#if showSeen}
          <img src={miniProfile} alt="Seen" class="w-3.5 h-3.5 rounded-full object-cover" />
        {/if}
      </div>
    {/if}
  </div>
{:else}
  {#if msg.content}
  <div class="msg-enter flex gap-2 items-end">
    {#if showAvatar}
      <img src={miniProfile} alt="Ushio Noa" class="w-7 h-7 rounded-full object-cover shrink-0" />
    {:else}
      <div class="w-7 shrink-0"></div>
    {/if}
    
    <div class="flex flex-col items-start">
      <div class="msg-bubble-noa max-w-[78%] px-4 py-2.5 text-sm leading-relaxed whitespace-pre-wrap rounded-[18px] rounded-bl-[4px]">
        {msg.content}
      </div>
      {#if showTime}
        <span class="text-[11px] text-nord-3/70 mt-1 px-1">{formatTime(msg.time)}</span>
      {/if}
    </div>
  </div>
  {/if}
{/if}
