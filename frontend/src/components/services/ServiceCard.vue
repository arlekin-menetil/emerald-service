<script setup>
import { ArrowRight } from '@lucide/vue'
import { useLanguage } from '../../composables/useLanguage'

defineProps({
  service: {
    type: Object,
    required: true,
  },

  categoryIcon: {
    type: [Object, Function],
    required: true,
  },

  number: {
    type: String,
    default: '01',
  },
})

const { t } = useLanguage()

function formatPrice(price) {
  if (price === 0) {
    return t('services.card.free')
  }

  return `${t('services.card.from')} ${new Intl.NumberFormat('ru-RU').format(price)} ${t('services.card.currency')}`
}

function getServiceImage(service) {
  return service.image_url || service.image || null
}
</script>

<template>
  <article class="service-card">

    <!-- =====================================================
         ИЗОБРАЖЕНИЕ УСЛУГИ
    ====================================================== -->

    <div class="service-card__image">

      <img
        v-if="getServiceImage(service)"
        :src="getServiceImage(service)"
        :alt="service.name"
        loading="lazy"
      />

      <!-- Заглушка, если картинки пока нет -->

      <div
        v-else
        class="service-card__image-placeholder"
      >
        <component
          :is="categoryIcon"
          :size="34"
          :stroke-width="1.6"
        />
      </div>

      <!-- Номер -->

      <span class="service-card__number">
        {{ number }}
      </span>

    </div>

    <!-- =====================================================
         ВЕРХ КАРТОЧКИ
    ====================================================== -->

    <div class="service-card__top">

      <div class="service-card__icon">
        <component
          :is="categoryIcon"
          :size="21"
          :stroke-width="1.8"
        />
      </div>

    </div>

    <!-- =====================================================
         НАЗВАНИЕ
    ====================================================== -->

    <h4>
      {{ service.name }}
    </h4>

    <!-- =====================================================
         ОПИСАНИЕ
    ====================================================== -->

    <p>
      {{ service.description }}
    </p>

    <!-- =====================================================
         НИЖНЯЯ ЧАСТЬ
    ====================================================== -->

    <div class="service-card__bottom">

      <div>
        <span>
          {{ t('services.card.price_label') }}
        </span>

        <strong>
          {{ formatPrice(service.price) }}
        </strong>
      </div>

      <!-- Переход к заявке -->

      <RouterLink
        :to="{
          path: '/request',
          query: {
            service: service.name,
            service_id: String(service.id),
          },
        }"
        class="service-card__link"
        :aria-label="`${t('services.card.call')}: ${service.name}`"
      >
        <ArrowRight :size="18" />
      </RouterLink>

    </div>

  </article>
</template>