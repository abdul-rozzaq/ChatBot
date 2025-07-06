class TranslationsService:
    UZ = "uz"
    EN = "en"
    RU = "ru"

    TEXTS = {
        UZ: {
            "hello": "Assalomu alaykum {}. Botimizga hush kelibsiz. Tilni tanlang",
            "language_selected": "Til muvaffaqqiyatli tanlandi. Savolingizni yozishingiz mumkin, men tayyorman",
        },
        EN: {},
        RU: {},
    }

    def get_text(self, text, lang="uz") -> str:
        return self.TEXTS.get(lang, self.TEXTS["uz"]).get(text, text)
