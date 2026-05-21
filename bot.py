import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode

TOKEN = "8077022394:AAHQ2reeEn4t4GV_ufzkYnHf82AqLTbf84c"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_tips_keyboard():
    buttons = [
        [InlineKeyboardButton(text="1⭐", callback_data="tip_1")],
        [
            InlineKeyboardButton(text="15⭐", callback_data="tip_15"),
            InlineKeyboardButton(text="25⭐", callback_data="tip_25")
        ],
        [
            InlineKeyboardButton(text="50⭐", callback_data="tip_50"),
            InlineKeyboardButton(text="100⭐", callback_data="tip_100")
        ]
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
        logging.error(f"Ошибка: {e}")

@dp.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: types.Message):
    stars = message.successful_payment.total_amount
    await message.answer(
        f"✨ Спасибо за пожертвования в проект! ✨\n\n"
        f"Спасибо за чаевые {stars} ⭐!\n\n"
        f"Поддержать меня👇👇👇\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n✅ Хороший гарант: @wozsk",
        parse_mode=ParseMode.MARKDOWN
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())