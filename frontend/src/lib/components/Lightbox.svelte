<script>
  import { X } from 'lucide-svelte'

  let {
    show = false,
    closing = false,
    onClose,
  } = $props()

  /* ── 3D Tilt effect ── */
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
</script>

{#if show}
  <div 
    class="{closing ? 'lightbox-overlay-closing' : 'lightbox-overlay'} fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-8"
    onclick={onClose}
    onkeydown={(e) => e.key === 'Escape' && onClose()}
    role="button"
    tabindex="0"
  >
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div 
      class="{closing ? 'lightbox-card-closing' : 'lightbox-card'}"
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
          src="/src/lib/assets/cover-photo.jpg" 
          alt="Noa Cover" 
          class="w-auto h-auto max-w-full max-h-[80vh] object-contain"
        />
      </div>
    </div>
    
    <!-- Close button -->
    <button 
      class="absolute top-6 right-6 w-10 h-10 rounded-full bg-white/20 backdrop-blur flex items-center justify-center text-white hover:bg-white/30 transition-all"
      onclick={onClose}
    >
      <X size={20} />
    </button>
  </div>
{/if}
