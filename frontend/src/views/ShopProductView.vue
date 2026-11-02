<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

import { useLanguage } from '../composables/useLanguage'
import '../assets/shop.css'

const API_BASE = 'http://127.0.0.1:8002'

const route = useRoute()
const router = useRouter()
const { t, currentLanguage } = useLanguage()

const product = ref(null)
const loading = ref(true)
const error = ref('')
const selectedImage = ref('')

const productId = computed(() => route.params.id)

const imageUrl = computed(() => {
  if (!product.value?.image) return ''

  if (product.value.image.startsWith('http')) {
    return product.value.image
  }

  return `${API_BASE}${product.value.image}`
})

const galleryImages = computed(() => {
  if (!product.value) return []

  const images = []

  if (product.value.image) {
    images.push({
      id: 'main',
      url: imageUrl.value,
    })
  }

  if (Array.isArray(product.value.gallery)) {
    product.value.gallery
      .slice(0, 4)
      .forEach(item => {
        if (!item?.image) return

        const url = item.image.startsWith('http')
          ? item.image
          : `${API_BASE}${item.image}`

        images.push({
          id: item.id,
          url,
        })
      })
  }

  return images
})

function selectImage(url) {
  selectedImage.value = url
}

watch(
  () => product.value,
  value => {
    selectedImage.value = value?.image
      ? (
          value.image.startsWith('http')
            ? value.image
            : `${API_BASE}${value.image}`
        )
      : ''
  },
  { immediate: true }
)

const formattedPrice = computed(() => {
  if (!product.value) return ''

  return new Intl.NumberFormat('ru-RU').format(product.value.price)
})

const isInStock = computed(() => {
  return Boolean(
    product.value?.is_available &&
    Number(product.value?.stock_quantity) > 0
  )
})

async function loadProduct() {
  loading.value = true
  error.value = ''
  product.value = null

  try {
    const lang = currentLanguage.value
    const category = route.query.category

    const productsUrl = category
      ? `${API_BASE}/api/shop/products/?category=${encodeURIComponent(category)}&lang=${encodeURIComponent(lang)}`
      : `${API_BASE}/api/shop/products/?lang=${encodeURIComponent(lang)}`

    const response = await axios.get(productsUrl)

    const products = response.data.results || []

    product.value = products.find(
      item => String(item.id) === String(productId.value)
    )

    if (!product.value) {
      throw new Error('Product not found')
    }
  } catch (err) {
    console.error('Product loading error:', err)
    error.value = t('shop.error')
  } finally {
    loading.value = false
  }
}

function backToCategory() {
  const categorySlug =
    route.query.category ||
    product.value?.category_slug ||
    ''

  if (categorySlug) {
    router.push({
      path: '/shop',
      query: {
        category: categorySlug,
      },
    })
    return
  }

  router.push('/shop')
}

onMounted(loadProduct)

watch(
  () => route.params.id,
  () => {
    loadProduct()
  }
)

watch(
  currentLanguage,
  () => {
    loadProduct()
  }
)
</script>

<template>
  <main class="shop-product-page">
    <div
      v-if="loading"
      class="shop-product-page__loading"
    >
      {{ t('shop.loading') }}
    </div>

    <div
      v-else-if="error || !product"
      class="shop-product-page__error"
    >
      <p>{{ error || t('shop.error') }}</p>

      <button
        type="button"
        class="shop-product-page__back"
        @click="backToCategory"
      >
        ← {{ t('shop.product.back_to_catalog') }}
      </button>
    </div>

    <template v-else>
      <div class="shop-product-page__container">

        <button
          type="button"
          class="shop-product-page__back"
          @click="backToCategory"
        >
          ← {{ t('shop.product.back_to_categories') }}
        </button>

        <section class="shop-product-detail">

          <div class="shop-product-detail__visual">
            <div
              v-if="product.is_featured"
              class="shop-product-detail__popular"
            >
              {{ t('shop.product.popular') }}
            </div>

            <div class="shop-product-detail__gallery">

              <div class="shop-product-detail__image">
                <img
                  v-if="selectedImage"
                  :src="selectedImage"
                  :alt="product.name"
                />

                <div
                  v-else
                  class="shop-product-detail__placeholder"
                >
                  EMERALD SERVICE
                </div>
              </div>

              <div
                v-if="galleryImages.length > 1"
                class="shop-product-detail__thumbnails"
              >
                <button
                  v-for="image in galleryImages"
                  :key="image.id"
                  type="button"
                  class="shop-product-detail__thumbnail"
                  :class="{
                    'is-active': selectedImage === image.url
                  }"
                  @click="selectImage(image.url)"
                >
                  <img
                    :src="image.url"
                    :alt="product.name"
                  />
                </button>
              </div>

            </div>
          </div>

          <div class="shop-product-detail__info">

            <span class="shop-product-detail__category">
              {{ product.category_name }}
            </span>

            <h1>
              {{ product.name }}
            </h1>

            <div class="shop-product-detail__price">
              {{ formattedPrice }}
              <span>{{ t('shop.product.currency') }}</span>
            </div>

            <div class="shop-product-detail__availability">
              <span
                class="shop-product-detail__status"
                :class="{
                  'is-available': isInStock,
                  'is-unavailable': !isInStock
                }"
              >
                <i></i>

                {{
                  isInStock
                    ? t('shop.product.in_stock')
                    : t('shop.product.out_of_stock')
                }}
              </span>

              <span v-if="isInStock">
                {{ product.stock_quantity }} {{ t('shop.product.units') }}
              </span>
            </div>

            <div class="shop-product-detail__divider"></div>

            <div
              v-if="product.description"
              class="shop-product-detail__description"
            >
              <h2>{{ t('shop.product.description') }}</h2>

              <p>
                {{ product.description }}
              </p>
            </div>

            <div class="shop-product-detail__meta">

              <div>
                <span>{{ t('shop.product.sku') }}</span>
                <strong>{{ product.sku }}</strong>
              </div>

              <div>
                <span>{{ t('shop.product.category') }}</span>
                <strong>{{ product.category_name }}</strong>
              </div>

            </div>

            <button
              type="button"
              class="shop-product-detail__request"
              @click="backToCategory"
            >
              {{ t('shop.product.back_to_catalog') }}
              <strong>→</strong>
            </button>

          </div>

        </section>

      </div>
    </template>
  </main>
</template>
