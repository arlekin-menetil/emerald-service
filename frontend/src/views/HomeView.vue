<script setup>
import HomeWorks from '../components/home/HomeWorks.vue'
import HomeVideos from '../components/home/HomeVideos.vue'
import { ArrowRight, Check, Wrench, Faucet, Waves, Flame, Zap, Settings2 } from '@lucide/vue'
import { useLanguage } from '../composables/useLanguage'

const { t } = useLanguage()
</script>

<template>
  <main class="home">
    <section class="hero">
      <div class="hero__container">

        <div class="hero__content">
          <div class="hero__badge">
            <span></span>
            {{ t('home.hero.badge') }}
          </div>

          <h1>
            {{ t('home.hero.title') }}
            <strong>{{ t('home.hero.title_strong') }}</strong>
            {{ t('home.hero.city') }}
          </h1>

          <p class="hero__description">
            {{ t('home.hero.description') }}
          </p>

          <div class="hero__actions">
            <a href="/request" class="hero__button hero__button--primary">
              <span>{{ t('home.hero.call') }}</span>
              <ArrowRight class="hero__arrow" :size="20" :stroke-width="2" />
            </a>

            <a href="#services" class="hero__button hero__button--secondary">
              {{ t('home.hero.services') }}
            </a>
          </div>

          <div class="hero__advantages">
            <div class="advantage">
              <div class="advantage__icon"><Check :size="18" :stroke-width="2.5" /></div>
              <div>
                <strong>{{ t('home.hero.advantage.quality') }}</strong>
                <span>{{ t('home.hero.advantage.quality_text') }}</span>
              </div>
            </div>

            <div class="advantage">
              <div class="advantage__icon"><Zap :size="24" :stroke-width="2.4" /></div>
              <div>
                <strong>{{ t('home.hero.advantage.fast') }}</strong>
                <span>{{ t('home.hero.advantage.fast_text') }}</span>
              </div>
            </div>

            <div class="advantage">
              <div class="advantage__icon">★</div>
              <div>
                <strong>{{ t('home.hero.advantage.masters') }}</strong>
                <span>{{ t('home.hero.advantage.masters_text') }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="hero__visual">
          <div class="hero__circle hero__circle--large"></div>
          <div class="hero__circle hero__circle--small"></div>

          <div class="hero__water-drop">
            <div class="drop">
              <img src="/tap.png" alt="" class="hero__tap" />
            </div>
          </div>

          <div class="floating-card floating-card--top">
            <div class="floating-card__icon"><Check :size="18" :stroke-width="2.5" /></div>
            <div>
              <strong>{{ t('home.hero.guarantee') }}</strong>
              <span>{{ t('home.hero.guarantee_text') }}</span>
            </div>
          </div>

          <div class="floating-card floating-card--bottom">
            <div class="floating-card__icon"><Settings2 :size="25" :stroke-width="2.1" /></div>
            <div>
              <strong>{{ t('home.hero.any_plumbing') }}</strong>
              <span>{{ t('home.hero.any_plumbing_text') }}</span>
            </div>
          </div>
        </div>

      </div>
    </section>

    <section id="services" class="services-preview">
      <div class="services-preview__container">
        <div class="section-heading">
          <span>{{ t('home.services.eyebrow') }}</span>
          <h2>{{ t('home.services.title') }}</h2>
          <p>
            {{ t('home.services.description') }}
          </p>
        </div>

        <div class="service-cards">
          <article class="service-card">
            <div class="service-card__icon"><Faucet :size="30" :stroke-width="1.8" /></div>
            <h3>{{ t('home.services.repair') }}</h3>
            <p>{{ t('home.services.repair_text') }}</p>
          </article>

          <article class="service-card">
            <div class="service-card__icon"><Wrench :size="30" :stroke-width="1.8" /></div>
            <h3>{{ t('home.services.installation') }}</h3>
            <p>{{ t('home.services.installation_text') }}</p>
          </article>

          <article class="service-card">
            <div class="service-card__icon"><Waves :size="30" :stroke-width="1.8" /></div>
            <h3>{{ t('home.services.sewerage') }}</h3>
            <p>{{ t('home.services.sewerage_text') }}</p>
          </article>

          <article class="service-card">
            <div class="service-card__icon"><Flame :size="30" :stroke-width="1.8" /></div>
            <h3>{{ t('home.services.heating') }}</h3>
            <p>{{ t('home.services.heating_text') }}</p>
          </article>
        </div>
      </div>
    
      <div class="services-preview__footer">
        <a href="/services" class="services-preview__all-link">
          <span>{{ t('home.services.all') }}</span>
          <ArrowRight :size="18" :stroke-width="2" />
        </a>
      </div>
</section>
  </main>


  
<!-- {{ t('home.discount.badge') }} -->
<section class="home-discount">
  <div class="home-discount__inner">
    <div class="home-discount__badge">
      <span>5–10%</span>
      <small>{{ t('home.discount.badge') }}</small>
    </div>

    <div class="home-discount__content">
      <span class="home-section-heading__eyebrow">{{ t('home.discount.eyebrow') }}</span>
      <h2>{{ t('home.discount.title') }}</h2>
      <p>
        {{ t('home.discount.description') }}
      </p>
    </div>
  </div>
</section>

<!-- НАШИ ЦЕННОСТИ -->
  <section class="home-values">
    <div class="home-values__inner">

      <div class="home-section-heading">
        <span class="home-section-heading__eyebrow">
          IZUMRUD SERVIS
        </span>

        <h2>{{ t('home.values.title') }}</h2>

        <p>
          {{ t('home.values.description') }}
        </p>
      </div>

      <div class="home-values__grid">

        <article class="home-values__card">
          <div class="home-values__icon">⏱</div>

          <div>
            <h3>{{ t('home.values.time.title') }}</h3>

            <p>
              {{ t('home.values.time.text') }}
            </p>
          </div>
        </article>


        <article class="home-values__card">
          <div class="home-values__icon">✓</div>

          <div>
            <h3>{{ t('home.values.transparency.title') }}</h3>

            <p>
              {{ t('home.values.transparency.text') }}
            </p>
          </div>
        </article>


        <article class="home-values__card">
          <div class="home-values__icon">▣</div>

          <div>
            <h3>{{ t('home.values.official.title') }}</h3>

            <p>
              {{ t('home.values.official.text') }}
            </p>
          </div>
        </article>

      </div>
    </div>
  </section>


  <!-- ДЛЯ ЮРИДИЧЕСКИХ ЛИЦ -->
  <section class="home-business">
    <div class="home-business__inner">

      <div class="home-business__content">

        <span class="home-section-heading__eyebrow">
          {{ t('home.business.eyebrow') }}
        </span>

        <h2>{{ t('home.business.title') }}</h2>

        <p class="home-business__lead">
          {{ t('home.business.lead') }}
        </p>

        <p>
          {{ t('home.business.description') }}
        </p>

        <p>
          {{ t('home.business.organizations') }}
        </p>

        <div class="home-business__features">
          <span>{{ t('home.services.sewerage') }}</span>
          <span>{{ t("home.business.water") }}</span>
          <span>{{ t('home.services.heating') }}</span>
          <span>{{ t("home.business.water") }}</span>
        </div>

      </div>


      <div class="home-business__side">

        <div class="home-business__number">
          B2B
        </div>

        <h3>
          {{ t('home.business.b2b_title') }}
        </h3>

        <p>
          {{ t('home.business.side_text') }}
        </p>

      </div>

    </div>
  </section>


  <!-- НАШИ ГАРАНТИИ -->
  <section class="home-guarantees">
    <div class="home-guarantees__inner">

      <div class="home-section-heading">

        <span class="home-section-heading__eyebrow">
          {{ t('home.guarantees.eyebrow') }}
        </span>

        <h2>{{ t('home.guarantees.title') }}</h2>

        <p>
          {{ t('home.guarantees.description') }}
        </p>

      </div>


      <div class="home-guarantees__grid">

        <article class="home-guarantees__card">

          <span class="home-guarantees__index">
            01
          </span>

          <h3>
            {{ t('home.guarantees.safety.title') }}
          </h3>

          <p>
            {{ t('home.guarantees.safety.text') }}
          </p>

        </article>


        <article class="home-guarantees__card">

          <span class="home-guarantees__index">
            02
          </span>

          <h3>
            {{ t('home.guarantees.result.title') }}
          </h3>

          <p>
            {{ t('home.guarantees.result.text') }}
          </p>

        </article>


        <article class="home-guarantees__card">

          <span class="home-guarantees__index">
            03
          </span>

          <h3>
            {{ t('home.guarantees.specialists.title') }}
          </h3>

          <p>
            {{ t('home.guarantees.specialists.text') }}
          </p>

        </article>

      </div>
    </div>
  </section>

  <HomeWorks />
  <HomeVideos />
</template>

<style scoped>
.home {
  min-height: 100vh;
  display: block;
  padding: 0;
  text-align: left;
  background: #f7faf8;
}

.hero {
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(circle at 85% 20%, rgba(0, 157, 116, 0.10), transparent 30%),
    linear-gradient(135deg, #f8fbf9 0%, #ffffff 52%, #eef8f4 100%);
}

.hero__container {
  width: min(1440px, calc(100% - 48px));
  min-height: 680px;
  margin: 0 auto;

  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  align-items: center;
  gap: 50px;
}

.hero__content {
  position: relative;
  z-index: 2;
  padding: 70px 0;
}

.hero__badge {
  display: inline-flex;
  align-items: center;
  gap: 9px;

  padding: 9px 15px;
  margin-bottom: 24px;

  border: 1px solid #d8ebe4;
  border-radius: 999px;

  background: rgba(255, 255, 255, 0.8);
  color: #187c63;

  font-size: 14px;
  font-weight: 600;
}

.hero__badge span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #00a77a;
}

.hero h1 {
  max-width: 700px;
  margin: 0;

  color: #15221d;

  font-size: clamp(42px, 5vw, 68px);
  line-height: 1.04;
  letter-spacing: -2.8px;
  font-weight: 700;
}

.hero h1 strong {
  display: block;
  color: #00966f;
}

.hero__description {
  max-width: 650px;
  margin: 28px 0 0;

  color: #66756e;
  font-size: 18px;
  line-height: 1.7;
}

.hero__actions {
  display: flex;
  gap: 14px;
  margin-top: 36px;
}

.hero__button {
  min-height: 54px;
  padding: 0 24px;

  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 16px;

  border-radius: 13px;

  font-size: 15px;
  font-weight: 700;

  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease;
}

.hero__button:hover {
  transform: translateY(-2px);
}

.hero__button--primary {
  color: white;
  background: #00966f;
  box-shadow: 0 12px 28px rgba(0, 150, 111, 0.2);
}

.hero__button--primary:hover {
  background: #007d5c;
  box-shadow: 0 16px 34px rgba(0, 150, 111, 0.28);
}

.hero__button--secondary {
  color: #08785f;
  border: 1px solid #a9d5c8;
  background: white;
}

.hero__button--secondary:hover {
  border-color: #00966f;
}

.hero__arrow {
  font-size: 20px;
}

.hero__advantages {
  display: flex;
  gap: 28px;
  margin-top: 45px;
}

.advantage {
  display: flex;
  align-items: center;
  gap: 10px;
}

.advantage__icon {
  width: 38px;
  height: 38px;

  display: grid;
  place-items: center;

  border-radius: 50%;
  background: #e4f5ef;
  color: #008d69;

  font-weight: 800;
}

.advantage strong,
.advantage span {
  display: block;
}

.advantage strong {
  color: #25332d;
  font-size: 13px;
}

.advantage span {
  margin-top: 3px;
  color: #7a8781;
  font-size: 11px;
}

.hero__visual {
  position: relative;
  min-height: 570px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.hero__circle {
  position: absolute;
  border-radius: 50%;
}

.hero__circle--large {
  width: 470px;
  height: 470px;
  background: linear-gradient(145deg, #d9f3eb, #b7e5d6);
  box-shadow:
    inset 0 0 0 25px rgba(255, 255, 255, 0.35),
    0 25px 60px rgba(20, 100, 78, 0.12);
}

.hero__circle--small {
  width: 270px;
  height: 270px;
  background: rgba(255, 255, 255, 0.7);
}

.hero__water-drop {
  position: relative;
  z-index: 2;

  width: 250px;
  height: 310px;

  display: grid;
  place-items: center;

  transform: rotate(-8deg);
}

.drop {
  width: 190px;
  height: 250px;

  display: grid;
  place-items: center;

  border-radius: 65% 35% 60% 40% / 60% 45% 55% 40%;

  background: linear-gradient(
    145deg,
    #00b889,
    #007b5e
  );

  box-shadow:
    -20px 20px 0 rgba(0, 111, 84, 0.08),
    0 35px 55px rgba(0, 125, 93, 0.22);

  transform: rotate(12deg);
}

.drop span {
  font-size: 90px;
  filter: grayscale(1) brightness(0) invert(1);
}

.floating-card {
  position: absolute;
  z-index: 4;

  display: flex;
  align-items: center;
  gap: 12px;

  padding: 15px 19px;

  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 17px;

  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 18px 45px rgba(27, 83, 66, 0.12);

  backdrop-filter: blur(12px);
}

.floating-card--top {
  top: 90px;
  right: -5px;
}

.floating-card--bottom {
  bottom: 95px;
  left: -10px;
}

.floating-card__icon {
  width: 43px;
  height: 43px;

  display: grid;
  place-items: center;

  border-radius: 13px;
  background: #e4f5ef;
  color: #008d69;

  font-weight: 800;
}

.floating-card strong,
.floating-card span {
  display: block;
}

.floating-card strong {
  color: #23332c;
  font-size: 14px;
}

.floating-card span {
  margin-top: 4px;
  color: #7b8982;
  font-size: 11px;
}

.services-preview {
  padding: 100px 0;
  background: white;
}

.services-preview__container {
  width: min(1200px, calc(100% - 40px));
  margin: 0 auto;
}

.section-heading {
  max-width: 650px;
  margin-bottom: 42px;
}

.section-heading > span {
  color: #00966f;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 2px;
}

.section-heading h2 {
  margin: 10px 0 12px;

  color: #17231e;
  font-size: clamp(30px, 4vw, 44px);
  line-height: 1.12;
  letter-spacing: -1.5px;
}

.section-heading p {
  color: #718078;
  font-size: 16px;
}

.service-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

.service-card {
  padding: 27px;

  border: 1px solid #e3ece8;
  border-radius: 20px;

  background: #fbfdfc;

  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    border-color 0.2s ease;
}

.service-card:hover {
  transform: translateY(-5px);
  border-color: #b8ded2;
  box-shadow: 0 18px 40px rgba(24, 95, 75, 0.08);
}

.service-card__icon {
  width: 50px;
  height: 50px;

  display: grid;
  place-items: center;

  margin-bottom: 22px;

  border-radius: 15px;
  background: #e6f6f0;

  font-size: 22px;
}

.service-card h3 {
  margin: 0 0 10px;

  color: #24322c;
  font-size: 17px;
}

.service-card p {
  margin: 0;

  color: #77847e;
  font-size: 14px;
  line-height: 1.6;
}

@media (max-width: 1000px) {
  .hero__container {
    grid-template-columns: 1fr;
    min-height: auto;
  }

  .hero__content {
    padding: 70px 0 30px;
    text-align: center;
  }

  .hero__badge,
  .hero__actions,
  .hero__advantages {
    justify-content: center;
  }

  .hero__description {
    margin-left: auto;
    margin-right: auto;
  }

  .hero__visual {
    min-height: 500px;
  }

  .service-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 650px) {
  .hero__container,
  .services-preview__container {
    width: min(100% - 28px, 1200px);
  }

  .hero h1 {
    font-size: 42px;
    letter-spacing: -1.8px;
  }

  .hero__description {
    font-size: 16px;
  }

  .hero__actions {
    flex-direction: column;
  }

  .hero__button {
    width: 100%;
  }

  .hero__advantages {
    flex-direction: column;
    align-items: flex-start;
    width: fit-content;
    margin-left: auto;
    margin-right: auto;
  }

  .hero__visual {
    min-height: 410px;
  }

  .hero__circle--large {
    width: 330px;
    height: 330px;
  }

  .hero__circle--small {
    width: 190px;
    height: 190px;
  }

  .drop {
    width: 130px;
    height: 180px;
  }

  .drop span {
    font-size: 65px;
  }

  .floating-card {
    padding: 11px 13px;
  }

  .floating-card--top {
    top: 30px;
    right: 0;
  }

  .floating-card--bottom {
    bottom: 25px;
    left: 0;
  }

  .service-cards {
    grid-template-columns: 1fr;
  }

  .services-preview {
    padding: 70px 0;
  }
}

.hero__tap {
  display: block;
  width: 68%;
  height: auto;
  object-fit: contain;
  position: relative;
  z-index: 2;
  transform: scaleX(-1);
}



/* HOME — VALUES / BUSINESS / GUARANTEES */

.home-values,
.home-business,
.home-guarantees {
  padding: 110px 24px;
}

.home-values {
  background: #f7fbf8;
}

.home-values__inner,
.home-business__inner,
.home-guarantees__inner {
  width: min(1180px, 100%);
  margin: 0 auto;
}

.home-section-heading {
  max-width: 720px;
  margin-bottom: 52px;
}

.home-section-heading__eyebrow {
  display: inline-block;
  margin-bottom: 14px;
  color: #16834f;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: .12em;
  text-transform: uppercase;
}

.home-section-heading h2,
.home-business h2 {
  margin: 0 0 16px;
  color: #173d2b;
  font-size: clamp(34px, 4vw, 52px);
  line-height: 1.05;
  letter-spacing: -.03em;
}

.home-section-heading p {
  margin: 0;
  color: #64746b;
  font-size: 17px;
  line-height: 1.7;
}

.home-values__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
}

.home-values__card {
  display: flex;
  gap: 20px;
  padding: 30px;
  border: 1px solid rgba(22, 131, 79, .10);
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 16px 45px rgba(21, 67, 45, .07);
}

.home-values__icon {
  flex: 0 0 52px;
  width: 52px;
  height: 52px;
  display: grid;
  place-items: center;
  border-radius: 16px;
  background: #e5f5eb;
  color: #16834f;
  font-size: 23px;
  font-weight: 800;
}

.home-values__card h3,
.home-guarantees__card h3 {
  margin: 0 0 10px;
  color: #173d2b;
  font-size: 20px;
}

.home-values__card p,
.home-guarantees__card p,
.home-business p {
  margin: 0;
  color: #68766e;
  font-size: 15px;
  line-height: 1.7;
}


/* BUSINESS */

.home-business {
  background:
    radial-gradient(
      circle at 85% 25%,
      rgba(188, 231, 207, .45),
      transparent 35%
    ),
    #edf8f1;
}

.home-business__inner {
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) minmax(280px, .7fr);
  gap: 70px;
  align-items: center;
}

.home-business__lead {
  max-width: 760px;
  margin-bottom: 20px !important;
  color: #315644 !important;
  font-size: 20px !important;
  line-height: 1.55 !important;
}

.home-business__content > p:not(.home-business__lead) {
  max-width: 760px;
  margin-bottom: 18px;
}

.home-business__features {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 30px;
}

.home-business__features span {
  padding: 10px 16px;
  border-radius: 999px;
  background: #fff;
  color: #16834f;
  font-size: 14px;
  font-weight: 700;
  box-shadow: 0 8px 25px rgba(21, 67, 45, .06);
}

.home-business__side {
  padding: 38px;
  border-radius: 28px;
  background: #173d2b;
  color: #fff;
  box-shadow: 0 24px 60px rgba(23, 61, 43, .20);
}

.home-business__number {
  margin-bottom: 22px;
  color: #9fe0b8;
  font-size: 54px;
  font-weight: 900;
  letter-spacing: -.05em;
}

.home-business__side h3 {
  margin: 0 0 14px;
  font-size: 25px;
  line-height: 1.2;
}

.home-business__side p {
  color: rgba(255, 255, 255, .72);
}


/* GUARANTEES */

.home-guarantees {
  background: #fff;
}

.home-guarantees__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
}

.home-guarantees__card {
  position: relative;
  min-height: 250px;
  padding: 32px;
  border: 1px solid #e5eee8;
  border-radius: 24px;
  background: #fff;
  box-shadow: 0 14px 40px rgba(21, 67, 45, .06);
}

.home-guarantees__index {
  display: block;
  margin-bottom: 35px;
  color: #16834f;
  font-size: 14px;
  font-weight: 900;
  letter-spacing: .12em;
}


/* RESPONSIVE */

@media (max-width: 900px) {
  .home-values__grid,
  .home-guarantees__grid {
    grid-template-columns: 1fr;
  }

  .home-business__inner {
    grid-template-columns: 1fr;
    gap: 40px;
  }
}

@media (max-width: 600px) {
  .home-values,
  .home-business,
  .home-guarantees {
    padding: 75px 18px;
  }

  .home-values__card {
    padding: 24px;
  }

  .home-business__side {
    padding: 28px;
  }

  .home-guarantees__card {
    min-height: auto;
    padding: 26px;
  }
}



/* ===== FIX: карточки услуг не растягиваем ===== */

.service-cards {
  align-items: start !important;
  grid-auto-rows: auto !important;
}

.service-card {
  height: auto !important;
  min-height: 250px !important;
  align-self: start !important;
}

.service-card__content {
  flex: none !important;
}



/* ===== FIX: кнопка всех услуг ===== */

.services-preview__footer {
  display: flex;
  justify-content: center;
  margin-top: 36px;
}

.services-preview__all-link {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 22px;
  border-radius: 12px;
  background: #00966f;
  color: #ffffff;
  text-decoration: none;
  font-size: 14px;
  font-weight: 700;
  transition:
    transform 0.2s ease,
    background 0.2s ease,
    box-shadow 0.2s ease;
}

.services-preview__all-link:hover {
  background: #007d5d;
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(0, 150, 111, 0.18);
}

.services-preview__all-link svg {
  transition: transform 0.2s ease;
}

.services-preview__all-link:hover svg {
  transform: translateX(3px);
}



/* ===== HOME DISCOUNT ===== */

.home-discount {
  padding: 72px 0;
  background: #f2faf6;
}

.home-discount__inner {
  width: min(1200px, calc(100% - 40px));
  margin: 0 auto;
  display: grid;
  grid-template-columns: 190px minmax(0, 1fr);
  align-items: center;
  gap: 48px;
  padding: 42px 48px;
  border: 1px solid #cfe9dc;
  border-radius: 28px;
  background:
    radial-gradient(
      circle at 8% 50%,
      rgba(0, 150, 111, 0.12),
      transparent 32%
    ),
    #ffffff;
  box-shadow: 0 18px 50px rgba(24, 95, 75, 0.07);
}

.home-discount__badge {
  width: 160px;
  height: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #00966f;
  color: #ffffff;
  box-shadow: 0 18px 35px rgba(0, 150, 111, 0.2);
}

.home-discount__badge span {
  font-size: 38px;
  line-height: 1;
  font-weight: 800;
  letter-spacing: -2px;
}

.home-discount__badge small {
  margin-top: 8px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 2px;
}

.home-discount__content {
  max-width: 780px;
}

.home-discount__content .home-section-heading__eyebrow {
  display: block;
  margin-bottom: 10px;
  color: #00966f;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 2px;
}

.home-discount__content h2 {
  margin: 0 0 16px;
  color: #17231e;
  font-size: clamp(28px, 4vw, 42px);
  line-height: 1.12;
  letter-spacing: -1.5px;
}

.home-discount__content p {
  margin: 0 0 10px;
  color: #68766f;
  font-size: 15px;
  line-height: 1.7;
}

.home-discount__content p:last-child {
  margin-bottom: 0;
}

@media (max-width: 800px) {
  .home-discount {
    padding: 60px 0;
  }

  .home-discount__inner {
    grid-template-columns: 1fr;
    gap: 28px;
    padding: 36px 28px;
    text-align: center;
  }

  .home-discount__badge {
    width: 130px;
    height: 130px;
    margin: 0 auto;
  }

  .home-discount__badge span {
    font-size: 32px;
  }

  .home-discount__content {
    max-width: none;
  }
}

@media (max-width: 560px) {
  .home-discount__inner {
    width: min(100% - 28px, 1200px);
    padding: 30px 20px;
    border-radius: 22px;
  }

  .home-discount__content h2 {
    font-size: 28px;
  }
}


/* ============================================================
   HOME HERO — FINAL MOBILE
   ============================================================ */

@media (max-width: 650px) {

  .hero {
    width: 100%;
    overflow: hidden;
  }

  .hero__container {
    width: calc(100% - 24px) !important;
    max-width: none !important;
    margin: 0 auto;

    display: flex !important;
    flex-direction: column;

    min-height: 0 !important;

    gap: 0 !important;
  }

  /* ----------------------------------------------------------
     CONTENT
     ---------------------------------------------------------- */

  .hero__content {
    width: 100%;
    max-width: none !important;

    padding: 30px 0 0 !important;

    text-align: left !important;
  }

  .hero__badge {
    width: 100%;
    max-width: 100%;

    box-sizing: border-box;

    justify-content: flex-start;

    padding: 9px 12px;

    font-size: 10px;

    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;

    border-radius: 999px;
  }

  .hero__badge span {
    width: 6px;
    height: 6px;
    flex: 0 0 6px;
  }

  .hero h1 {
    width: 100%;
    max-width: 100% !important;

    margin: 20px 0 0 !important;

    font-size: 36px !important;
    line-height: 1.02 !important;
    letter-spacing: -1.7px !important;

    overflow-wrap: normal;
    word-break: normal;
  }

  .hero h1 strong {
    display: block;
  }

  .hero__description {
    width: 100%;
    max-width: 100% !important;

    margin: 17px 0 0 !important;

    font-size: 13px !important;
    line-height: 1.55 !important;

    color: #66756e;
  }

  /* ----------------------------------------------------------
     BUTTONS
     ---------------------------------------------------------- */

  .hero__actions {
    width: 100%;

    display: flex !important;
    flex-direction: column !important;

    gap: 8px !important;

    margin-top: 20px !important;
  }

  .hero__button {
    width: 100% !important;
    min-height: 48px;

    box-sizing: border-box;

    padding: 0 18px;

    border-radius: 11px;

    font-size: 12px;
  }

  .hero__button--primary {
    justify-content: center;
  }

  .hero__button--secondary {
    justify-content: center;
  }

  /* ----------------------------------------------------------
     ADVANTAGES
     ---------------------------------------------------------- */

  .hero__advantages {
    width: 100% !important;

    display: grid !important;
    grid-template-columns: 1fr;

    gap: 10px !important;

    margin: 23px 0 0 !important;

    align-items: stretch !important;
  }

  .advantage {
    width: 100%;

    display: flex;

    align-items: center;

    gap: 10px;
  }

  .advantage__icon {
    width: 34px;
    height: 34px;

    flex: 0 0 34px;
  }

  .advantage strong {
    font-size: 11px;
  }

  .advantage span {
    margin-top: 2px;

    font-size: 9px;
  }


  /* ----------------------------------------------------------
     VISUAL
     ---------------------------------------------------------- */

  .hero__visual {
    width: 100%;

    min-height: 300px !important;
    height: 300px;

    margin-top: 18px;

    position: relative;

    overflow: hidden;
  }

  .hero__circle--large {
    width: 270px !important;
    height: 270px !important;

    right: 50%;
    bottom: -135px;

    transform: translateX(50%);
  }

  .hero__circle--small {
    width: 145px !important;
    height: 145px !important;

    left: -42px;
    top: 22px;
  }

  .hero__water-drop {
    position: absolute;

    left: 50%;
    top: 50%;

    transform: translate(-50%, -50%);
  }

  .drop {
    width: 105px !important;
    height: 145px !important;

    border-radius: 55% 45% 55% 45%;
  }

  .drop span {
    font-size: 52px !important;
  }

  .hero__tap {
    width: 72% !important;
  }

  /* ----------------------------------------------------------
     FLOATING CARDS
     ---------------------------------------------------------- */

  .floating-card {
    z-index: 5;

    min-width: 0 !important;

    padding: 10px 12px !important;

    border-radius: 12px;

    box-sizing: border-box;
  }

  .floating-card strong {
    font-size: 10px;
  }

  .floating-card span {
    font-size: 8px;
  }

  .floating-card__icon {
    width: 30px;
    height: 30px;
  }

  .floating-card--top {
    top: 24px !important;
    right: 0 !important;
  }

  .floating-card--bottom {
    bottom: 20px !important;
    left: 0 !important;
  }
}


/* ============================================================
   iPHONE / SMALL MOBILE
   ============================================================ */

@media (max-width: 430px) {

  .hero__container {
    width: calc(100% - 20px) !important;
  }

  .hero__content {
    padding-top: 25px !important;
  }

  .hero__badge {
    padding: 8px 10px;
    font-size: 9px;
  }

  .hero h1 {
    font-size: 34px !important;
    line-height: 1.01 !important;
    letter-spacing: -1.5px !important;

    margin-top: 18px !important;
  }

  .hero__description {
    font-size: 12px !important;
    line-height: 1.5 !important;

    margin-top: 14px !important;
  }

  .hero__actions {
    margin-top: 17px !important;
  }

  .hero__button {
    min-height: 47px;
  }

  .hero__advantages {
    margin-top: 20px !important;
    gap: 9px !important;
  }

  .hero__visual {
    height: 275px;
    min-height: 275px !important;

    margin-top: 14px;
  }

  .hero__circle--large {
    width: 245px !important;
    height: 245px !important;

    bottom: -125px;
  }

  .hero__circle--small {
    width: 125px !important;
    height: 125px !important;

    left: -38px;
    top: 20px;
  }

  .drop {
    width: 95px !important;
    height: 132px !important;
  }

  .floating-card--top {
    top: 18px !important;
  }

  .floating-card--bottom {
    bottom: 16px !important;
  }
}

</style>
