<script setup>
import {
  ArrowRight,
  Wrench,
  Faucet,
  Waves,
  Flame,
} from '@lucide/vue'
import { useLanguage } from '../../composables/useLanguage'

const { t } = useLanguage()
</script>

<template>
  <section class="services-telegram">
    <div class="services-container">
      <div class="services-telegram__inner">

        <div class="services-telegram__content">
          <span class="services-telegram__label">
            {{ t('telegram.eyebrow') }}
          </span>

          <h2>
            {{ t('telegram.title') }}
            <strong>{{ t('telegram.title_accent') }}</strong>
          </h2>

          <p>
            {{ t('telegram.description') }}
          </p>

          <a
            href="#"
            class="services-button services-button--telegram"
          >
            {{ t('telegram.button') }}
            <ArrowRight :size="18" />
          </a>
        </div>

        <div class="services-telegram__visual">
          <div class="services-telegram__phone">

            <div class="services-telegram__phone-header">
              <div class="services-telegram__avatar">
                И
              </div>

              <div>
                <strong>{{ t('telegram.bot_name') }}</strong>
                <span>{{ t('telegram.bot') }}</span>
              </div>
            </div>

            <div class="services-telegram__message">
              <strong>
                {{ t('telegram.bot.question') }}
              </strong>
            </div>

            <div class="services-telegram__buttons">
              <div>
                <Wrench :size="14" />
                {{ t('telegram.bot.repair') }}
              </div>

              <div>
                <Faucet :size="14" />
                {{ t('telegram.bot.installation') }}
              </div>

              <div>
                <Waves :size="14" />
                {{ t('telegram.bot.sewerage') }}
              </div>

              <div>
                <Flame :size="14" />
                {{ t('telegram.bot.heating') }}
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  </section>
</template>
