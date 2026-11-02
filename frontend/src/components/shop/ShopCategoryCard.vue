<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useLanguage } from '../../composables/useLanguage'

const API_BASE = 'http://127.0.0.1:8002'
const router = useRouter()
const { t } = useLanguage()

const props = defineProps({
  category: {
    type: Object,
    required: true,
  },
})

const imageUrl = computed(() => {
  if (!props.category.image) return ''
  if (props.category.image.startsWith('http')) return props.category.image
  return `${API_BASE}${props.category.image}`
})

function openCategory() {
  router.push({
    path: '/shop',
    query: { category: props.category.slug },
  })
}
</script>

<template>
  <article
    class="shop-category-card"
    role="button"
    tabindex="0"
    @click="openCategory"
    @keydown.enter="openCategory"
    @keydown.space.prevent="openCategory"
  >
    <div class="shop-category-card__number">
      {{ String(category.sort_order).padStart(2, '0') }}
    </div>

    <div class="shop-category-card__image">
      <img v-if="category.image" :src="imageUrl" :alt="category.name" />
      <div v-else class="shop-category-card__image-placeholder"></div>
    </div>

    <div class="shop-category-card__content">
      <h3>{{ category.name }}</h3>
      <p v-if="category.description">{{ category.description }}</p>
      <span class="shop-category-card__link">
        {{ t('shop.categories.view_products') }}
        <strong>→</strong>
      </span>
    </div>
  </article>
</template>
