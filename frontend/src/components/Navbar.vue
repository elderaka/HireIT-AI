<template>
  <nav class="bg-gradient-to-r from-slate-900 to-neutral-800 border-b border-neutral-700 px-6 py-3 relative z-50 shadow-lg">
    <div class="flex items-center justify-between">
      <!-- Logo -->
      <router-link 
        to="/" 
        class="flex items-center gap-3 group"
      >
        <span class="text-3xl group-hover:scale-110 transition-transform">🎯</span>
        <div class="flex flex-col">
          <span class="text-2xl font-bold text-white group-hover:text-sky-400 transition-colors font-['IBM_Plex_Sans']">
            HireIT
          </span>
          <span class="text-xs text-neutral-400 -mt-1 font-['IBM_Plex_Sans']">
            AI Recruitment Orchestrator
          </span>
        </div>
      </router-link>

      <!-- Status Indicator -->
      <div class="flex items-center gap-2 px-3 py-1 bg-green-500/20 border border-green-500/30 rounded-full">
        <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
        <span class="text-xs text-green-400 font-medium">Active</span>
      </div>
    </div>
  </nav>
</template>

<script setup>
// Navigation component
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,700;0,800;1,400;1,700;1,800&display=swap");

.font-ibm-plex-sans {
  font-family: "IBM Plex Sans", sans-serif;
}
</style>
