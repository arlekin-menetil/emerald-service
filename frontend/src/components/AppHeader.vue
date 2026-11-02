<script setup>
import { ref, onMounted } from 'vue'
import {
  Menu,
  Phone,
  X,
  Star,
  Bot,
  Building2,
  MapPin,
  ShoppingBag,
  Languages,
} from '@lucide/vue'

import { useLanguage } from '../composables/useLanguage'

const isMenuOpen = ref(false)

const {
  currentLanguage,
  setLanguage,
  loadTranslations,
  t,
} = useLanguage()

const closeMenu = () => {
  isMenuOpen.value = false
}

const languages = [
  { code: 'ru', label: 'RU' },
  { code: 'uz', label: 'UZ' },
  { code: 'en', label: 'EN' },
  { code: 'zh', label: '中文' },
]

const changeLanguage = async (language) => {
  await setLanguage(language)
}

onMounted(() => {
  loadTranslations()
})

const lastScrollY = ref(0)
const headerHidden = ref(false)

const handleScroll = () => {
  const currentScrollY = window.scrollY

  if (currentScrollY < 20) {
    headerHidden.value = false
  } else if (currentScrollY > lastScrollY.value + 5) {
    headerHidden.value = true
  } else if (currentScrollY < lastScrollY.value - 5) {
    headerHidden.value = false
  }

  lastScrollY.value = currentScrollY
}

onMounted(() => {
  lastScrollY.value = window.scrollY
  window.addEventListener("scroll", handleScroll, { passive: true })
})

</script>

<template>
  <header class="header" :class="{ 'header--hidden': headerHidden }">
    <div class="header__inner">

      <!-- ЛОГОТИП -->
      <RouterLink
        to="/"
        class="logo"
        @click="closeMenu"
      >
        <img
          src="/logo.png"
          alt="ИЗУМРУД СЕРВИС"
        />
      </RouterLink>

      <!-- DESKTOP NAV -->
      <nav class="nav">

        <RouterLink
          to="/"
          class="nav__link"
        >
          {{ t('header.home') }}
        </RouterLink>

        <RouterLink
          to="/services"
          class="nav__link"
        >
          {{ t('header.services') }}
        </RouterLink>

        <RouterLink
          to="/about"
          class="nav__link"
        >
          {{ t('header.about') }}
        </RouterLink>

        <!-- РЕЙТИНГ УСЛУГ -->
        <RouterLink
          to="/ratings"
          class="nav__link"
        >
          {{ t('header.ratings') }}
        </RouterLink>

        <!-- TELEGRAM -->
        <RouterLink
          to="/telegram-bot"
          class="nav__link"
        >
          {{ t('header.telegram') }}
        </RouterLink>

        <!-- МАГАЗИН -->
        <RouterLink
          to="/shop"
          class="nav__link"
        >
          {{ t('header.shop') }}
        </RouterLink>

        <!-- КОНТАКТЫ -->
        <RouterLink
          to="/contacts"
          class="nav__link"
        >
          {{ t('header.contacts') }}
        </RouterLink>

      </nav>

      <!-- ACTIONS -->
      <div class="header__actions">

        <!-- LANGUAGE -->
        <div class="language-switcher">

          <button
            v-for="language in languages"
            :key="language.code"
            type="button"
            :class="[
              'language-switcher__item',
              {
                'language-switcher__item--active':
                  currentLanguage === language.code,
              },
            ]"
            @click="changeLanguage(language.code)"
          >
            {{ language.label }}
          </button>
        </div>

        <!-- CALL -->
        <RouterLink
          to="/request"
          class="phone"
        >
          <Phone
            :size="17"
            :stroke-width="2.2"
          />

          <span>
            {{ t('header.call_plumber') }}
          </span>
        </RouterLink>

        <!-- MOBILE MENU -->
        <button
          class="menu-button"
          type="button"
          :aria-label="
            isMenuOpen
              ? t('menu.close')
              : t('menu.open')
          "
          :aria-expanded="isMenuOpen"
          @click="isMenuOpen = !isMenuOpen"
        >
          <X
            v-if="isMenuOpen"
            :size="27"
            :stroke-width="2"
          />

          <Menu
            v-else
            :size="27"
            :stroke-width="2"
          />
        </button>

      </div>
    </div>

    <!-- MOBILE MENU -->
    <Transition name="mobile-menu">
      <div
        v-if="isMenuOpen"
        class="mobile-menu"
      >
        <nav class="mobile-nav">

          <!-- MOBILE LANGUAGE -->
          <div class="mobile-language">

            <Languages
              :size="18"
              :stroke-width="2"
            />

            <span class="mobile-language__title">
              {{ t('header.language') }}
            </span>

            <div class="mobile-language__options">
              <button
                v-for="language in languages"
                :key="language.code"
                type="button"
                :class="[
                  'mobile-language__item',
                  {
                    'mobile-language__item--active':
                      currentLanguage === language.code,
                  },
                ]"
                @click="changeLanguage(language.code)"
              >
                {{ language.label }}
              </button>
            </div>

          </div>

          <!-- Главная -->
          <RouterLink
            to="/"
            class="mobile-nav__link"
            @click="closeMenu"
          >
            <Building2 :size="19" />
            <span>{{ t('header.home') }}</span>
          </RouterLink>

          <!-- Услуги -->
          <RouterLink
            to="/services"
            class="mobile-nav__link"
            @click="closeMenu"
          >
            <Phone :size="19" />
            <span>{{ t('header.services') }}</span>
          </RouterLink>

          <!-- О компании -->
          <RouterLink
            to="/about"
            class="mobile-nav__link"
            @click="closeMenu"
          >
            <Building2 :size="19" />
            <span>{{ t('header.about') }}</span>
          </RouterLink>

          <!-- Рейтинг услуг -->
          <RouterLink
            to="/ratings"
            class="mobile-nav__link"
            @click="closeMenu"
          >
            <Star :size="19" />
            <span>{{ t('header.ratings') }}</span>
          </RouterLink>

          <!-- Telegram -->
          <RouterLink
            to="/telegram-bot"
            class="mobile-nav__link"
            @click="closeMenu"
          >
            <Bot :size="19" />
            <span>{{ t('header.telegram') }}</span>
          </RouterLink>

          <!-- Магазин -->
          <RouterLink
            to="/shop"
            class="mobile-nav__link"
            @click="closeMenu"
          >
            <ShoppingBag :size="19" />
            <span>{{ t('header.shop') }}</span>
          </RouterLink>

          <!-- Контакты -->
          <RouterLink
            to="/contacts"
            class="mobile-nav__link"
            @click="closeMenu"
          >
            <MapPin :size="19" />
            <span>{{ t('header.contacts') }}</span>
          </RouterLink>

          <!-- CTA -->
          <RouterLink
            to="/request"
            class="mobile-nav__cta"
            @click="closeMenu"
          >
            <Phone :size="18" />
            <span>{{ t('header.call_plumber') }}</span>
          </RouterLink>

        </nav>
      </div>
    </Transition>
  </header>
</template>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  transform: translateY(0);
  transition: transform 0.3s ease;
  transition: transform 0.25s ease;

  background: rgba(255, 255, 255, 0.94);

  border-bottom: 1px solid #e7eee9;

  backdrop-filter: blur(12px);
}

.header--hidden {
  transform: translateY(-100%);
}


.header__inner {
  width: min(1280px, calc(100% - 48px));

  min-height: 82px;

  margin: 0 auto;

  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 38px;
}

.logo {
  display: flex;
  align-items: center;

  flex-shrink: 0;
}

.logo img {
  display: block;

  width: 158px;
  height: auto;
}

.nav {
  display: flex;
  align-items: stretch;
  justify-content: space-between;

  flex: 1;
  gap: 10px;

  margin-left: 24px;
}

.nav__link {
  flex: 1;
  min-width: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  text-align: center;
  white-space: normal;

  color: #34433b;

  font-size: 14px;
  font-weight: 500;

  transition:
    color 0.2s ease,
    opacity 0.2s ease;
}

.nav__link:hover {
  color: #008c68;
}

.nav__link.router-link-active {
  color: #008c68;

  font-weight: 600;
}

.header__actions {
  display: flex;
  align-items: center;

  gap: 16px;
}

/* LANGUAGE SWITCHER */

.language-switcher {
  display: flex;
  align-items: center;

  gap: 2px;

  padding: 4px;

  border: 1px solid #dce8e3;
  border-radius: 10px;

  background: #f7faf8;

  color: #008c68;
}

.language-switcher__item {
  min-width: 34px;
  height: 30px;

  padding: 0 7px;

  border: 0;
  border-radius: 7px;

  background: transparent;

  color: #66756e;

  font-family: inherit;

  font-size: 11px;
  font-weight: 700;

  cursor: pointer;

  transition:
    background 0.2s ease,
    color 0.2s ease;
}

.language-switcher__item:hover {
  color: #008c68;

  background: #edf8f4;
}

.language-switcher__item--active {
  background: #008c68;

  color: #ffffff;
}

.language-switcher__item--active:hover {
  background: #007658;

  color: #ffffff;
}

/* CALL BUTTON */

.phone {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  gap: 8px;

  min-height: 44px;

  padding: 0 20px;

  border-radius: 12px;

  color: #ffffff;

  background: #008c68;

  font-size: 13px;
  font-weight: 700;

  transition:
    background 0.2s ease,
    transform 0.2s ease;
}

.phone:hover {
  background: #007658;

  transform: translateY(-1px);
}

/* MOBILE BUTTON */

.menu-button {
  display: none;

  width: 42px;
  height: 42px;

  align-items: center;
  justify-content: center;

  border: 1px solid #dce8e3;

  border-radius: 11px;

  background: #ffffff;

  color: #17201b;

  cursor: pointer;
}

.mobile-menu {
  display: none;
}

/* MOBILE LANGUAGE */

.mobile-language {
  display: flex;
  align-items: center;

  gap: 10px;

  min-height: 48px;

  padding: 0 13px;

  margin-bottom: 5px;

  border-bottom: 1px solid #e5eee9;

  color: #008c68;
}

.mobile-language__title {
  color: #34433b;

  font-size: 14px;
  font-weight: 600;
}

.mobile-language__options {
  display: flex;
  align-items: center;

  gap: 3px;

  margin-left: auto;
}

.mobile-language__item {
  min-width: 35px;
  height: 30px;

  padding: 0 7px;

  border: 1px solid #dce8e3;

  border-radius: 7px;

  background: #ffffff;

  color: #66756e;

  font-family: inherit;

  font-size: 10px;
  font-weight: 700;

  cursor: pointer;

  transition:
    background 0.2s ease,
    color 0.2s ease,
    border-color 0.2s ease;
}

.mobile-language__item:hover {
  border-color: #008c68;

  color: #008c68;
}

.mobile-language__item--active {
  border-color: #008c68;

  background: #008c68;

  color: #ffffff;
}

.mobile-language__item--active:hover {
  background: #007658;

  color: #ffffff;
}

/* Mobile */

@media (max-width: 1050px) {
  .nav {
    gap: 19px;
  }

  .nav__link {
    font-size: 13px;
  }

  .phone span {
    display: none;
  }

  .phone {
    width: 44px;
    height: 44px;

    padding: 0;
  }
}

@media (max-width: 850px) {
  .header__inner {
    min-height: 72px;

    width: min(100% - 28px, 1200px);
  }

  .logo img {
    width: 125px;
  }

  .nav {
    display: none;
  }

  .phone {
    display: none;
  }

  .language-switcher {
    display: none;
  }

  .menu-button {
    display: flex;
  }

  .mobile-menu {
    display: block;

    position: absolute;

    top: 100%;

    left: 0;
    right: 0;

    padding: 12px 14px 18px;

    border-bottom: 1px solid #e1ebe6;

    background: rgba(255, 255, 255, 0.98);

    box-shadow:
      0 18px 35px rgba(20, 50, 40, 0.1);
  }

  .mobile-nav {
    width: min(100%, 520px);

    margin: 0 auto;

    display: grid;

    gap: 5px;
  }

  .mobile-nav__link {
    display: flex;
    align-items: center;

    gap: 12px;

    min-height: 48px;

    padding: 0 13px;

    border-radius: 10px;

    color: #34433b;

    font-size: 14px;
    font-weight: 600;
  }

  .mobile-nav__link:hover {
    background: #edf8f4;

    color: #008c68;
  }

  .mobile-nav__link svg {
    color: #008c68;
  }

  .mobile-nav__cta {
    display: flex;
    align-items: center;
    justify-content: center;

    gap: 9px;

    min-height: 48px;

    margin-top: 8px;

    border-radius: 11px;

    background: #008c68;

    color: #ffffff;

    font-size: 14px;
    font-weight: 700;
  }
}

/* Animation */

.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;

  transform: translateY(-8px);
}
</style>
