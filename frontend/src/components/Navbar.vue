<template>
  <nav class=" px-6 py-3 relative z-50 shadow-lg" style="background-color: #0f62fe;">
    <div class="flex items-center justify-between">
      <!-- Logo -->
      <router-link 
        to="/" 
        class="flex items-center gap-3 group"
      >
        <img src="/layer_2.png" alt="HireIT AI" class="w-10 h-10 group-hover:scale-110 transition-transform" />
        <div class="flex flex-col">
          <span class="text-2xl font-bold text-white group-hover:text-sky-400 transition-colors font-['IBM_Plex_Sans']">
            HireIT AI
          </span>
          <span class="text-xs text-white -mt-1 font-['IBM_Plex_Sans']">
            AI Recruitment Orchestrator
          </span>
        </div>
      </router-link>

      <!-- Right Side -->
      <div class="flex items-center gap-4">
        <!-- Status Indicator -->
        <div class="flex items-center gap-2 px-3 py-1 bg-green-500/20 border border-green-500/30 rounded-full">
          <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
        </div>

        <!-- GitHub Link -->
        <a
          href="https://github.com/elderaka/HireIT-AI"
          target="_blank"
          rel="noopener noreferrer"
          class="text-white hover:text-sky-400 transition-colors"
          title="View on GitHub"
        >
          <svg class="w-10 h-10" fill="white" viewBox="0 0 24 24">
            <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd" />
          </svg>
        </a>
      </div>
    </div>
  </nav>
</template>

<script setup>
// Navigation component
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,700;0,800;1,400;1,700;1,800&display=swap");
</style>

<style scoped>
.font-ibm-plex-sans {
  font-family: "IBM Plex Sans", sans-serif;
}
</style>
