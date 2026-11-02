<script setup>
import { useLanguage } from '../../composables/useLanguage'

const { t } = useLanguage()
</script>

<template>
  <section class="shop-cta">
    <div>
      <span>{{ t('shop.cta.eyebrow') }}</span>
      <h2>
        {{ t('shop.cta.title') }}
        <strong>{{ t('shop.cta.title_accent') }}</strong>
      </h2>
      <p>{{ t('shop.cta.description') }}</p>
    </div>

    <RouterLink to="/request">
      {{ t('shop.cta.button') }}
    </RouterLink>
  </section>
</template>
