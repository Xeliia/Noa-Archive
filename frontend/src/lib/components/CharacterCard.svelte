<script>
  import { X, Cake } from 'lucide-svelte'

  let {
    show = false,
    onClose,
    onOpenLightbox,
  } = $props()

  let profileFlipped = $state(false)

  // 3D tilt
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

<div class="card-panel-wrapper shrink-0 overflow-hidden transition-all duration-300 ease-out {show ? '' : 'max-lg:pointer-events-none'}" style="width: {show ? '24rem' : '0'}; height: min(700px, 85vh);">
  <div class="character-card w-96 h-full flex flex-col rounded-3xl overflow-hidden" style="opacity: {show ? '1' : '0'}; transform: translateX({show ? '0' : '100%'});">
    <button 
      class="absolute top-3 right-3 z-10 w-8 h-8 rounded-full bg-white/80 backdrop-blur flex items-center justify-center text-nord-3 hover:text-nord-0 hover:bg-white transition-all shadow-sm cursor-pointer"
      onclick={onClose}
    >
      <X size={16} />
    </button>

    <div class="flex flex-col items-center pt-8 pb-6 px-6">
      <div class="relative mb-4">
        <button 
          class="profile-image-wrapper w-32 h-32 rounded-full bg-gradient-to-br from-nord-8/30 to-nord-9/30 p-1 cursor-pointer"
          class:flipped={profileFlipped}
          onclick={() => profileFlipped = !profileFlipped}
        >
          <div class="flipper w-full h-full">
            <img src="/src/lib/assets/mini-profile.png" alt="Ushio Noa - Front" class="profile-face profile-front" />
            <img src="/src/lib/assets/mini-profile2.png" alt="Ushio Noa - Back" class="profile-face profile-back" />
          </div>
        </button>
      </div>

      <h2 class="text-xl font-semibold text-nord-0 mb-1">Ushio Noa</h2>
      <p class="text-sm text-nord-3 italic mb-4">The Melancholy of Kivotos</p>

      <div class="aurora-pill aurora-purple inline-flex items-center gap-2">
        <Cake size={16} />
        <span class="text-sm font-medium">April 13th</span>
      </div>
    </div>

    <div class="mx-6 border-t border-nord-5"></div>

    <div class="flex-1 p-6 flex flex-col min-h-0">
      <p class="text-xs text-nord-3 uppercase tracking-wider font-medium mb-3 text-center">
        Cover Photo
      </p>

      <button 
        class="tilt-card flex-1 w-full rounded-2xl overflow-hidden shadow-lg cursor-pointer min-h-0"
        onclick={onOpenLightbox}
        onmousemove={handleTiltMove}
        onmouseleave={handleTiltLeave}
      >
        <img 
          src="/src/lib/assets/cover-photo.jpg" 
          alt="Noa Cover" 
          class="w-full h-full object-cover" 
        />
      </button>
    </div>
  </div>
</div>
