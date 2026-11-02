<script setup>
import ShopCategoryCard from './ShopCategoryCard.vue'
import { useLanguage } from '../../composables/useLanguage'

defineProps({
  categories: {
    type: Array,
    default: () => [],
  },
})

const { t } = useLanguage()
</script>

<template>
  <section id="shop-categories" class="shop-categories">
    <div class="shop-section-heading">
      <div>
        <span>{{ t('shop.categories.eyebrow') }}</span>
        <h2>{{ t('shop.categories.title') }}</h2>
      </div>
      <p>{{ t('shop.categories.description') }}</p>
    </div>

    <div class="shop-categories__grid">
      <ShopCategoryCard
        v-for="category in categories"
        :key="category.id"
        :category="category"
      />
    </div>
  </section>
</template>
