<script setup>
import {
  ArrowRight,
  Banknote,
  Clock3,
  MapPin,
  MessageCircle,
  Phone,
  Send,
  Wrench,
} from '@lucide/vue'

import { ref } from 'vue'
import { useLanguage } from '../composables/useLanguage'

const { t, currentLanguage } = useLanguage()


const vacancyForm = ref({
  name: '',
  phone: '',
  experience: '',
  specialization: '',
  about: '',
})

const vacancySubmitting = ref(false)
const vacancySuccess = ref(false)
const vacancyError = ref('')

const submitVacancyApplication = async () => {
  vacancySuccess.value = false
  vacancyError.value = ''

  const fields = Object.values(vacancyForm.value)

  if (fields.some(value => !String(value).trim())) {
    vacancyError.value = t('contacts.form.required')
    return
  }

  vacancySubmitting.value = true

  try {
    const response = await fetch(
      `${API_BASE}/api/career/applications/`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...vacancyForm.value,
          language: currentLanguage.value,
        }),
      }
    )

    const data = await response.json()

    if (!response.ok) {
      const firstError = Object.values(data || {}).flat()?.[0]
      throw new Error(
        typeof firstError === 'string'
          ? firstError
          : t('contacts.form.error')
      )
    }

    vacancySuccess.value = true

    vacancyForm.value = {
      name: '',
      phone: '',
      experience: '',
      specialization: '',
      about: '',
    }
  } catch (error) {
    console.error('Vacancy application error:', error)
    vacancyError.value = error.message || t('contacts.form.error')
  } finally {
    vacancySubmitting.value = false
  }
}

</script>

<template>
  <main class="contacts-page">

    <!-- HERO -->
    <section class="contacts-hero">
      <div class="contacts-container contacts-hero__inner">
        <div class="contacts-hero__content">
          <div class="contacts-eyebrow">
            <span></span>
            {{ t('contacts.hero.eyebrow') }}
          </div>

          <h1>
            {{ t('contacts.hero.title') }}
          </h1>

          <p>
            {{ t('contacts.hero.description') }}
          </p>

          <div class="contacts-hero__actions">
            <a href="tel:+998777091933" class="contacts-button contacts-button--primary">
              <Phone :size="19" />
              {{ t('contacts.hero.call') }}
            </a>

            <a
              href="https://t.me/EmeraldServiceOrdersBot"
              target="_blank"
              rel="noopener noreferrer"
              class="contacts-button contacts-button--telegram"
            >
              <Send :size="18" />
              {{ t('contacts.hero.telegram') }}
            </a>
          </div>
        </div>

        <div class="contacts-hero__visual">
          <div class="contacts-circle contacts-circle--large"></div>
          <div class="contacts-circle contacts-circle--small"></div>

          <div class="contacts-hero-card">
            <div class="contacts-hero-card__icon">
              <Wrench :size="30" />
            </div>

            <div>
              <strong>{{ t('contacts.hero.plumber_nearby') }}</strong>
              <span>{{ t('contacts.hero.ready_to_help') }}</span>
            </div>

            <div class="contacts-status">
              <span></span>
              {{ t('contacts.hero.online') }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CONTACT CARDS -->
    <section class="contacts-info">
      <div class="contacts-container">
        <div class="contacts-section-heading">
          <span>{{ t('contacts.info.eyebrow') }}</span>
          <h2>{{ t('contacts.info.title') }}</h2>
          <p>
            {{ t('contacts.info.description') }}
          </p>
        </div>

        <div class="contacts-grid">

          <a href="tel:+998777091933" class="contact-card">
            <div class="contact-card__icon">
              <Phone :size="25" />
            </div>

            <div class="contact-card__body">
              <span class="contact-card__label">{{ t("contacts.phone.label") }}</span>
              <strong>+998 77 709 19 33</strong>
              <p>{{ t('contacts.phone.description') }}</p>
            </div>

            <ArrowRight :size="20" class="contact-card__arrow" />
          </a>

          <a
            href="https://t.me/EmeraldServiceOrdersBot"
            target="_blank"
            rel="noopener noreferrer"
            class="contact-card"
          >
            <div class="contact-card__icon contact-card__icon--telegram">
              <MessageCircle :size="25" />
            </div>

            <div class="contact-card__body">
              <span class="contact-card__label">Telegram</span>
              <strong>@EmeraldServiceOrdersBot</strong>
              <p>{{ t('contacts.telegram.description') }}</p>
            </div>

            <ArrowRight :size="20" class="contact-card__arrow" />
          </a>

          <div class="contact-card">
            <div class="contact-card__icon">
              <MapPin :size="25" />
            </div>

            <div class="contact-card__body">
              <span class="contact-card__label">{{ t("contacts.address.label") }}</span>
              <strong>{{ t('contacts.address.city') }}</strong>
              <p>{{ t('contacts.address.description') }}</p>
            </div>
          </div>

          <div class="contact-card">
            <div class="contact-card__icon">
              <Clock3 :size="25" />
            </div>

            <div class="contact-card__body">
              <span class="contact-card__label">{{ t("contacts.hours.label") }}</span>
              <strong>{{ t('contacts.hours.daily') }}</strong>
              <p>{{ t('contacts.hours.description') }}</p>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- MAP / LOCATION -->
    <section class="contacts-vacancies">
      <div class="contacts-container">

        <div class="contacts-section-heading contacts-section-heading--left contacts-vacancies__heading">
          <span>{{ t('contacts.vacancy.eyebrow') }}</span>
          <h2>{{ t('contacts.vacancy.title') }}</h2>
          <p>
            {{ t('contacts.vacancy.description') }}
          </p>
        </div>

        <div class="contacts-vacancies__layout">

          <!-- INFO -->
          <div class="contacts-vacancy-card">

            <div class="contacts-vacancy-card__top">
              <div class="contacts-vacancy-card__icon">
                <Wrench :size="27" />
              </div>

              <div>
                <span class="contacts-vacancy-card__label">
                  {{ t('contacts.vacancy.open') }}
                </span>
                <h3>{{ t('contacts.vacancy.plumber') }}</h3>
              </div>
            </div>

            <p class="contacts-vacancy-card__intro">
              {{ t('contacts.vacancy.intro') }}
            </p>

            <div class="contacts-vacancy-card__section">
              <strong>{{ t('contacts.vacancy.requirements') }}</strong>

              <ul>
                <li>{{ t('contacts.vacancy.req_experience') }}</li>
                <li>{{ t('contacts.vacancy.req_responsibility') }}</li>
                <li>{{ t('contacts.vacancy.req_organization') }}</li>
                <li>{{ t('contacts.vacancy.req_teamwork') }}</li>
                <li>{{ t('contacts.vacancy.req_client') }}</li>
              </ul>
            </div>

            <div class="contacts-vacancy-card__condition">
              <span class="contacts-vacancy-card__condition-title">
  <Banknote :size="17" />
  {{ t('contacts.vacancy.payment') }}
</span>
              <strong>{{ t('contacts.vacancy.payment_value') }}</strong>
            </div>

            <a
              href="tel:+998777091933"
              class="contacts-vacancy-card__phone"
            >
              <Phone :size="18" />
              <span>
                <small>{{ t('contacts.vacancy.additional') }}</small>
                +998 77 709 19 33
              </span>
            </a>

          </div>

          <!-- FORM -->
          <div class="contacts-vacancy-form">

            <div class="contacts-vacancy-form__heading">
              <span>{{ t('contacts.vacancy.apply_eyebrow') }}</span>
              <h3>{{ t('contacts.vacancy.form_title') }}</h3>
              <p>
                {{ t('contacts.vacancy.form_description') }}
              </p>
            </div>

            <form
              class="contacts-vacancy-form__body"
              @submit.prevent="submitVacancyApplication"
            >

              <label>
                <span>{{ t('contacts.form.name') }}</span>
                <input
                  type="text"
                  name="name"
                  v-model="vacancyForm.name"
                  required
                  :placeholder="t('contacts.form.name_placeholder')"
                />
              </label>

              <label>
                <span>{{ t('contacts.form.phone') }}</span>
                <input
                  type="tel"
                  name="phone"
                  v-model="vacancyForm.phone"
                  required
                  placeholder="+998 90 123 45 67"
                />
              </label>

              <div class="contacts-vacancy-form__row">

                <label>
                  <span>{{ t('contacts.form.experience') }}</span>
                  <input
                    type="text"
                    name="experience"
                    v-model="vacancyForm.experience"
                    required
                    :placeholder="t('contacts.form.experience_placeholder')"
                  />
                </label>

                <label>
                  <span>{{ t('contacts.form.specialization') }}</span>
                  <input
                    type="text"
                    name="specialization"
                    v-model="vacancyForm.specialization"
                    required
                    :placeholder="t('contacts.form.specialization_placeholder')"
                  />
                </label>

              </div>

              <label>
                <span>{{ t('contacts.form.about') }}</span>
                <textarea
                  name="about"
                  v-model="vacancyForm.about"
                  required
                  rows="5"
                  :placeholder="t('contacts.form.about_placeholder')"
                ></textarea>
              </label>

              <button
                type="submit"
                class="contacts-vacancy-form__submit"
                :disabled="vacancySubmitting"
              >
                <span>
                  {{
                    vacancySubmitting
                      ? t('contacts.form.sending')
                      : t('contacts.form.submit')
                  }}
                </span>
                <ArrowRight v-if="!vacancySubmitting" :size="18" />
              </button>

              <p
                v-if="vacancySuccess"
                class="contacts-vacancy-form__message contacts-vacancy-form__message--success"
              >
                {{ t('contacts.form.success') }}
              </p>

              <p
                v-if="vacancyError"
                class="contacts-vacancy-form__message contacts-vacancy-form__message--error"
              >
                {{ vacancyError }}
              </p>

              <p class="contacts-vacancy-form__note">
                {{ t('contacts.form.note') }}
              </p>

            </form>

          </div>

        </div>
      </div>
    </section>

<section class="contacts-location">
      <div class="contacts-container contacts-location__grid">

        <div class="contacts-location__content">
          <div class="contacts-section-heading contacts-section-heading--left">
            <span>{{ t('contacts.location.eyebrow') }}</span>
            <h2>{{ t('contacts.location.title') }}</h2>
            <p>
              {{ t('contacts.location.description') }}
            </p>
          </div>

          <div class="contacts-location__points">
            <div>
              <MapPin :size="19" />
              <span>{{ t('contacts.location.city_districts') }}</span>
            </div>

            <div>
              <Wrench :size="19" />
              <span>{{ t('contacts.location.plumbing') }}</span>
            </div>

            <div>
              <Clock3 :size="19" />
              <span>{{ t('contacts.location.fast') }}</span>
            </div>
          </div>
        </div>

        <div class="contacts-map">
          <div class="contacts-map__grid"></div>

          <div class="contacts-map__pin">
            <div class="contacts-map__pin-icon">
              <MapPin :size="25" />
            </div>

            <strong>{{ t('contacts.location.company') }}</strong>
            <span>{{ t('contacts.location.city') }}</span>
          </div>
        </div>

      </div>
    </section>

    <!-- CTA -->
    <section class="contacts-cta">
      <div class="contacts-container">
        <div class="contacts-cta__inner">
          <div>
            <span>{{ t('contacts.cta.eyebrow') }}</span>
            <h2>{{ t('contacts.cta.title') }}</h2>
            <p>{{ t('contacts.cta.description') }}</p>
          </div>

          <div class="contacts-cta__actions">
            <a href="tel:+998777091933" class="contacts-button contacts-button--white">
              <Phone :size="18" />
              {{ t('contacts.hero.call') }}
            </a>

            <a
              href="https://t.me/EmeraldServiceOrdersBot"
              target="_blank"
              rel="noopener noreferrer"
              class="contacts-button contacts-button--outline"
            >
              {{ t('contacts.cta.telegram') }}
              <ArrowRight :size="18" />
            </a>
          </div>
        </div>
      </div>
    </section>

  </main>
</template>

<style scoped>
.contacts-page {
  color: #15352a;
  background: #f7fbf8;
}

.contacts-container {
  width: min(1180px, calc(100% - 40px));
  margin: 0 auto;
}

/* HERO */

.contacts-hero {
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(circle at 78% 45%, #d8f1e2 0%, #edf8f1 38%, #f7fbf8 75%);
}

.contacts-hero__inner {
  min-height: 540px;
  display: grid;
  grid-template-columns: 1.05fr .95fr;
  align-items: center;
  gap: 40px;
}

.contacts-eyebrow {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #16834f;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: .12em;
  text-transform: uppercase;
  margin-bottom: 20px;
}

.contacts-eyebrow span {
  width: 28px;
  height: 2px;
  background: #16834f;
}

.contacts-hero h1 {
  max-width: 680px;
  margin: 0;
  font-size: clamp(48px, 6vw, 76px);
  line-height: .98;
  letter-spacing: -.055em;
  color: #123d2c;
}

.contacts-hero p {
  max-width: 590px;
  margin: 26px 0 0;
  color: #60766b;
  font-size: 18px;
  line-height: 1.65;
}

.contacts-hero__actions {
  display: flex;
  gap: 12px;
  margin-top: 34px;
  flex-wrap: wrap;
}

.contacts-button {
  min-height: 52px;
  padding: 0 22px;
  border-radius: 13px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  text-decoration: none;
  font-weight: 800;
  transition: .2s ease;
}

.contacts-button:hover {
  transform: translateY(-2px);
}

.contacts-button--primary {
  color: #fff;
  background: #16834f;
  box-shadow: 0 12px 28px rgba(22, 131, 79, .2);
}

.contacts-button--telegram {
  color: #16834f;
  background: #e5f5ec;
}

.contacts-hero__visual {
  position: relative;
  min-height: 410px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.contacts-circle {
  position: absolute;
  border-radius: 50%;
}

.contacts-circle--large {
  width: 390px;
  height: 390px;
  background: #c5ead3;
  right: 20px;
  bottom: -70px;
}

.contacts-circle--small {
  width: 180px;
  height: 180px;
  background: rgba(255,255,255,.7);
  left: 50px;
  top: 50px;
  filter: blur(3px);
}

.contacts-hero-card {
  position: relative;
  z-index: 2;
  width: min(390px, 90%);
  padding: 25px;
  border-radius: 24px;
  background: rgba(255,255,255,.9);
  border: 1px solid rgba(255,255,255,.8);
  box-shadow: 0 30px 70px rgba(35, 84, 62, .13);
  backdrop-filter: blur(12px);
}

.contacts-hero-card__icon {
  width: 64px;
  height: 64px;
  display: grid;
  place-items: center;
  border-radius: 18px;
  color: #16834f;
  background: #e4f5eb;
  margin-bottom: 20px;
}

.contacts-hero-card strong,
.contacts-hero-card span {
  display: block;
}

.contacts-hero-card strong {
  font-size: 22px;
  color: #173e2f;
}

.contacts-hero-card > div:nth-child(2) span {
  margin-top: 5px;
  color: #779085;
}

.contacts-status {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 28px;
  padding-top: 18px;
  border-top: 1px solid #e4eee8;
  color: #4e7161;
  font-size: 14px;
  font-weight: 700;
}

.contacts-status span {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #25b66b;
}

/* INFO */

.contacts-info {
  padding: 100px 0;
  background: #fff;
}

.contacts-section-heading {
  max-width: 650px;
  margin: 0 auto 46px;
  text-align: center;
}

.contacts-section-heading--left {
  margin-left: 0;
  text-align: left;
}

.contacts-section-heading > span {
  color: #16834f;
  font-size: 12px;
  font-weight: 900;
  letter-spacing: .15em;
}

.contacts-section-heading h2 {
  margin: 12px 0 14px;
  color: #153d2d;
  font-size: clamp(32px, 4vw, 48px);
  line-height: 1.05;
  letter-spacing: -.04em;
}

.contacts-section-heading p {
  margin: 0;
  color: #708279;
  font-size: 16px;
  line-height: 1.7;
}

.contacts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
}

.contact-card {
  position: relative;
  min-height: 150px;
  padding: 25px;
  display: flex;
  align-items: center;
  gap: 18px;
  text-decoration: none;
  color: inherit;
  border: 1px solid #e4eee8;
  border-radius: 20px;
  background: #fbfdfc;
  transition: .2s ease;
}

.contact-card:hover {
  transform: translateY(-3px);
  border-color: #bfe3cd;
  box-shadow: 0 18px 45px rgba(36, 87, 61, .08);
}

.contact-card__icon {
  flex: 0 0 58px;
  width: 58px;
  height: 58px;
  display: grid;
  place-items: center;
  border-radius: 16px;
  color: #16834f;
  background: #e4f5eb;
}

.contact-card__icon--telegram {
  color: #188bc0;
  background: #e5f4fb;
}

.contact-card__body {
  min-width: 0;
}

.contact-card__label {
  display: block;
  color: #83938b;
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .1em;
}

.contact-card__body strong {
  display: block;
  margin-top: 6px;
  color: #183f2f;
  font-size: 20px;
}

.contact-card__body p {
  margin: 6px 0 0;
  color: #788a81;
  font-size: 14px;
  line-height: 1.4;
}

.contact-card__arrow {
  margin-left: auto;
  color: #16834f;
}

/* LOCATION */

.contacts-location {
  padding: 130px 0 110px;
  background: #f1f8f4;
}

.contacts-location__grid {
  display: grid;
  grid-template-columns: .9fr 1.1fr;
  gap: 70px;
  align-items: center;
}

.contacts-location__points {
  display: grid;
  gap: 14px;
}

.contacts-location__points div {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #446457;
  font-weight: 700;
}

.contacts-location__points svg {
  flex: 0 0 auto;
  color: #16834f;
}

.contacts-map {
  position: relative;
  height: 390px;
  overflow: hidden;
  border-radius: 28px;
  background:
    linear-gradient(rgba(255,255,255,.8) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.8) 1px, transparent 1px),
    #dcefe3;
  background-size: 42px 42px;
  box-shadow: 0 25px 60px rgba(34, 82, 58, .1);
}

.contacts-map::before,
.contacts-map::after {
  content: "";
  position: absolute;
  background: #fff;
  opacity: .65;
}

.contacts-map::before {
  width: 180%;
  height: 80px;
  left: -30%;
  top: 44%;
  transform: rotate(-14deg);
}

.contacts-map::after {
  width: 120%;
  height: 60px;
  left: -10%;
  top: 15%;
  transform: rotate(24deg);
}

.contacts-map__pin {
  position: absolute;
  z-index: 2;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 190px;
  padding: 17px;
  border-radius: 18px;
  background: rgba(255,255,255,.96);
  text-align: center;
  box-shadow: 0 18px 45px rgba(30, 78, 53, .15);
}

.contacts-map__pin-icon {
  width: 48px;
  height: 48px;
  margin: -40px auto 10px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  color: #fff;
  background: #16834f;
  border: 5px solid #dcefe3;
}

.contacts-map__pin strong,
.contacts-map__pin span {
  display: block;
}

.contacts-map__pin strong {
  color: #173e2f;
}

.contacts-map__pin span {
  margin-top: 3px;
  color: #84948c;
  font-size: 13px;
}

/* CTA */

.contacts-cta {
  padding: 70px 0;
  background: #16834f;
}

.contacts-cta__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 35px;
}

.contacts-cta__inner > div:first-child {
  max-width: 620px;
}

.contacts-cta__inner span {
  color: rgba(255,255,255,.72);
  font-size: 12px;
  font-weight: 900;
  letter-spacing: .15em;
}

.contacts-cta h2 {
  margin: 12px 0 10px;
  color: #fff;
  font-size: clamp(32px, 4vw, 48px);
  line-height: 1.05;
  letter-spacing: -.04em;
}

.contacts-cta p {
  margin: 0;
  color: rgba(255,255,255,.78);
  line-height: 1.6;
}

.contacts-cta__actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.contacts-button--white {
  color: #16834f;
  background: #fff;
}

.contacts-button--outline {
  color: #fff;
  border: 1px solid rgba(255,255,255,.5);
  background: transparent;
}

/* ============================================================
   {{ t('contacts.vacancy.eyebrow') }}
============================================================ */

.contacts-vacancies {
  padding: 110px 0;
  background: #f7fbf8;
}

.contacts-vacancies__heading {
  max-width: 760px;
  margin-left: 0;
  margin-bottom: 48px;
}

.contacts-vacancies__layout {
  display: grid;
  grid-template-columns: .9fr 1.1fr;
  gap: 24px;
  align-items: stretch;
}

/* INFO CARD */

.contacts-vacancy-card {
  padding: 34px;
  border: 1px solid #dcebe2;
  border-radius: 26px;
  background:
    radial-gradient(
      circle at 90% 0%,
      rgba(22, 131, 79, .09),
      transparent 32%
    ),
    #ffffff;
  box-shadow: 0 20px 55px rgba(35, 84, 62, .07);
}

.contacts-vacancy-card__top {
  display: flex;
  align-items: center;
  gap: 16px;
}

.contacts-vacancy-card__icon {
  width: 60px;
  height: 60px;
  flex: 0 0 60px;
  display: grid;
  place-items: center;
  border-radius: 17px;
  color: #16834f;
  background: #e4f5eb;
}

.contacts-vacancy-card__label {
  display: block;
  margin-bottom: 5px;
  color: #16834f;
  font-size: 11px;
  font-weight: 900;
  letter-spacing: .13em;
}

.contacts-vacancy-card h3 {
  margin: 0;
  color: #173e2f;
  font-size: 28px;
}

.contacts-vacancy-card__intro {
  margin: 28px 0 26px;
  color: #687b72;
  font-size: 15px;
  line-height: 1.7;
}

.contacts-vacancy-card__section {
  padding-top: 24px;
  border-top: 1px solid #e5eee9;
}

.contacts-vacancy-card__section > strong {
  display: block;
  margin-bottom: 14px;
  color: #244b3a;
  font-size: 16px;
}

.contacts-vacancy-card__section ul {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 11px;
}

.contacts-vacancy-card__section li {
  position: relative;
  padding-left: 25px;
  color: #687b72;
  font-size: 14px;
  line-height: 1.5;
}

.contacts-vacancy-card__section li::before {
  content: "✓";
  position: absolute;
  left: 0;
  top: 0;
  color: #16834f;
  font-weight: 900;
}

.contacts-vacancy-card__condition {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-top: 28px;
  padding: 17px 18px;
  border-radius: 15px;
  background: #f1f8f4;
}

.contacts-vacancy-card__condition-title {
  display: flex;
  align-items: center;
  gap: 7px;
  color: #16834f;
  font-size: 13px;
  font-weight: 800;
}

.contacts-vacancy-card__condition-title svg {
  flex: 0 0 auto;
}

.contacts-vacancy-card__condition strong {
  color: #315747;
  font-size: 14px;
}

.contacts-vacancy-card__phone {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 20px;
  padding: 17px 18px;
  border-radius: 15px;
  color: #16834f;
  background: #e5f5ec;
  text-decoration: none;
  transition: .2s ease;
}

.contacts-vacancy-card__phone:hover {
  transform: translateY(-2px);
  background: #dcefe5;
}

.contacts-vacancy-card__phone svg {
  flex: 0 0 auto;
}

.contacts-vacancy-card__phone span {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.contacts-vacancy-card__phone small {
  color: #6f877b;
  font-size: 11px;
}

.contacts-vacancy-card__phone span {
  font-weight: 800;
}

/* FORM */

.contacts-vacancy-form {
  padding: 34px;
  border-radius: 26px;
  background: #ffffff;
  border: 1px solid #dcebe2;
  box-shadow: 0 20px 55px rgba(35, 84, 62, .07);
}

.contacts-vacancy-form__heading {
  margin-bottom: 26px;
}

.contacts-vacancy-form__heading > span {
  color: #16834f;
  font-size: 11px;
  font-weight: 900;
  letter-spacing: .13em;
}

.contacts-vacancy-form__heading h3 {
  margin: 8px 0 8px;
  color: #173e2f;
  font-size: 30px;
  line-height: 1.1;
}

.contacts-vacancy-form__heading p {
  margin: 0;
  color: #75877e;
  font-size: 14px;
  line-height: 1.6;
}

.contacts-vacancy-form__body {
  display: grid;
  gap: 17px;
}

.contacts-vacancy-form__body label {
  display: grid;
  gap: 8px;
}

.contacts-vacancy-form__body label > span {
  color: #38594a;
  font-size: 13px;
  font-weight: 800;
}

.contacts-vacancy-form__body input,
.contacts-vacancy-form__body textarea {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #dce8e1;
  border-radius: 13px;
  padding: 13px 14px;
  color: #244b3a;
  background: #fbfdfc;
  font: inherit;
  font-size: 14px;
  outline: none;
  transition: .2s ease;
}

.contacts-vacancy-form__body input {
  min-height: 48px;
}

.contacts-vacancy-form__body textarea {
  min-height: 120px;
  resize: vertical;
}

.contacts-vacancy-form__body input::placeholder,
.contacts-vacancy-form__body textarea::placeholder {
  color: #a1aea8;
}

.contacts-vacancy-form__body input:focus,
.contacts-vacancy-form__body textarea:focus {
  border-color: #7dc19e;
  background: #fff;
  box-shadow: 0 0 0 4px rgba(22, 131, 79, .08);
}

.contacts-vacancy-form__row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.contacts-vacancy-form__submit {
  min-height: 52px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  margin-top: 4px;
  padding: 0 22px;
  border: 0;
  border-radius: 13px;
  color: #fff;
  background: #16834f;
  box-shadow: 0 12px 28px rgba(22, 131, 79, .18);
  font: inherit;
  font-weight: 800;
  cursor: pointer;
  transition: .2s ease;
}

.contacts-vacancy-form__submit:hover {
  transform: translateY(-2px);
  background: #116f43;
}

.contacts-vacancy-form__submit svg {
  transition: transform .2s ease;
}

.contacts-vacancy-form__submit:hover svg {
  transform: translateX(3px);
}

.contacts-vacancy-form__message {
  margin: 0;
  padding: 12px 14px;
  border-radius: 11px;
  font-size: 12px;
  line-height: 1.5;
}

.contacts-vacancy-form__message--success {
  color: #17633f;
  background: #e9f8ef;
  border: 1px solid #bfe5cc;
}

.contacts-vacancy-form__message--error {
  color: #a33a3a;
  background: #fff1f1;
  border: 1px solid #f0caca;
}

.contacts-vacancy-form__submit:disabled {
  opacity: .65;
  cursor: not-allowed;
  transform: none;
}

.contacts-vacancy-form__note {
  margin: -3px 0 0;
  color: #98a59f;
  font-size: 11px;
  line-height: 1.5;
  text-align: center;
}

/* RESPONSIVE */

@media (max-width: 900px) {
  .contacts-vacancies__layout {
    grid-template-columns: 1fr;
  }

  .contacts-vacancy-card,
  .contacts-vacancy-form {
    padding: 28px;
  }
}

@media (max-width: 650px) {
  .contacts-vacancies {
    padding: 75px 0;
  }

  .contacts-vacancies__heading {
    margin-bottom: 34px;
  }

  .contacts-vacancy-card,
  .contacts-vacancy-form {
    padding: 22px;
    border-radius: 21px;
  }

  .contacts-vacancy-card h3 {
    font-size: 25px;
  }

  .contacts-vacancy-form__heading h3 {
    font-size: 26px;
  }

  .contacts-vacancy-form__row {
    grid-template-columns: 1fr;
  }
}



@media (max-width: 900px) {
  .contacts-hero__inner {
    grid-template-columns: 1fr;
    padding: 70px 0;
  }

  .contacts-hero__visual {
    min-height: 330px;
  }

  .contacts-location__grid {
    grid-template-columns: 1fr;
    gap: 50px;
  }

  .contacts-cta__inner {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 650px) {
  .contacts-container {
    width: min(100% - 28px, 1180px);
  }

  .contacts-hero h1 {
    font-size: 46px;
  }

  .contacts-hero p {
    font-size: 16px;
  }

  .contacts-grid {
    grid-template-columns: 1fr;
  }

  .contacts-info,
  .contacts-location {
    padding: 70px 0;
  }

  .contacts-circle--large {
    width: 300px;
    height: 300px;
    right: -20px;
  }

  .contacts-map {
    height: 300px;
  }

  .contact-card {
    min-height: 125px;
    padding: 20px;
  }

  .contact-card__body strong {
    font-size: 17px;
  }
}

/* ============================================================
   MOBILE FIX — CONTACTS PAGE
   ============================================================ */

@media (max-width: 768px) {
  .contacts-page {
    width: 100%;
    max-width: 100%;
    overflow-x: hidden;
  }

  .contacts-page *,
  .contacts-page *::before,
  .contacts-page *::after {
    box-sizing: border-box;
  }

  .contacts-container {
    width: calc(100% - 32px);
    max-width: 100%;
    min-width: 0;
  }

  /* HERO */
  .contacts-hero {
    overflow: hidden;
  }

  .contacts-hero__inner {
    width: 100%;
    min-width: 0;
    padding: 42px 0 48px;
  }

  .contacts-hero__content,
  .contacts-hero__visual {
    width: 100%;
    min-width: 0;
    max-width: 100%;
  }

  .contacts-hero h1 {
    max-width: 100%;
    margin: 0;
    font-size: clamp(32px, 10vw, 42px);
    line-height: 1.02;
    letter-spacing: -0.045em;
    overflow-wrap: anywhere;
  }

  .contacts-hero p {
    max-width: 100%;
    font-size: 14px;
    line-height: 1.6;
  }

  .contacts-hero__visual {
    min-height: 250px;
  }

  /* CONTACTS */
  .contacts-info,
  .contacts-location {
    padding: 48px 0;
  }

  .contacts-grid,
  .contacts-location__grid {
    width: 100%;
    min-width: 0;
    gap: 28px;
  }

  .contacts-info > *,
  .contacts-location > *,
  .contacts-location__content,
  .contacts-location__points,
  .contacts-map {
    min-width: 0;
    max-width: 100%;
  }

  .contacts-section-heading {
    max-width: 100%;
  }

  .contacts-section-heading h2 {
    max-width: 100%;
    font-size: clamp(28px, 8vw, 36px);
    line-height: 1.05;
    letter-spacing: -0.035em;
    overflow-wrap: anywhere;
  }

  .contacts-section-heading p {
    max-width: 100%;
    font-size: 13px;
    line-height: 1.6;
  }

  .contact-card {
    width: 100%;
    min-width: 0;
    min-height: auto;
    padding: 16px;
    border-radius: 16px;
  }

  .contact-card__body {
    min-width: 0;
    overflow: hidden;
  }

  .contact-card__body strong,
  .contact-card__body p {
    max-width: 100%;
    overflow-wrap: anywhere;
    word-break: break-word;
  }

  .contact-card__body strong {
    font-size: 15px;
  }

  .contact-card__body p {
    font-size: 12px;
    line-height: 1.45;
  }

  /* LOCATION */
  .contacts-location__grid {
    gap: 30px;
  }

  .contacts-location__points {
    display: grid;
    gap: 10px;
  }

  .contacts-location__points > div {
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
  }

  .contacts-location__points span {
    min-width: 0;
    font-size: 13px;
    line-height: 1.4;
    overflow-wrap: anywhere;
  }

  .contacts-map {
    width: 100%;
    height: 250px;
    min-height: 250px;
    border-radius: 20px;
    overflow: hidden;
  }

  .contacts-map__pin {
    width: min(180px, calc(100% - 40px));
    max-width: calc(100% - 40px);
  }

  /* VACANCIES */
  .contacts-vacancies {
    padding: 52px 0;
  }

  .contacts-vacancies__heading {
    width: 100%;
    max-width: 100%;
    margin-bottom: 28px;
  }

  .contacts-vacancies__layout {
    width: 100%;
    max-width: 100%;
    min-width: 0;
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .contacts-vacancy-card,
  .contacts-vacancy-form {
    width: 100%;
    max-width: 100%;
    min-width: 0;
    padding: 20px;
    border-radius: 18px;
  }

  .contacts-vacancy-card__top {
    align-items: flex-start;
    gap: 12px;
  }

  .contacts-vacancy-card__icon {
    width: 48px;
    height: 48px;
    flex: 0 0 48px;
    border-radius: 14px;
  }

  .contacts-vacancy-card__label {
    font-size: 9px;
    line-height: 1.3;
  }

  .contacts-vacancy-card h3 {
    font-size: 23px;
    line-height: 1.1;
  }

  .contacts-vacancy-card__intro {
    margin: 20px 0;
    font-size: 13px;
    line-height: 1.6;
  }

  .contacts-vacancy-card__section {
    padding-top: 18px;
  }

  .contacts-vacancy-card__section > strong {
    margin-bottom: 11px;
    font-size: 14px;
  }

  .contacts-vacancy-card__section ul {
    gap: 8px;
  }

  .contacts-vacancy-card__section li {
    padding-left: 20px;
    font-size: 12px;
    line-height: 1.45;
  }

  .contacts-vacancy-card__condition {
    margin-top: 18px;
    padding: 14px;
  }

  .contacts-vacancy-card__condition strong {
    font-size: 12px;
    line-height: 1.45;
  }

  .contacts-vacancy-card__phone {
    margin-top: 12px;
    padding: 14px;
  }

  .contacts-vacancy-card__phone small {
    font-size: 10px;
  }

  .contacts-vacancy-card__phone span {
    min-width: 0;
    overflow-wrap: anywhere;
  }

  /* FORM */
  .contacts-vacancy-form__heading {
    margin-bottom: 20px;
  }

  .contacts-vacancy-form__heading h3 {
    font-size: 23px;
    line-height: 1.1;
  }

  .contacts-vacancy-form__heading p {
    font-size: 12px;
    line-height: 1.55;
  }

  .contacts-vacancy-form__body {
    width: 100%;
    min-width: 0;
    gap: 13px;
  }

  .contacts-vacancy-form__row {
    grid-template-columns: 1fr;
    gap: 13px;
  }

  .contacts-vacancy-form__body label {
    min-width: 0;
  }

  .contacts-vacancy-form__body input,
  .contacts-vacancy-form__body textarea {
    width: 100%;
    max-width: 100%;
    min-width: 0;
    font-size: 14px;
  }

  .contacts-vacancy-form__body textarea {
    min-height: 105px;
  }

  .contacts-vacancy-form__submit {
    width: 100%;
    min-height: 48px;
    padding: 0 16px;
  }

  .contacts-vacancy-form__note {
    font-size: 10px;
    line-height: 1.45;
  }

  /* CTA */
  .contacts-cta {
    padding: 46px 0;
  }

  .contacts-cta__inner {
    width: 100%;
    min-width: 0;
    gap: 24px;
  }

  .contacts-cta__inner > div:first-child {
    width: 100%;
    max-width: 100%;
  }

  .contacts-cta h2 {
    max-width: 100%;
    font-size: clamp(28px, 8vw, 38px);
    line-height: 1.05;
  }

  .contacts-cta p {
    max-width: 100%;
    font-size: 13px;
    line-height: 1.55;
  }

  .contacts-cta__actions {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .contacts-button {
    width: 100%;
    min-height: 48px;
    justify-content: center;
  }
}

@media (max-width: 380px) {
  .contacts-container {
    width: calc(100% - 24px);
  }

  .contacts-hero__inner {
    padding: 34px 0 40px;
  }

  .contacts-hero h1 {
    font-size: 31px;
  }

  .contacts-section-heading h2 {
    font-size: 27px;
  }

  .contacts-vacancy-card,
  .contacts-vacancy-form {
    padding: 16px;
    border-radius: 16px;
  }

  .contacts-vacancy-card h3,
  .contacts-vacancy-form__heading h3 {
    font-size: 21px;
  }

  .contacts-map {
    height: 220px;
    min-height: 220px;
  }
}


/* ============================================================
   FINAL MOBILE — HERO + LOCATION
   ============================================================ */

@media (max-width: 768px) {

  /* =========================
     HERO
     ========================= */

  .contacts-hero {
    overflow: hidden;
  }

  .contacts-hero__inner {
    min-height: auto;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: 0;
    padding: 30px 0 34px;
  }

  .contacts-hero__content {
    width: 100%;
    max-width: 100%;
  }

  .contacts-eyebrow {
    margin-bottom: 12px;
    font-size: 9px;
    letter-spacing: .15em;
  }

  .contacts-hero h1 {
    margin: 0;
    max-width: 100%;
    font-size: clamp(31px, 8.8vw, 38px);
    line-height: 1.02;
    letter-spacing: -.045em;
  }

  .contacts-hero p {
    margin: 14px 0 0;
    max-width: 100%;
    font-size: 13px;
    line-height: 1.55;
  }

  .contacts-hero__actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    width: 100%;
    margin-top: 18px;
  }

  .contacts-hero__actions .contacts-button {
    width: 100%;
    min-height: 46px;
    padding: 0 10px;
    justify-content: center;
    font-size: 12px;
    border-radius: 10px;
  }

  .contacts-hero__visual {
    position: relative;
    width: 100%;
    min-height: 220px;
    margin-top: 22px;
  }

  .contacts-circle--large {
    width: 240px;
    height: 240px;
    right: -18px;
    bottom: -80px;
  }

  .contacts-circle--small {
    width: 100px;
    height: 100px;
    left: 0;
    top: 20px;
  }

  .contacts-hero-card {
    width: min(100%, 270px);
    margin: 0 auto;
    position: relative;
    z-index: 2;
    padding: 18px;
    border-radius: 18px;
  }

  .contacts-hero-card__icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
  }

  .contacts-hero-card strong {
    font-size: 15px;
  }

  .contacts-hero-card span {
    font-size: 11px;
  }

  .contacts-status {
    margin-top: 13px;
    padding-top: 10px;
    font-size: 10px;
  }


  /* =========================
     LOCATION / МЫ РЯДОМ
     ========================= */

  .contacts-location {
    padding: 46px 0 42px;
    background: #f1f8f4;
  }

  .contacts-location__grid {
    display: flex;
    flex-direction: column;
    gap: 24px;
    align-items: stretch;
  }

  .contacts-location__content {
    width: 100%;
    max-width: 100%;
  }

  .contacts-location .contacts-section-heading {
    margin-bottom: 22px;
  }

  .contacts-location .contacts-section-heading > span {
    display: block;
    margin-bottom: 9px;
    font-size: 9px;
    letter-spacing: .15em;
  }

  .contacts-location .contacts-section-heading h2 {
    margin: 0;
    max-width: 100%;
    font-size: clamp(27px, 7.5vw, 34px);
    line-height: 1.04;
    letter-spacing: -.04em;
  }

  .contacts-location .contacts-section-heading p {
    margin-top: 11px;
    max-width: 100%;
    font-size: 12px;
    line-height: 1.55;
  }

  .contacts-location__points {
    display: grid;
    gap: 8px;
  }

  .contacts-location__points div {
    min-height: 36px;
    gap: 9px;
    font-size: 12px;
    line-height: 1.35;
  }

  .contacts-location__points svg {
    width: 16px;
    height: 16px;
  }

  .contacts-map {
    width: 100%;
    height: 245px;
    min-height: 245px;
    border-radius: 20px;
    box-shadow: 0 16px 35px rgba(34, 82, 58, .08);
  }

  .contacts-map__pin {
    width: 165px;
    padding: 14px;
    border-radius: 16px;
  }

  .contacts-map__pin-icon {
    width: 42px;
    height: 42px;
    margin: -34px auto 8px;
  }

  .contacts-map__pin strong {
    font-size: 11px;
  }

  .contacts-map__pin span {
    font-size: 11px;
  }
}


/* =========================
   VERY SMALL PHONES
   ========================= */

@media (max-width: 380px) {

  .contacts-hero__inner {
    padding-top: 26px;
    padding-bottom: 28px;
  }

  .contacts-hero h1 {
    font-size: 30px;
  }

  .contacts-hero p {
    font-size: 12px;
  }

  .contacts-hero__actions {
    gap: 6px;
  }

  .contacts-hero__actions .contacts-button {
    font-size: 11px;
    min-height: 44px;
  }

  .contacts-hero__visual {
    min-height: 205px;
    margin-top: 18px;
  }

  .contacts-hero-card {
    max-width: 250px;
  }

  .contacts-location {
    padding-top: 38px;
  }

  .contacts-location .contacts-section-heading h2 {
    font-size: 26px;
  }

  .contacts-map {
    height: 220px;
    min-height: 220px;
  }
}


/* ============================================================
   CONTACTS — FINAL MOBILE COMPOSITION
   HERO + LOCATION
   ============================================================ */

@media (max-width: 768px) {

  /* ==========================================================
     HERO
     ========================================================== */

  .contacts-hero {
    width: 100%;
    overflow: hidden;
    background:
      radial-gradient(
        circle at 80% 70%,
        #d7f1e1 0%,
        #edf8f1 42%,
        #f7fbf8 78%
      );
  }

  .contacts-hero__inner {
    width: calc(100% - 24px);
    min-height: 0 !important;
    margin: 0 auto;
    padding: 28px 0 34px !important;

    display: flex !important;
    flex-direction: column;
    align-items: stretch;
    gap: 0 !important;
  }

  .contacts-hero__content {
    width: 100%;
    max-width: none;
  }

  .contacts-eyebrow {
    margin: 0 0 11px !important;
    font-size: 8px !important;
    letter-spacing: .16em;
    gap: 8px;
  }

  .contacts-eyebrow span {
    width: 20px;
    height: 1px;
  }

  .contacts-hero h1 {
    width: 100%;
    max-width: none !important;
    margin: 0 !important;

    font-size: 34px !important;
    line-height: .98 !important;
    letter-spacing: -.045em !important;
  }

  .contacts-hero p {
    width: 100%;
    max-width: none !important;
    margin: 13px 0 0 !important;

    font-size: 12px !important;
    line-height: 1.5 !important;
  }

  /* buttons */

  .contacts-hero__actions {
    width: 100%;
    display: grid !important;
    grid-template-columns: 1fr 1fr;
    gap: 7px !important;
    margin-top: 17px !important;
  }

  .contacts-hero__actions .contacts-button {
    width: 100%;
    min-width: 0;
    min-height: 44px !important;

    padding: 0 8px !important;
    border-radius: 10px;

    font-size: 11px;
    gap: 6px;
  }

  .contacts-hero__actions .contacts-button svg {
    width: 15px;
    height: 15px;
  }

  /* visual */

  .contacts-hero__visual {
    width: 100%;
    min-height: 185px !important;
    height: 185px;

    margin-top: 19px;

    display: flex;
    align-items: center;
    justify-content: center;

    overflow: hidden;
  }

  .contacts-circle--large {
    width: 245px !important;
    height: 245px !important;

    right: -72px !important;
    bottom: -118px !important;
  }

  .contacts-circle--small {
    width: 125px !important;
    height: 125px !important;

    left: -42px !important;
    top: 2px !important;
  }

  .contacts-hero-card {
    width: 255px !important;
    max-width: calc(100% - 28px);

    padding: 17px !important;
    border-radius: 18px;

    box-shadow: 0 18px 40px rgba(35, 84, 62, .10);
  }

  .contacts-hero-card__icon {
    width: 40px !important;
    height: 40px !important;

    margin-bottom: 11px !important;
    border-radius: 11px;
  }

  .contacts-hero-card__icon svg {
    width: 20px;
    height: 20px;
  }

  .contacts-hero-card strong {
    font-size: 14px !important;
    line-height: 1.15;
  }

  .contacts-hero-card > div:nth-child(2) span {
    margin-top: 4px !important;
    font-size: 10px;
  }

  .contacts-status {
    margin-top: 12px !important;
    padding-top: 9px !important;

    font-size: 9px !important;
    gap: 6px;
  }

  .contacts-status span {
    width: 6px !important;
    height: 6px !important;
  }


  /* ==========================================================
     LOCATION — МЫ РЯДОМ
     ========================================================== */

  .contacts-location {
    width: 100%;
    padding: 38px 0 42px !important;
    background: #f1f8f4;
  }

  .contacts-location > .contacts-container {
    width: calc(100% - 24px);
    margin: 0 auto;
  }

  .contacts-location__grid {
    width: 100%;
    display: flex !important;
    flex-direction: column;
    align-items: stretch;

    gap: 21px !important;
  }

  .contacts-location__content {
    width: 100%;
    max-width: none;
  }

  .contacts-location .contacts-section-heading {
    width: 100%;
    max-width: none;

    margin: 0 0 20px !important;
    text-align: left;
  }

  .contacts-location .contacts-section-heading > span {
    display: block;
    margin-bottom: 9px;

    font-size: 8px !important;
    letter-spacing: .17em;
  }

  .contacts-location .contacts-section-heading h2 {
    margin: 0 !important;

    font-size: 29px !important;
    line-height: 1.02 !important;
    letter-spacing: -.04em !important;
  }

  .contacts-location .contacts-section-heading p {
    margin: 10px 0 0 !important;

    max-width: 100%;
    font-size: 11px !important;
    line-height: 1.55 !important;
  }

  /* three points */

  .contacts-location__points {
    width: 100%;
    display: grid;
    gap: 7px !important;
  }

  .contacts-location__points div {
    width: 100%;
    min-height: 34px;

    display: flex;
    align-items: center;

    gap: 9px;

    color: #446457;
    font-size: 11px !important;
    line-height: 1.3;
  }

  .contacts-location__points svg {
    width: 15px;
    height: 15px;
    flex: 0 0 15px;
  }

  /* map */

  .contacts-map {
    width: 100%;
    height: 220px !important;
    min-height: 220px !important;

    border-radius: 18px !important;

    box-shadow:
      0 14px 32px rgba(34, 82, 58, .08);
  }

  .contacts-map__pin {
    width: 150px !important;
    padding: 12px !important;
    border-radius: 14px;
  }

  .contacts-map__pin-icon {
    width: 40px !important;
    height: 40px !important;

    margin: -31px auto 7px !important;
  }

  .contacts-map__pin-icon svg {
    width: 20px;
    height: 20px;
  }

  .contacts-map__pin strong {
    font-size: 10px;
  }

  .contacts-map__pin span {
    margin-top: 2px !important;
    font-size: 9px;
  }
}


/* ============================================================
   393px / iPhone 16
   ============================================================ */

@media (max-width: 430px) {

  .contacts-hero__inner {
    width: calc(100% - 20px);
    padding-top: 25px !important;
    padding-bottom: 29px !important;
  }

  .contacts-hero h1 {
    font-size: 32px !important;
  }

  .contacts-hero p {
    font-size: 11.5px !important;
  }

  .contacts-hero__visual {
    height: 175px;
    min-height: 175px !important;
    margin-top: 16px;
  }

  .contacts-hero-card {
    width: 248px !important;
  }

  .contacts-location {
    padding-top: 34px !important;
    padding-bottom: 38px !important;
  }

  .contacts-location > .contacts-container {
    width: calc(100% - 20px);
  }

  .contacts-location .contacts-section-heading h2 {
    font-size: 27px !important;
  }

  .contacts-map {
    height: 205px !important;
    min-height: 205px !important;
  }
}

</style>
