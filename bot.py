import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode

# Твой токен
TOKEN = "8077022394:AAHQ2reeEn4t4GV_ufzkYnHf82AqLTbf84c"

# Логирование
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Клавиатура с чаевыми - 2 ряда по 3 и 2 кнопки
def get_tips_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="⭐ 1 звезда", callback_data="tip_1"),
            InlineKeyboardButton(text="⭐⭐ 15 звёзд", callback_data="tip_15"),
            InlineKeyboardButton(text="⭐⭐⭐ 25 звёзд", callback_data="tip_25")
        ],
        [
            InlineKeyboardButton(text="⭐⭐⭐⭐ 50 звёзд", callback_data="tip_50"),
            InlineKeyboardButton(text="⭐⭐⭐⭐⭐ 100 звёзд", callback_data="tip_100")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    text = (
        "🎯 **Поддержи проект!**\n\n"
        "👉 **Поддержи меня звёздами**\n"
        "👈 **Чаевые за работу!**\n\n"
        "Выбери сумму:\n"
        "👇 Нажми на кнопку 👇\n\n"
        "———————————————\n"
        "✅ **Хороший гарант:** @wozsk"
    )
    await message.answer(text, reply_markup=get_tips_keyboard(), parse_mode=ParseMode.MARKDOWN)

# Обработка нажатия на кнопки
@dp.callback_query(F.data.startswith("tip_"))
async def process_tip(callback: types.CallbackQuery):
    amount = callback.data.split("_")[1]
    stars = int(amount)
    
    title = f"Чаевые {stars} ⭐"
    description = "Поддержи меня звёздами!"
    payload = f"tip_{stars}"
    currency = "XTR"
    prices = [{"label": "Чаевые за работу!", "amount": stars}]
    
    try:
        await bot.send_invoice(
            chat_id=callback.from_user.id,
            title=title,
            description=description,
            payload=payload,
            provider_token="",
            currency=currency,
            prices=prices,
        )
        await callback.answer("💰 Отправляю счёт...")
    except Exception as e:
        await callback.answer("Ошибка!", show_alert=True)
        logging.error(f"Ошибка: {e}")

# Проверка оплаты
@dp.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Успешная оплата
@dp.message(F.successful_payment)
async def successful_payment(message: types.Message):
    stars = message.successful_payment.total_amount
    await message.answer(
        f"✨ Спасибо за чаевые {stars} ⭐!\n"
        f"Твоя поддержка очень важна 🤝\n\n"
        f"———————————————\n"
        f"✅ **Хороший гарант:** @wozsk",
        parse_mode=ParseMode.MARKDOWN
    )

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())