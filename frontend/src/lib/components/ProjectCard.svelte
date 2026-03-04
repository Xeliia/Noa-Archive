<script>
  import { X, Github, ExternalLink } from 'lucide-svelte'

  let {
    show = false,
    onClose,
  } = $props()
</script>

<div class="card-panel-wrapper shrink-0 overflow-hidden transition-all duration-300 ease-out {show ? '' : 'max-lg:pointer-events-none'}" style="width: {show ? '20rem' : '0'}; height: min(600px, 80vh);">
  <div class="project-card w-80 h-full flex flex-col rounded-3xl overflow-hidden" style="opacity: {show ? '1' : '0'}; transform: translateX({show ? '0' : '-100%'});">
    <button 
      class="absolute top-3 right-3 z-10 w-8 h-8 rounded-full bg-white/80 backdrop-blur flex items-center justify-center text-nord-3 hover:text-nord-0 hover:bg-white transition-all shadow-sm cursor-pointer"
      onclick={onClose}
    >
      <X size={16} />
    </button>

    <div class="px-6 pt-8 pb-6">
      <h2 class="text-xl font-semibold text-nord-0 mb-1">About This Project</h2>
      <p class="text-sm text-nord-3">Noa AI Chatbot</p>
    </div>

    <div class="flex-1 overflow-y-auto px-6 pb-6">
      <div class="mb-6">
        <h3 class="text-xs text-nord-3 uppercase tracking-wider font-medium mb-2">Description</h3>
        <p class="text-sm text-nord-0 leading-relaxed">
          A conversational AI chatbot featuring Ushio Noa from Blue Archive. Built with Svelte and powered by your local LLM.
        </p>
      </div>

      <div class="mb-6">
        <h3 class="text-xs text-nord-3 uppercase tracking-wider font-medium mb-2">Tech Stack</h3>
        <div class="flex flex-wrap gap-2">
          <span class="aurora-pill aurora-red">Svelte 5</span>
          <span class="aurora-pill aurora-orange">Tailwind CSS</span>
          <span class="aurora-pill aurora-yellow">DaisyUI</span>
          <span class="aurora-pill aurora-purple">Local LLM</span>
          <span class="aurora-pill aurora-green">FastAPI</span>
          <span class="aurora-pill aurora-red">ngrok</span>
        </div>
      </div>

      <div class="mb-6">
        <h3 class="text-xs text-nord-3 uppercase tracking-wider font-medium mb-2">Future Plans</h3>
        <p class="text-sm text-nord-0 leading-relaxed">
          - Add support for image and audio messages<br>
          - Add support for Cloud LLMs and API-based models (Currently only supports OpenAI and Gemini Models)<br>
        </p>
      </div>

      <div class="mb-6">
        <h3 class="text-xs text-nord-3 uppercase tracking-wider font-medium mb-2">Credits</h3>
        <p class="text-sm text-nord-0 leading-relaxed">
          Character © NEXON Games / Blue Archive
        </p>
      </div>

      <div>
        <h3 class="text-xs text-nord-3 uppercase tracking-wider font-medium mb-3">Links</h3>
        <div class="flex flex-col gap-2">
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

    <div class="px-6 py-4 border-t border-nord-5 bg-nord-6/50">
      <p class="text-xs text-nord-3 text-center">
        Version 1.0.0 • Made with ♥
      </p>
    </div>
  </div>
</div>
