import { ref } from 'vue'

const SUPPORTED_LANGUAGES = ['ru', 'uz', 'en', 'zh']
const API_URL = 'http://127.0.0.1:8002/api/translations/'

const savedLanguage = localStorage.getItem('site_language')

const currentLanguage = ref(
  SUPPORTED_LANGUAGES.includes(savedLanguage)
    ? savedLanguage
    : 'ru'
)

const translations = ref({})
const loading = ref(false)
const error = ref(null)

const loadTranslations = async (language = currentLanguage.value) => {
  if (!SUPPORTED_LANGUAGES.includes(language)) {
    language = 'ru'
  }

  loading.value = true
  error.value = null

  try {
    const response = await fetch(
      `${API_URL}?lang=${encodeURIComponent(language)}`
    )

    if (!response.ok) {
      throw new Error(`Translation request failed: ${response.status}`)
    }

    const data = await response.json()

    translations.value = data.translations || {}
    currentLanguage.value = data.language || language

    localStorage.setItem('site_language', currentLanguage.value)
  } catch (err) {
    console.error('Failed to load translations:', err)
    error.value = err
  } finally {
    loading.value = false
  }
}

const setLanguage = async (language) => {
  if (!SUPPORTED_LANGUAGES.includes(language)) {
    language = 'ru'
  }

  await loadTranslations(language)
}

const t = (key) => {
  return translations.value[key] || key
}

export function useLanguage() {
  return {
    currentLanguage,
    translations,
    loading,
    error,
    t,
    setLanguage,
    loadTranslations,
    SUPPORTED_LANGUAGES,
  }
}
