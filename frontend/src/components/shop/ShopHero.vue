<script setup>
import { ShoppingBag, ArrowDown } from '@lucide/vue'
import { useLanguage } from '../../composables/useLanguage'

const { t } = useLanguage()
</script>

<template>
  <section class="shop-hero">
    <div class="shop-hero__pattern"></div>
    <div class="shop-hero__content">
      <div class="shop-hero__eyebrow">
        <ShoppingBag :size="16" />
        <span>{{ t('shop.hero.eyebrow') }}</span>
      </div>
      <h1>
        {{ t('shop.hero.title') }}<br />
        {{ t('shop.hero.title_accent') }}
      </h1>
      <p>{{ t('shop.hero.description') }}</p>
      <div class="shop-hero__actions">
        <a href="#shop-categories" class="shop-hero__button">
          {{ t('shop.hero.catalog') }}
          <ArrowDown :size="17" />
        </a>
        <RouterLink to="/request" class="shop-hero__link">
          {{ t('shop.hero.master_help') }}
        </RouterLink>
      </div>
    </div>
    <div class="shop-hero__badge">
      <ShoppingBag :size="25" />
      <span>{{ t('shop.hero.badge') }}</span>
    </div>
  </section>
</template>
