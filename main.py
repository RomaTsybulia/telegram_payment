import env
import logging

from aiogram import Bot, Dispatcher, executor, types

from aiogram.types.message import ContentType


logging.basicConfig(level=logging.INFO)

bot = Bot(token=env.TOKEN)
dp = Dispatcher(bot)

PRICE = types.LabeledPrice(label="Payment", amount=5 * 100)


@dp.message_handler(commands=["payment"])
async def payment(message: types.Message):
    if env.PAYMENT_TOKEN.split(":")[1] == "TEST":
        await bot.send_message(message.chat.id, "Payment!")

    await bot.send_invoice(
        message.chat.id,
        title="Payment for...",
        description="Payment description",
        provider_token=env.PAYMENT_TOKEN,
        currency="uah",
        is_flexible=False,
        prices=[PRICE],
        start_parameter="payment",
        payload="test-invoice-payload"
    )


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("Successful payment:")
    payment_info = message.successful_payment.to_python()
    for key, value in payment_info.items():
        print(f"{key} = {value}")

    await bot.send_message(message.chat.id, f"Payment for the amount {message.successful_payment.total_amount // 100} {message.successful_payment.currency} passed successfuly!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
