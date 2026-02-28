<script>
  import { tick } from 'svelte'

  // -- Components --
  import ChatHeader from './lib/components/ChatHeader.svelte'
  import ChatMessage from './lib/components/ChatMessage.svelte'
  import RichMessage from './lib/components/RichMessage.svelte'
  import TypingIndicator from './lib/components/TypingIndicator.svelte'
  import ChatInput from './lib/components/ChatInput.svelte'
  import CharacterCard from './lib/components/CharacterCard.svelte'
  import ProjectCard from './lib/components/ProjectCard.svelte'
  import HistoryPanel from './lib/components/HistoryPanel.svelte'
  import Lightbox from './lib/components/Lightbox.svelte'

  // -- API Configuration --
  const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
  const API_KEY = import.meta.env.VITE_API_KEY ?? 'changeme'

  /* -- Theme state -- */
  let isDark = $state(false)
  
  function toggleTheme() {
    isDark = !isDark
  }

  /* -- Card panel states -- */
  let showCharacterCard = $state(false)
  let showProjectCard = $state(false)
  let showHistoryPanel = $state(false)
  let showLightbox = $state(false)
  
  /* -- Closing animation states -- */
  let closingLightbox = $state(false)
  
  function closeLightbox() {
    closingLightbox = true
    setTimeout(() => {
      showLightbox = false
      closingLightbox = false
    }, 250)
  }

  /* -- Message Presets -- */
  const MESSAGE_PRESETS = [
    [
      { role: 'assistant', content: "Welcome. I'm Ushio Noa, Student Council President of South City Homes Academy's Senior High School department.", type: 'text' },
      { role: 'assistant', content: "I've already organized today's agenda, so feel free to ask me anything about our school.", type: 'text' },
      { role: 'assistant', content: "Whether it's admissions, academic strands, or campus life — I have it all committed to memory.", type: 'text' }
    ],
    [
      { role: 'assistant', content: "Oh, a visitor. How fortunate — I just finished reviewing the enrollment records.", type: 'text' },
      { role: 'assistant', content: "I'm Noa, Student Council President here at SCHA. Consider me your personal guide.", type: 'text' },
      { role: 'assistant', content: "Now then, what would you like to know? I assure you, my memory is quite reliable. Fufu.", type: 'text' }
    ],
    [
      { role: 'assistant', content: "Good day. I was just cataloging some documents for the registrar's office.", type: 'text' },
      { role: 'assistant', content: "But I can certainly spare a moment. As Student Council President, assisting visitors is part of my duty.", type: 'text' },
      { role: 'assistant', content: "Ask me anything about South City Homes Academy. I promise not a single detail will be overlooked.", type: 'text' }
    ],
    [
      { role: 'assistant', content: "Fufu, another curious visitor. I do appreciate people who seek information proactively.", type: 'text' },
      { role: 'assistant', content: "I'm Ushio Noa — Student Council President representing the Senior High School department of SCHA.", type: 'text' },
      { role: 'assistant', content: "Go ahead and ask your questions. I've memorized every detail worth knowing about this academy.", type: 'text' }
    ],
    [
      { role: 'assistant', content: "It's a quiet afternoon. Perfect for a thorough consultation.", type: 'text' },
      { role: 'assistant', content: "I'm Noa, your guide to everything about South City Homes Academy.", type: 'text' },
      { role: 'assistant', content: "From academic strands to enrollment procedures — I have it all on record. What would you like to know?", type: 'text' }
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
  let abortController = $state(null)

  /* -- Chat History (localStorage) -- */
  const HISTORY_KEY = 'noa-chat-history'
  const MAX_HISTORY = 50

  let chatHistory = $state(loadHistory())
  let currentChatId = $state(null)

  function loadHistory() {
    try {
      const raw = localStorage.getItem(HISTORY_KEY)
      return raw ? JSON.parse(raw) : []
    } catch { return [] }
  }

  function saveHistory() {
    try {
      localStorage.setItem(HISTORY_KEY, JSON.stringify(chatHistory.slice(0, MAX_HISTORY)))
    } catch { /* storage full -- silently fail */ }
  }

  function getChatTitle(msgs) {
    const firstUser = msgs.find(m => m.role === 'user' && m.type === 'text')
    if (firstUser) {
      const text = firstUser.content.trim()
      return text.length > 50 ? text.slice(0, 50) + '\u2026' : text
    }
    return 'New conversation'
  }

  function hasUserMessages(msgs) {
    return msgs.some(m => m.role === 'user' && m.type === 'text')
  }

  function saveCurrentChat() {
    if (!hasUserMessages(messages)) return

    const chatEntry = {
      id: currentChatId ?? Date.now().toString(),
      title: getChatTitle(messages),
      messages: messages.map(m => ({
        ...m,
        time: m.time instanceof Date ? m.time.toISOString() : m.time
      })),
      createdAt: new Date().toISOString(),
      lastMessageAt: new Date().toISOString()
    }

    const existingIdx = chatHistory.findIndex(c => c.id === chatEntry.id)
    if (existingIdx >= 0) {
      chatHistory[existingIdx] = chatEntry
    } else {
      chatHistory = [chatEntry, ...chatHistory]
    }
    currentChatId = chatEntry.id
    saveHistory()
  }

  function loadChat(chat) {
    saveCurrentChat()
    messages = chat.messages.map(m => ({
      ...m,
      time: new Date(m.time)
    }))
    currentChatId = chat.id
    showHistoryPanel = false
    input = ''
    loading = false
    if (abortController) {
      abortController.abort()
      abortController = null
    }
  }

  function deleteChat(chatId) {
    chatHistory = chatHistory.filter(c => c.id !== chatId)
    if (currentChatId === chatId) currentChatId = null
    saveHistory()
  }

  function clearAllHistory() {
    chatHistory = []
    currentChatId = null
    saveHistory()
  }

  function formatHistoryDate(isoString) {
    const date = new Date(isoString)
    const now = new Date()
    const diffMs = now - date
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / 86400000)

    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffHours < 24) return `${diffHours}h ago`
    if (diffDays < 7) return `${diffDays}d ago`
    return date.toLocaleDateString([], { month: 'short', day: 'numeric' })
  }

  /* -- Interrupt Presets -- */
  const INTERRUPT_RESPONSES = [
    "Fufu, interrupting the Student Council President mid-sentence? That's rather bold of you.",
    "...I wasn't quite finished. But I suppose I'll reorganize my thoughts. How troublesome.",
    "Patience is a virtue, you know. I was about to reach the important part.",
    "Fufu, cutting me off already? I'll have to make a note of this in today's records.",
    "...That was rather abrupt. I'll let it slide this time — but do try to let me finish next time.",
    "Hmm, I suppose I'll just start over. My memory won't let me forget where I left off, at least.",
    "Interrupting someone with perfect memory is rather pointless, you know. I remember exactly where I was. Fufu.",
  ]

  /* -- Message helpers -- */
  function formatTime(date) {
    return date.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true })
  }

  function shouldShowTime(index) {
    if (index === messages.length - 1) return true
    return messages[index].role !== messages[index + 1].role
  }

  function shouldShowAvatar(index) {
    if (index === messages.length - 1) return true
    return messages[index].role !== messages[index + 1].role
  }

  function shouldShowSeen(index) {
    const msg = messages[index]
    if (msg.role !== 'user') return false
    return index === messages.length - 1
  }

  async function scrollToBottom() {
    await tick()
    bottomEl?.scrollIntoView({ behavior: 'smooth' })
  }

  function clearChat() {
    if (abortController) {
      abortController.abort()
      abortController = null
    }
    saveCurrentChat()
    currentChatId = null
    messages = getRandomPreset()
    input = ''
    loading = false
  }

  function stopGenerating() {
    if (abortController) {
      abortController.abort()
      abortController = null
    }
  }

  async function sendMessage() {
    const content = input.trim()
    if (!content || loading) return

    input = ''

    const userMsg = { id: Date.now(), role: 'user', content, time: new Date(), type: 'text' }
    messages = [...messages, userMsg]
    loading = true
    abortController = new AbortController()
    await scrollToBottom()

    let paragraphCount = 0
    const baseId = Date.now() + 1

    try {
      const history = messages
        .filter(m => m.type === 'text' && m.content)
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
        signal: abortController.signal,
      })

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`)
      }

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let currentParagraph = ''
      let lineBuffer = ''
      const pendingBubbles = []

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        lineBuffer += decoder.decode(value, { stream: true })
        const lines = lineBuffer.split('\n')
        lineBuffer = lines.pop() ?? ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data.trim() === '[DONE]') continue

            try {
              const parsed = JSON.parse(data)
              if (parsed.error) {
                currentParagraph = parsed.error
              } else if (parsed.content) {
                currentParagraph += parsed.content

                const parts = currentParagraph.split(/\n\n+/)
                while (parts.length > 1) {
                  const completedParagraph = parts.shift().trim()
                  if (completedParagraph) {
                    pendingBubbles.push(completedParagraph)
                  }
                  currentParagraph = parts.join('\n\n')
                }
              }
            } catch (e) {
              // Skip invalid JSON
            }
          }
        }
      }

      // Process remaining line buffer
      if (lineBuffer.trim()) {
        const line = lineBuffer.trim()
        if (line.startsWith('data: ')) {
          const data = line.slice(6)
          if (data.trim() !== '[DONE]') {
            try {
              const parsed = JSON.parse(data)
              if (parsed.content) currentParagraph += parsed.content
            } catch (e) { /* skip */ }
          }
        }
      }

      const remaining = currentParagraph.trim()
      if (remaining) {
        pendingBubbles.push(remaining)
      }

      // Display bubbles with natural typing delay
      for (let i = 0; i < pendingBubbles.length; i++) {
        if (i > 0) {
          const delay = 1500 + Math.random() * 1000
          await new Promise(r => setTimeout(r, delay))
        }
        const bubbleId = baseId + paragraphCount++
        messages = [...messages, {
          id: bubbleId,
          role: 'assistant',
          content: pendingBubbles[i],
          time: new Date(),
          type: 'text'
        }]
        await scrollToBottom()
      }

      if (paragraphCount === 0) {
        messages = [...messages, {
          id: baseId,
          role: 'assistant',
          content: "Sorry, I couldn't respond.",
          time: new Date(),
          type: 'text'
        }]
      }
    } catch (err) {
      if (err.name === 'AbortError') {
        const interruptMsg = INTERRUPT_RESPONSES[Math.floor(Math.random() * INTERRUPT_RESPONSES.length)]
        messages = [...messages, {
          id: baseId + paragraphCount,
          role: 'assistant',
          content: interruptMsg,
          time: new Date(),
          type: 'text'
        }]
      } else {
        messages = [...messages, {
          id: baseId + paragraphCount,
          role: 'assistant',
          content: 'Something went wrong. Please try again.',
          time: new Date(),
          type: 'text'
        }]
      }
    } finally {
      loading = false
      abortController = null
      await scrollToBottom()
      saveCurrentChat()
    }
  }

  /* -- Panel toggle helpers -- */
  function toggleCharacter() {
    showCharacterCard = !showCharacterCard
    showProjectCard = false
    showHistoryPanel = false
  }

  function toggleProject() {
    showProjectCard = !showProjectCard
    showCharacterCard = false
    showHistoryPanel = false
  }

  function toggleHistory() {
    showHistoryPanel = !showHistoryPanel
    showCharacterCard = false
    showProjectCard = false
  }

  function closeAllPanels() {
    showCharacterCard = false
    showProjectCard = false
    showHistoryPanel = false
  }
</script>

<!-- Mobile/Tablet overlay backdrop -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div 
  class="mobile-overlay lg:hidden {showCharacterCard || showProjectCard || showHistoryPanel ? 'active' : ''}"
  onclick={closeAllPanels}
  onkeydown={(e) => e.key === 'Escape' && closeAllPanels()}
  role="presentation"
></div>

<div data-theme={isDark ? 'nord-dark' : 'nord'} class="theme-wrapper min-h-screen flex items-center justify-center p-4 md:p-8 gap-4">

  <!-- Character Info Card (Left) -->
  <CharacterCard 
    show={showCharacterCard}
    onClose={() => showCharacterCard = false}
    onOpenLightbox={() => showLightbox = true}
  />

  <!-- Main Chat Card -->
  <div class="chat-card w-full max-w-2xl flex flex-col overflow-hidden" style="height: min(1000px, 90vh); width: clamp(320px, 90vw, 1200px);">

    <!-- Header -->
    <ChatHeader 
      {isDark}
      {showCharacterCard}
      {showProjectCard}
      {showHistoryPanel}
      onToggleTheme={toggleTheme}
      onToggleCharacter={toggleCharacter}
      onToggleProject={toggleProject}
      onToggleHistory={toggleHistory}
      onClearChat={clearChat}
    />

    <!-- Messages -->
    <div class="flex-1 overflow-y-auto px-5 py-5 flex flex-col gap-1.5 bg-white">

      {#each messages as msg, i (msg.id)}
        {#if msg.type === 'text'}
          <ChatMessage 
            {msg}
            showTime={shouldShowTime(i)}
            showAvatar={shouldShowAvatar(i)}
            showSeen={shouldShowSeen(i)}
            {formatTime}
          />
        {:else if msg.type === 'rich'}
          <RichMessage 
            {msg}
            showTime={shouldShowTime(i)}
            showAvatar={shouldShowAvatar(i)}
            {formatTime}
          />
        {/if}
      {/each}

      {#if loading}
        <TypingIndicator />
      {/if}

      <div bind:this={bottomEl}></div>
    </div>

    <!-- Input Area -->
    <ChatInput 
      bind:input
      {loading}
      onSend={sendMessage}
      onStop={stopGenerating}
    />

  </div>

  <!-- Project Info Card (Right) -->
  <ProjectCard 
    show={showProjectCard}
    onClose={() => showProjectCard = false}
  />

  <!-- Chat History Panel -->
  <HistoryPanel 
    show={showHistoryPanel}
    {chatHistory}
    {currentChatId}
    onClose={() => showHistoryPanel = false}
    onLoadChat={loadChat}
    onDeleteChat={deleteChat}
    onClearAll={clearAllHistory}
    {formatHistoryDate}
  />

</div>

<!-- Lightbox Modal -->
<Lightbox 
  show={showLightbox}
  closing={closingLightbox}
  onClose={closeLightbox}
/>
