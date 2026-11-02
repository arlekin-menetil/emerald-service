<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { ArrowRight, Maximize2 } from '@lucide/vue'
import { useLanguage } from '../../composables/useLanguage'

const API_BASE_URL = 'http://127.0.0.1:8002'

const { t, currentLanguage } = useLanguage()

const works = ref([])
const loading = ref(true)
const error = ref('')
const activeWork = ref(null)

const getLocalized = (work, field) => {
  const suffix = {
    ru: '',
    uz: '_uz',
    en: '_en',
    zh: '_zh',
  }[currentLanguage.value]

  return work[`${field}${suffix}`] || work[field] || ''
}

const getCategoryName = (category) => {
  const keys = {
    plumbing: 'home.works.category.plumbing',
    bathroom: 'home.works.category.bathroom',
    sewerage: 'home.works.category.sewerage',
    heating: 'home.works.category.heating',
    installation: 'home.works.category.installation',
    other: 'home.works.category.other',
  }

  return keys[category] ? t(keys[category]) : category
}

const openWork = (work) => {
  activeWork.value = work
}

const closeWork = () => {
  activeWork.value = null
}

const loadWorks = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await axios.get(`${API_BASE_URL}/api/content/works/`)
    works.value = response.data.results || []
  } catch (err) {
    console.error('Не удалось загрузить выполненные работы:', err)
    error.value = 'Не удалось загрузить выполненные работы'
  } finally {
    loading.value = false
  }
}

onMounted(loadWorks)
</script>

<template>
  <section class="home-works" id="works">
    <div class="home-works__container">

      <div class="home-works__header">
        <div>
          <span class="home-works__eyebrow">
            {{ t('home.works.eyebrow') }}
          </span>

          <h2 class="home-works__title">
            {{ t('home.works.title') }}
          </h2>

          <p class="home-works__subtitle">
            {{ t('home.works.subtitle') }}
            
          </p>
        </div>

        <a href="/services" class="home-works__link">
          <span>{{ t('home.works.all_services') }}</span>
          <ArrowRight :size="18" />
        </a>
      </div>

      <div v-if="loading" class="home-works__loading">
        {{ t('home.works.loading') }}
      </div>

      <div v-else-if="error" class="home-works__error">
        {{ error }}
      </div>

      <div
        v-else-if="works.length"
        class="home-works__grid"
      >
        <article
          v-for="work in works"
          :key="work.id"
          class="home-work-card"
          @click="openWork(work)"
        >
          <div class="home-work-card__image">
            <img
              v-if="work.image_url"
              :src="work.image_url"
              :alt="getLocalized(work, 'title')"
            />

            <div
              v-else
              class="home-work-card__placeholder"
            >
              {{ t('home.works.no_photo') }}
            </div>

            <div class="home-work-card__overlay"></div>

            <span class="home-work-card__zoom">
              <Maximize2 :size="19" />
            </span>

            <span class="home-work-card__category">
              {{ getCategoryName(work.category) }}
            </span>
          </div>

          <div class="home-work-card__content">
            <h3>
              {{ getLocalized(work, 'title') }}
            </h3>

            <p v-if="getLocalized(work, 'description')">
              {{ getLocalized(work, 'description') }}
            </p>
          </div>
        </article>
      </div>

      <div v-else class="home-works__empty">
        {{ t('home.works.empty') }}
      </div>
    </div>

    <Transition name="home-work-modal">
      <div
        v-if="activeWork"
        class="home-work-modal"
        @click.self="closeWork"
      >
        <div class="home-work-modal__dialog">
          <button
            type="button"
            class="home-work-modal__close"
            :aria-label="t('home.works.close')"
            @click="closeWork"
          >
            ×
          </button>

          <div class="home-work-modal__image">
            <img
              v-if="activeWork.image_url"
              :src="activeWork.image_url"
              :alt="getLocalized(activeWork, 'title')"
            />
          </div>

          <div class="home-work-modal__info">
            <span>
              {{ getCategoryName(activeWork.category) }}
            </span>

            <h3>
              {{ getLocalized(activeWork, 'title') }}
            </h3>

            <p v-if="getLocalized(activeWork, 'description')">
              {{ getLocalized(activeWork, 'description') }}
            </p>
          </div>
        </div>
      </div>
    </Transition>
  </section>
</template>

<style scoped>
.home-works {
  padding: 110px 0;
  background: #ffffff;
}

.home-works__container {
  width: min(1180px, calc(100% - 40px));
  margin: 0 auto;
}

.home-works__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 40px;
  margin-bottom: 46px;
}

.home-works__eyebrow {
  display: inline-block;
  margin-bottom: 12px;
  color: #16834f;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: .08em;
  text-transform: uppercase;
}

.home-works__title {
  max-width: 760px;
  margin: 0;
  color: #10231a;
  font-size: clamp(32px, 4vw, 52px);
  line-height: 1.08;
}

.home-works__subtitle {
  max-width: 680px;
  margin: 18px 0 0;
  color: #65756d;
  font-size: 17px;
  line-height: 1.65;
}

.home-works__link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  color: #16834f;
  font-weight: 700;
  text-decoration: none;
}

.home-works__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.home-work-card {
  overflow: hidden;
  border: 1px solid #e2eee7;
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 15px 40px rgba(20, 75, 48, .06);
  cursor: pointer;
  transition: transform .3s ease, box-shadow .3s ease;
}

.home-work-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 22px 50px rgba(20, 75, 48, .11);
}

.home-work-card__image {
  position: relative;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  background: #eaf4ee;
}

.home-work-card__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform .45s ease;
}

.home-work-card:hover .home-work-card__image img {
  transform: scale(1.05);
}

.home-work-card__placeholder {
  display: grid;
  width: 100%;
  height: 100%;
  place-items: center;
  color: #789087;
  font-size: 14px;
}

.home-work-card__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(8, 35, 22, .62),
    rgba(8, 35, 22, 0) 60%
  );
}

.home-work-card__zoom {
  position: absolute;
  top: 16px;
  right: 16px;
  display: grid;
  width: 42px;
  height: 42px;
  place-items: center;
  color: #fff;
  border: 1px solid rgba(255,255,255,.35);
  border-radius: 50%;
  background: rgba(8, 35, 22, .38);
  backdrop-filter: blur(6px);
}

.home-work-card__category {
  position: absolute;
  left: 18px;
  bottom: 16px;
  padding: 7px 11px;
  color: #fff;
  border-radius: 999px;
  background: rgba(22, 131, 79, .9);
  font-size: 12px;
  font-weight: 700;
}

.home-work-card__content {
  padding: 22px;
}

.home-work-card__content h3 {
  margin: 0;
  color: #10231a;
  font-size: 20px;
  line-height: 1.3;
}

.home-work-card__content p {
  margin: 10px 0 0;
  color: #718078;
  font-size: 14px;
  line-height: 1.55;
}

.home-works__loading,
.home-works__error,
.home-works__empty {
  padding: 50px;
  color: #65756d;
  text-align: center;
}

.home-work-modal {
  position: fixed;
  z-index: 9999;
  inset: 0;
  display: grid;
  padding: 24px;
  place-items: center;
  background: rgba(7, 24, 16, .82);
  backdrop-filter: blur(8px);
}

.home-work-modal__dialog {
  position: relative;
  width: min(1050px, 100%);
  max-height: calc(100vh - 48px);
  overflow: auto;
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 30px 80px rgba(0, 0, 0, .35);
}

.home-work-modal__close {
  position: absolute;
  z-index: 2;
  top: 12px;
  right: 12px;
  display: grid;
  width: 42px;
  height: 42px;
  place-items: center;
  border: 0;
  border-radius: 50%;
  color: #fff;
  background: rgba(0, 0, 0, .55);
  font-size: 30px;
  line-height: 1;
  cursor: pointer;
}

.home-work-modal__image {
  max-height: 70vh;
  background: #edf5f0;
}

.home-work-modal__image img {
  display: block;
  width: 100%;
  max-height: 70vh;
  object-fit: contain;
}

.home-work-modal__info {
  padding: 24px 28px 30px;
}

.home-work-modal__info > span {
  color: #16834f;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}

.home-work-modal__info h3 {
  margin: 8px 0 0;
  color: #10231a;
  font-size: 26px;
}

.home-work-modal__info p {
  margin: 10px 0 0;
  color: #65756d;
  line-height: 1.6;
}

.home-work-modal-enter-active,
.home-work-modal-leave-active {
  transition: opacity .2s ease;
}

.home-work-modal-enter-from,
.home-work-modal-leave-to {
  opacity: 0;
}

@media (max-width: 850px) {
  .home-works__header {
    align-items: flex-start;
    flex-direction: column;
  }

  .home-works__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 560px) {
  .home-works {
    padding: 75px 0;
  }

  .home-works__container {
    width: min(100% - 28px, 1180px);
  }

  .home-works__grid {
    grid-template-columns: 1fr;
  }

  .home-work-modal {
    padding: 10px;
  }

  .home-work-modal__dialog {
    border-radius: 18px;
  }
}
</style>
