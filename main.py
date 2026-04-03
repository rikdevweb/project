from flask import Flask, request, render_template
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import threading, os

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")

app = Flask(__name__)

user_code = {}

# ===== WEB =====

@app.route("/")
def home():
    return "🚀 Cloud IDE Running"

@app.route("/editor")
def editor():
    return render_template("editor.html")

@app.route("/load")
def load():
    user = request.args.get("user")
    return user_code.get(user, "<h1>Start Coding 🚀</h1>")

@app.route("/save", methods=["POST"])
def save():
    data = request.json
    user_code[data["user"]] = data["code"]
    return "OK"

@app.route("/preview")
def preview():
    user = request.args.get("user")
    code = user_code.get(user, "<h1>No Code</h1>")

    return f"""
    <iframe style='width:100%;height:100vh;border:none'
    srcdoc='{code}'></iframe>
    """

# ===== BOT =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)

    await update.message.reply_text(
        f"🚀 IDE siap!\n\n👉 {BASE_URL}/editor?user={uid}"
    )

async def run_web(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)

    await update.message.reply_text(
        f"🔥 Preview:\n{BASE_URL}/preview?user={uid}"
    )

def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("run", run_web))
    app_bot.run_polling()

# ===== RUN =====

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))from flask import Flask, request, render_template
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import threading, os

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")

app = Flask(__name__)

user_code = {}

# ===== WEB =====

@app.route("/")
def home():
    return "🚀 Cloud IDE Running"

@app.route("/editor")
def editor():
    return render_template("editor.html")

@app.route("/load")
def load():
    user = request.args.get("user")
    return user_code.get(user, "<h1>Start Coding 🚀</h1>")

@app.route("/save", methods=["POST"])
def save():
    data = request.json
    user_code[data["user"]] = data["code"]
    return "OK"

@app.route("/preview")
def preview():
    user = request.args.get("user")
    code = user_code.get(user, "<h1>No Code</h1>")

    return f"""
    <iframe style='width:100%;height:100vh;border:none'
    srcdoc='{code}'></iframe>
    """

# ===== BOT =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)

    await update.message.reply_text(
        f"🚀 IDE siap!\n\n👉 {BASE_URL}/editor?user={uid}"
    )

async def run_web(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)

    await update.message.reply_text(
        f"🔥 Preview:\n{BASE_URL}/preview?user={uid}"
    )

def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("run", run_web))
    app_bot.run_polling()

# ===== RUN =====

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
