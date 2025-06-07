
from pyrogram import Client, filters
from pyrogram.types import Message
import json
import os
from data.config import OWNER_ID

ORDERS_FILE = "data/orders.json"

# Utilities for order management
def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, "r") as f:
        return json.load(f)

def save_orders(orders):
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)

def add_order(name, user_id, price_filter):
    orders = load_orders()
    orders.append({"name": name, "target_user": user_id, "filter": price_filter})
    save_orders(orders)

def remove_order(name):
    orders = load_orders()
    orders = [o for o in orders if o["name"] != name]
    save_orders(orders)

# Simulated list of available gifts
def list_gifts():
    return ["gift_premium", "gift_vip", "gift_basic"]

# Simulated manual purchase function
async def manual_purchase(gift_name, user_id, quantity):
    print(f"Buying {quantity}x '{gift_name}' for user {user_id}...")

# Command: /start
@Client.on_message(filters.command("start") & filters.user(OWNER_ID))
async def start_bot(client: Client, message: Message):
    await message.reply("✅ Bot started.")

# Command: /stop
@Client.on_message(filters.command("stop") & filters.user(OWNER_ID))
async def stop_bot(client: Client, message: Message):
    await message.reply("🛑 Bot stopped.")

# Command: /status
@Client.on_message(filters.command("status") & filters.user(OWNER_ID))
async def status_bot(client: Client, message: Message):
    await message.reply("📊 Bot is online.")

# Command: /orders
@Client.on_message(filters.command("orders") & filters.user(OWNER_ID))
async def list_orders(client: Client, message: Message):
    orders = load_orders()
    if not orders:
        await message.reply("📭 No active orders.")
    else:
        text = "\n".join([f"🔹 {o['name']} ({o['target_user']}) - {o['filter']}" for o in orders])
        await message.reply(f"📦 Active Orders:\n{text}")

# Command: /add_order [name] [user_id] [filter]
@Client.on_message(filters.command("add_order") & filters.user(OWNER_ID))
async def cmd_add_order(client: Client, message: Message):
    try:
        _, name, user_id, price_filter = message.text.split()
        add_order(name, int(user_id), price_filter)
        await message.reply(f"✅ Order '{name}' added for user {user_id} with filter {price_filter}.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# Command: /remove_order [name]
@Client.on_message(filters.command("remove_order") & filters.user(OWNER_ID))
async def cmd_remove_order(client: Client, message: Message):
    try:
        _, name = message.text.split()
        remove_order(name)
        await message.reply(f"🗑️ Order '{name}' removed.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

# Command: /gifts
@Client.on_message(filters.command("gifts") & filters.user(OWNER_ID))
async def cmd_list_gifts(client: Client, message: Message):
    gifts = list_gifts()
    await message.reply("🎁 Available gifts:\n" + "\n".join(gifts))

# Command: /buy [gift_name] [user_id] [quantity]
@Client.on_message(filters.command("buy") & filters.user(OWNER_ID))
async def cmd_buy_gift(client: Client, message: Message):
    try:
        _, gift_name, user_id, qty = message.text.split()
        await manual_purchase(gift_name, int(user_id), int(qty))
        await message.reply(f"🛒 Purchased {qty}x '{gift_name}' for user {user_id}.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")
