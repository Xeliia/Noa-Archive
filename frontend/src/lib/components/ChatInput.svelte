<script>
  import { Send, CircleStop } from 'lucide-svelte'

  let {
    input = $bindable(''),
    loading = false,
    onSend,
    onStop,
  } = $props()

  let textareaEl = $state(null)

  function adjustTextarea() {
    if (!textareaEl) return
    textareaEl.style.height = 'auto'
    textareaEl.style.height = Math.min(textareaEl.scrollHeight, 120) + 'px'
  }

  function handleKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      onSend()
    }
  }

  // Reset textarea height when input is cleared externally
  $effect(() => {
    if (input === '' && textareaEl) {
      textareaEl.style.height = 'auto'
    }
  })
</script>

<div class="px-5 py-4 border-t border-nord-5 rounded-b-[24px]">
  <div class="flex items-center gap-2 bg-nord-6 rounded-full px-4 py-1.5 transition-all duration-200 focus-within:ring-2 focus-within:ring-nord-8/30">

    <!-- Input -->
    <textarea
      bind:this={textareaEl}
      bind:value={input}
      oninput={adjustTextarea}
      onkeydown={handleKeydown}
      placeholder="Write a Message"
      disabled={loading}
      rows="1"
      class="flex-1 bg-transparent border-none outline-none resize-none text-sm text-nord-0 placeholder-nord-3/50 max-h-28 py-2.5 leading-none"
    ></textarea>

    <!-- Send / Stop -->
    {#if loading}
      <button
        class="w-10 h-10 rounded-full flex items-center justify-center shrink-0 border-none transition-all duration-200
          bg-red-500/80 text-white shadow-sm hover:bg-red-600 hover:scale-105 cursor-pointer"
        onclick={onStop}
        title="Stop generating"
      >
        <CircleStop size={18} />
      </button>
    {:else}
      <button
        class="w-10 h-10 rounded-full flex items-center justify-center shrink-0 border-none transition-all duration-200
          {input.trim()
            ? 'bg-nord-0 text-white shadow-sm hover:bg-nord-1 hover:scale-105 cursor-pointer'
            : 'bg-nord-4/60 text-nord-3/40 cursor-default'}"
        onclick={onSend}
        disabled={!input.trim()}
      >
        <Send size={18} />
      </button>
    {/if}
  </div>
</div>
