<script>
  import { Send, Trash, Info, X, Sun, Moon, History } from 'lucide-svelte'

  let {
    isDark,
    showCharacterCard,
    showProjectCard,
    showHistoryPanel,
    onToggleTheme,
    onToggleCharacter,
    onToggleProject,
    onToggleHistory,
    onClearChat,
  } = $props()
</script>

<div class="flex items-center gap-3 px-6 py-4 border-b border-nord-5">
  <button 
    class="relative group cursor-pointer"
    onclick={onToggleCharacter}
  >
    <img src="/src/lib/assets/mini-profile.png" alt="Ushio Noa" class="header-avatar w-11 h-11 rounded-full object-cover shadow-sm transition-transform group-hover:scale-105" />
    <span class="status-indicator absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 bg-nord-14 rounded-full border-2 border-white"></span>
  </button>

  <div class="flex-1 min-w-0">
    <h1 class="font-semibold text-nord-0 text-base leading-tight">Ushio Noa</h1>
    <p class="text-xs text-nord-14 font-medium flex items-center gap-1">
      <span class="inline-block w-1.5 h-1.5 rounded-full bg-nord-14"></span>
      Online
    </p>
  </div>

  <div class="flex items-center gap-1">
    <button 
      class="theme-toggle btn btn-ghost btn-sm btn-square transition-colors"
      onclick={onToggleTheme}
      title={isDark ? "Switch to light mode" : "Switch to dark mode"}
    >
      <div class="theme-icon-wrapper">
        {#if isDark}
          <Sun size={18} class="theme-icon sun-icon" />
        {:else}
          <Moon size={18} class="theme-icon moon-icon" />
        {/if}
      </div>
    </button>
    
    <button 
      class="btn btn-ghost btn-sm btn-square text-nord-3 hover:text-nord-0 transition-colors"
      onclick={onToggleProject}
      title="Project Info"
    >
      <Info size={18} />
    </button>
    <button 
      class="btn btn-ghost btn-sm btn-square text-nord-3 hover:text-nord-0 transition-colors"
      onclick={onToggleHistory}
      title="Chat History"
    >
      <History size={18} />
    </button>
    <button class="btn btn-ghost btn-sm btn-square text-nord-11 hover:bg-nord-11/10 transition-colors" onclick={onClearChat} title="Clear chat">
      <Trash size={18} />
    </button>
  </div>
</div>
