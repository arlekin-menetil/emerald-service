<script setup>
import { onMounted, ref, watch } from 'vue'
import axios from 'axios'
import {
  ArrowRight,
  Check,
  ShieldCheck,
  Clock3,
  Wrench,
  Users,
} from '@lucide/vue'
import { useLanguage } from '../composables/useLanguage'

const { t, currentLanguage } = useLanguage()

const masters = ref([])
const loading = ref(true)

function getDisplayName(employee) {
  return employee.website_name?.trim() || employee.name || ''
}

function normalizePhoto(photo) {
  if (!photo) return ''

  try {
    return new URL(photo).pathname
  } catch {
    return photo
  }
}

async function loadMasters() {
  loading.value = true

  try {
    const response = await axios.get('/api/employees/', {
      params: {
        lang: currentLanguage.value,
      },
    })

    masters.value = (response.data.results || response.data || [])
      .filter((employee) => employee.is_active !== false)
      .filter((employee) => employee.is_published !== false)
      .map((employee) => ({
        ...employee,
        displayName: getDisplayName(employee),
        photo: normalizePhoto(employee.photo),
      }))
  } catch (error) {
    console.error('Не удалось загрузить мастеров:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadMasters()
})

watch(currentLanguage, () => {
  loadMasters()
})
</script>

<template>
  <main class="about-page">

    <!-- HERO -->
    <section class="about-hero">
      <div class="about-container">

        <div class="about-hero__content">
          <span class="about-eyebrow">
            {{ t('about.eyebrow') }}
          </span>

          <h1>
            {{ t('about.hero.title') }}
            <strong>{{ t('about.hero.title_accent') }}</strong>
          </h1>

          <p>
            {{ t('about.hero.description') }}
          </p>
        </div>

        <div class="about-hero__visual">
          <div class="about-hero__rings"></div>

          <div class="about-hero__team">
            <img
              src="/team.png"
              :alt="t('about.hero.image_alt')"
            />
          </div>
        </div>

      </div>
    </section>


    <!-- ABOUT COMPANY -->
    <section class="about-story">
      <div class="about-container about-story__grid">

        <div>
          <span class="about-section-label">
            {{ t('about.story.eyebrow') }}
          </span>

          <h2>
            {{ t('about.story.title') }}
            <strong>{{ t('about.story.title_accent') }}</strong>
          </h2>
        </div>

        <div class="about-story__text">
          <p>
            {{ t('about.story.description') }}
          </p>

          <p>
            {{ t('about.story.description_2') }}
          </p>
        </div>

      </div>
    </section>


    <!-- ADVANTAGES -->
    <section class="about-advantages">
      <div class="about-container">

        <div class="about-heading">
          <span class="about-section-label">
            {{ t('about.advantages.eyebrow') }}
          </span>

          <h2>
            {{ t('about.advantages.title') }}
            <strong>{{ t('about.advantages.title_accent') }}</strong>
          </h2>
        </div>

        <div class="about-advantages__grid">

          <article class="about-advantage">
            <div class="about-advantage__icon">
              <Wrench :size="23" />
            </div>

            <h3>{{ t('about.advantage.experienced.title') }}</h3>

            <p>
              {{ t('about.advantage.experienced.description') }}
            </p>
          </article>


          <article class="about-advantage">
            <div class="about-advantage__icon">
              <Clock3 :size="23" />
            </div>

            <h3>{{ t('about.advantage.fast.title') }}</h3>

            <p>
              {{ t('about.advantage.fast.description') }}
            </p>
          </article>


          <article class="about-advantage">
            <div class="about-advantage__icon">
              <ShieldCheck :size="23" />
            </div>

            <h3>{{ t('about.advantage.guarantee.title') }}</h3>

            <p>
              {{ t('about.advantage.guarantee.description') }}
            </p>
          </article>


          <article class="about-advantage">
            <div class="about-advantage__icon">
              <Users :size="23" />
            </div>

            <h3>{{ t('about.advantage.real.title') }}</h3>

            <p>
              {{ t('about.advantage.real.description') }}
            </p>
          </article>

        </div>
      </div>
    </section>


    <!-- TEAM -->
    <section class="about-team">
      <div class="about-container">

        <div class="about-heading about-heading--center">
          <span class="about-section-label">
            {{ t('about.team.eyebrow') }}
          </span>

          <h2>
            {{ t('about.team.title') }}
            <strong>{{ t('about.team.title_accent') }}</strong>
          </h2>

          <p>
            {{ t('about.team.description') }}
          </p>
        </div>


        <div
          v-if="masters.length"
          class="masters-list"
        >

          <article
            v-for="master in masters"
            :key="master.id"
            class="master-card"
          >

            <div class="master-card__photo">

              <div class="master-card__circle"></div>

              <img
                v-if="master.photo"
                :src="master.photo"
                :alt="`${master.displayName} — ${master.position}`"
              />

              <div class="master-card__badge">
                <Check :size="16" />
                {{ t('about.master.verified') }}
              </div>

            </div>


            <div class="master-card__content">

              <span class="master-card__label">
                {{ master.position }}
              </span>

              <h3>
                {{ master.displayName }}
              </h3>

              <p class="master-card__position">
                {{ master.position }}
              </p>

              <p class="master-card__description">
                {{ t('about.master.description') }}
              </p>

              <div class="master-card__experience">
                <strong>{{ master.experience }}</strong>
                <span>{{ t('about.master.experience') }}</span>
              </div>


              <div class="master-card__checks">

                <div>
                  <Check :size="17" />
                  <span>{{ t('about.master.skill.repair') }}</span>
                </div>

                <div>
                  <Check :size="17" />
                  <span>{{ t('about.master.skill.installation') }}</span>
                </div>

                <div>
                  <Check :size="17" />
                  <span>{{ t('about.master.skill.leaks') }}</span>
                </div>

              </div>

            </div>

          </article>

        </div>


        <div
          v-else-if="loading"
          class="master-loading"
        >
          {{ t('about.team.loading') }}
        </div>

      </div>
    </section>


    <!-- CTA -->
    <section class="about-cta">
      <div class="about-container">

        <div class="about-cta__inner">

          <div>
            <span>
              {{ t('about.cta.eyebrow') }}
            </span>

            <h2>
              {{ t('about.cta.title') }}
              <strong>{{ t('about.cta.title_accent') }}</strong>
            </h2>

            <p>
              {{ t('about.cta.description') }}
            </p>
          </div>

          <RouterLink
            to="/request"
            class="about-cta__button"
          >
            {{ t('about.cta.button') }}
            <ArrowRight :size="18" />
          </RouterLink>

        </div>

      </div>
    </section>

  </main>
</template>


<style scoped>

.about-page {
  color: #17201b;
  background: #fff;
}

.about-container {
  width: min(1180px, calc(100% - 48px));
  margin: 0 auto;
}


/* ==========================================================
   HERO
========================================================== */

.about-hero {
  padding: 90px 0 100px;

  background:
    radial-gradient(
      circle at 80% 35%,
      rgba(28, 175, 115, 0.13),
      transparent 32%
    ),
    #f4faf7;
}

.about-hero .about-container {
  display: grid;
  grid-template-columns: 1fr 0.85fr;
  gap: 70px;
  align-items: center;
}

.about-hero__content {
  max-width: 650px;
}

.about-eyebrow,
.about-section-label {
  display: inline-block;
  margin-bottom: 18px;

  color: #149968;

  font-size: 12px;
  font-weight: 800;
  letter-spacing: .14em;
}

.about-hero h1 {
  margin: 0;

  font-size: clamp(42px, 6vw, 72px);
  line-height: .98;
  letter-spacing: -.045em;
}

.about-hero h1 strong,
.about-story h2 strong,
.about-heading h2 strong,
.about-cta h2 strong {
  color: #08a875;
}

.about-hero p {
  max-width: 600px;
  margin: 26px 0 0;

  color: #617168;

  font-size: 17px;
  line-height: 1.7;
}


/* ==========================================================
   HERO TEAM VISUAL
========================================================== */

.about-hero__visual {
  position: relative;

  min-height: 390px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.about-hero__rings {
  position: absolute;

  width: 330px;
  height: 330px;

  border-radius: 50%;

  background: #08a875;

  box-shadow:
    0 0 0 25px rgba(8, 168, 117, .12),
    0 0 0 50px rgba(8, 168, 117, .06);
}


/*
 * Само изображение team.png.
 *
 * Оно масштабируется и обрезается внутри круга.
 * Благодаря этому внешние элементы исходного изображения
 * не вываливаются за пределы Hero.
 */

.about-hero__team {
  position: relative;

  z-index: 2;

  width: 330px;
  height: 330px;

  overflow: hidden;

  border-radius: 50%;
}

.about-hero__team img {
  position: absolute;

  left: 50%;
  top: 50%;

  width: 145%;
  height: 145%;

  max-width: none;

  object-fit: cover;

  transform: translate(-50%, -50%);

  object-position: center center;
}


/* ==========================================================
   STORY
========================================================== */

.about-story {
  padding: 105px 0;
}

.about-story__grid {
  display: grid;

  grid-template-columns: 1fr 0.85fr;

  gap: 70px;

  align-items: center;
}

.about-story h2,
.about-heading h2 {
  margin: 0;

  font-size: clamp(36px, 4.5vw, 54px);
  line-height: 1.03;
  letter-spacing: -.04em;
}

.about-story__text {
  color: #65746c;

  font-size: 16px;
  line-height: 1.75;
}

.about-story__text p {
  margin: 0 0 20px;
}


/* ==========================================================
   ADVANTAGES
========================================================== */

.about-advantages {
  padding: 100px 0;

  background: #f4faf7;
}

.about-heading {
  max-width: 650px;
}

.about-advantages__grid {
  display: grid;

  grid-template-columns: repeat(4, 1fr);

  gap: 16px;

  margin-top: 48px;
}

.about-advantage {
  padding: 28px;

  border: 1px solid #e2eee8;
  border-radius: 20px;

  background: #fff;
}

.about-advantage__icon {
  display: grid;
  place-items: center;

  width: 46px;
  height: 46px;

  margin-bottom: 22px;

  border-radius: 13px;

  color: #079968;
  background: #e8f8f0;
}

.about-advantage h3 {
  margin: 0 0 10px;

  font-size: 17px;
}

.about-advantage p {
  margin: 0;

  color: #718078;

  font-size: 13px;
  line-height: 1.6;
}


/* ==========================================================
   TEAM
========================================================== */

.about-team {
  padding: 110px 0;
}

.about-heading--center {
  max-width: 650px;

  margin: 0 auto;

  text-align: center;
}

.about-heading--center p {
  color: #718078;
  line-height: 1.6;
}

.masters-list {
  display: grid;

  gap: 32px;

  margin-top: 55px;
}

.master-card {
  display: grid;

  grid-template-columns: .9fr 1.1fr;

  overflow: hidden;

  border-radius: 30px;

  background: #eaf8f1;

  border: 1px solid #dcefe6;
}

.master-card__photo {
  position: relative;

  min-height: 510px;

  display: flex;
  align-items: flex-end;
  justify-content: center;

  overflow: hidden;
}

.master-card__circle {
  position: absolute;

  width: 390px;
  height: 390px;

  bottom: -100px;

  border-radius: 50%;

  background: #c8ead8;
}

.master-card__photo img {
  position: relative;

  z-index: 2;

  width: min(90%, 430px);
  max-height: 520px;

  object-fit: contain;
  object-position: bottom center;
}

.master-card__badge {
  position: absolute;

  top: 28px;
  left: 28px;

  z-index: 3;

  display: flex;
  align-items: center;

  gap: 7px;

  padding: 11px 15px;

  border-radius: 999px;

  background: #fff;

  color: #079968;

  font-size: 12px;
  font-weight: 700;

  box-shadow:
    0 12px 30px rgba(25, 80, 55, .1);
}

.master-card__content {
  display: flex;

  flex-direction: column;
  justify-content: center;

  padding: 65px;
}

.master-card__label {
  color: #079968;

  font-size: 11px;
  font-weight: 800;

  letter-spacing: .15em;
}

.master-card h3 {
  margin: 12px 0 0;

  font-size: clamp(42px, 5vw, 64px);

  line-height: 1;

  letter-spacing: -.045em;
}

.master-card__position {
  margin: 10px 0 0;

  color: #079968;

  font-size: 18px;
  font-weight: 700;
}

.master-card__description {
  max-width: 500px;

  margin: 22px 0;

  color: #66766d;

  line-height: 1.7;
}

.master-card__experience {
  display: flex;
  align-items: baseline;

  gap: 10px;

  margin-bottom: 22px;
}

.master-card__experience strong {
  color: #079968;

  font-size: 38px;
}

.master-card__experience span {
  color: #65746c;

  font-size: 14px;
  font-weight: 600;
}

.master-card__checks {
  display: grid;

  gap: 9px;

  margin-bottom: 28px;
}

.master-card__checks div {
  display: flex;
  align-items: center;

  gap: 9px;

  color: #46554d;

  font-size: 13px;
}

.master-card__checks svg {
  color: #079968;
}


/* ==========================================================
   CTA
========================================================== */

.about-cta {
  padding: 0 0 100px;
}

.about-cta__inner {
  display: flex;

  flex-direction: column;

  align-items: center;
  justify-content: center;

  gap: 18px;

  padding: 42px 55px;

  border-radius: 24px;

  background: #078d63;

  color: #fff;

  text-align: center;
}

.about-cta__inner > div {
  max-width: 700px;
}

.about-cta__inner span {
  font-size: 10px;
  font-weight: 800;

  letter-spacing: .14em;
}

.about-cta h2 {
  margin: 10px 0 8px;

  font-size: clamp(28px, 4vw, 42px);

  line-height: 1;
}

.about-cta h2 strong {
  color: #8ff0c5;
}

.about-cta p {
  margin: 0;

  color: rgba(255,255,255,.75);

  font-size: 14px;
}

.about-cta__button {
  display: inline-flex;

  align-items: center;
  justify-content: center;

  gap: 9px;

  padding: 15px 21px;

  border-radius: 13px;

  background: #fff;

  color: #078d63;

  font-size: 14px;
  font-weight: 700;
}


/* ==========================================================
   TABLET
========================================================== */

@media (max-width: 900px) {

  .about-container.about-story__grid,
  .about-hero .about-container,
  .master-card {
    grid-template-columns: 1fr;
  }

  .about-hero__visual {
    min-height: 330px;
  }

  .about-advantages__grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .master-card__content {
    padding: 45px 35px;
  }

}


/* ==========================================================
   MOBILE
========================================================== */

@media (max-width: 600px) {

  .about-container {
    width: min(100% - 32px, 1180px);
  }

  .about-hero {
    padding: 65px 0 70px;
  }

  .about-hero__visual {
    min-height: 280px;
  }

  .about-hero__rings {
    width: 235px;
    height: 235px;

    box-shadow:
      0 0 0 18px rgba(8, 168, 117, .12),
      0 0 0 36px rgba(8, 168, 117, .06);
  }

  .about-hero__team {
    width: 235px;
    height: 235px;
  }

  .about-hero__team img {
    width: 150%;
    height: 150%;
  }

  .about-story,
  .about-advantages,
  .about-team {
    padding: 75px 0;
  }

  .about-advantages__grid {
    grid-template-columns: 1fr;
  }

  .master-card__photo {
    min-height: 360px;
  }

  .master-card__circle {
    width: 290px;
    height: 290px;
  }

  .master-card__content {
    padding: 35px 25px;
  }

  .about-cta {
    padding-bottom: 60px;
  }

  .about-cta__inner {
    flex-direction: column;

    align-items: center;

    padding: 35px 25px;

    text-align: center;
  }

}
</style>