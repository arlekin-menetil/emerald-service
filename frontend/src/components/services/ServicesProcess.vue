<script setup>
import { useLanguage } from '../../composables/useLanguage'

const { t } = useLanguage()
</script>

<template>
  <section class="services-process">
    <div class="services-container">
      <div class="services-section-heading services-section-heading--center">
        <span>{{ t('process.title') }}</span>

        <h2>
          {{ t('process.subtitle') }}
          <strong>{{ t('process.subtitle_accent') }}</strong>
        </h2>
      </div>

      <div class="services-process-grid">
        <article class="services-process-step">
          <div class="services-process-step__number">01</div>
          <h3>{{ t('process.step1.title') }}</h3>
          <p>{{ t('process.step1.description') }}</p>
        </article>

        <article class="services-process-step">
          <div class="services-process-step__number">02</div>
          <h3>{{ t('process.step2.title') }}</h3>
          <p>{{ t('process.step2.description') }}</p>
        </article>

        <article class="services-process-step">
          <div class="services-process-step__number">03</div>
          <h3>{{ t('process.step3.title') }}</h3>
          <p>{{ t('process.step3.description') }}</p>
        </article>

        <article class="services-process-step">
          <div class="services-process-step__number">04</div>
          <h3>{{ t('process.step4.title') }}</h3>
          <p>{{ t('process.step4.description') }}</p>
        </article>
      </div>
    </div>
  </section>
</template>
