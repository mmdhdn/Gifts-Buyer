
import asyncio
import traceback
import os

from pyrogram import Client

from app.core.banner import display_title, get_app_info, set_window_title
from app.core.callbacks import new_callback
from app.notifications import send_start_message
from app.utils.detector import detector
from app.utils.logger import info, error
from data.config import config, t, get_language_display, OWNER_ID

app_info = get_app_info()

# Dummy function to simulate fetching balance from API
def get_stars_balance():
    import random
    return random.randint(0, 100)

BALANCE_FILE = "data/last_balance.txt"

def load_last_balance():
    if not os.path.exists(BALANCE_FILE):
        return 0
    with open(BALANCE_FILE, "r") as f:
        return int(f.read())

def save_last_balance(balance):
    with open(BALANCE_FILE, "w") as f:
        f.write(str(balance))

async def check_balance_alert(client: Client):
    while True:
        try:
            current = get_stars_balance()
            last = load_last_balance()
            if current > last:
                await client.send_message(OWNER_ID, f"📈 Star balance increased: {last} → {current}")
                save_last_balance(current)
        except Exception as e:
            error(f"[BALANCE CHECK ERROR] {e}")
        await asyncio.sleep(30)

async def main() -> None:
    set_window_title(app_info)
    display_title(app_info, get_language_display(config.LANGUAGE))

    async with Client(
            name=config.SESSION,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            phone_number=config.PHONE_NUMBER
    ) as client:
        await send_start_message(client)
        asyncio.create_task(check_balance_alert(client))
        await detector(client, new_callback)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        info(t("console.terminated"))
    except Exception:
        error(t("console.unexpected_error"))
