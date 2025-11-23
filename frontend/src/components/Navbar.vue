<template>
  <nav class="bg-white border-b border-neutral-300 px-6 py-1 relative z-50">
    <div class="flex items-center justify-between">
      <!-- Logo -->
      <router-link 
        to="/" 
        class="text-2xl font-bold text-slate-900 hover:text-sky-50 transition-colors font-['IBM_Plex_Sans']"
      >
        HireIT
      </router-link>

      <!-- Navigation items can be added here later -->
      <div class="flex items-center gap-6">
        <!-- Placeholder for future nav items -->
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
