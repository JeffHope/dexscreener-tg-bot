import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN
from dexscreener import DexScreenerClient

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

current_pair = None
min_usd = 0
tx_type = 'buy'

@dp.message(Command('start'))
async def start(message: types.Message):
    buttons = [
        [KeyboardButton(text="Set Pair"), KeyboardButton(text="Check Transactions")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer(
        "👋 Welcome to DexScreener Bot!\n"
        "Use /setpair <pair_address> to set a token pair.",
        reply_markup=kb
    )

@dp.message(lambda message: message.text == "Check Transactions")
async def check_transactions_button(message: types.Message):
    await check_transactions(message)

@dp.message(Command('setpair'))
async def set_pair(message: types.Message, command: CommandObject):
    global current_pair
    if not command.args:
        await message.answer("❌ Please provide a pair address.")
        return
    current_pair = command.args.strip()
    client = DexScreenerClient(token_address=current_pair)
    pairs = await client.get_transactions()
    if not pairs:
        await message.answer("❌ Invalid pair or no data.")
        return
    await message.answer(f"✅ Pair set: {current_pair}")

@dp.message(Command('setmin'))
async def set_min_amount(message: types.Message, command: CommandObject):
    global min_usd
    if not command.args:
        await message.answer("❌ Please provide minimum USD amount.")
        return
    try:
        min_usd = float(command.args.strip())
        await message.answer(f"✅ Minimum USD set: {min_usd}")
    except ValueError:
        await message.answer("❌ Invalid amount.")

@dp.message(Command('settype'))
async def set_tx_type(message: types.Message, command: CommandObject):
    global tx_type
    if not command.args or command.args.lower() not in ['buy', 'sell']:
        await message.answer("❌ Please provide transaction type (buy/sell).")
        return
    tx_type = command.args.lower()
    await message.answer(f"✅ Transaction type set: {tx_type}")

@dp.message(Command('check'))
async def check_transactions(message: types.Message):
    if not current_pair:
        await message.answer("❌ Please set a pair first.")
        return
    client = DexScreenerClient(token_address=current_pair)
    pairs = await client.get_transactions()
    print(f"Pairs received: {pairs}")  # Отладочный вывод
    filtered = client.filter_transactions(pairs, min_usd=min_usd, tx_type=tx_type)
    print(f"Filtered transactions: {filtered}")  # Отладочный вывод
    if not filtered:
        await message.answer("❌ No transactions match the criteria.")
        return
    msg = f"✅ Transactions ({tx_type}):\n"
    for tx in filtered:
        if 'usd' in tx and isinstance(tx['usd'], str):
            msg += f"{tx['usd']}\n"
        else:
            msg += f"USD: {tx.get('usd', 'N/A')}\n"
    await message.answer(msg)

async def main():
    print("🤖 Bot started...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())