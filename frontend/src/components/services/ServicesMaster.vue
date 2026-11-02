<script setup>
import {
  ArrowRight,
  Check,
  Clock3,
  ShieldCheck,
  Wrench,
} from '@lucide/vue'
import { useLanguage } from '../../composables/useLanguage'

const { t } = useLanguage()

const getMasterCutoutPhoto = (photo) => {
  if (!photo) return ''
  return photo.replace(/[^/]+$/, 'usta-master-cutout.png')
}

const getMasterAlt = (master) => {
  const name = master?.website_name || master?.name || ''
  const position = master?.position || ''

  if (!name) return position

  return `${name} — ${position}`
}

defineProps({
  master: {
    type: Object,
    default: null,
  },
})
</script>

<template>
  <section v-if="master" class="services-master">
    <div class="services-container">

      <div class="services-master__card">

        <!-- =========================
             ЛЕВАЯ ЧАСТЬ
        ========================== -->
        <div class="services-master__content">

          <div class="services-master__eyebrow">
            <span class="services-master__eyebrow-dot"></span>
            <span>{{ t('services.master.eyebrow') }}</span>
          </div>

          <div class="services-master__heading">

            <span class="services-master__overline">
              {{ t('services.master.title') }}
            </span>

            <h2>
              {{ master.website_name || master.name }}
            </h2>

            <div class="services-master__position">
              {{ master.position }}
            </div>

          </div>

          <p class="services-master__description">
            {{ t('services.master.description') }}
          </p>

          <!-- Статистика -->
          <div class="services-master__stats">

            <div class="services-master__stat">

              <div class="services-master__stat-icon">
                <Clock3 :size="18" />
              </div>

              <div class="services-master__stat-content">
                <strong>
                  {{ master.experience }}
                </strong>

                <span>
                  {{ t('services.master.experience') }}
                </span>
              </div>

            </div>


            <div class="services-master__stat">

              <div class="services-master__stat-icon">
                <Wrench :size="18" />
              </div>

              <div class="services-master__stat-content">
                <strong>
                  24/7
                </strong>

                <span>
                  {{ t('services.master.requests') }}
                </span>
              </div>

            </div>


            <div class="services-master__stat">

              <div class="services-master__stat-icon">
                <ShieldCheck :size="18" />
              </div>

              <div class="services-master__stat-content">
                <strong>
                  100%
                </strong>

                <span>
                  {{ t('services.master.attention') }}
                </span>
              </div>

            </div>

          </div>


          <!-- Кнопка -->
          <RouterLink
            to="/request"
            class="services-master__button"
          >
            <span>
              {{ t('services.master.call') }}
            </span>

            <ArrowRight :size="18" />
          </RouterLink>

        </div>


        <!-- =========================
             ПРАВАЯ ЧАСТЬ
        ========================== -->
        <div class="services-master__visual">

          <!-- Основной зелёный фон -->
          <div class="services-master__visual-bg"></div>

          <!-- Мягкое свечение -->
          <div class="services-master__visual-glow"></div>


          <!-- Декоративная линия -->
          <div class="services-master__visual-line"></div>


          <!-- Мастер -->
          <div class="services-master__master">

            <img
              :src="getMasterCutoutPhoto(master.photo)"
              :alt="getMasterAlt(master)"
            />

          </div>


          <!-- Бейдж -->
          <div class="services-master__badge">

            <div class="services-master__badge-icon">
              <Check :size="15" />
            </div>

            <div class="services-master__badge-text">
              <strong>
                {{ t('services.master.badge') }}
              </strong>

              <span>
                {{ t('services.master.company') }}
              </span>
            </div>

          </div>


          <!-- Подпись -->
          <div class="services-master__caption">

            <span>
              {{ t('services.master.caption.label') }}
            </span>

            <strong>
              {{ t('services.master.caption.title') }}
            </strong>

          </div>


          <!-- Маленький декоративный элемент -->
          <div class="services-master__corner">

            <span></span>
            <span></span>
            <span></span>

          </div>

        </div>

      </div>

    </div>
  </section>
</template>