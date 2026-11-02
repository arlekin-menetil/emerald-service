<script setup>

const { currentLanguage, t, loadTranslations } = useLanguage()

import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useLanguage } from '../composables/useLanguage'

import {
  ArrowLeft,
  CheckCircle2,
  ChevronDown,
  Clock3,
  MapPin,
  Phone,
  Send,
  User,
  Wrench,
} from '@lucide/vue'

const route = useRoute()
const router = useRouter()

import { API_BASE } from '../config/api'

const API_BASE_URL = API_BASE

const services = ref([])
const loadingServices = ref(true)
const submitting = ref(false)
const success = ref(false)
const error = ref('')

const geocoding = ref(false)
const geocodeError = ref('')
const foundAddress = ref('')
const geocodedAddress = ref('')
const latitude = ref(null)
const longitude = ref(null)

const form = ref({
  name: '',
  phone: '',
  address: '',
  service_id: '',
  date: '',
  time: '',
  comment: '',
})

/*
|--------------------------------------------------------------------------
| Выбранная услуга
|--------------------------------------------------------------------------
*/

const selectedService = computed(() => {
  return services.value.find(
    (service) =>
      String(service.id) === String(form.value.service_id)
  )
})

/*
|--------------------------------------------------------------------------
| Минимальная дата
|--------------------------------------------------------------------------
*/

const minDate = computed(() => {
  const now = new Date()

  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
})

/*
|--------------------------------------------------------------------------
| Формат цены
|--------------------------------------------------------------------------
*/

function formatPrice(price) {
  const value = Number(price || 0)

  if (value === 0) {
    return t('request.price.free')
  }

  const formatted = new Intl.NumberFormat(
    currentLanguage.value === 'ru'
      ? 'ru-RU'
      : currentLanguage.value === 'uz'
        ? 'uz-UZ'
        : currentLanguage.value === 'zh'
          ? 'zh-CN'
          : 'en-US'
  ).format(value)

  return `${t('request.price.from')} ${formatted} ${t('request.price.currency')}`
}

/*
|--------------------------------------------------------------------------
| Получение изображения услуги
|--------------------------------------------------------------------------
*/

function getServiceImage(service) {
  if (!service) {
    return null
  }

  return service.image_url || service.image || null
}

/*
|--------------------------------------------------------------------------
| Загрузка услуг
|--------------------------------------------------------------------------
*/

async function loadServices() {
  try {
    loadingServices.value = true
    error.value = ''

    const response = await axios.get(
      `${API_BASE_URL}/api/services/?lang=${encodeURIComponent(currentLanguage.value)}`
    )

    services.value = Array.isArray(response.data)
      ? response.data
      : response.data.results || []

    /*
     * Если пользователь пришёл с карточки услуги:
     *
     * /request?service=Установка сифона&service_id=14
     *
     * автоматически выбираем услугу по ID.
     */
    const serviceId = route.query.service_id

    if (serviceId) {
      const exists = services.value.some(
        (service) =>
          String(service.id) === String(serviceId)
      )

      if (exists) {
        form.value.service_id = String(serviceId)
      }
    }
  } catch (err) {
    console.error(
      'Не удалось загрузить услуги:',
      err
    )

    error.value =
      'Не удалось загрузить список услуг.'
  } finally {
    loadingServices.value = false
  }
}

/*
|--------------------------------------------------------------------------
| Нормализация телефона
|--------------------------------------------------------------------------
*/

function normalizePhone(phone) {
  return phone
    .replace(/\s+/g, '')
    .replace(/[()-]/g, '')
}


function resetGeocode() {
  latitude.value = null
  longitude.value = null
  foundAddress.value = ''
  geocodeError.value = ''
  geocodedAddress.value = ''
}

async function geocodeAddress() {
  const address = form.value.address.trim()

  if (address.length < 5) {
    resetGeocode()
    return false
  }

  if (
    geocodedAddress.value === address &&
    latitude.value !== null &&
    longitude.value !== null
  ) {
    return true
  }

  try {
    geocoding.value = true
    geocodeError.value = ''

    const response = await axios.post(
      `${API_BASE_URL}/api/service-requests/geocode/`,
      { address }
    )

    latitude.value = Number(response.data.latitude)
    longitude.value = Number(response.data.longitude)
    foundAddress.value = response.data.found_address || ''
    geocodedAddress.value = address

    return true
  } catch (err) {
    console.error('Ошибка геокодирования адреса:', err)

    latitude.value = null
    longitude.value = null
    foundAddress.value = ''
    geocodedAddress.value = ''

    if (err.response?.data?.detail) {
      geocodeError.value = err.response.data.detail
    } else {
      geocodeError.value = t('request.error.geocode')
    }

    return false
  } finally {
    geocoding.value = false
  }
}

/*
|--------------------------------------------------------------------------
| Проверка формы
|--------------------------------------------------------------------------
*/

function validateForm() {
  error.value = ''

  if (form.value.name.trim().length < 2) {
    error.value = t('request.error.name')
    return false
  }

  const phone = normalizePhone(
    form.value.phone
  )

  if (!/^\+998\d{9}$/.test(phone)) {
    error.value =
      t('request.error.phone_format')
    return false
  }

  if (form.value.address.trim().length < 5) {
    error.value = t('request.error.address')
    return false
  }

  if (!form.value.service_id) {
    error.value = t('request.error.service')
    return false
  }

  if (!form.value.date) {
    error.value = t('request.error.date')
    return false
  }

  if (!form.value.time) {
    error.value = t('request.error.time')
    return false
  }

  const selectedHour = Number(form.value.time.split(':')[0])

  if (selectedHour > 17) {
    error.value = t('request.error.time_limit')
    return false
  }

  const selectedDateTime = new Date(
    `${form.value.date}T${form.value.time}:00`
  )

  if (Number.isNaN(selectedDateTime.getTime())) {
    error.value =
      t('request.error.datetime_invalid')
    return false
  }

  if (selectedDateTime <= new Date()) {
    error.value =
      t('request.error.future_time')
    return false
  }

  return true
}

/*
|--------------------------------------------------------------------------
| Отправка заявки
|--------------------------------------------------------------------------
*/

async function submitRequest() {
  if (!validateForm()) {
    return
  }

  const geocoded = await geocodeAddress()

  if (!geocoded) {
    error.value =
      geocodeError.value || t('request.error.geocode')
    return
  }

  try {
    submitting.value = true
    error.value = ''

    const scheduledAt = new Date(
      `${form.value.date}T${form.value.time}:00`
    ).toISOString()

    const payload = {
      name: form.value.name.trim(),

      phone: normalizePhone(
        form.value.phone
      ),

      address: form.value.address.trim(),

      latitude: latitude.value,
      longitude: longitude.value,

      service: Number(
        form.value.service_id
      ),

      scheduled_at: scheduledAt,

      comment: form.value.comment.trim(),

      language: currentLanguage.value,
    }

    console.log(
      'Отправляем заявку:',
      payload
    )

    await axios.post(
      `${API_BASE_URL}/api/service-requests/`,
      payload
    )

    success.value = true
  } catch (err) {
    console.error(
      'Ошибка создания заявки:',
      err
    )

    if (err.response?.data) {
      const data = err.response.data

      if (typeof data === 'string') {
        error.value = data
      } else if (data.detail) {
        error.value = data.detail
      } else {
        const firstError =
          Object.values(data)[0]

        if (Array.isArray(firstError)) {
          error.value = firstError[0]
        } else if (
          typeof firstError === 'string'
        ) {
          error.value = firstError
        } else {
          error.value =
            t('request.error.submit_failed')
        }
      }
    } else {
      error.value =
        t('request.error.connection_failed')
    }
  } finally {
    submitting.value = false
  }
}

/*
|--------------------------------------------------------------------------
| Навигация
|--------------------------------------------------------------------------
*/

function goBack() {
  router.back()
}

function goHome() {
  router.push('/')
}

/*
|--------------------------------------------------------------------------
| Загрузка
|--------------------------------------------------------------------------
*/

onMounted(async () => {
  await loadTranslations(currentLanguage.value)
  await loadServices()
})

watch(currentLanguage, async () => {
  await loadTranslations(currentLanguage.value)
  await loadServices()
})
</script>

<template>
  <main class="request-page">
    <div class="request-container">

      <!-- =========================================================
           HEADER
      ========================================================== -->

      <section class="request-header">

        <button
          type="button"
          class="request-back"
          @click="goBack"
        >
          <ArrowLeft :size="18" />

          <span>
            {{ t('request.back') }}
          </span>
        </button>

        <div class="request-header__badge">
          <Wrench :size="16" />

          {{ t('request.hero.eyebrow') }}
        </div>

        <h1>
          {{ t('request.submit') }}
        </h1>

        <p>
          {{ t('request.hero.description') }}
         
        </p>
      </section>

      <!-- =========================================================
           SUCCESS
      ========================================================== -->

      <section
        v-if="success"
        class="request-success"
      >
        <div class="request-success__icon">
          <CheckCircle2 :size="42" />
        </div>

        <h2>
          {{ t('request.success.title') }}
        </h2>

        <p>
          {{ t('request.success.text') }}
          {{ t('request.success.contact') }}
        </p>

        <button
          type="button"
          class="request-success__button"
          @click="goHome"
        >
          {{ t('request.success.home') }}
        </button>
      </section>

      <!-- =========================================================
           FORM
      ========================================================== -->

      <section
        v-else
        class="request-card"
      >

        <form
          @submit.prevent="submitRequest"
        >

          <!-- =====================================================
               SERVICE
          ====================================================== -->

          <div class="request-section">

            <div class="request-section__title">

              <div class="request-section__icon">
                <Wrench :size="19" />
              </div>

              <div>
                <h2>
                  {{ t('request.service.title') }}
                </h2>

                <p>
                  {{ t('request.service.subtitle') }}
                </p>
              </div>

            </div>

            <!-- Selected service -->

            <div
              v-if="selectedService"
              class="request-selected-service"
            >

              <!-- Image -->

              <div class="request-selected-service__image">

                <img
                  v-if="getServiceImage(selectedService)"
                  :src="getServiceImage(selectedService)"
                  :alt="selectedService.name"
                />

                <Wrench
                  v-else
                  :size="24"
                />

              </div>

              <!-- Content -->

              <div class="request-selected-service__content">

                <strong>
                  {{ selectedService.name }}
                </strong>

                <span>
                  {{
                    selectedService.short_description ||
                    selectedService.description ||
                    t('request.service.default_description')
                  }}
                </span>

              </div>

              <!-- Price -->

              <b>
                {{ formatPrice(selectedService.price_from) }}
              </b>

            </div>

            <!-- Service select -->

            <div class="request-field">

              <label
                for="service"
              >
                {{ t('request.service.label') }}
              </label>

              <div class="request-select">

                <select
                  id="service"
                  v-model="form.service_id"
                  :disabled="loadingServices"
                >

                  <option value="">
                    {{
                      loadingServices
                        ? t('request.service.loading')
                        : t('request.service.placeholder')
                    }}
                  </option>

                  <option
                    v-for="service in services"
                    :key="service.id"
                    :value="String(service.id)"
                  >
                    {{ service.name }}
                  </option>

                </select>

                <ChevronDown
                  class="request-select__arrow"
                  :size="18"
                  :stroke-width="2"
                />

              </div>

            </div>

          </div>

          <!-- =====================================================
               CONTACT DATA
          ====================================================== -->

          <div class="request-section">

            <div class="request-section__title">

              <div class="request-section__icon">
                <User :size="19" />
              </div>

              <div>
                <h2>
                  {{ t('request.contact.title') }}
                </h2>

                <p>
                  {{ t('request.contact.subtitle') }}
                </p>
              </div>

            </div>

            <div class="request-grid">

              <!-- Name -->

              <div class="request-field">

                <label for="name">
                  {{ t('request.name') }}
                </label>

                <div class="request-input">

                  <User :size="18" />

                  <input
                    id="name"
                    v-model="form.name"
                    type="text"
                    :placeholder="t('request.name.placeholder')"
                    autocomplete="name"
                  />

                </div>

              </div>

              <!-- Phone -->

              <div class="request-field">

                <label for="phone">
                  {{ t('request.phone') }}
                </label>

                <div class="request-input">

                  <Phone :size="18" />

                  <input
                    id="phone"
                    v-model="form.phone"
                    type="tel"
                    placeholder="+998 90 123 45 67"
                    autocomplete="tel"
                  />

                </div>

              </div>

            </div>

          </div>

          <!-- =====================================================
               ADDRESS
          ====================================================== -->

          <div class="request-section">

            <div class="request-section__title">

              <div class="request-section__icon">
                <MapPin :size="19" />
              </div>

              <div>
                <h2>
                  {{ t('request.address.label') }}
                </h2>

                <p>
                  {{ t('request.address.subtitle') }}
                </p>
              </div>

            </div>

            <div class="request-field">

              <label for="address">
                {{ t('request.address.label') }}
              </label>

              <div class="request-input">

                <MapPin :size="18" />

                <input
                  id="address"
                  v-model="form.address"
                  type="text"
                  :placeholder="t('request.address.placeholder')"
                  autocomplete="street-address"
                />

              </div>

            </div>

          </div>

          <!-- =====================================================
               DATE / TIME
          ====================================================== -->

          <div class="request-section">

            <div class="request-section__title">

              <div class="request-section__icon">
                <Clock3 :size="19" />
              </div>

              <div>
                <h2>
                  {{ t('request.date.title') }}
                </h2>

                <p>
                  {{ t('request.date.subtitle') }}
                </p>
              </div>

            </div>

            <div class="request-grid">

              <!-- Date -->

              <div class="request-field">

                <label for="date">
                  {{ t('request.date') }}
                </label>

                <input
                  id="date"
                  v-model="form.date"
                  class="request-control"
                  type="date"
                  :min="minDate"
                />

              </div>

              <!-- Time -->

              <div class="request-field">

                <label for="time">
                  {{ t('request.time') }}
                </label>

                <input
                  id="time"
                  v-model="form.time"
                  class="request-control"
                  type="time"
                  min="09:00"
                  max="17:00"
                />

              </div>

            </div>

          </div>

          <!-- =====================================================
               COMMENT
          ====================================================== -->

          <div class="request-section">

            <div class="request-section__title">

              <div class="request-section__icon">
                <Send :size="19" />
              </div>

              <div>
                <h2>
                  {{ t('request.comment.title') }}
                </h2>

                <p>
                  {{ t('request.comment.subtitle') }}
                </p>
              </div>

            </div>

            <div class="request-field">

              <label for="comment">

                {{ t('request.comment.title') }}

                <span>
                  {{ t('request.comment.optional') }}
                </span>

              </label>

              <textarea
                id="comment"
                v-model="form.comment"
                rows="4"
                maxlength="2000"
                :placeholder="t('request.comment.placeholder')"
              />

            </div>

          </div>

          <!-- =====================================================
               ERROR
          ====================================================== -->

          <div
            v-if="error"
            class="request-error"
          >
            {{ error }}
          </div>

          <!-- =====================================================
               SUBMIT
          ====================================================== -->

          <button
            type="submit"
            class="request-submit"
            :disabled="submitting || loadingServices"
          >

            <template v-if="submitting">

              <span>
                {{ t('request.submit.loading') }}
              </span>

            </template>

            <template v-else>

              <Send :size="19" />

              <span>
                {{ t('request.submit') }}
              </span>

            </template>

          </button>

          <p class="request-note">
              {{ t('request.footer') }}
            </p>

        </form>

      </section>

    </div>
  </main>
</template>

<style scoped>
/* ================================================================
   PAGE
================================================================ */

.request-page {
  min-height: calc(100vh - 80px);
  padding: 70px 24px 100px;

  background:
    radial-gradient(
      circle at 10% 10%,
      rgba(28, 157, 99, 0.08),
      transparent 30%
    ),
    linear-gradient(
      180deg,
      #f7faf8 0%,
      #ffffff 100%
    );
}

.request-container {
  width: min(900px, 100%);
  margin: 0 auto;
}

/* ================================================================
   HEADER
================================================================ */

.request-header {
  margin-bottom: 34px;
}

.request-back {
  display: inline-flex;
  align-items: center;
  gap: 8px;

  margin-bottom: 28px;
  padding: 0;

  border: 0;
  background: transparent;

  color: #64716a;

  font-size: 14px;
  font-weight: 600;

  transition:
    color 0.2s ease,
    transform 0.2s ease;
}

.request-back:hover {
  color: #15945b;
  transform: translateX(-2px);
}

.request-header__badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;

  margin-bottom: 14px;
  padding: 8px 13px;

  border-radius: 999px;

  background: #e7f7ef;
  color: #15945b;

  font-size: 13px;
  font-weight: 700;
}

.request-header h1 {
  margin: 0 0 12px;

  color: #17201b;

  font-size: clamp(34px, 5vw, 52px);
  line-height: 1.05;
  letter-spacing: -1.5px;
}

.request-header p {
  max-width: 650px;

  margin: 0;

  color: #68746d;

  font-size: 17px;
  line-height: 1.65;
}

/* ================================================================
   CARD
================================================================ */

.request-card {
  padding: 34px;

  border: 1px solid #e5ebe7;
  border-radius: 28px;

  background: #ffffff;

  box-shadow:
    0 18px 60px rgba(25, 50, 38, 0.08);
}

/* ================================================================
   SECTION
================================================================ */

.request-section {
  padding: 28px 0;

  border-bottom: 1px solid #edf1ee;
}

.request-section:first-child {
  padding-top: 0;
}

.request-section:last-of-type {
  border-bottom: 0;
}

.request-section__title {
  display: flex;
  align-items: center;
  gap: 13px;

  margin-bottom: 22px;
}

.request-section__icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 42px;
  height: 42px;
  flex: 0 0 42px;

  border-radius: 12px;

  background: #e9f8f0;
  color: #15945b;
}

.request-section__title h2 {
  margin: 0 0 3px;

  color: #17201b;

  font-size: 18px;
}

.request-section__title p {
  margin: 0;

  color: #87918b;

  font-size: 13px;
}

/* ================================================================
   SELECTED SERVICE
================================================================ */

.request-selected-service {
  display: flex;
  align-items: center;
  gap: 15px;

  margin-bottom: 18px;
  padding: 14px 16px;

  border: 1px solid #cfe9dc;
  border-radius: 15px;

  background: #f2fbf6;
}

.request-selected-service__image {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 76px;
  height: 76px;
  flex: 0 0 76px;

  overflow: hidden;

  border-radius: 12px;

  background: #e5f5ed;
  color: #15945b;
}

.request-selected-service__image img {
  display: block;

  width: 100%;
  height: 100%;

  object-fit: cover;
}

.request-selected-service__content {
  min-width: 0;
  flex: 1;
}

.request-selected-service__content strong {
  display: block;

  margin-bottom: 5px;

  color: #173f2d;

  font-size: 15px;
  line-height: 1.3;
}

.request-selected-service__content span {
  display: -webkit-box;

  overflow: hidden;

  color: #738078;

  font-size: 13px;
  line-height: 1.45;

  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
}

.request-selected-service > b {
  flex-shrink: 0;

  color: #15945b;

  font-size: 14px;
  white-space: nowrap;
}

/* ================================================================
   FORM GRID
================================================================ */

.request-grid {
  display: grid;
  grid-template-columns: repeat(
    2,
    minmax(0, 1fr)
  );

  gap: 18px;
}

/* ================================================================
   FIELD
================================================================ */

.request-field {
  display: flex;
  flex-direction: column;

  gap: 8px;
}

.request-field label {
  color: #303b35;

  font-size: 14px;
  font-weight: 700;
}

.request-field label span {
  margin-left: 5px;

  color: #9aa39e;

  font-size: 12px;
  font-weight: 400;
}

/* ================================================================
   INPUT / SELECT / TEXTAREA
================================================================ */

.request-field input,
.request-field select,
.request-field textarea,
.request-control {
  width: 100%;

  border: 1px solid #dfe6e1;
  border-radius: 13px;

  outline: none;

  background: #ffffff;
  color: #17201b;

  font-size: 15px;

  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.request-field input,
.request-field select,
.request-control {
  height: 52px;

  padding: 0 15px;
}

.request-field textarea {
  min-height: 120px;

  padding: 14px 15px;

  resize: vertical;

  line-height: 1.5;
}

.request-field input:focus,
.request-field select:focus,
.request-field textarea:focus,
.request-control:focus {
  border-color: #43b87e;

  box-shadow:
    0 0 0 4px rgba(67, 184, 126, 0.1);
}

/* ================================================================
   SELECT
================================================================ */

.request-select {
  position: relative;
  width: 100%;
}

.request-select select {
  appearance: none;
  -webkit-appearance: none;

  padding-right: 48px;

  cursor: pointer;
}

.request-select select:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.request-select__arrow {
  position: absolute;

  top: 50%;
  right: 16px;

  color: #68746d;

  pointer-events: none;

  transform: translateY(-50%);
}

/* ================================================================
   INPUT WITH ICON
================================================================ */

.request-input {
  position: relative;
}

.request-input svg {
  position: absolute;

  top: 50%;
  left: 15px;

  z-index: 1;

  color: #8c9891;

  transform: translateY(-50%);

  pointer-events: none;
}

.request-input input {
  padding-left: 45px;
}

/* ================================================================
   ERROR
================================================================ */

.request-error {
  margin-top: 22px;
  padding: 13px 16px;

  border: 1px solid #f1caca;
  border-radius: 12px;

  background: #fff5f5;
  color: #c44242;

  font-size: 14px;
  line-height: 1.5;
}

/* ================================================================
   SUBMIT
================================================================ */

.request-submit {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;

  width: 100%;
  height: 56px;

  margin-top: 26px;

  border: 0;
  border-radius: 14px;

  background: #15945b;
  color: #ffffff;

  font-size: 15px;
  font-weight: 700;

  box-shadow:
    0 10px 24px rgba(21, 148, 91, 0.2);

  transition:
    background 0.2s ease,
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.request-submit:hover:not(:disabled) {
  background: #117e4d;

  transform: translateY(-1px);

  box-shadow:
    0 13px 28px rgba(21, 148, 91, 0.25);
}

.request-submit:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}

.request-note {
  max-width: 600px;

  margin: 15px auto 0;

  color: #8b958f;

  font-size: 12px;
  line-height: 1.5;

  text-align: center;
}

/* ================================================================
   SUCCESS
================================================================ */

.request-success {
  padding: 65px 35px;

  border: 1px solid #dcebe2;
  border-radius: 28px;

  background: #ffffff;

  box-shadow:
    0 18px 60px rgba(25, 50, 38, 0.08);

  text-align: center;
}

.request-success__icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 76px;
  height: 76px;

  margin: 0 auto 22px;

  border-radius: 50%;

  background: #e6f7ee;
  color: #15945b;
}

.request-success h2 {
  margin: 0 0 12px;

  color: #17201b;

  font-size: 30px;
}

.request-success p {
  max-width: 500px;

  margin: 0 auto 28px;

  color: #707b74;

  line-height: 1.6;
}

.request-success__button {
  height: 48px;

  padding: 0 22px;

  border: 0;
  border-radius: 12px;

  background: #15945b;
  color: #ffffff;

  font-weight: 700;

  transition:
    background 0.2s ease,
    transform 0.2s ease;
}

.request-success__button:hover {
  background: #117e4d;
  transform: translateY(-1px);
}

/* ================================================================
   MOBILE
================================================================ */

@media (max-width: 700px) {

  .request-page {
    padding: 45px 16px 70px;
  }

  .request-card {
    padding: 22px 18px;

    border-radius: 22px;
  }

  .request-header h1 {
    font-size: 36px;
  }

  .request-header p {
    font-size: 15px;
  }

  .request-grid {
    grid-template-columns: 1fr;
  }

  .request-selected-service {
    align-items: flex-start;
  }

  .request-selected-service__image {
    width: 64px;
    height: 64px;
    flex-basis: 64px;
  }

  .request-selected-service > b {
    align-self: center;
  }

  .request-success {
    padding: 45px 22px;
  }
}

/* ================================================================
   SMALL MOBILE
================================================================ */

@media (max-width: 480px) {

  .request-page {
    padding-right: 12px;
    padding-left: 12px;
  }

  .request-card {
    padding: 20px 15px;
  }

  .request-section__title {
    gap: 10px;
  }

  .request-section__icon {
    width: 38px;
    height: 38px;
    flex-basis: 38px;
  }

  .request-selected-service {
    display: grid;

    grid-template-columns: 58px minmax(0, 1fr);

    gap: 12px;

    padding: 12px;
  }

  .request-selected-service__image {
    width: 58px;
    height: 58px;
    flex-basis: 58px;

    grid-row: span 2;
  }

  .request-selected-service__content {
    grid-column: 2;
  }

  .request-selected-service > b {
    grid-column: 2;

    justify-self: start;
  }

  .request-header h1 {
    font-size: 32px;
  }
}
</style>