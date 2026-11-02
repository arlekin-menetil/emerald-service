<script setup>
import { useLanguage } from '../../composables/useLanguage'

const { t } = useLanguage()

defineProps({
  advantages: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <section class="services-advantages">
    <div class="services-container">
      <div class="services-section-heading services-section-heading--center">
        <span>{{ t('why.title') }}</span>

        <h2>
          {{ t('why.subtitle') }}
        </h2>

        <p>
          {{ t('why.description') }}
        </p>
      </div>

      <div class="services-advantages-grid">
        <article
          v-for="advantage in advantages"
          :key="advantage.titleKey"
          class="services-advantage-card"
        >
          <div class="services-advantage-card__icon">
            <component
              :is="advantage.icon"
              :size="24"
              :stroke-width="1.9"
            />
          </div>

          <h3>{{ t(advantage.titleKey) }}</h3>
          <p>{{ t(advantage.textKey) }}</p>
        </article>
      </div>
    </div>
  </section>
</template>