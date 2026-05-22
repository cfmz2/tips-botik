import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode
from aiohttp import web
import os

TOKEN = "8669610102:AAH59AUn8lEXOvLzX6b2-kxitcWYMmtl9Tw"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_tips_keyboard():
    buttons = [
        [InlineKeyboardButton(text="1⭐", callback_data="tip_1")],
        [InlineKeyboardButton(text="15⭐", callback_data="tip_15"), InlineKeyboardButton(text="25⭐", callback_data="tip_25")],
        [InlineKeyboardButton(text="50⭐", callback_data="tip_50"), InlineKeyboardButton(text="100⭐", callback_data="tip_100")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    text = "Поддержать меня👇👇👇\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n✅ Хороший гарант: @wozsk"
    await message.answer(text, reply_markup=get_tips_keyboard(), parse_mode=ParseMode.MARKDOWN)

@dp.callback_query(F.data.startswith("tip_"))
async def process_tip(callback: types.CallbackQuery):
    stars = int(callback.data.split("_")[1])
    try:
        await bot.send_invoice(
            chat_id=callback.from_user.id,
            title=f"Чаевые {stars} ⭐",
            description="Поддержать меня",
            payload=f"tip_{stars}",
            provider_token="",
            currency="XTR",
            prices=[{"label": "Чаевые за работу!", "amount": stars}],
        )
        await callback.answer("💰 Отправляю счёт...")
    except Exception as e:
        await callback.answer("Ошибка!", show_alert=True)

@dp.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: types.Message):
    await message.answer("Спасибо за пожертвования в проект!")

# Веб-сервер для Render
async def handle(request):
    return web.Response(text="Bot is running")

async def main():
    # Запускаем веб-сервер
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())