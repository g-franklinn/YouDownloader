let currentLanguage = 'english';

async function loadTranslations(language) {
    const response = await fetch("./static/translations.json");
    const data = await response.json();
    return data[language];
}

async function updateContent(language) {
    currentLanguage = language;
    const translation = await loadTranslations(language);
    for (const key in translation) {
        if (translation.hasOwnProperty(key)) {
            const element = document.getElementById(key);
            if (element) {
                element.innerHTML = translation[key];
            }
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('pt-btn').addEventListener("click", () => {
      document.documentElement.lang = "pt-br";
      updateContent("portuguese");
    });
  
    document.getElementById('en-btn').addEventListener("click", () => {
      document.documentElement.lang = "en";
      updateContent("english");
    });
  });