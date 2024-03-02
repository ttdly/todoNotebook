import { createRouter, createWebHistory } from 'vue-router';
import DashBordVue from '@/views/DashBord.vue';
import ClaVue from '@/components/MyCalendar.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashbord',
      component: DashBordVue,
    },
    {
      path: '/a',
      name:'aa',
      component: ClaVue
    }
  ],
});

export default router;
