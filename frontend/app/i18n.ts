import { initReactI18next } from "react-i18next";

import i18n from "i18next";
import LanguageDetector from "i18next-browser-languagedetector";

import translationEn from "./locales/translation-en.json";
import translationJa from "./locales/translation-ja.json";

const resources = {
  ja: { translation: translationJa },
  en: { translation: translationEn },
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: "ja",
    supportedLngs: ["ja", "en"],
    load: "languageOnly",
    resources,
    interpolation: { escapeValue: false },
  });

export default i18n;
