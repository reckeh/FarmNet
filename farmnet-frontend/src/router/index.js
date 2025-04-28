import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import Profile from '../views/Profile.vue';
import FarmerDashboard from '../views/FarmerDashboard.vue';
import BuyerDashboard from '../views/BuyerDashboard.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import AgriExpertDashboard from '../views/AgriExpertDashboard.vue';
import MarketPrices from '../views/MarketPrices.vue';
import ProductList from '../views/ProductList.vue';
import AskQuestion from '../views/AskQuestion.vue';
import CartView from '../views/Cart.vue';
import CheckoutView from '../views/Checkout.vue';
import Feedback from '../views/Feedback.vue';
import { useUserStore } from '../stores/userStore';

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView, meta: { requiresGuest: true } },
  { path: '/register', name: 'Register', component: RegisterView, meta: { requiresGuest: true } },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: {
      requiresAuth: true
    }
    },
  {
    path: '/farmer-dashboard',
    name: 'FarmerDashboard',
    component: FarmerDashboard,
    meta: { requiresAuth: true, requiredRole: 'FARMER' }
  },
  {
    path: '/buyer-dashboard',
    name: 'BuyerDashboard',
    component: BuyerDashboard,
    meta: { requiresAuth: true, requiredRole: 'BUYER' }
  },
  {
    path: '/cart',
    name: 'Cart',
    component: CartView,
    meta: { requiresAuth: true, requiredRole: 'BUYER' }
  },
  {
    path: '/checkout',
    name: 'Checkout',
    component: CheckoutView,
    meta: { requiresAuth: true, requiredRole: 'BUYER' }
  },  
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, requiredRole: 'ADMIN' }
  },
  {
    path: '/expert-dashboard',
    name: 'AgriExpertDashboard',
    component: AgriExpertDashboard,
    meta: { requiresAuth: true, requiredRole: 'AGRI_EXPERT' }
  },
  {
    path: '/market-prices',
    name: 'MarketPrices',
    component: MarketPrices
  },
  {
    path: '/products',
    name: 'ProductList',
    component: ProductList,
  },
  
  {
    path: '/ask-expert',
    name: 'AskQuestion',
    component: AskQuestion,
    meta: { requiresAuth: true, requiredRole: 'FARMER' }
  },
  {
    path: '/feedback',
    name: 'Feedback',
    component: Feedback,
    meta: { requiresAuth: true, requiredRole: 'FARMER' }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

// ✅ Global navigation guard
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();

  if (!userStore.token && !userStore.user) {
    await userStore.initialize();
  }

  const isLoggedIn = userStore.isAuthenticated;
  const userRole = userStore.user?.role;

  const dashboards = {
    FARMER: 'FarmerDashboard',
    BUYER: 'BuyerDashboard',
    ADMIN: 'AdminDashboard',
    AGRI_EXPERT: 'AgriExpertDashboard'
  };

  if (to.meta.requiresGuest && isLoggedIn) {
    return next({ name: dashboards[userRole] || 'Home' });
  }

  if (to.meta.requiresAuth && !isLoggedIn) {
    return next({ name: 'Login' });
  }

  if (to.meta.requiredRole && to.meta.requiredRole !== userRole) {
    return next({ name: dashboards[userRole] || 'Home' });
  }

  return next();
});

export default router;
