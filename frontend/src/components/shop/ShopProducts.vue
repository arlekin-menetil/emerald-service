<script setup>
import { useRouter } from 'vue-router'
import { useLanguage } from '../../composables/useLanguage'

const router = useRouter()

defineProps({
  products: {
    type: Array,
    default: () => [],
  },
  categoryName: {
    type: String,
    default: '',
  },
})

const { t } = useLanguage()

function openProduct(product) {
  router.push({
    path: `/shop/product/${product.id}`,
    query: {
      category: product.category_slug || '',
    },
  })
}
</script>

<template>
  <section id="shop-products" class="shop-products">
    <div class="shop-section-heading">
      <div>
        <span>{{ t('shop.products.eyebrow') }}</span>
        <h2>{{ categoryName || t('shop.products.title') }}</h2>
      </div>
    </div>

    <div v-if="products.length" class="shop-products__grid">
      <article
        v-for="product in products"
        :key="product.id"
        class="shop-product-card"
        role="button"
        tabindex="0"
        @click="openProduct(product)"
        @keydown.enter="openProduct(product)"
        @keydown.space.prevent="openProduct(product)"
      >
        <img
          v-if="product.image"
          :src="product.image"
          :alt="product.name"
        />

        <div class="shop-product-card__body">
          <span>{{ product.category_name }}</span>
          <h3>{{ product.name }}</h3>

          <strong>
            {{ new Intl.NumberFormat('ru-RU').format(product.price) }}
            {{ t('shop.product.currency') }}
          </strong>

        </div>
      </article>
    </div>

    <div v-else class="shop-products__empty">
      <h3>{{ t('shop.products.empty.title') }}</h3>
      <p>{{ t('shop.products.empty.description') }}</p>
    </div>
  </section>
</template>
