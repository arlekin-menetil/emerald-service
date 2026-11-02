<script setup>
import { useLanguage } from '../composables/useLanguage'

import {
  ArrowRight,
  Bot,
  Check,
  Clock3,
  MapPin,
  MessageCircle,
  Phone,
  Send,
  Star,
  Wrench,
} from '@lucide/vue'

const features = [
  {
    icon: Wrench,
    title: 'telegram.feature.service.title',
    text: 'telegram.feature.service.text',
  },
  {
    icon: MapPin,
    title: 'telegram.feature.address.title',
    text: 'telegram.feature.address.text',
  },
  {
    icon: Clock3,
    title: 'telegram.feature.fast.title',
    text: 'telegram.feature.fast.text',
  },
  {
    icon: Star,
    title: 'telegram.feature.rating.title',
    text: 'telegram.feature.rating.text',
  },
]


const steps = [
  {
    number: '01',
    title: 'telegram.step.open.title',
    text: 'telegram.step.open.text',
  },
  {
    number: '02',
    title: 'telegram.step.service.title',
    text: 'telegram.step.service.text',
  },
  {
    number: '03',
    title: 'telegram.step.request.title',
    text: 'telegram.step.request.text',
  },
  {
    number: '04',
    title: 'telegram.step.wait.title',
    text: 'telegram.step.wait.text',
  },
]
const { t } = useLanguage()

</script>

<template>
  <main class="telegram-page">

    <!-- HERO -->
    <section class="telegram-hero">
      <div class="telegram-container telegram-hero__grid">

        <div class="telegram-hero__content">

          <div class="telegram-badge">
            <span class="telegram-badge__dot"></span>
            {{ t('telegram.page.eyebrow') }}
          </div>

          <h1>
            {{ t('telegram.page.title') }}
            <span>{{ t('telegram.page.title_accent') }}</span>
          </h1>

          <p>
            {{ t('telegram.page.description') }}
          </p>

          <div class="telegram-hero__actions">
            <a
              href="#how-it-works"
              class="telegram-button telegram-button--primary"
            >
              {{ t('telegram.page.button_how') }}
              <ArrowRight :size="18" />
            </a>

            <a
              href="#features"
              class="telegram-button telegram-button--secondary"
            >
              {{ t('telegram.page.button_features') }}
            </a>
          </div>

          <div class="telegram-hero__trust">
            <div>
              <Check :size="16" />
              <span>{{ t('telegram.page.trust.fast') }}</span>
            </div>

            <div>
              <Check :size="16" />
              <span>{{ t('telegram.page.trust.no_calls') }}</span>
            </div>

            <div>
              <Check :size="16" />
              <span>{{ t('telegram.page.trust.24_7') }}</span>
            </div>
          </div>

        </div>

        <!-- TELEGRAM PHONE -->
        <div class="telegram-hero__visual">

          <div class="telegram-orbit telegram-orbit--one"></div>
          <div class="telegram-orbit telegram-orbit--two"></div>

          <div class="telegram-phone">

            <div class="telegram-phone__top">
              <div class="telegram-phone__camera"></div>
              <span>Telegram</span>
            </div>

            <div class="telegram-phone__header">

              <div class="telegram-phone__avatar">
                <Bot :size="25" />
              </div>

              <div class="telegram-phone__identity">
                <strong>{{ t('telegram.bot_name') }}</strong>
                <span>{{ t('telegram.phone.online') }}</span>
              </div>

              <MessageCircle :size="19" />

            </div>

            <div class="telegram-phone__chat">

              <div class="telegram-message telegram-message--bot">
                <span class="telegram-message__time">
                  20:41
                </span>

                <strong>
                  {{ t('telegram.phone.greeting') }}
                </strong>

                <p>
                  {{ t('telegram.phone.question') }}
                </p>
              </div>

              <div class="telegram-options">

                <div class="telegram-option">
                  <Wrench :size="16" />
                  <span>{{ t('telegram.bot.repair') }}</span>
                </div>

                <div class="telegram-option">
                  <Wrench :size="16" />
                  <span>{{ t('telegram.bot.installation') }}</span>
                </div>

                <div class="telegram-option">
                  <MapPin :size="16" />
                  <span>{{ t('telegram.bot.sewerage') }}</span>
                </div>

                <div class="telegram-option">
                  <Phone :size="16" />
                  <span>{{ t('telegram.bot.heating') }}</span>
                </div>

              </div>

              <div class="telegram-message telegram-message--user">
                {{ t('telegram.phone.user_message') }}
                <span>20:42</span>
              </div>

              <div class="telegram-message telegram-message--bot">
                <strong>
                  {{ t('telegram.phone.request_accepted') }} 👍
                </strong>

                <p>
                  {{ t('telegram.phone.address_request') }}
                </p>

                <span class="telegram-message__time">
                  20:42
                </span>
              </div>

            </div>

            <div class="telegram-phone__input">
              <span>{{ t('telegram.phone.message_placeholder') }}</span>
              <div class="telegram-phone__send">
                <Send :size="16" />
              </div>
            </div>

          </div>

          <div class="telegram-floating-card telegram-floating-card--top">
            <div class="telegram-floating-card__icon">
              <Check :size="16" />
            </div>

            <div>
              <strong>{{ t('telegram.phone.request_accepted') }}</strong>
              <span>{{ t('telegram.bot_name') }}</span>
            </div>
          </div>

          <div class="telegram-floating-card telegram-floating-card--bottom">
            <div class="telegram-floating-card__icon">
              <Clock3 :size="16" />
            </div>

            <div>
              <strong>24/7</strong>
              <span>{{ t('telegram.phone.requests_24_7') }}</span>
            </div>
          </div>

        </div>

      </div>
    </section>

    <!-- FEATURES -->
    <section
      id="features"
      class="telegram-features"
    >
      <div class="telegram-container">

        <div class="telegram-heading">
          <span>{{ t('telegram.features.eyebrow') }}</span>

          <h2>
            {{ t('telegram.features.title') }}
            <strong>{{ t('telegram.features.title_accent') }}</strong>
          </h2>

          <p>
            {{ t('telegram.features.description') }}
          </p>
        </div>

        <div class="telegram-features__grid">

          <article
            v-for="feature in features"
            :key="feature.title"
            class="telegram-feature"
          >
            <div class="telegram-feature__icon">
              <component
                :is="feature.icon"
                :size="23"
              />
            </div>

            <h3>
              {{ t(feature.title) }}
            </h3>

            <p>
              {{ t(feature.text) }}
            </p>
          </article>

        </div>

      </div>
    </section>

    <!-- HOW IT WORKS -->
    <section
      id="how-it-works"
      class="telegram-process"
    >
      <div class="telegram-container">

        <div class="telegram-heading telegram-heading--center">
          <span>{{ t('telegram.process.eyebrow') }}</span>

          <h2>
            {{ t('telegram.process.title') }}
            <strong>{{ t('telegram.process.title_accent') }}</strong>
          </h2>

          <p>
            {{ t('telegram.process.description') }}
          </p>
        </div>

        <div class="telegram-steps">

          <article
            v-for="step in steps"
            :key="step.number"
            class="telegram-step"
          >
            <div class="telegram-step__number">
              {{ step.number }}
            </div>

            <div class="telegram-step__line"></div>

            <h3>
              {{ t(step.title) }}
            </h3>

            <p>
              {{ t(step.text) }}
            </p>
          </article>

        </div>

      </div>
    </section>

    <!-- CTA -->
    <section class="telegram-cta">
      <div class="telegram-container">

        <div class="telegram-cta__inner">

          <div class="telegram-cta__icon">
            <Send :size="30" />
          </div>

          <div class="telegram-cta__content">
            <span>{{ t('telegram.cta.eyebrow') }}</span>

            <h2>
              {{ t('telegram.cta.title') }}
              <strong>{{ t('telegram.cta.title_accent') }}</strong>
            </h2>

            <p>
              {{ t('telegram.cta.description') }}
            </p>
          </div>

          <a
            href="https://t.me/EmeraldServiceOrdersBot"
            class="telegram-button telegram-button--white"
                    >
            {{ t('telegram.cta.button') }}
            <ArrowRight :size="18" />
          </a>

        </div>

      </div>
    </section>

  </main>
</template>

<style scoped>
.telegram-page {
  min-height: 100vh;
  background: #f7fbf8;
  color: #15221c;
}

.telegram-container {
  width: min(1200px, calc(100% - 40px));
  margin: 0 auto;
}

/* HERO */

.telegram-hero {
  position: relative;
  overflow: hidden;
  padding: 82px 0 100px;

  background:
    radial-gradient(
      circle at 75% 45%,
      rgba(184, 232, 205, 0.52),
      transparent 38%
    ),
    linear-gradient(
      180deg,
      #f5fbf7 0%,
      #ffffff 100%
    );
}

.telegram-hero::before {
  content: "";
  position: absolute;
  width: 560px;
  height: 560px;
  right: -180px;
  top: -180px;
  border: 1px solid rgba(0, 140, 104, 0.08);
  border-radius: 50%;
}

.telegram-hero__grid {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 0.9fr;
  align-items: center;
  gap: 70px;
}

.telegram-hero__content {
  max-width: 620px;
}

.telegram-badge {
  display: inline-flex;
  align-items: center;
  gap: 9px;

  margin-bottom: 24px;

  color: #008c68;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.18em;
}

.telegram-badge__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #00a878;
  box-shadow: 0 0 0 5px rgba(0, 168, 120, 0.1);
}

.telegram-hero h1 {
  max-width: 650px;
  margin: 0;

  font-size: clamp(46px, 5vw, 72px);
  line-height: 0.98;
  letter-spacing: -0.055em;
  font-weight: 800;
}

.telegram-hero h1 span {
  display: block;
  color: #009b70;
}

.telegram-hero p {
  max-width: 570px;
  margin: 30px 0 0;

  color: #64736b;
  font-size: 17px;
  line-height: 1.75;
}

.telegram-hero__actions {
  display: flex;
  gap: 12px;
  margin-top: 34px;
}

.telegram-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;

  min-height: 50px;
  padding: 0 22px;

  border-radius: 12px;

  font-size: 14px;
  font-weight: 700;

  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.telegram-button:hover {
  transform: translateY(-2px);
}

.telegram-button--primary {
  color: #fff;
  background: #009b70;
  box-shadow: 0 12px 28px rgba(0, 155, 112, 0.2);
}

.telegram-button--secondary {
  color: #34443c;
  background: #fff;
  border: 1px solid #dce9e2;
}

.telegram-hero__trust {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;

  margin-top: 30px;
}

.telegram-hero__trust div {
  display: flex;
  align-items: center;
  gap: 7px;

  color: #6c7a73;
  font-size: 12px;
}

.telegram-hero__trust svg {
  color: #009b70;
}

/* PHONE */

.telegram-hero__visual {
  position: relative;
  min-height: 610px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.telegram-orbit {
  position: absolute;
  border: 1px solid rgba(0, 155, 112, 0.1);
  border-radius: 50%;
}

.telegram-orbit--one {
  width: 500px;
  height: 500px;
}

.telegram-orbit--two {
  width: 390px;
  height: 390px;
}

.telegram-phone {
  position: relative;
  z-index: 2;

  width: 310px;
  height: 590px;

  overflow: hidden;

  border: 8px solid #17251f;
  border-radius: 38px;

  background: #f2f7f4;

  box-shadow:
    0 35px 80px rgba(28, 72, 54, 0.18),
    0 8px 20px rgba(28, 72, 54, 0.1);
}

.telegram-phone__top {
  height: 31px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: #68766f;
  font-size: 9px;

  background: #fff;
}

.telegram-phone__camera {
  position: absolute;
  top: 8px;
  left: 50%;
  width: 55px;
  height: 15px;
  transform: translateX(-50%);
  border-radius: 20px;
  background: #17251f;
}

.telegram-phone__header {
  display: flex;
  align-items: center;
  gap: 10px;

  padding: 13px 15px;

  color: #fff;
  background: #008c68;
}

.telegram-phone__avatar {
  width: 38px;
  height: 38px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;
  background: rgba(255, 255, 255, 0.18);
}

.telegram-phone__identity {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.telegram-phone__identity strong {
  font-size: 12px;
}

.telegram-phone__identity span {
  margin-top: 2px;
  font-size: 9px;
  opacity: 0.72;
}

.telegram-phone__chat {
  height: 440px;
  padding: 15px 12px;

  display: flex;
  flex-direction: column;
  gap: 10px;

  background:
    radial-gradient(
      circle at 30% 20%,
      rgba(0, 155, 112, 0.06),
      transparent 35%
    ),
    #eef5f1;
}

.telegram-message {
  position: relative;
  max-width: 85%;
  padding: 11px 12px;

  border-radius: 13px;

  font-size: 11px;
  line-height: 1.45;
}

.telegram-message strong {
  display: block;
  margin-bottom: 4px;
}

.telegram-message p {
  margin: 0;
  color: #617069;
}

.telegram-message--bot {
  align-self: flex-start;
  background: #fff;
  box-shadow: 0 3px 10px rgba(20, 70, 50, 0.05);
}

.telegram-message--user {
  align-self: flex-end;
  color: #fff;
  background: #008c68;
}

.telegram-message--user span {
  margin-left: 7px;
  font-size: 8px;
  opacity: 0.7;
}

.telegram-message__time {
  display: block;
  margin-top: 5px;

  color: #9ba8a2;
  font-size: 8px;
  text-align: right;
}

.telegram-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}

.telegram-option {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;

  min-height: 34px;

  color: #008c68;
  font-size: 9px;
  font-weight: 700;

  border: 1px solid rgba(0, 140, 104, 0.18);
  border-radius: 8px;
  background: #fff;
}

.telegram-phone__input {
  display: flex;
  align-items: center;
  justify-content: space-between;

  height: 52px;
  padding: 0 10px 0 14px;

  color: #a1ada7;
  font-size: 10px;

  background: #fff;
  border-top: 1px solid #e0e9e4;
}

.telegram-phone__send {
  width: 32px;
  height: 32px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: #fff;
  border-radius: 50%;
  background: #009b70;
}

/* FLOATING CARDS */

.telegram-floating-card {
  position: absolute;
  z-index: 4;

  display: flex;
  align-items: center;
  gap: 10px;

  padding: 11px 14px;

  border: 1px solid rgba(0, 140, 104, 0.08);
  border-radius: 13px;

  background: rgba(255, 255, 255, 0.94);

  box-shadow: 0 14px 35px rgba(24, 72, 51, 0.12);

  backdrop-filter: blur(12px);
}

.telegram-floating-card--top {
  top: 92px;
  right: 0;
}

.telegram-floating-card--bottom {
  bottom: 85px;
  left: 0;
}

.telegram-floating-card__icon {
  width: 32px;
  height: 32px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: #fff;
  border-radius: 9px;
  background: #009b70;
}

.telegram-floating-card div:last-child {
  display: flex;
  flex-direction: column;
}

.telegram-floating-card strong {
  font-size: 11px;
}

.telegram-floating-card span {
  margin-top: 3px;
  color: #89958f;
  font-size: 9px;
}

/* HEADINGS */

.telegram-features,
.telegram-process {
  padding: 110px 0;
}

.telegram-heading {
  max-width: 650px;
  margin-bottom: 50px;
}

.telegram-heading--center {
  margin-right: auto;
  margin-left: auto;
  text-align: center;
}

.telegram-heading > span {
  color: #008c68;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.18em;
}

.telegram-heading h2 {
  margin: 14px 0 0;

  font-size: clamp(34px, 4vw, 48px);
  line-height: 1.05;
  letter-spacing: -0.04em;
}

.telegram-heading h2 strong {
  color: #009b70;
}

.telegram-heading p {
  margin: 18px 0 0;

  color: #6b7972;
  line-height: 1.7;
}

/* FEATURES */

.telegram-features {
  background: #fff;
}

.telegram-features__grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}

.telegram-feature {
  padding: 28px;

  border: 1px solid #e2ece6;
  border-radius: 18px;

  background: #fbfdfc;

  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.telegram-feature:hover {
  transform: translateY(-4px);
  box-shadow: 0 18px 35px rgba(25, 80, 55, 0.08);
}

.telegram-feature__icon {
  width: 48px;
  height: 48px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: #009b70;
  border-radius: 13px;
  background: #e6f6ee;
}

.telegram-feature h3 {
  margin: 24px 0 10px;
  font-size: 17px;
}

.telegram-feature p {
  margin: 0;
  color: #718078;
  font-size: 13px;
  line-height: 1.65;
}

/* PROCESS */

.telegram-process {
  background:
    linear-gradient(
      180deg,
      #f7fbf8 0%,
      #eef8f2 100%
    );
}

.telegram-steps {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 25px;
}

.telegram-step {
  position: relative;
}

.telegram-step__number {
  width: 52px;
  height: 52px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: #008c68;
  font-size: 12px;
  font-weight: 800;

  border: 1px solid #cfe6da;
  border-radius: 50%;
  background: #fff;
}

.telegram-step__line {
  position: absolute;
  top: 26px;
  left: 52px;
  right: -25px;

  height: 1px;

  background: #d6e8de;
}

.telegram-step:last-child .telegram-step__line {
  display: none;
}

.telegram-step h3 {
  margin: 25px 0 9px;
  font-size: 17px;
}

.telegram-step p {
  margin: 0;
  color: #718078;
  font-size: 13px;
  line-height: 1.65;
}

/* CTA */

.telegram-cta {
  padding: 80px 0;
}

.telegram-cta__inner {
  position: relative;
  overflow: hidden;

  display: flex;
  align-items: center;
  gap: 24px;

  padding: 48px 55px;

  color: #fff;
  border-radius: 25px;

  background:
    radial-gradient(
      circle at 80% 20%,
      rgba(255, 255, 255, 0.14),
      transparent 30%
    ),
    linear-gradient(
      135deg,
      #008c68,
      #006f53
    );

  box-shadow: 0 25px 60px rgba(0, 110, 80, 0.2);
}

.telegram-cta__icon {
  width: 62px;
  height: 62px;

  display: flex;
  align-items: center;
  justify-content: center;

  flex-shrink: 0;

  border-radius: 17px;
  background: rgba(255, 255, 255, 0.13);
}

.telegram-cta__content {
  flex: 1;
}

.telegram-cta__content > span {
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.18em;
  opacity: 0.7;
}

.telegram-cta h2 {
  margin: 7px 0;
  font-size: 30px;
}

.telegram-cta h2 strong {
  color: #bff0d8;
}

.telegram-cta p {
  margin: 0;
  max-width: 520px;
  color: rgba(255, 255, 255, 0.75);
  font-size: 13px;
  line-height: 1.6;
}

.telegram-button--white {
  flex-shrink: 0;
  color: #008c68;
  background: #fff;
}

/* RESPONSIVE */

@media (max-width: 1000px) {
  .telegram-hero__grid {
    grid-template-columns: 1fr;
  }

  .telegram-hero__content {
    max-width: 700px;
  }

  .telegram-hero__visual {
    min-height: 620px;
  }

  .telegram-features__grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .telegram-steps {
    grid-template-columns: repeat(2, 1fr);
    row-gap: 45px;
  }

  .telegram-step:nth-child(2) .telegram-step__line {
    display: none;
  }
}

@media (max-width: 700px) {
  .telegram-hero {
    padding: 55px 0 70px;
  }

  .telegram-hero h1 {
    font-size: 45px;
  }

  .telegram-hero p {
    font-size: 15px;
  }

  .telegram-hero__actions {
    flex-direction: column;
  }

  .telegram-button {
    width: 100%;
  }

  .telegram-hero__visual {
    min-height: 570px;
  }

  .telegram-phone {
    width: 285px;
    height: 550px;
  }

  .telegram-phone__chat {
    height: 400px;
  }

  .telegram-floating-card--top {
    right: -5px;
  }

  .telegram-floating-card--bottom {
    left: -5px;
  }

  .telegram-features,
  .telegram-process {
    padding: 75px 0;
  }

  .telegram-features__grid {
    grid-template-columns: 1fr;
  }

  .telegram-steps {
    grid-template-columns: 1fr;
  }

  .telegram-step__line {
    display: none;
  }

  .telegram-cta__inner {
    flex-direction: column;
    align-items: flex-start;
    padding: 35px 28px;
  }

  .telegram-button--white {
    width: auto;
  }
}

@media (max-width: 480px) {
  .telegram-container {
    width: min(100% - 28px, 1200px);
  }

  .telegram-hero h1 {
    font-size: 39px;
  }

  .telegram-hero__visual {
    min-height: 520px;
  }

  .telegram-phone {
    width: 260px;
    height: 500px;
  }

  .telegram-phone__chat {
    height: 350px;
  }

  .telegram-orbit--one {
    width: 390px;
    height: 390px;
  }

  .telegram-orbit--two {
    width: 315px;
    height: 315px;
  }

  .telegram-floating-card {
    transform: scale(0.86);
  }
}
</style>
