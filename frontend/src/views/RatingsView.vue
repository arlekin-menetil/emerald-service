<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import axios from 'axios'
import { useLanguage } from '../composables/useLanguage'
import {
  Star,
  ArrowRight,
  LoaderCircle,
  CheckCircle2,
  Award,
  TrendingUp,
} from '@lucide/vue'

const { t, currentLanguage } = useLanguage()

const loading = ref(true)
const error = ref('')

const ratingData = ref({
  average_rating: null,
  total_ratings: 0,
  services: [],
})

const bestService = computed(() => {
  if (!ratingData.value.services.length) {
    return null
  }

  return [...ratingData.value.services].sort((a, b) => {
    if (b.average_rating !== a.average_rating) {
      return b.average_rating - a.average_rating
    }

    return b.total_ratings - a.total_ratings
  })[0]
})

const otherServices = computed(() => {
  if (!bestService.value) {
    return ratingData.value.services
  }

  return ratingData.value.services.filter(
    service => service.id !== bestService.value.id,
  )
})

async function loadRatings() {
  loading.value = true
  error.value = ''

  try {
    const response = await axios.get(
      `/api/service-requests/ratings/?lang=${encodeURIComponent(currentLanguage.value)}`
    )

    ratingData.value = response.data
  } catch (err) {
    console.error(
      'Ошибка загрузки рейтинга:',
      err,
    )

    error.value =
      'Не удалось загрузить рейтинг услуг.'
  } finally {
    loading.value = false
  }
}

function formatRating(value) {
  if (
    value === null ||
    value === undefined
  ) {
    return '—'
  }

  return Number(value).toFixed(2)
}

function ratingPercent(value) {
  return `${Math.min(
    (Number(value) / 5) * 100,
    100,
  )}%`
}

function pluralRatings(count) {
  const language = currentLanguage.value

  if (language === 'ru') {
    if (count % 10 === 1 && count % 100 !== 11) {
      return t('ratings.count.one')
    }

    if (
      count % 10 >= 2 &&
      count % 10 <= 4 &&
      (count % 100 < 10 || count % 100 >= 20)
    ) {
      return t('ratings.count.few')
    }

    return t('ratings.count.many')
  }

  if (language === 'en') {
    return count === 1
      ? t('ratings.count.one')
      : t('ratings.count.many')
  }

  if (language === 'uz') {
    return t('ratings.count.one')
  }

  if (language === 'zh') {
    return t('ratings.count.one')
  }

  return t('ratings.count.many')
}

function isFullStar(rating, star) {
  return Number(rating) >= star
}

function goToRequest() {
  window.location.href = '/request'
}

onMounted(loadRatings)
watch(currentLanguage, loadRatings)
</script>


<template>
  <main class="ratings-page">

    <!-- =====================================================
         HERO
    ====================================================== -->

    <section class="ratings-hero">

      <div class="ratings-container">

        <div class="ratings-hero__grid">

          <!-- LEFT -->
          <div class="ratings-hero__content">

            <div class="ratings-eyebrow">
              <span
                class="ratings-eyebrow__line"
              ></span>

              <span>
                {{ t('ratings.eyebrow') }}
              </span>
            </div>

            <h1>
              {{ t('ratings.hero.title') }}
              <span>
                {{ t('ratings.hero.title_accent') }}
              </span>
            </h1>

            <p class="ratings-hero__description">
              {{ t('ratings.hero.description') }}
              {{ t('ratings.hero.description_2') }}
              {{ t('ratings.hero.description_3') }}
            </p>

            <div class="ratings-benefits">

              <div class="ratings-benefit">

                <div
                  class="ratings-benefit__icon"
                >
                  <CheckCircle2
                    :size="18"
                  />
                </div>

                <div>
                  <strong>
                    {{ t('ratings.benefit.real.title') }}
                  </strong>

                  <span>
                    {{ t('ratings.benefit.real.description') }}
                  </span>
                </div>

              </div>


              <div class="ratings-benefit">

                <div
                  class="ratings-benefit__icon"
                >
                  <Award
                    :size="18"
                  />
                </div>

                <div>
                  <strong>
                    {{ t('ratings.benefit.honest.title') }}
                  </strong>

                  <span>
                    {{ t('ratings.benefit.honest.description') }}
                  </span>
                </div>

              </div>

            </div>

          </div>


          <!-- RIGHT -->
          <div class="ratings-hero__visual">

            <div
              class="
                ratings-orbit
                ratings-orbit--one
              "
            ></div>

            <div
              class="
                ratings-orbit
                ratings-orbit--two
              "
            ></div>


            <div class="ratings-score">

              <div class="ratings-score__top">

                <span>
                  {{ t('ratings.score.label') }}
                </span>

                <div
                  class="ratings-score__badge"
                >
                  <Star
                    :size="14"
                    fill="currentColor"
                  />

                  <span>
                    5.0
                  </span>
                </div>

              </div>


              <div
                class="ratings-score__main"
              >

                <div
                  class="
                    ratings-score__number
                  "
                >
                  {{
                    formatRating(
                      ratingData.average_rating,
                    )
                  }}
                </div>

                <div
                  class="ratings-score__max"
                >
                  / 5
                </div>

              </div>


              <div
                class="ratings-score__stars"
              >
                <Star
                  v-for="star in 5"
                  :key="star"
                  :size="26"
                  :fill="
                    isFullStar(
                      ratingData.average_rating,
                      star,
                    )
                      ? 'currentColor'
                      : 'none'
                  "
                />
              </div>


              <div
                class="ratings-score__line"
              ></div>


              <div
                class="ratings-score__bottom"
              >

                <div>
                  <strong>
                    {{
                      ratingData.total_ratings
                    }}
                  </strong>

                  <span>
                    {{
                      pluralRatings(
                        ratingData.total_ratings,
                      )
                    }}
                  </span>
                </div>

                <span
                  class="
                    ratings-score__verified
                  "
                >
                  <CheckCircle2
                    :size="15"
                  />

                  {{ t('ratings.score.verified') }}
                </span>

              </div>

            </div>

          </div>

        </div>

      </div>

    </section>


    <!-- =====================================================
         BEST SERVICE
    ====================================================== -->

    <section
      v-if="!loading && bestService"
      class="ratings-featured"
    >

      <div class="ratings-container">

        <div
          class="ratings-featured__head"
        >

          <div>
            <div class="ratings-eyebrow">
              <span
                class="ratings-eyebrow__line"
              ></span>

              <span>
                {{ t('ratings.featured.eyebrow') }}
              </span>
            </div>

            <h2>
              {{ t('ratings.featured.title') }}
            </h2>
          </div>

          <div
            class="ratings-featured__trend"
          >
            <TrendingUp
              :size="16"
            />

            <span>
              {{ t('ratings.featured.subtitle') }}
            </span>
          </div>

        </div>


        <article
          class="featured-service"
        >

          <!-- IMAGE -->
          <div
            class="featured-service__image"
          >

            <img
              v-if="bestService.image"
              :src="bestService.image"
              :alt="bestService.name"
            />

            <div
              v-else
              class="
                featured-service__image-placeholder
              "
            >
              <Star
                :size="42"
              />
            </div>


            <div
              class="
                featured-service__image-overlay
              "
            ></div>


            <div
              class="
                featured-service__label
              "
            >
              <Star
                :size="15"
                fill="currentColor"
              />

              {{ t('ratings.featured.badge') }}
            </div>

          </div>


          <!-- CONTENT -->
          <div
            class="featured-service__content"
          >

            <div
              class="
                featured-service__number
              "
            >
              01
            </div>

            <h3>
              {{ bestService.name }}
            </h3>

            <p>
              {{ t('ratings.featured.description') }}
            </p>


            <div
              class="featured-service__rating"
            >

              <div
                class="
                  featured-service__rating-value
                "
              >
                {{
                  formatRating(
                    bestService.average_rating,
                  )
                }}
              </div>

              <div>

                <div
                  class="
                    featured-service__stars
                  "
                >
                  <Star
                    v-for="star in 5"
                    :key="star"
                    :size="19"
                    :fill="
                      isFullStar(
                        bestService.average_rating,
                        star,
                      )
                        ? 'currentColor'
                        : 'none'
                    "
                  />
                </div>

                <span>
                  {{
                    bestService.total_ratings
                  }}
                  {{
                    pluralRatings(
                      bestService.total_ratings,
                    )
                  }}
                </span>

              </div>

            </div>


            <div
              class="
                featured-service__progress
              "
            >
              <div
                class="
                  featured-service__progress-fill
                "
                :style="{
                  width: ratingPercent(
                    bestService.average_rating,
                  ),
                }"
              ></div>
            </div>

          </div>

        </article>

      </div>

    </section>


    <!-- =====================================================
         ALL SERVICES
    ====================================================== -->

    <section class="ratings-services">

      <div class="ratings-container">

        <div
          class="ratings-section-head"
        >

          <div>

            <div class="ratings-eyebrow">
              <span
                class="ratings-eyebrow__line"
              ></span>

              <span>
                {{ t('ratings.services.eyebrow') }}
              </span>
            </div>

            <h2>
              {{ t('ratings.services.title') }}
            </h2>

          </div>

          <p>
            {{ t('ratings.services.description') }}
          </p>

        </div>


        <!-- LOADING -->

        <div
          v-if="loading"
          class="ratings-state"
        >

          <LoaderCircle
            :size="30"
            class="ratings-loader"
          />

          <span>
            {{ t('ratings.services.loading') }}
          </span>

        </div>


        <!-- ERROR -->

        <div
          v-else-if="error"
          class="
            ratings-state
            ratings-state--error
          "
        >
          {{ error }}
        </div>


        <!-- EMPTY -->

        <div
          v-else-if="!ratingData.services.length"
          class="ratings-state"
        >
          {{ t('ratings.empty') }}
        </div>


        <!-- CARDS -->

        <div
          v-else
          class="ratings-grid"
        >

          <article
            v-for="service in otherServices"
            :key="service.id"
            class="rating-card"
          >

            <!-- IMAGE -->

            <div
              class="rating-card__image"
            >

              <img
                v-if="service.image"
                :src="service.image"
                :alt="service.name"
                loading="lazy"
              />

              <div
                v-else
                class="
                  rating-card__image-placeholder
                "
              >
                <Star :size="30" />
              </div>


              <div
                class="
                  rating-card__image-gradient
                "
              ></div>


              <div
                class="rating-card__score"
              >
                {{
                  formatRating(
                    service.average_rating,
                  )
                }}
              </div>

            </div>


            <!-- CONTENT -->

            <div
              class="rating-card__content"
            >

              <h3>
                {{ service.name }}
              </h3>


              <div
                class="rating-card__rating"
              >

                <div
                  class="
                    rating-card__stars
                  "
                >
                  <Star
                    v-for="star in 5"
                    :key="star"
                    :size="15"
                    :fill="
                      isFullStar(
                        service.average_rating,
                        star,
                      )
                        ? 'currentColor'
                        : 'none'
                    "
                  />
                </div>

                <span>
                  {{
                    service.total_ratings
                  }}
                  {{
                    pluralRatings(
                      service.total_ratings,
                    )
                  }}
                </span>

              </div>


              <div
                class="
                  rating-card__progress
                "
              >
                <div
                  class="
                    rating-card__progress-fill
                  "
                  :style="{
                    width: ratingPercent(
                      service.average_rating,
                    ),
                  }"
                ></div>
              </div>

            </div>

          </article>

        </div>

      </div>

    </section>


    <!-- =====================================================
         CTA
    ====================================================== -->

    <section class="ratings-cta">

      <div class="ratings-cta__glow"></div>

      <div class="ratings-container">

        <div
          class="ratings-cta__box"
        >

          <div
            class="ratings-cta__content"
          >

            <div
              class="ratings-cta__eyebrow"
            >
              <span></span>

              {{ t('ratings.cta.eyebrow') }}
            </div>

            <h2>
              {{ t('ratings.cta.title') }}
            </h2>

            <p>
              {{ t('ratings.cta.description') }}
            </p>

          </div>


          <button
            type="button"
            class="ratings-cta__button"
            @click="goToRequest"
          >

            <span>
              {{ t('ratings.cta.button') }}
            </span>

            <ArrowRight
              :size="18"
            />

          </button>

        </div>

      </div>

    </section>

  </main>
</template>


<style scoped>

/* =========================================================
   BASE
========================================================= */

.ratings-page {
  min-height: 100vh;

  overflow: hidden;

  color: #17201b;

  background: #f7faf8;
}

.ratings-container {
  width: min(
    1180px,
    calc(100% - 48px)
  );

  margin: 0 auto;
}


/* =========================================================
   EYEBROW
========================================================= */

.ratings-eyebrow {
  display: flex;

  align-items: center;

  gap: 10px;

  margin-bottom: 17px;

  color: #159447;

  font-size: 10px;

  font-weight: 800;

  letter-spacing: 0.2em;
}

.ratings-eyebrow__line {
  width: 26px;
  height: 2px;

  border-radius: 99px;

  background: #159447;
}


/* =========================================================
   HERO
========================================================= */

.ratings-hero {
  position: relative;

  overflow: hidden;

  padding: 82px 0 88px;

  background:
    radial-gradient(
      circle at 78% 50%,
      rgba(21, 148, 71, 0.13),
      transparent 27%
    ),
    linear-gradient(
      135deg,
      #f9fcfa,
      #f5faf7 55%,
      #edf7f1
    );
}

.ratings-hero::before {
  content: '';

  position: absolute;

  width: 600px;
  height: 600px;

  left: -330px;
  bottom: -390px;

  border: 1px solid
    rgba(21, 148, 71, 0.06);

  border-radius: 50%;
}

.ratings-hero::after {
  content: '';

  position: absolute;

  width: 680px;
  height: 680px;

  right: -360px;
  top: -390px;

  border: 1px solid
    rgba(21, 148, 71, 0.07);

  border-radius: 50%;
}

.ratings-hero__grid {
  position: relative;

  z-index: 2;

  display: grid;

  grid-template-columns:
    minmax(0, 1.05fr)
    minmax(400px, 0.95fr);

  align-items: center;

  gap: 70px;
}


/* HERO TEXT */

.ratings-hero h1 {
  max-width: 690px;

  margin: 0;

  font-size: clamp(
    50px,
    5.2vw,
    76px
  );

  font-weight: 800;

  line-height: 0.97;

  letter-spacing: -0.06em;
}

.ratings-hero h1 span {
  display: block;

  color: #159447;
}

.ratings-hero__description {
  max-width: 540px;

  margin: 27px 0 0;

  color: #68756e;

  font-size: 16px;

  line-height: 1.7;
}


/* BENEFITS */

.ratings-benefits {
  display: flex;

  flex-wrap: wrap;

  gap: 28px;

  margin-top: 38px;
}

.ratings-benefit {
  display: flex;

  align-items: center;

  gap: 11px;
}

.ratings-benefit__icon {
  display: flex;

  align-items: center;
  justify-content: center;

  width: 39px;
  height: 39px;

  border-radius: 11px;

  color: #159447;

  background: #e4f5ea;
}

.ratings-benefit strong,
.ratings-benefit span {
  display: block;
}

.ratings-benefit strong {
  margin-bottom: 3px;

  color: #26332c;

  font-size: 12px;
}

.ratings-benefit span {
  color: #89948e;

  font-size: 10px;
}


/* =========================================================
   HERO SCORE
========================================================= */

.ratings-hero__visual {
  position: relative;

  display: flex;

  align-items: center;
  justify-content: center;

  min-height: 415px;
}

.ratings-orbit {
  position: absolute;

  border: 1px solid
    rgba(21, 148, 71, 0.11);

  border-radius: 50%;
}

.ratings-orbit--one {
  width: 415px;
  height: 415px;
}

.ratings-orbit--two {
  width: 505px;
  height: 505px;

  border-color:
    rgba(21, 148, 71, 0.055);
}

.ratings-score {
  position: relative;

  z-index: 2;

  width: min(
    100%,
    425px
  );

  padding: 37px 38px 33px;

  border: 1px solid
    rgba(21, 148, 71, 0.14);

  border-radius: 31px;

  background:
    linear-gradient(
      145deg,
      rgba(255, 255, 255, 0.99),
      rgba(245, 251, 247, 0.98)
    );

  box-shadow:
    0 35px 85px
      rgba(23, 32, 27, 0.1),
    0 8px 25px
      rgba(21, 148, 71, 0.06);

  backdrop-filter: blur(14px);
}

.ratings-score__top {
  display: flex;

  align-items: center;
  justify-content: space-between;
}

.ratings-score__top > span {
  color: #7e8983;

  font-size: 10px;

  font-weight: 800;

  letter-spacing: 0.18em;
}

.ratings-score__badge {
  display: flex;

  align-items: center;

  gap: 5px;

  padding: 7px 10px;

  border-radius: 9px;

  color: #159447;

  background: #e7f6ed;

  font-size: 11px;

  font-weight: 800;
}

.ratings-score__main {
  display: flex;

  align-items: flex-end;

  gap: 8px;

  margin-top: 21px;
}

.ratings-score__number {
  color: #159447;

  font-size: 92px;

  font-weight: 800;

  line-height: 0.88;

  letter-spacing: -0.075em;
}

.ratings-score__max {
  padding-bottom: 6px;

  color: #89948e;

  font-size: 15px;
}

.ratings-score__stars {
  display: flex;

  gap: 5px;

  margin-top: 26px;

  color: #159447;
}

.ratings-score__line {
  width: 100%;
  height: 1px;

  margin: 27px 0 19px;

  background: #dce9e1;
}

.ratings-score__bottom {
  display: flex;

  align-items: center;
  justify-content: space-between;
}

.ratings-score__bottom > div {
  display: flex;

  align-items: baseline;

  gap: 5px;
}

.ratings-score__bottom strong {
  color: #17201b;

  font-size: 17px;
}

.ratings-score__bottom span {
  color: #7f8b84;

  font-size: 11px;
}

.ratings-score__verified {
  display: flex;

  align-items: center;

  gap: 5px;

  color: #159447 !important;

  font-weight: 700;
}


/* =========================================================
   FEATURED
========================================================= */

.ratings-featured {
  padding: 90px 0 100px;

  background: #fff;
}

.ratings-featured__head {
  display: flex;

  align-items: flex-end;
  justify-content: space-between;

  gap: 30px;

  margin-bottom: 37px;
}

.ratings-featured__head h2 {
  margin: 0;

  font-size: clamp(
    35px,
    4vw,
    52px
  );

  font-weight: 800;

  line-height: 0.98;

  letter-spacing: -0.055em;
}

.ratings-featured__trend {
  display: flex;

  align-items: center;

  gap: 7px;

  margin-bottom: 4px;

  color: #159447;

  font-size: 11px;

  font-weight: 700;
}


/* FEATURED CARD */

.featured-service {
  display: grid;

  grid-template-columns:
    minmax(0, 1.12fr)
    minmax(390px, 0.88fr);

  min-height: 390px;

  overflow: hidden;

  border: 1px solid #dce8e1;

  border-radius: 28px;

  background: #f7faf8;

  box-shadow:
    0 20px 55px
      rgba(23, 32, 27, 0.07);
}


/* IMAGE */

.featured-service__image {
  position: relative;

  min-height: 390px;

  overflow: hidden;

  background: #e8f1eb;
}

.featured-service__image img {
  display: block;

  width: 100%;
  height: 100%;

  object-fit: cover;

  transition:
    transform 0.6s ease;
}

.featured-service:hover
.featured-service__image img {
  transform: scale(1.045);
}

.featured-service__image-overlay {
  position: absolute;

  inset: 0;

  background:
    linear-gradient(
      90deg,
      transparent 55%,
      rgba(14, 29, 20, 0.2)
    );
}

.featured-service__image-placeholder {
  display: flex;

  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;

  color: #159447;

  background: #e8f5ec;
}

.featured-service__label {
  position: absolute;

  left: 24px;
  top: 24px;

  display: inline-flex;

  align-items: center;

  gap: 7px;

  padding: 9px 12px;

  border-radius: 10px;

  color: #fff;

  background: rgba(15, 31, 22, 0.76);

  backdrop-filter: blur(10px);

  font-size: 10px;

  font-weight: 800;

  letter-spacing: 0.04em;
}


/* FEATURED CONTENT */

.featured-service__content {
  display: flex;

  flex-direction: column;

  justify-content: center;

  padding: 48px;
}

.featured-service__number {
  margin-bottom: 18px;

  color: #159447;

  font-size: 11px;

  font-weight: 800;

  letter-spacing: 0.2em;
}

.featured-service__content h3 {
  max-width: 450px;

  margin: 0;

  color: #18231d;

  font-size: clamp(
    34px,
    4vw,
    49px
  );

  font-weight: 800;

  line-height: 1;

  letter-spacing: -0.055em;
}

.featured-service__content p {
  max-width: 390px;

  margin: 18px 0 30px;

  color: #77847d;

  font-size: 13px;

  line-height: 1.65;
}

.featured-service__rating {
  display: flex;

  align-items: center;

  gap: 17px;
}

.featured-service__rating-value {
  color: #159447;

  font-size: 44px;

  font-weight: 800;

  line-height: 1;

  letter-spacing: -0.05em;
}

.featured-service__stars {
  display: flex;

  gap: 3px;

  color: #159447;
}

.featured-service__rating span {
  display: block;

  margin-top: 5px;

  color: #89958e;

  font-size: 10px;
}

.featured-service__progress {
  width: 100%;
  height: 5px;

  margin-top: 27px;

  overflow: hidden;

  border-radius: 99px;

  background: #dfeae3;
}

.featured-service__progress-fill {
  height: 100%;

  border-radius: inherit;

  background:
    linear-gradient(
      90deg,
      #159447,
      #2db967
    );
}


/* =========================================================
   SERVICES
========================================================= */

.ratings-services {
  padding: 92px 0 105px;

  background: #f7faf8;
}

.ratings-section-head {
  display: flex;

  align-items: flex-end;
  justify-content: space-between;

  gap: 50px;

  margin-bottom: 40px;
}

.ratings-section-head h2 {
  margin: 0;

  font-size: clamp(
    35px,
    4vw,
    52px
  );

  font-weight: 800;

  line-height: 0.98;

  letter-spacing: -0.055em;
}

.ratings-section-head p {
  max-width: 340px;

  margin: 0 0 4px;

  color: #7c8982;

  font-size: 12px;

  line-height: 1.7;
}


/* GRID */

.ratings-grid {
  display: grid;

  grid-template-columns:
    repeat(3, minmax(0, 1fr));

  gap: 18px;
}


/* CARD */

.rating-card {
  overflow: hidden;

  border: 1px solid #dfe9e3;

  border-radius: 22px;

  background: #fff;

  box-shadow:
    0 8px 25px
      rgba(23, 32, 27, 0.035);

  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease,
    border-color 0.25s ease;
}

.rating-card:hover {
  transform: translateY(-6px);

  border-color: #b9d9c5;

  box-shadow:
    0 22px 50px
      rgba(23, 32, 27, 0.09);
}


/* IMAGE */

.rating-card__image {
  position: relative;

  height: 205px;

  overflow: hidden;

  background: #e9f2ec;
}

.rating-card__image img {
  display: block;

  width: 100%;
  height: 100%;

  object-fit: cover;

  transition:
    transform 0.45s ease;
}

.rating-card:hover
.rating-card__image img {
  transform: scale(1.06);
}

.rating-card__image-gradient {
  position: absolute;

  inset: 0;

  background:
    linear-gradient(
      180deg,
      transparent 48%,
      rgba(11, 25, 17, 0.45)
    );
}

.rating-card__image-placeholder {
  display: flex;

  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;

  color: #159447;
}

.rating-card__score {
  position: absolute;

  right: 15px;
  bottom: 14px;

  padding: 8px 10px;

  border-radius: 9px;

  color: #fff;

  background: rgba(14, 31, 21, 0.78);

  backdrop-filter: blur(8px);

  font-size: 15px;

  font-weight: 800;
}


/* CONTENT */

.rating-card__content {
  padding: 21px 21px 22px;
}

.rating-card h3 {
  min-height: 42px;

  margin: 0 0 17px;

  color: #1b2720;

  font-size: 14px;

  font-weight: 750;

  line-height: 1.45;
}

.rating-card__rating {
  display: flex;

  align-items: center;
  justify-content: space-between;

  gap: 10px;
}

.rating-card__stars {
  display: flex;

  gap: 3px;

  color: #159447;
}

.rating-card__rating > span {
  color: #89948e;

  font-size: 10px;

  white-space: nowrap;
}

.rating-card__progress {
  width: 100%;
  height: 4px;

  margin-top: 17px;

  overflow: hidden;

  border-radius: 99px;

  background: #e9efeb;
}

.rating-card__progress-fill {
  height: 100%;

  border-radius: inherit;

  background:
    linear-gradient(
      90deg,
      #159447,
      #2db967
    );
}


/* =========================================================
   STATES
========================================================= */

.ratings-state {
  display: flex;

  min-height: 250px;

  align-items: center;
  justify-content: center;

  gap: 12px;

  color: #718078;

  font-size: 14px;
}

.ratings-state--error {
  color: #b23c3c;
}

.ratings-loader {
  animation:
    ratings-spin 1s linear infinite;
}

@keyframes ratings-spin {
  to {
    transform: rotate(360deg);
  }
}


/* =========================================================
   CTA
========================================================= */

.ratings-cta {
  position: relative;

  overflow: hidden;

  padding: 78px 0;

  background: #101915;
}

.ratings-cta::before {
  content: '';

  position: absolute;

  width: 620px;
  height: 620px;

  right: -180px;
  top: 50%;

  transform:
    translateY(-50%);

  border: 1px solid
    rgba(70, 205, 116, 0.13);

  border-radius: 50%;
}

.ratings-cta::after {
  content: '';

  position: absolute;

  width: 440px;
  height: 440px;

  right: -85px;
  top: 50%;

  transform:
    translateY(-50%);

  border: 1px solid
    rgba(70, 205, 116, 0.08);

  border-radius: 50%;
}

.ratings-cta__glow {
  position: absolute;

  width: 450px;
  height: 450px;

  right: -60px;
  top: 50%;

  transform:
    translateY(-50%);

  border-radius: 50%;

  background:
    radial-gradient(
      circle,
      rgba(31, 177, 89, 0.22),
      transparent 68%
    );

  filter: blur(5px);
}

.ratings-cta .ratings-container {
  position: relative;

  z-index: 2;
}

.ratings-cta__box {
  display: flex;

  align-items: center;
  justify-content: space-between;

  gap: 60px;

  padding: 51px 57px;

  border: 1px solid
    rgba(255, 255, 255, 0.08);

  border-radius: 30px;

  background:
    linear-gradient(
      120deg,
      #18251e,
      #142019 65%,
      #182a20
    );

  box-shadow:
    0 30px 80px
      rgba(0, 0, 0, 0.24);
}

.ratings-cta__content {
  max-width: 650px;
}

.ratings-cta__eyebrow {
  display: flex;

  align-items: center;

  gap: 9px;

  margin-bottom: 14px;

  color: #62d78e;

  font-size: 10px;

  font-weight: 800;

  letter-spacing: 0.21em;
}

.ratings-cta__eyebrow span {
  width: 23px;
  height: 2px;

  border-radius: 99px;

  background: #31b966;
}

.ratings-cta h2 {
  margin: 0;

  color: #fff;

  font-size: clamp(
    41px,
    4.5vw,
    58px
  );

  font-weight: 800;

  line-height: 0.95;

  letter-spacing: -0.055em;
}

.ratings-cta p {
  max-width: 500px;

  margin: 17px 0 0;

  color: rgba(
    255,
    255,
    255,
    0.55
  );

  font-size: 13px;

  line-height: 1.7;
}

.ratings-cta__button {
  display: inline-flex;

  flex-shrink: 0;

  align-items: center;
  justify-content: center;

  gap: 12px;

  min-width: 210px;

  padding: 17px 22px;

  border: 1px solid
    rgba(255, 255, 255, 0.8);

  border-radius: 14px;

  color: #12301f;

  background: #fff;

  font-size: 12px;

  font-weight: 800;

  box-shadow:
    0 15px 35px
      rgba(0, 0, 0, 0.2);

  transition:
    transform 0.22s ease,
    box-shadow 0.22s ease,
    background 0.22s ease;
}

.ratings-cta__button svg {
  transition:
    transform 0.22s ease;
}

.ratings-cta__button:hover {
  transform: translateY(-4px);

  background: #f2fff6;

  box-shadow:
    0 21px 45px
      rgba(0, 0, 0, 0.28);
}

.ratings-cta__button:hover svg {
  transform: translateX(4px);
}


/* =========================================================
   TABLET
========================================================= */

@media (max-width: 980px) {

  .ratings-hero__grid {
    grid-template-columns: 1fr;

    gap: 55px;
  }

  .ratings-hero__content {
    max-width: 720px;
  }

  .ratings-hero__visual {
    max-width: 520px;

    margin: 0 auto;
  }

  .featured-service {
    grid-template-columns: 1fr;
  }

  .featured-service__image {
    min-height: 340px;
  }

  .ratings-grid {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));
  }

  .ratings-section-head,
  .ratings-featured__head {
    align-items: flex-start;

    flex-direction: column;

    gap: 18px;
  }
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 620px) {

  .ratings-container {
    width:
      calc(100% - 28px);
  }


  /* HERO */

  .ratings-hero {
    padding: 55px 0 65px;
  }

  .ratings-hero h1 {
    font-size: 45px;
  }

  .ratings-hero__description {
    font-size: 14px;
  }

  .ratings-benefits {
    flex-direction: column;

    gap: 15px;

    margin-top: 29px;
  }


  /* SCORE */

  .ratings-hero__visual {
    min-height: 350px;
  }

  .ratings-orbit--one {
    width: 340px;
    height: 340px;
  }

  .ratings-orbit--two {
    width: 400px;
    height: 400px;
  }

  .ratings-score {
    padding: 30px;

    border-radius: 25px;
  }

  .ratings-score__number {
    font-size: 70px;
  }

  .ratings-score__bottom {
    align-items: flex-start;

    flex-direction: column;

    gap: 10px;
  }


  /* FEATURED */

  .ratings-featured {
    padding: 65px 0 72px;
  }

  .ratings-featured__head h2 {
    font-size: 36px;
  }

  .featured-service {
    border-radius: 23px;
  }

  .featured-service__image {
    min-height: 250px;
  }

  .featured-service__content {
    padding: 30px 25px;
  }

  .featured-service__content h3 {
    font-size: 36px;
  }

  .featured-service__rating-value {
    font-size: 38px;
  }


  /* SERVICES */

  .ratings-services {
    padding: 65px 0 75px;
  }

  .ratings-section-head h2 {
    font-size: 36px;
  }

  .ratings-grid {
    grid-template-columns: 1fr;

    gap: 14px;
  }

  .rating-card__image {
    height: 220px;
  }


  /* CTA */

  .ratings-cta {
    padding: 48px 0;
  }

  .ratings-cta__box {
    align-items: flex-start;

    flex-direction: column;

    gap: 29px;

    padding: 35px 25px;

    border-radius: 24px;
  }

  .ratings-cta__box::before {
    display: none;
  }

  .ratings-cta h2 {
    font-size: 40px;
  }

  .ratings-cta__button {
    width: 100%;
  }
}

</style>