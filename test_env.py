from dotenv import load_dotenv
import os

load_dotenv()

print("BOT_TOKEN =", os.getenv("TELEGRAM_BOT_TOKEN"))
