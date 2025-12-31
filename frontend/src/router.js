import { createRouter, createWebHistory } from 'vue-router';

// Layouts
import Layout from './components/Layout.vue';
import BlankLayout from './components/BlankLayout.vue';

// Views (eager loaded)
import Login from './views/Login.vue';
import Dashboard from './views/Dashboard.vue';
import OccurrenceList from './views/OccurrenceList.vue';
import EntryExitList from './views/EntryExitList.vue';
import VisitorList from './views/VisitorList.vue';

const routes = [
  // ============================================
  // EXTERNAL/PUBLIC ROUTES (No Sidebar, No Auth)
  // ============================================
  {
    path: '/externo',
    component: BlankLayout,
    children: [
      {
        path: 'citas',
        name: 'RegistroCita',
        component: () => import('./views/RegistroCita.vue'),
      },
      {
        path: 'turnos',
        name: 'TurnTicket',
        component: () => import('./views/TurnTicket.vue'),
      },
    ],
  },
  // Pantalla de TV para sala de espera (sin layout, pantalla completa)
  {
    path: '/pantalla-turnos',
    name: 'WaitingScreen',
    component: () => import('./views/WaitingScreen.vue'),
  },
  {
    path: '/login',
    component: BlankLayout,
    children: [
      {
        path: '',
        name: 'Login',
        component: Login,
      },
    ],
  },

  // ============================================
  // INTERNAL/ADMIN ROUTES (With Sidebar, Auth Required)
  // ============================================
  {
    path: '/',
    component: Layout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: Dashboard,
      },
      {
        path: 'occurrence/list',
        name: 'OccurrenceList',
        component: OccurrenceList,
      },
      {
        path: 'entry-exit/list',
        name: 'EntryExitList',
        component: EntryExitList,
      },
      {
        path: 'visitor/list',
        name: 'VisitorList',
        component: VisitorList,
      },
      {
        path: 'vehicle/control',
        name: 'VehicleControl',
        component: () => import('./views/VehicleControl.vue'),
      },
      {
        path: 'citas/gestion',
        name: 'GestionCitas',
        component: () => import('./views/GestionCitas.vue'),
      },
      {
        path: 'license/management',
        name: 'LicenseManagement',
        component: () => import('./views/LicenseManagement.vue'),
      },
      {
        path: 'hr/management',
        name: 'HRManagement',
        component: () => import('./views/HRManagement.vue'),
      },
      {
        path: 'turn/management',
        name: 'TurnManagement',
        component: () => import('./views/TurnManagement.vue'),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      };
    }
    return {
      top: 0,
      behavior: 'smooth',
    };
  },
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  // Check if route or any parent route requires auth
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  
  if (requiresAuth && !token) {
    next('/login');
  } else {
    next();
  }
});

export default router;
