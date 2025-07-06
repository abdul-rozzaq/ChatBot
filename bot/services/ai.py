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

        async with aiohttp.ClientSession() as session:
            async with session.post(settings.AI_BASE_URL, headers=headers, json=data, timeout=30) as response:
                status = response.status

                if 200 <= status <= 299:
                    json_data = await response.json()
                    message = json_data["choices"][0]["message"]["content"]
                else:
                    message = "Kechirasiz, hozircha javob bera olmayman. Iltimos, keyinroq urinib ko'ring."

                return (status, message)
