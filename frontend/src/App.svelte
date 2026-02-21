<script>
  import { tick } from 'svelte'
  import { Send, Trash, Info, X, Github, ExternalLink, Cake, Sun, Moon, Eye, Pen, Book } from 'lucide-svelte';

  // ── API Configuration ──
  // Change this to your ngrok URL when using remote access
  const API_URL = 'http://localhost:8000'
  const API_KEY = 'changeme'  // Must match backend .env API_KEY

  /* ── Theme state ── */
  let isDark = $state(false)
  
  function toggleTheme() {
    isDark = !isDark
  }

  /* ── Card panel states ── */
  let showCharacterCard = $state(false)
  let showProjectCard = $state(false)
  let showLightbox = $state(false)
  
  /* ── Profile flip state ── */
  let profileFlipped = $state(false)
  
  /* ── Closing animation states ── */
  let closingLightbox = $state(false)
  
  function closeLightbox() {
    closingLightbox = true
    setTimeout(() => {
      showLightbox = false
      closingLightbox = false
    }, 250)
  }

  /* ── Message Presets ── */
  const MESSAGE_PRESETS = [
    // Preset #1
    [
      { role: 'assistant', content: "Welcome, Sensei. I've been reviewing the logs since you were last active.", type: 'text' },
      { role: 'assistant', content: "According to my schedule, we should be preparing for the next Seminar meeting now...", type: 'text' },
      { role: 'assistant', content: "But I suppose I can spare a few moments for a morning check. Shall we?", type: 'text' }
    ],
    // Preset #2
    [
      { role: 'assistant', content: "Oh, Sensei. Perfect timing.", type: 'text' },
      { role: 'assistant', content: "I was just showing Yuuka the data from your last 'productive' session.", type: 'text' },
      { role: 'assistant', content: "Her reaction was... quite memorable. I've archived it for later. Hehe.", type: 'text' }
    ],
    // Preset #3
    [
      { role: 'assistant', content: "Records aren't just bureaucracy, Sensei.", type: 'text' },
      { role: 'assistant', content: "They are safeguards against being overlooked.", type: 'text' },
      {
        role: 'assistant',
        content: "I've already initialized today's observation parameters:",
        type: 'rich',
        stats: [
          { icon: 'eye', label: 'Sensei Status', value: 'Present' },
          { icon: 'pen', label: 'Ink Levels', value: 'Full' },
          { icon: 'book', label: 'Unread Logs', value: '0' }
        ]
      },
      { role: 'assistant', content: "Now what shall we record today, Sensei.", type: 'text' }
    ],
    // Preset #4
    [
      { role: 'assistant', content: "It's nice to be remembered by others.", type: 'text' },
      { role: 'assistant', content: "Thank you for thinking of me today, Sensei.", type: 'text' },
      { role: 'assistant', content: "My pen is ready whenever you are. What shall we record first?", type: 'text' }
    ],
    // Preset #5
    [
      { role: 'assistant', content: "It's quiet today. I've cleared my desk of everything but the essentials.", type: 'text' },
      { role: 'assistant', content: "A minimalist workspace leads to a clear record, after all.", type: 'text' },
      { role: 'assistant', content: "Is there anything you'd like to commit to memory today?", type: 'text' }
    ]
  ]

  function getRandomPreset() {
    const preset = MESSAGE_PRESETS[Math.floor(Math.random() * MESSAGE_PRESETS.length)]
    let idCounter = 1
    return preset.map(msg => ({
      ...msg,
      id: idCounter++,
      time: new Date(Date.now() - (idCounter * 1000))
    }))
  }

  let messages = $state(getRandomPreset())

  let input = $state('')
  let loading = $state(false)
  let bottomEl = $state(null)
  let textareaEl = $state(null)

  function formatTime(date) {
    return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true })
  }

  function shouldShowTime(index) {
    if (index === messages.length - 1) return true
    const currentTime = formatTime(messages[index].time)
    const nextTime = formatTime(messages[index + 1].time)
    return currentTime !== nextTime
  }

  function shouldShowAvatar(index) {
    if (index === messages.length - 1) return true
    return messages[index].role !== messages[index + 1].role
  }

  function shouldShowSeen(index) {
    // Show seen indicator on last user message only if AI hasn't responded yet
    const msg = messages[index]
    if (msg.role !== 'user') return false
    // Check if this is the last message overall (no AI response yet) or if typing
    return index === messages.length - 1
  }

  function adjustTextarea() {
    if (!textareaEl) return
    textareaEl.style.height = 'auto'
    textareaEl.style.height = Math.min(textareaEl.scrollHeight, 120) + 'px'
  }

  async function scrollToBottom() {
    await tick()
    bottomEl?.scrollIntoView({ behavior: 'smooth' })
  }

  function clearChat() {
    messages = getRandomPreset()
    input = ''
  }

  async function sendMessage(text) {
    const content = text ?? input.trim()
    if (!content || loading) return

    input = ''
    if (textareaEl) textareaEl.style.height = 'auto'

    const userMsg = { id: Date.now(), role: 'user', content, time: new Date(), type: 'text' }
    messages = [...messages, userMsg]
    loading = true
    await scrollToBottom()

    // Create placeholder for streaming response
    const assistantMsgId = Date.now() + 1
    const assistantMsg = { id: assistantMsgId, role: 'assistant', content: '', time: new Date(), type: 'text' }
    messages = [...messages, assistantMsg]

    try {
      const history = messages
        .filter(m => m.type === 'text' && m.content && m.id !== assistantMsgId)
        .map(m => ({ role: m.role, content: m.content }))
      
      const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${API_KEY}`
        },
        body: JSON.stringify({
          messages: history,
          stream: true
        }),
      })

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`)
      }

      // Handle streaming response (SSE)
      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let accumulated = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data.trim() === '[DONE]') continue

            try {
              const parsed = JSON.parse(data)
              if (parsed.error) {
                accumulated = parsed.error
              } else if (parsed.content) {
                accumulated += parsed.content
                // Update the message reactively
                messages = messages.map(m => 
                  m.id === assistantMsgId 
                    ? { ...m, content: accumulated }
                    : m
                )
                await scrollToBottom()
              }
            } catch (e) {
              // Skip invalid JSON
            }
          }
        }
      }

      // Ensure final update
      if (!accumulated) {
        accumulated = "Sorry, I couldn't respond."
      }
      messages = messages.map(m => 
        m.id === assistantMsgId 
          ? { ...m, content: accumulated }
          : m
      )
    } catch {
      messages = messages.map(m => 
        m.id === assistantMsgId 
          ? { ...m, content: 'Something went wrong. Please try again.' }
          : m
      )
    } finally {
      loading = false
      await scrollToBottom()
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  /* ── 3D Tilt effect (cursor-following) ── */
  function handleTiltMove(e) {
    const card = e.currentTarget
    const rect = card.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top
    const centerX = rect.width / 2
    const centerY = rect.height / 2
    const rotateX = ((y - centerY) / centerY) * -15
    const rotateY = ((x - centerX) / centerX) * 15
    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`
  }

  function handleTiltLeave(e) {
    e.currentTarget.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)'
  }

  /* ── Close any open panel (for mobile overlay) ── */
  function closeAllPanels() {
    showCharacterCard = false
    showProjectCard = false
  }
</script>

<!-- Mobile/Tablet overlay backdrop -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div 
  class="mobile-overlay lg:hidden {showCharacterCard || showProjectCard ? 'active' : ''}"
  onclick={closeAllPanels}
  onkeydown={(e) => e.key === 'Escape' && closeAllPanels()}
  role="presentation"
></div>

<div data-theme={isDark ? 'nord-dark' : 'nord'} class="theme-wrapper min-h-screen flex items-center justify-center p-4 md:p-8 gap-4">

  <!-- ─── Character Info Card (Left) ─── -->
  <div class="card-panel-wrapper shrink-0 overflow-hidden transition-all duration-300 ease-out {showCharacterCard ? '' : 'max-lg:pointer-events-none'}" style="width: {showCharacterCard ? '24rem' : '0'}; height: min(700px, 85vh);">
    <div class="character-card w-96 h-full flex flex-col rounded-3xl overflow-hidden" style="opacity: {showCharacterCard ? '1' : '0'}; transform: translateX({showCharacterCard ? '0' : '-100%'});">
      <!-- Close button -->
      <button 
        class="absolute top-3 right-3 z-10 w-8 h-8 rounded-full bg-white/80 backdrop-blur flex items-center justify-center text-nord-3 hover:text-nord-0 hover:bg-white transition-all shadow-sm cursor-pointer"
        onclick={() => showCharacterCard = false}
      >
        <X size={16} />
      </button>

      <!-- Profile section -->
      <div class="flex flex-col items-center pt-8 pb-6 px-6 bg-gradient-to-b from-nord-8/20 to-transparent">
        <!-- Avatar (flippable) -->
        <div class="relative mb-4">
          <button 
            class="profile-image-wrapper w-32 h-32 rounded-full bg-gradient-to-br from-nord-8/30 to-nord-9/30 p-1 cursor-pointer"
            class:flipped={profileFlipped}
            onclick={() => profileFlipped = !profileFlipped}
          >
            <div class="flipper w-full h-full">
              <img src="/src/assets/mini-profile.png" alt="Ushio Noa - Front" class="profile-face profile-front" />
              <img src="/src/assets/mini-profile2.png" alt="Ushio Noa - Back" class="profile-face profile-back" />
            </div>
          </button>
        </div>

        <!-- Name -->
        <h2 class="text-xl font-semibold text-nord-0 mb-1">Noa</h2>
        <p class="text-sm text-nord-3 italic mb-4">The Melancholy of Kivotos</p>

        <!-- Birthday badge -->
        <div class="aurora-pill aurora-purple inline-flex items-center gap-2">
          <Cake size={16} />
          <span class="text-sm font-medium">April 13th</span>
        </div>
      </div>

      <!-- Divider -->
      <div class="mx-6 border-t border-nord-5"></div>

      <!-- Cover photo thumbnail -->
      <div class="flex-1 p-6 flex flex-col min-h-0">
        <p class="text-xs text-nord-3 uppercase tracking-wider font-medium mb-3 text-center">
          Cover Photo
        </p>

        <button 
          class="tilt-card flex-1 w-full rounded-2xl overflow-hidden shadow-lg cursor-pointer min-h-0"
          onclick={() => showLightbox = true}
          onmousemove={handleTiltMove}
          onmouseleave={handleTiltLeave}
        >
          <img 
            src="/src/assets/cover-photo.jpg" 
            alt="Noa Cover" 
            class="w-full h-full object-cover" 
          />
        </button>
      </div>
    </div>
  </div>

  <!-- ─── Main Chat Card ─── -->
  <div class="chat-card w-full max-w-2xl flex flex-col overflow-hidden" style="height: min(1000px, 90vh); width: clamp(320px, 90vw, 1200px);">

    <!-- ─── Header ─── -->
    <div class="flex items-center gap-3 px-6 py-4 border-b border-nord-5">
      <!-- Avatar (clickable) -->
      <button 
        class="relative group cursor-pointer"
        onclick={() => { 
          showCharacterCard = !showCharacterCard
          showProjectCard = false
        }}
      >
        <img src="/src/assets/mini-profile.png" alt="Ushio Noa" class="header-avatar w-11 h-11 rounded-full object-cover shadow-sm transition-transform group-hover:scale-105" />
        <span class="status-indicator absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 bg-nord-14 rounded-full border-2 border-white"></span>
      </button>

      <!-- Name & status -->
      <div class="flex-1 min-w-0">
        <h1 class="font-semibold text-nord-0 text-base leading-tight">Ushio Noa</h1>
        <p class="text-xs text-nord-14 font-medium flex items-center gap-1">
          <span class="inline-block w-1.5 h-1.5 rounded-full bg-nord-14"></span>
          Online
        </p>
      </div>

      <!-- Utility icons -->
      <div class="flex items-center gap-1">
        <!-- Theme Toggle -->
        <button 
          class="theme-toggle btn btn-ghost btn-sm btn-square transition-colors"
          onclick={toggleTheme}
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
        
        <!-- Info -->
        <button 
          class="btn btn-ghost btn-sm btn-square text-nord-3 hover:text-nord-0 transition-colors"
          onclick={() => { 
            showProjectCard = !showProjectCard
            showCharacterCard = false
          }}
          title="Project Info"
        >
          <Info size={18} />
        </button>
        <!-- Clear chat -->
        <button class="btn btn-ghost btn-sm btn-square text-nord-11 hover:bg-nord-11/10 transition-colors" onclick={clearChat} title="Clear chat">
          <Trash size={18} />
        </button>
      </div>
    </div>

    <!-- ─── Messages ─── -->
    <div class="flex-1 overflow-y-auto px-5 py-5 flex flex-col gap-1.5 bg-white">

      {#each messages as msg, i (msg.id)}

        <!-- ── Text message ── -->
        {#if msg.type === 'text'}
          {#if msg.role === 'user'}
            <!-- User message (right-aligned, no avatar) -->
            <div class="msg-enter flex flex-col items-end">
              <div class="max-w-[78%] px-4 py-2.5 text-sm leading-relaxed whitespace-pre-wrap bg-[#88C0D0] text-white rounded-[18px] rounded-br-[4px]">
                {msg.content}
              </div>
              <!-- Time and Seen indicator -->
              {#if shouldShowTime(i) || shouldShowSeen(i)}
                <div class="flex items-center gap-1.5 mt-1 px-1">
                  {#if shouldShowTime(i)}
                    <span class="text-[11px] text-nord-3/70">{formatTime(msg.time)}</span>
                  {/if}
                  <!-- Seen indicator (small avatar) on last user message when AI hasn't responded -->
                  {#if shouldShowSeen(i)}
                    <img src="/src/assets/mini-profile.png" alt="Seen" class="w-3.5 h-3.5 rounded-full object-cover" />
                  {/if}
                </div>
              {/if}
            </div>
          {:else}
            <!-- Assistant message (left-aligned, with avatar) -->
            <div class="msg-enter flex gap-2 items-end">
              {#if shouldShowAvatar(i)}
                <img src="/src/assets/mini-profile.png" alt="Ushio Noa" class="w-7 h-7 rounded-full object-cover shrink-0" />
              {:else}
                <div class="w-7 shrink-0"></div>
              {/if}
              
              <div class="flex flex-col items-start">
                <div class="max-w-[78%] px-4 py-2.5 text-sm leading-relaxed whitespace-pre-wrap bg-nord-0 text-white rounded-[18px] rounded-bl-[4px]">
                  {msg.content}
                </div>
                {#if shouldShowTime(i)}
                  <span class="text-[11px] text-nord-3/70 mt-1 px-1">{formatTime(msg.time)}</span>
                {/if}
              </div>
            </div>
          {/if}

        <!-- ── Rich message (text + stats + images) ── -->
        {:else if msg.type === 'rich'}
          <div class="msg-enter flex gap-2 items-end">
            <!-- Avatar -->
            {#if shouldShowAvatar(i)}
              <img src="/src/assets/mini-profile.png" alt="Ushio Noa" class="w-7 h-7 rounded-full object-cover shrink-0" />
            {:else}
              <div class="w-7 shrink-0"></div>
            {/if}
            
            <div class="flex flex-col items-start max-w-[85%]">
            <!-- Text bubble -->
            <div class="bg-nord-0 text-white rounded-[18px] rounded-bl-[4px] px-4 py-2.5 text-sm leading-relaxed w-full">
              {msg.content}
            </div>

            <!-- Stats card -->
            {#if msg.stats}
              <div class="stats-card w-full mt-2 bg-white border border-nord-5 rounded-2xl overflow-hidden">
                <div class="stats-grid grid grid-cols-3 divide-x divide-nord-5">
                  {#each msg.stats as stat}
                    <div class="stat-item flex flex-col items-center py-4 px-3 gap-1.5">
                      <!-- Icon -->
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
                  {#each msg.images as _, i}
                    <div class="relative aspect-[4/3] bg-nord-2 rounded-lg overflow-hidden
                      {i === 0 ? 'col-span-2 row-span-2 aspect-square' : ''}">
                      <!-- Placeholder image pattern -->
                      <div class="absolute inset-0 bg-gradient-to-br
                        {i === 0 ? 'from-nord-3 to-nord-1' : i === 1 ? 'from-nord-2 to-nord-3' : i === 2 ? 'from-nord-13/30 to-nord-2' : 'from-nord-1 to-nord-3'}
                        flex items-center justify-center">
                        {#if i === msg.images.length - 1 && msg.images.length > 3}
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

              {#if shouldShowTime(i)}
                <span class="text-[11px] text-nord-3/70 mt-1 px-1">{formatTime(msg.time)}</span>
              {/if}
            </div>
          </div>
        {/if}

      {/each}

      <!-- ── Typing Indicator ── -->
      {#if loading}
        <div class="msg-enter flex gap-2 items-end">
          <img src="/src/assets/mini-profile.png" alt="Ushio Noa" class="w-7 h-7 rounded-full object-cover shrink-0" />
          <div class="bg-nord-0 rounded-[18px] rounded-bl-[4px] px-4 py-3">
            <div class="flex items-center gap-2">
              <span class="text-xs text-white/60 italic">AI is thinking</span>
              <div class="flex gap-1 items-center">
                {#each [0, 1, 2] as i}
                  <span class="dot-bounce block w-1.5 h-1.5 rounded-full bg-white/70"
                    style="animation-delay: {i * 0.2}s"></span>
                {/each}
              </div>
            </div>
          </div>
        </div>
      {/if}

      <div bind:this={bottomEl}></div>
    </div>

    <!-- ─── Input Area ─── -->
    <div class="px-5 py-4 border-t border-nord-5 bg-white rounded-b-[24px]">
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

        <!-- Send -->
        <button
          class="w-10 h-10 rounded-full flex items-center justify-center shrink-0 border-none transition-all duration-200
            {input.trim() && !loading
              ? 'bg-nord-0 text-white shadow-sm hover:bg-nord-1 hover:scale-105 cursor-pointer'
              : 'bg-nord-4/60 text-nord-3/40 cursor-default'}"
          onclick={() => sendMessage()}
          disabled={!input.trim() || loading}
        >
          <Send size={18} />
        </button>
      </div>
    </div>

  </div>

  <!-- ─── Project Info Card (Right) ─── -->
  <div class="card-panel-wrapper shrink-0 overflow-hidden transition-all duration-300 ease-out {showProjectCard ? '' : 'max-lg:pointer-events-none'}" style="width: {showProjectCard ? '20rem' : '0'}; height: min(600px, 80vh);">
    <div class="project-card w-80 h-full flex flex-col rounded-3xl overflow-hidden" style="opacity: {showProjectCard ? '1' : '0'}; transform: translateX({showProjectCard ? '0' : '100%'});">
      <!-- Close button -->
      <button 
        class="absolute top-3 right-3 z-10 w-8 h-8 rounded-full bg-white/80 backdrop-blur flex items-center justify-center text-nord-3 hover:text-nord-0 hover:bg-white transition-all shadow-sm cursor-pointer"
        onclick={() => showProjectCard = false}
      >
        <X size={16} />
      </button>

      <!-- Header -->
      <div class="px-6 pt-8 pb-6 bg-gradient-to-b from-nord-9/20 to-transparent">
        <h2 class="text-xl font-semibold text-nord-0 mb-1">About This Project</h2>
        <p class="text-sm text-nord-3">Noa AI Chatbot</p>
      </div>

      <!-- Content -->
      <div class="flex-1 overflow-y-auto px-6 pb-6">
        <!-- Description -->
        <div class="mb-6">
          <h3 class="text-xs text-nord-3 uppercase tracking-wider font-medium mb-2">Description</h3>
          <p class="text-sm text-nord-0 leading-relaxed">
            <!-- PLACEHOLDER: Add your project description here -->
            A conversational AI chatbot featuring Ushio Noa from Blue Archive. Built with Svelte and powered by your local LLM.
          </p>
        </div>

        <!-- Tech Stack -->
        <div class="mb-6">
          <h3 class="text-xs text-nord-3 uppercase tracking-wider font-medium mb-2">Tech Stack</h3>
          <div class="flex flex-wrap gap-2">
            <!-- PLACEHOLDER: Add/modify tech badges -->
            <span class="aurora-pill aurora-red">Svelte 5</span>
            <span class="aurora-pill aurora-orange">Tailwind CSS</span>
            <span class="aurora-pill aurora-yellow">DaisyUI</span>
            <span class="aurora-pill aurora-purple">Local LLM</span>
            <span class="aurora-pill aurora-green">FastAPI</span>
            <span class="aurora-pill aurora-red">ngrok</span>
          </div>
        </div>

        <!-- Future Plans -->
        <div class="mb-6">
          <h3 class="text-xs text-nord-3 uppercase tracking-wider font-medium mb-2">Future Plans</h3>
          <p class="text-sm text-nord-0 leading-relaxed">
            <!-- PLACEHOLDER: Add future plans -->
            - Add support for image and audio messages<br>
            - Add support for Cloud LLMs and API-based models<br>
          </p>
        </div>

        <!-- Credits -->
        <div class="mb-6">
          <h3 class="text-xs text-nord-3 uppercase tracking-wider font-medium mb-2">Credits</h3>
          <p class="text-sm text-nord-0 leading-relaxed">
            <!-- PLACEHOLDER: Add credits -->
            Character © NEXON Games / Blue Archive
          </p>
        </div>

        <!-- Links -->
        <div>
          <h3 class="text-xs text-nord-3 uppercase tracking-wider font-medium mb-3">Links</h3>
          <div class="flex flex-col gap-2">
            <!-- TODO: Update these hrefs with actual links -->
            <a href="https://github.com" target="_blank" rel="noopener noreferrer" class="flex items-center gap-3 px-4 py-3 bg-nord-6 hover:bg-nord-5 rounded-xl transition-colors group">
              <Github size={18} class="text-nord-0" />
              <span class="text-sm text-nord-0 font-medium">GitHub Repository</span>
              <ExternalLink size={14} class="text-nord-3 ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
            </a>
            <a href="https://example.com" target="_blank" rel="noopener noreferrer" class="flex items-center gap-3 px-4 py-3 bg-nord-6 hover:bg-nord-5 rounded-xl transition-colors group">
              <ExternalLink size={18} class="text-nord-0" />
              <span class="text-sm text-nord-0 font-medium">Live Demo</span>
              <ExternalLink size={14} class="text-nord-3 ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
            </a>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="px-6 py-4 border-t border-nord-5 bg-nord-6/50">
        <p class="text-xs text-nord-3 text-center">
          <!-- PLACEHOLDER: Version/Build info -->
          Version 1.0.0 • Made with ♥
        </p>
      </div>
    </div>
  </div>

</div>

<!-- ─── Lightbox Modal ─── -->
{#if showLightbox}
  <div 
    class="{closingLightbox ? 'lightbox-overlay-closing' : 'lightbox-overlay'} fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-8"
    onclick={closeLightbox}
    onkeydown={(e) => e.key === 'Escape' && closeLightbox()}
    role="button"
    tabindex="0"
  >
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div 
      class="{closingLightbox ? 'lightbox-card-closing' : 'lightbox-card'}"
      onclick={(e) => e.stopPropagation()}
      onkeydown={(e) => e.stopPropagation()}
      role="presentation"
    >
      <div 
        class="cover-3d-card rounded-3xl overflow-hidden shadow-2xl" 
        style="max-width: 80vw; max-height: 80vh;"
        onmousemove={handleTiltMove}
        onmouseleave={handleTiltLeave}
        role="img"
        aria-label="Noa cover photo with 3D tilt effect"
      >
        <img 
          src="/src/assets/cover-photo.jpg" 
          alt="Noa Cover" 
          class="w-auto h-auto max-w-full max-h-[80vh] object-contain"
        />
      </div>
    </div>
    
    <!-- Close button -->
    <button 
      class="absolute top-6 right-6 w-10 h-10 rounded-full bg-white/20 backdrop-blur flex items-center justify-center text-white hover:bg-white/30 transition-all"
      onclick={closeLightbox}
    >
      <X size={20} />
    </button>
  </div>
{/if}
