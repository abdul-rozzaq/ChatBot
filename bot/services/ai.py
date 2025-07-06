import aiohttp

from config import settings


class AI:
    async def send_prompt(self, text, lang, old_messages):
        headers = {
            "Authorization": f"Bearer {settings.AI_TOKEN}",
            "Content-Type": "application/json",
        }

        messages = [
            {
                "role": "system",
                "content": f"Savollar qanday tilda bo'lishiga qaramay Siz savollarga {lang} tilida javob berasiz, sizning ismingiz ChatBot.",
            },
            {
                "role": "system",
                "content": "Matnlarni formatlashda markdown ishlating, lekin telegram qoidalariga amal qilgan holda. Markdown to'g'ri ishlatilganiga qattiq e'tibor berish kerak",
            },
            {
                "role": "system",
                "content": "Qisqa va londa javob qaytarishga harakat qiling. Response max uzunligi 4000 tagacha bo'lsin",
            },
        ]

        if old_messages:
            messages.extend(old_messages)

        messages.append({"role": "user", "content": text})

        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
        }

        try:
            # return "Salom qanday yordam bera olaman ?"

            async with aiohttp.ClientSession() as session:
                async with session.post(settings.AI_BASE_URL, headers=headers, json=data, timeout=30) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    return json_data["choices"][0]["message"]["content"]

        except Exception as e:
            # Log the error if you have a logger, or print for debugging
            print(f"AI request failed: {e}")
            return "Kechirasiz, hozircha javob bera olmayman. Iltimos, keyinroq urinib ko'ring."
