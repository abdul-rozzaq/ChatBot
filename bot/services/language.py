class TranslationsService:
    UZ = "uz"
    EN = "en"
    RU = "ru"

    TEXTS = {
        UZ: {
            "hello": "Assalomu alaykum, {}! Botimizga xush kelibsiz. Iltimos, tilni tanlang.",
            "language_selected": "Til muvaffaqiyatli tanlandi. Endi savolingizni yozishingiz mumkin. Men tayyorman.",
            "usage_count": "Sizda {count} ta savol berish imkoniyati qoldi.",
            "limit_exceeded": "Kechirasiz, bugungi savol berish limitiga yetdingiz. Yangi savollarni ertaga bera olasiz.",
        },
        EN: {
            "hello": "Hello, {}! Welcome to our bot. Please choose your language.",
            "language_selected": "Language successfully selected. You can now type your question. I'm ready.",
            "usage_count": "You have {count} questions remaining.",
            "limit_exceeded": "Sorry, you have reached today's question limit. You can ask new questions tomorrow.",
        },
        RU: {
            "hello": "Здравствуйте, {}! Добро пожаловать в нашего бота. Пожалуйста, выберите язык.",
            "language_selected": "Язык успешно выбран. Теперь вы можете задать свой вопрос. Я готов.",
            "usage_count": "У вас осталось {count} вопросов.",
            "limit_exceeded": "Извините, вы достигли лимита вопросов на сегодня. Вы сможете задать новые вопросы завтра.",
        },
    }

    def get_text(self, text: str, lang: str = "uz") -> str:
        return self.TEXTS.get(lang, self.TEXTS[self.UZ]).get(text, text)
