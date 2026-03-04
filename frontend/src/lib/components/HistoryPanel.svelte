<script>
  import { X, History, MessageSquare, Trash2 } from 'lucide-svelte'

  let {
    show = false,
    chatHistory = [],
    currentChatId = null,
    onClose,
    onLoadChat,
    onDeleteChat,
    onClearAll,
    formatHistoryDate,
  } = $props()
</script>

<div class="card-panel-wrapper shrink-0 overflow-hidden transition-all duration-300 ease-out {show ? '' : 'max-lg:pointer-events-none'}" style="width: {show ? '22rem' : '0'}; height: min(700px, 85vh);">
  <div class="history-card w-[22rem] h-full flex flex-col rounded-3xl overflow-hidden" style="opacity: {show ? '1' : '0'}; transform: translateX({show ? '0' : '-100%'});">
    <button 
      class="absolute top-3 right-3 z-10 w-8 h-8 rounded-full bg-white/80 backdrop-blur flex items-center justify-center text-nord-3 hover:text-nord-0 hover:bg-white transition-all shadow-sm cursor-pointer"
      onclick={onClose}
    >
      <X size={16} />
    </button>

    <div class="px-6 pt-8 pb-4">
      <div class="flex items-center gap-2 mb-1">
        <History size={20} class="text-nord-0" />
        <h2 class="text-xl font-semibold text-nord-0">Chat History</h2>
      </div>
      <p class="text-sm text-nord-3">{chatHistory.length} saved conversation{chatHistory.length !== 1 ? 's' : ''}</p>
    </div>

    <div class="mx-6 border-t border-nord-5"></div>

    <div class="flex-1 overflow-y-auto px-4 py-3">
      {#if chatHistory.length === 0}
        <div class="flex flex-col items-center justify-center h-full text-center px-4">
          <MessageSquare size={32} class="text-nord-3/40 mb-3" />
          <p class="text-sm text-nord-3/70">No saved conversations yet</p>
          <p class="text-xs text-nord-3/50 mt-1">Your chat history will appear here after you send messages</p>
        </div>
      {:else}
        <div class="flex flex-col gap-1.5">
          {#each chatHistory as chat, idx (chat.id)}
            <button
              class="history-item group w-full text-left px-4 py-3 rounded-xl transition-all duration-200 cursor-pointer
                {currentChatId === chat.id ? 'history-item-active' : ''}"
              onclick={() => onLoadChat(chat)}
            >
              <div class="flex items-start gap-3">
                <MessageSquare size={16} class="history-icon history-icon-{idx % 5} shrink-0 mt-0.5" />
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-nord-0 truncate leading-tight">{chat.title}</p>
                  <p class="text-[11px] text-nord-3/70 mt-1">{formatHistoryDate(chat.lastMessageAt)}</p>
                </div>
                <!-- Delete button (hover only) -->
                <!-- svelte-ignore a11y_no_static_element_interactions -->
                <div
                  class="opacity-0 group-hover:opacity-100 transition-opacity shrink-0"
                  onclick={(e) => { e.stopPropagation(); onDeleteChat(chat.id) }}
                  onkeydown={(e) => { if(e.key === 'Enter') { e.stopPropagation(); onDeleteChat(chat.id) } }}
                  role="button"
                  tabindex="-1"
                >
                  <Trash2 size={14} class="text-nord-11/60 hover:text-nord-11 transition-colors" />
                </div>
              </div>
            </button>
          {/each}
        </div>
      {/if}
    </div>

    {#if chatHistory.length > 0}
      <div class="px-6 py-4 border-t border-nord-5 bg-nord-6/50">
        <button 
          class="w-full text-xs text-nord-11/70 hover:text-nord-11 transition-colors py-2 cursor-pointer"
          onclick={onClearAll}
        >
          Clear all history
        </button>
      </div>
    {/if}
  </div>
</div>
