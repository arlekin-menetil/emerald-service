<script setup>
import { onMounted, ref, watch } from 'vue'
import axios from 'axios'
import { useLanguage } from '../composables/useLanguage'

import {
  Car,
  Check,
  CircleHelp,
  Faucet,
  Flame,
  MessageCircle,
  Wrench,
  Waves,
  Zap,
} from '@lucide/vue'

import ServicesHero from '../components/services/ServicesHero.vue'
import ServicesCategories from '../components/services/ServicesCategories.vue'
import ServicesMaster from '../components/services/ServicesMaster.vue'
import ServicesAdvantages from '../components/services/ServicesAdvantages.vue'
import ServicesProcess from '../components/services/ServicesProcess.vue'
import ServicesTelegram from '../components/services/ServicesTelegram.vue'
import ServicesCta from '../components/services/ServicesCta.vue'

import '../assets/services.css'

import { API_BASE } from '../config/api'

const API_BASE_URL = API_BASE

const categories = ref([])
const rawServices = ref([])
const master = ref(null)
const loading = ref(true)
const error = ref(null)
const { t, currentLanguage } = useLanguage()

const advantages = [
  {
    titleKey: 'why.fast.title',
    textKey: 'why.fast.description',
    icon: Zap,
  },
  {
    titleKey: 'why.masters.title',
    textKey: 'why.masters.description',
    icon: Wrench,
  },
  {
    titleKey: 'why.guarantee.title',
    textKey: 'why.guarantee.description',
    icon: Check,
  },
  {
    titleKey: 'why.convenient.title',
    textKey: 'why.convenient.description',
    icon: MessageCircle,
  },
]

function getCategoryIcon(categoryName = '') {
  const name = categoryName.toLowerCase()

  if (
    name.includes('ремонт') ||
    name.includes('неисправ') ||
    name.includes('утеч')
  ) {
    return Wrench
  }

  if (
    name.includes('монтаж') ||
    name.includes('сантех')
  ) {
    return Faucet
  }

  if (
    name.includes('канал') ||
    name.includes('засор') ||
    name.includes('слив')
  ) {
    return Waves
  }

  if (
    name.includes('отоп') ||
    name.includes('кот') ||
    name.includes('тепл')
  ) {
    return Flame
  }

  if (
    name.includes('консульт') ||
    name.includes('диагност')
  ) {
    return CircleHelp
  }

  return Wrench
}

function getCategoryDescription(categoryName = '') {
  const name = categoryName.toLowerCase()

  if (name.includes('ремонт') || name.includes('неисправ')) {
    return t('services.category.repair.description')
  }

  if (name.includes('монтаж') || name.includes('сантех')) {
    return t('services.category.installation.description')
  }

  if (name.includes('канал')) {
    return t('services.category.sewerage.description')
  }

  if (name.includes('отоп')) {
    return t('services.category.heating.description')
  }

  if (name.includes('консульт') || name.includes('диагност')) {
    return t('services.category.consultation.description')
  }

  return t('services.catalog.description')
}

function getCategoryShortTitle(categoryName = '') {
  const name = categoryName.toLowerCase()

  if (name.includes('ремонт')) {
    return t('services.category.repair')
  }

  if (name.includes('монтаж')) {
    return t('services.category.installation')
  }

  if (name.includes('канал')) {
    return t('services.category.sewerage')
  }

  if (name.includes('отоп')) {
    return t('services.category.heating')
  }

  if (name.includes('консульт') || name.includes('диагност')) {
    return t('services.category.consultation')
  }

  return categoryName
}

function getCategoryTitle(categoryName = '') {
  const name = categoryName.toLowerCase()

  if (name.includes('ремонт') || name.includes('неисправ')) {
    return t('services.category.repair.title')
  }

  if (name.includes('монтаж') || name.includes('сантех')) {
    return t('services.category.installation.title')
  }

  if (name.includes('канал')) {
    return t('services.category.sewerage.title')
  }

  if (name.includes('отоп')) {
    return t('services.category.heating.title')
  }

  if (name.includes('консульт') || name.includes('диагност')) {
    return t('services.category.consultation.title')
  }

  return categoryName
}

function normalizeService(service) {
  return {
    ...service,

    // ServiceCard сейчас использует price.
    // Значение приходит с backend из price_from.
    price: Number(service.price_from || 0),

    // ServiceCard использует description.
    // Если подробного description нет, используем short_description.
    description:
      service.description?.trim() ||
      service.short_description?.trim() ||
      'Подробности услуги уточняются у специалиста.',

    // Реальная фотография услуги из backend.
    image_url:
      service.image_url ||
      service.image ||
      null,
  }
}

function buildCategories(services) {
  const grouped = new Map()

  services.forEach((rawService) => {
    const service = normalizeService(rawService)

    const categoryName =
      service.category_name?.trim() ||
      'Другие услуги'

    if (!grouped.has(categoryName)) {
      grouped.set(categoryName, [])
    }

    grouped.get(categoryName).push(service)
  })

  return Array.from(grouped.entries()).map(
    ([categoryName, categoryServices]) => ({
      title: getCategoryTitle(categoryName),
      shortTitle: getCategoryShortTitle(categoryName),
      description: getCategoryDescription(categoryName),
      icon: getCategoryIcon(categoryName),
      services: categoryServices.sort(
        (a, b) => (a.sort_order || 0) - (b.sort_order || 0)
      ),
    })
  )
}

async function loadServices() {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/services/`,
      {
        params: {
          lang: currentLanguage.value,
        },
      }
    )

    const services = Array.isArray(response.data)
      ? response.data
      : response.data.results || []

    rawServices.value = services
    categories.value = buildCategories(services)
  } catch (err) {
    console.error(
      'Не удалось загрузить услуги:',
      err
    )

    error.value =
      'Не удалось загрузить список услуг.'
  }
}

async function loadMaster() {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/employees/4/`,
      {
        params: {
          lang: currentLanguage.value,
        },
      }
    )

    master.value = response.data
  } catch (err) {
    console.error(
      'Не удалось загрузить данные мастера:',
      err
    )
  }
}

async function loadPageData() {
  loading.value = true
  error.value = null

  await Promise.all([
    loadServices(),
    loadMaster(),
  ])

  loading.value = false
}

watch(currentLanguage, () => {
  loadServices()
  loadMaster()
})

onMounted(() => {
  loadPageData()
})
</script>

<template>
  <main class="services-page">
    <ServicesHero />

    <section class="services-callout">
      <div class="services-container">
        <div class="services-callout__inner">

          <div class="services-callout__icon">
            <Car :size="26" :stroke-width="1.8" />
          </div>

          <div class="services-callout__content">
            <span class="services-callout__label">
              {{ t('services.visit_terms.label') }}
            </span>

            <h2>
              {{ t('services.visit_terms.title') }}
              <strong>{{ t('services.visit_terms.price') }}</strong>
            </h2>

            <p>
              {{ t('services.visit_terms.description') }}
            </p>
          </div>

        </div>
      </div>
    </section>

    <div
      v-if="loading"
      class="services-container"
    >
      <div class="services-loading">
        Загружаем услуги...
      </div>
    </div>

    <div
      v-else-if="error"
      class="services-container"
    >
      <div class="services-error">
        {{ error }}
      </div>
    </div>

<ServicesCategories
      v-else
      :categories="categories"
    />

    <ServicesMaster
      :master="master"
    />

    <ServicesAdvantages
      :advantages="advantages"
    />

    <ServicesProcess />

    <ServicesTelegram />

    
    <!-- УСЛОВИЯ ВЫЕЗДА МАСТЕРА -->

<ServicesCta />
  </main>
</template>
