<template>
  <div
    class="min-h-screen w-full relative overflow-hidden inline-flex flex-col justify-center align-center items-left gap-3 px-6 md:gap-6 md:px-20 font-['IBM_Plex_Sans']"
    style="background: linear-gradient(180deg, #0f62fe 0%, #001141 100%)"
  >
    <img src="../assets/radix-icons_people.png" alt="Decorative" class="absolute right-0 top-1/2 transform -translate-y-1/2 opacity-80 pointer-events-none md:block animate-slide-in-right" />
    <div class="flex flex-col justify-end items-start gap-3 animate-fade-in-up">
      <b
        class="justify-start text-White text-3xl md:text-4xl font-bold"
      >
        HireIT
      </b>
      <b
        class="justify-start text-White text-3xl md:text-6xl font-bold"
      >
        Your AI Recruitment Orchestrator
      </b>
      <i
        class="justify-start text-White text-lg md:text-3xl font-bold italic "
      >
        One intelligent agent that coordinates your entire hiring workflow.
      </i>
    </div>
    <router-link
      to="/chat"
      class="px-6 py-4 bg-sky-50/20 rounded-2xl inline-flex justify-center items-center gap-2.5 hover:bg-sky-50/30 transition-colors w-fit animate-fade-in-up animation-delay-300"
    >
      <div
        class="justify-start text-white text-xl md:text-2xl font-bold font-['IBM_Plex_Sans']"
      >
        Get Started
      </div>
      <img class="w-10 h-10 relative max-h-full" alt="Arrow Icon" src="../assets/mi_arrow-left.png" />
    </router-link>
    
  </div>
</template>

<script setup>
</script>

<style scoped>
/* Animation keyframes */
@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100px) ;
  }
  to {
    opacity: 0.8;
    transform: translateX(0) ;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-in-right {
  animation: slideInRight 1.2s ease-out forwards;
}

.animate-fade-in-up {
  opacity: 0;
  animation: fadeInUp 1s ease-out forwards;
}

.animation-delay-300 {
  animation-delay: 0.3s;
}

@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,700;0,800;1,400;1,700;1,800&display=swap");

.font-ibm-plex-sans {
  font-family: "IBM Plex Sans", sans-serif;
}
</style>
