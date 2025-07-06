class TranslationsService:
    UZ = "uz"
    EN = "en"
    RU = "ru"

    TEXTS = {
        UZ: {
            "hello": "Assalomu alaykum, {}! Botimizga xush kelibsiz. Iltimos, tilni tanlang.",
            "language_selected": "Til muvaffaqiyatli tanlandi. Endi savolingizni yozishingiz mumkin. Men tayyorman.",
        },
        EN: {
            "hello": "Hello, {}! Welcome to our bot. Please choose your language.",
            "language_selected": "Language successfully selected. You can now type your question. I'm ready.",
        },
        RU: {
            "hello": "Здравствуйте, {}! Добро пожаловать в нашего бота. Пожалуйста, выберите язык.",
            "language_selected": "Язык успешно выбран. Теперь вы можете задать свой вопрос. Я готов.",
        },
    }

    def get_text(self, text: str, lang: str = "uz") -> str:
        return self.TEXTS.get(lang, self.TEXTS[self.UZ]).get(text, text)
