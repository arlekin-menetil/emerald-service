import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
  path: '/contacts',
  component: () => import('../views/ContactsView.vue'),
},
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
  },

  {
    path: '/services',
    name: 'services',
    component: () => import('../views/ServicesView.vue'),
  },

  {
    path: '/shop',
    name: 'shop',
    component: () => import('../views/ShopView.vue'),
  },

  {
    path: '/shop/product/:id',
    name: 'shop-product',
    component: () => import('../views/ShopProductView.vue'),
  },

  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue'),
  },

  {
    path: '/ratings',
    name: 'ratings',
    component: () => import('../views/RatingsView.vue'),
  },

  {
    path: '/telegram-bot',
    component: () => import('../views/TelegramBotView.vue'),
  },
  {
    path: '/request',
    name: 'request',
    component: () => import('../views/RequestView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,

  scrollBehavior() {
    return {
      top: 0,
    }
  },
})

export default router