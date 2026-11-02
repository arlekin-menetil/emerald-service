<script setup>
import { ArrowRight } from '@lucide/vue'
import { useLanguage } from '../../composables/useLanguage'

const { t } = useLanguage()
</script>

<template>
  <section class="services-cta">
    <div class="services-container">
      <div class="services-cta__inner">
        <div>
          <span>{{ t('cta.eyebrow') }}</span>

          <h2>{{ t('cta.title') }}</h2>

          <p>
            {{ t('cta.description') }}
          </p>
        </div>

        <RouterLink
          to="/request"
          class="services-button services-button--white"
        >
          {{ t('cta.button') }}
          <ArrowRight :size="18" />
        </RouterLink>
      </div>
    </div>
  </section>
</template>
