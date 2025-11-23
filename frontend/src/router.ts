import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from './pages/LandingPage.vue';
import ChatPage from './pages/ChatPage.vue';

const routes = [
  { path: '/', component: LandingPage },
  { path: '/chat', component: ChatPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
