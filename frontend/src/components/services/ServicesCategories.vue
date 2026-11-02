<script setup>
import ServiceCard from './ServiceCard.vue'
import { useLanguage } from '../../composables/useLanguage'

const { t } = useLanguage()

defineProps({
  categories: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <section id="all-services" class="services-catalog">
    <div class="services-container">

      <div class="services-section-heading">
        <span>{{ t('services.catalog.eyebrow') }}</span>

        <h2>
          {{ t('services.catalog.title_prefix') }}
          <strong>{{ t('services.catalog.title_suffix') }}</strong>
        </h2>

        <p>
          {{ t('services.catalog.description') }}
        </p>
      </div>

      <nav
        class="services-category-nav"
        :aria-label="t('services.catalog.aria_label')"
      >
        <a
          v-for="category in categories"
          :key="category.title"
          :href="`#${category.shortTitle}`"
        >
          <component
            :is="category.icon"
            :size="16"
          />

          {{ category.shortTitle }}
        </a>
      </nav>

      <section
        v-for="category in categories"
        :id="category.shortTitle"
        :key="category.title"
        class="service-group"
      >
        <div class="service-group__heading">

          <div class="service-group__title">
            <div class="service-group__icon">
              <component
                :is="category.icon"
                :size="25"
                :stroke-width="1.8"
              />
            </div>

            <div>
              <span>{{ t('services.catalog.category_label') }}</span>
              <h3>{{ category.title }}</h3>
            </div>
          </div>

          <p>
            {{ category.description }}
          </p>

        </div>

        <div class="service-grid">
          <ServiceCard
            v-for="(service, index) in category.services"
            :key="service.id || service.name"
            :service="service"
            :category-icon="category.icon"
            :number="String(index + 1).padStart(2, '0')"
          />
        </div>

      </section>

    </div>
  </section>
</template>
