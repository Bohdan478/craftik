import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from python_aternos import Client

TOKEN = os.getenv("BOT_TOKEN")
ATERNOS_USERNAME = os.getenv("ATERNOS_USER")
ATERNOS_PASSWORD = os.getenv("ATERNOS_PASS")

aternos = Client()
aternos.login(ATERNOS_USERNAME, ATERNOS_PASSWORD)

account = aternos.account
servers = account.list_servers()
server = servers[2]  # або індекс, який тобі треба

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Бот активований!")

async def run_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        server.start()
        await update.message.reply_text("🚀 Сервер запускається!")
    except Exception as e:
        await update.message.reply_text(f"❌ Помилка: {e}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        server.fetch()
        status = getattr(server, "status_str", server.status)
        await update.message.reply_text(f"📊 Статус: {status}")
    except Exception as e:
        await update.message.reply_text(f"❌ Помилка: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("run", run_server))
app.add_handler(CommandHandler("status", status))

print("Бот працює...")
app.run_polling()
