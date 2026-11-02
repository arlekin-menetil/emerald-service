<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

import ShopHero from '../components/shop/ShopHero.vue'
import ShopCategories from '../components/shop/ShopCategories.vue'
import ShopProducts from '../components/shop/ShopProducts.vue'
import ShopCta from '../components/shop/ShopCta.vue'
import { useLanguage } from '../composables/useLanguage'
import '../assets/shop.css'

import { API_BASE } from '../config/api'

const route = useRoute()
const router = useRouter()

const { t, currentLanguage } = useLanguage()

const categories = ref([])
const products = ref([])
const loading = ref(true)
const error = ref('')

const selectedCategory = computed(() => route.query.category || '')

const selectedCategoryName = computed(() => {
  if (!selectedCategory.value) return ''

  const category = categories.value.find(
    item => item.slug === selectedCategory.value
  )

  return category?.name || ''
})

const visibleProducts = computed(() => {
  if (selectedCategory.value) {
    return products.value
  }

  return products.value.filter(product => product.is_featured)
})

async function loadShop() {
  loading.value = true
  error.value = ''

  try {
    const category = route.query.category
    const lang = currentLanguage.value

    const categoriesUrl =
      `${API_BASE}/api/shop/categories/?lang=${encodeURIComponent(lang)}`

    const productsUrl = category
      ? `${API_BASE}/api/shop/products/?category=${encodeURIComponent(category)}&lang=${encodeURIComponent(lang)}`
      : `${API_BASE}/api/shop/products/?lang=${encodeURIComponent(lang)}`

    const [categoriesResponse, productsResponse] = await Promise.all([
      axios.get(categoriesUrl),
      axios.get(productsUrl),
    ])

    categories.value = categoriesResponse.data.results || []
    products.value = productsResponse.data.results || []

    if (category) {
      await nextTick()

      document.getElementById('shop-products')?.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      })
    }
  } catch (err) {
    console.error('Shop loading error:', err)
    error.value = t('shop.error')
  } finally {
    loading.value = false
  }
}

function backToCategories() {
  router.push({
    path: '/shop',
  })
}

onMounted(loadShop)

watch(
  () => route.query.category,
  () => {
    loadShop()
  }
)

watch(
  currentLanguage,
  () => {
    loadShop()
  }
)
</script>

<template>
  <main class="shop-page">
    <ShopHero />

    <div
      v-if="loading"
      class="shop-loading"
    >
      {{ t('shop.loading') }}
    </div>

    <div
      v-else-if="error"
      class="shop-error"
    >
      {{ error }}
    </div>

    <template v-else>
      <ShopCategories
        v-if="!selectedCategory"
        :categories="categories"
      />

      <section
        v-else
        class="shop-category-back"
      >
        <button
          type="button"
          class="shop-category-back__button"
          @click="backToCategories"
        >
          ← {{ t('shop.product.back_to_categories') }}
        </button>
      </section>

      <ShopProducts
        :products="visibleProducts"
        :category-name="selectedCategoryName"
      />
    </template>

    <ShopCta />
  </main>
</template>
