<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { Play, ArrowRight } from '@lucide/vue'
import { useLanguage } from '../../composables/useLanguage'

import { API_BASE } from '../../config/api'

const API_BASE_URL = API_BASE

const { t, currentLanguage } = useLanguage()

const videos = ref([])
const loading = ref(true)
const error = ref('')
const activeVideo = ref(null)

const getLocalized = (video, field) => {
  const suffix = {
    ru: '',
    uz: '_uz',
    en: '_en',
    zh: '_zh',
  }[currentLanguage.value]

  return video[`${field}${suffix}`] || video[field] || ''
}

const getCategoryLabel = (category) => {
  const keys = {
    plumbing: 'home.videos.category.plumbing',
    bathroom: 'home.videos.category.bathroom',
    sewerage: 'home.videos.category.sewerage',
    heating: 'home.videos.category.heating',
    installation: 'home.videos.category.installation',
    other: 'home.videos.category.other',
  }

  return keys[category] ? t(keys[category]) : category
}

const getThumbnail = (video) => {
  if (video.thumbnail_url) return video.thumbnail_url

  if (video.youtube_id) {
    return `https://img.youtube.com/vi/${video.youtube_id}/maxresdefault.jpg`
  }

  return ''
}

const getYoutubeEmbedUrl = (video) => {
  if (!video.youtube_id) return ''

  return `https://www.youtube.com/embed/${video.youtube_id}?autoplay=1&rel=0&modestbranding=1`
}

const openVideo = (video) => {
  activeVideo.value = video
}

const closeVideo = () => {
  activeVideo.value = null
}

const loadVideos = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await axios.get(`${API_BASE_URL}/api/content/videos/`)
    videos.value = response.data.results || []
  } catch (err) {
    console.error('Не удалось загрузить видео:', err)
    error.value = t('home.videos.error')
  } finally {
    loading.value = false
  }
}

onMounted(loadVideos)
</script>

<template>
  <section class="home-videos" id="videos">
    <div class="home-videos__container">

      <div class="home-videos__header">
        <div>
          <span class="home-videos__eyebrow">
            {{ t('home.videos.eyebrow') }}
          </span>

          <h2 class="home-videos__title">
            {{ t('home.videos.title') }}
          </h2>

          <p class="home-videos__subtitle">
            {{ t('home.videos.subtitle') }}
          </p>
        </div>

        <a href="/telegram-bot" class="home-videos__link">
          <span>{{ t('home.videos.ask_question') }}</span>
          <ArrowRight :size="18" />
        </a>
      </div>

      <div v-if="loading" class="home-videos__loading">
        {{ t('home.videos.loading') }}
      </div>

      <div v-else-if="error" class="home-videos__error">
        {{ error }}
      </div>

      <div
        v-else-if="videos.length"
        class="home-videos__grid"
      >
        <article
          v-for="video in videos"
          :key="video.id"
          class="home-video-card"
        >
          <button
            type="button"
            class="home-video-card__media"
            @click="openVideo(video)"
          >
            <img
              :src="getThumbnail(video)"
              :alt="getLocalized(video, 'title')"
              class="home-video-card__thumbnail"
            />

            <span class="home-video-card__overlay"></span>

            <span class="home-video-card__play">
              <Play :size="25" fill="currentColor" />
            </span>

            <span class="home-video-card__watch">
              {{ t('home.videos.watch') }}
            </span>
          </button>

          <div class="home-video-card__content">
            <span class="home-video-card__category">
              {{ getCategoryLabel(video.category) }}
            </span>

            <h3>
              {{ getLocalized(video, 'title') }}
            </h3>

            <p v-if="getLocalized(video, 'description')">
              {{ getLocalized(video, 'description') }}
            </p>
          </div>
        </article>
      </div>

      <div v-else class="home-videos__empty">
        {{ t('home.videos.empty') }}
      </div>
    </div>

    <Transition name="home-video-modal">
      <div
        v-if="activeVideo"
        class="home-video-modal"
        @click.self="closeVideo"
      >
        <div class="home-video-modal__dialog">
          <button
            type="button"
            class="home-video-modal__close"
            :aria-label="t('home.videos.close')"
            @click="closeVideo"
          >
            ×
          </button>

          <div class="home-video-modal__player">
            <iframe
              :src="getYoutubeEmbedUrl(activeVideo)"
              :title="getLocalized(activeVideo, 'title')"
              frameborder="0"
              allow="autoplay; encrypted-media; picture-in-picture"
              allowfullscreen
            ></iframe>
          </div>

          <div class="home-video-modal__info">
            <h3>
              {{ getLocalized(activeVideo, 'title') }}
            </h3>

            <p v-if="getLocalized(activeVideo, 'description')">
              {{ getLocalized(activeVideo, 'description') }}
            </p>
          </div>
        </div>
      </div>
    </Transition>
  </section>
</template>

<style scoped>
.home-videos {
  padding: 110px 0;
  background: #f7fbf8;
}

.home-videos__container {
  width: min(1180px, calc(100% - 40px));
  margin: 0 auto;
}

.home-videos__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 40px;
  margin-bottom: 46px;
}

.home-videos__eyebrow {
  display: inline-block;
  margin-bottom: 12px;
  color: #16834f;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: .08em;
  text-transform: uppercase;
}

.home-videos__title {
  margin: 0;
  color: #10231a;
  font-size: clamp(32px, 4vw, 52px);
  line-height: 1.08;
}

.home-videos__subtitle {
  max-width: 650px;
  margin: 18px 0 0;
  color: #65756d;
  font-size: 17px;
  line-height: 1.65;
}

.home-videos__link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  color: #16834f;
  font-weight: 700;
  text-decoration: none;
}

.home-videos__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.home-video-card {
  overflow: hidden;
  border: 1px solid #e2eee7;
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 15px 40px rgba(20, 75, 48, .07);
}

.home-video-card__media {
  position: relative;
  display: block;
  width: 100%;
  padding: 0;
  border: 0;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  cursor: pointer;
  background: #dfeee5;
}

.home-video-card__thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform .45s ease;
}

.home-video-card__media:hover .home-video-card__thumbnail {
  transform: scale(1.04);
}

.home-video-card__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(8, 35, 22, .62),
    rgba(8, 35, 22, .05) 65%
  );
}

.home-video-card__play {
  position: absolute;
  top: 50%;
  left: 50%;
  display: grid;
  width: 66px;
  height: 66px;
  place-items: center;
  color: #fff;
  border-radius: 50%;
  background: #16834f;
  box-shadow: 0 12px 30px rgba(22, 131, 79, .35);
  transform: translate(-50%, -50%);
  transition: transform .25s ease, background .25s ease;
}

.home-video-card__media:hover .home-video-card__play {
  background: #126e43;
  transform: translate(-50%, -50%) scale(1.08);
}

.home-video-card__watch {
  position: absolute;
  left: 20px;
  bottom: 17px;
  color: #fff;
  font-size: 13px;
  font-weight: 700;
}

.home-video-card__content {
  padding: 22px;
}

.home-video-card__category {
  color: #16834f;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}

.home-video-card__content h3 {
  margin: 9px 0 0;
  color: #10231a;
  font-size: 20px;
  line-height: 1.3;
}

.home-video-card__content p {
  margin: 10px 0 0;
  color: #718078;
  font-size: 14px;
  line-height: 1.55;
}

.home-videos__loading,
.home-videos__error,
.home-videos__empty {
  padding: 50px;
  color: #65756d;
  text-align: center;
}

.home-video-modal {
  position: fixed;
  z-index: 9999;
  inset: 0;
  display: grid;
  padding: 24px;
  place-items: center;
  background: rgba(7, 24, 16, .82);
  backdrop-filter: blur(8px);
}

.home-video-modal__dialog {
  position: relative;
  width: min(1000px, 100%);
  overflow: hidden;
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 30px 80px rgba(0, 0, 0, .35);
}

.home-video-modal__close {
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

.home-video-modal__player {
  aspect-ratio: 16 / 9;
  background: #000;
}

.home-video-modal__player iframe {
  display: block;
  width: 100%;
  height: 100%;
  border: 0;
}

.home-video-modal__info {
  padding: 24px 28px 28px;
}

.home-video-modal__info h3 {
  margin: 0;
  color: #10231a;
  font-size: 24px;
}

.home-video-modal__info p {
  margin: 10px 0 0;
  color: #65756d;
  line-height: 1.6;
}

.home-video-modal-enter-active,
.home-video-modal-leave-active {
  transition: opacity .2s ease;
}

.home-video-modal-enter-from,
.home-video-modal-leave-to {
  opacity: 0;
}

@media (max-width: 850px) {
  .home-videos__header {
    align-items: flex-start;
    flex-direction: column;
  }

  .home-videos__grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 560px) {
  .home-videos {
    padding: 75px 0;
  }

  .home-videos__container {
    width: min(100% - 28px, 1180px);
  }

  .home-videos__header {
    margin-bottom: 32px;
  }

  .home-video-card__content {
    padding: 18px;
  }

  .home-video-modal {
    padding: 10px;
  }

  .home-video-modal__dialog {
    border-radius: 18px;
  }
}
</style>
