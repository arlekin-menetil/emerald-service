<script setup>
import {
  ArrowRight,
  Wrench,
  ShieldCheck,
  Zap,
  LayoutGrid,
  PhoneCall,
} from '@lucide/vue'

import { useLanguage } from '../../composables/useLanguage'

const { t } = useLanguage()
</script>

<template>
  <section class="services-hero">
    <div class="services-container services-hero__grid">

      <div class="services-hero__content">

        <div class="services-badge">
          <span></span>
          {{ t('services.hero.badge') }}
        </div>

        <h1>
          {{ t('services.hero.title_prefix') }}
          <span>{{ t('services.hero.title_brand') }}</span>
          {{ t('services.hero.title_suffix') }}
        </h1>

        <p>
          {{ t('services.hero.description') }}
        </p>

        <div class="services-hero__actions">

          <RouterLink
            to="/request"
            class="services-button services-button--primary"
          >
            {{ t('services.hero.call') }}
            <ArrowRight :size="18" />
          </RouterLink>

          <a
            href="#all-services"
            class="services-button services-button--secondary"
          >
            {{ t('services.hero.all') }}
          </a>

        </div>

        <div class="services-hero__stats">

          <div class="services-hero__stat">
            <div class="services-hero__stat-main">
              <div class="services-hero__stat-icon">
                <Wrench :size="17" />
              </div>
              <strong>18</strong>
            </div>
            <span>{{ t('services.hero.stats.services') }}</span>
          </div>

          <div class="services-hero__stat">
            <div class="services-hero__stat-main">
              <div class="services-hero__stat-icon">
                <LayoutGrid :size="17" />
              </div>
              <strong>5</strong>
            </div>
            <span>{{ t('services.hero.stats.categories') }}</span>
          </div>

          <div class="services-hero__stat">
            <div class="services-hero__stat-main">
              <div class="services-hero__stat-icon">
                <PhoneCall :size="17" />
              </div>
              <strong>24/7</strong>
            </div>
            <span>{{ t('services.hero.stats.requests') }}</span>
          </div>

        </div>

      </div>

      <div class="services-hero__visual">

        <div class="services-hero__circle services-hero__circle--outer"></div>
        <div class="services-hero__circle services-hero__circle--middle"></div>

        <div class="services-hero__icon">
          <Wrench :size="72" :stroke-width="1.5" />
        </div>

        <div class="services-floating-card services-floating-card--top">
          <div class="services-floating-card__icon">
            <ShieldCheck :size="19" />
          </div>

          <div>
            <strong>{{ t('services.hero.guarantee') }}</strong>
            <span>{{ t('services.hero.guarantee_text') }}</span>
          </div>
        </div>

        <div class="services-floating-card services-floating-card--bottom">
          <div class="services-floating-card__icon">
            <Zap :size="19" />
          </div>

          <div>
            <strong>{{ t('services.hero.fast') }}</strong>
            <span>{{ t('services.hero.fast_text') }}</span>
          </div>
        </div>

      </div>

    </div>
  </section>
</template>

<style scoped>

.services-hero {
  padding: 72px 0 90px;

  background:
    radial-gradient(
      circle at 80% 35%,
      rgba(0, 169, 125, 0.11),
      transparent 34%
    ),
    linear-gradient(
      180deg,
      #ffffff 0%,
      #f5faf8 100%
    );

  overflow: hidden;
}

.services-container {
  width: min(1120px, calc(100% - 48px));
  margin: 0 auto;
  position: relative;
}

.services-hero .services-container {
  display: grid;
  grid-template-columns: 1fr 0.85fr;
  align-items: center;
  gap: 70px;
}

.services-hero__content {
  max-width: 600px;
}

.services-badge {
  display: inline-flex;
  align-items: center;
  gap: 9px;

  padding: 9px 14px;

  border: 1px solid #cde9df;
  border-radius: 999px;

  background: #ffffff;
  color: #008f6b;

  font-size: 13px;
  font-weight: 600;
}

.services-badge span {
  width: 7px;
  height: 7px;

  border-radius: 50%;
  background: #00a77d;
}

.services-hero h1 {
  margin: 25px 0 20px;

  font-size: clamp(42px, 5vw, 68px);
  line-height: 0.98;

  letter-spacing: -2.8px;
  font-weight: 750;
}

.services-hero h1 span {
  display: block;
  color: #00a77d;
}

.services-hero p {
  max-width: 590px;
  margin: 0;

  color: #687871;

  font-size: 17px;
  line-height: 1.7;
}

.services-hero__actions {
  display: flex;
  gap: 12px;
  margin-top: 32px;
}

.services-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;

  min-height: 48px;
  padding: 0 22px;

  border-radius: 10px;

  font-size: 14px;
  font-weight: 700;

  transition: 0.2s ease;
}

.services-button--primary {
  background: #00a77d;
  color: #ffffff;

  box-shadow:
    0 12px 25px rgba(0, 167, 125, 0.2);
}

.services-button--primary:hover {
  background: #008f6b;
  transform: translateY(-2px);
}

.services-button--secondary {
  border: 1px solid #b8ddd2;

  background: #ffffff;
  color: #008f6b;
}

.services-button--secondary:hover {
  border-color: #00a77d;
}

.services-hero__visual {
  position: relative;

  min-height: 440px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.services-hero__circle {
  position: absolute;

  border-radius: 50%;
  transform: rotate(-12deg);
}

.services-hero__circle--outer {
  width: 390px;
  height: 390px;

  background: rgba(0, 167, 125, 0.09);
}

.services-hero__circle--middle {
  width: 285px;
  height: 350px;

  background: rgba(0, 167, 125, 0.22);
}

.services-hero__icon {
  position: relative;
  z-index: 2;

  width: 185px;
  height: 235px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 48% 52% 46% 54%;

  background:
    linear-gradient(
      145deg,
      #00b889,
      #008f6b
    );

  color: #ffffff;

  transform: rotate(-12deg);

  box-shadow:
    0 25px 50px rgba(0, 143, 107, 0.2);
}

.services-hero__icon svg {
  transform: rotate(12deg);
}

.services-floating-card {
  position: absolute;
  z-index: 4;

  display: flex;
  align-items: center;
  gap: 12px;

  padding: 14px 17px;

  border: 1px solid #edf1ef;
  border-radius: 14px;

  background: rgba(255, 255, 255, 0.96);

  box-shadow:
    0 15px 35px rgba(28, 61, 49, 0.1);
}

.services-floating-card--top {
  top: 50px;
  right: -5px;
}

.services-floating-card--bottom {
  bottom: 55px;
  left: 0;
}

.services-floating-card__icon {
  width: 38px;
  height: 38px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 11px;

  background: #e4f5ef;
  color: #00a77d;
}

.services-floating-card strong,
.services-floating-card span {
  display: block;
}

.services-floating-card strong {
  font-size: 13px;
}

.services-floating-card span {
  margin-top: 4px;

  color: #8a9792;
  font-size: 10px;
}

.services-hero__stats {
  display: flex;
  gap: 38px;
  margin-top: 38px;
}

.services-hero__stat {
  display: flex;
  flex-direction: column;
}

.services-hero__stat-main {
  display: flex;
  align-items: center;
  gap: 9px;
}

.services-hero__stat-icon {
  width: 30px;
  height: 30px;

  display: flex;
  align-items: center;
  justify-content: center;

  flex: 0 0 30px;

  border-radius: 8px;

  background: #e4f5ef;
  color: #00a77d;
}

.services-hero__stats strong {
  font-size: 22px;
  line-height: 1;
  color: #111;
}

.services-hero__stats span {
  margin-top: 7px;

  color: #87938e;
  font-size: 11px;
}

@media (max-width: 900px) {

  .services-hero .services-container {
    grid-template-columns: 1fr;
  }

  .services-hero__content {
    max-width: none;
    text-align: center;
  }

  .services-badge,
  .services-hero__actions {
    justify-content: center;
  }

  .services-hero__visual {
    min-height: 390px;
  }
}

@media (max-width: 620px) {

  .services-container {
    width: min(100% - 32px, 1120px);
  }

  .services-hero {
    padding: 65px 0;
  }

  .services-hero h1 {
    font-size: 42px;
    letter-spacing: -1.8px;
  }

  .services-hero__actions {
    flex-direction: column;
  }

  .services-button {
    width: 100%;
  }

  .services-hero__visual {
    min-height: 330px;
  }

  .services-hero__circle--outer {
    width: 300px;
    height: 300px;
  }

  .services-hero__circle--middle {
    width: 220px;
    height: 270px;
  }

  .services-hero__icon {
    width: 145px;
    height: 190px;
  }

  .services-floating-card--top {
    right: -5px;
    top: 20px;
  }

  .services-floating-card--bottom {
    left: -5px;
    bottom: 20px;
  }
}

</style>
