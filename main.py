from flask import Flask, request, render_template
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import threading, os

from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

# ================= CONFIG =================
TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = "https://your-app.up.railway.app"
DATABASE_URL = os.getenv("DATABASE_URL")

# ================= DB =================
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class UserCode(Base):
    __tablename__ = "usercode"
    user_id = Column(String, primary_key=True)
    code = Column(Text)
    plan = Column(String, default="free")

Base.metadata.create_all(engine)

# ================= APP =================
app = Flask(__name__)

# ================= WEB =================

@app.route("/")
def home():
    return "Cloud IDE Running 🚀"

@app.route("/editor")
def editor():
    return render_template("editor.html")

@app.route("/load")
def load():
    user = request.args.get("user")
    data = session.query(UserCode).filter_by(user_id=user).first()
    return data.code if data else "<h1>Start Coding 🚀</h1>"

@app.route("/save", methods=["POST"])
def save():
    data = request.json
    user = data["user"]
    code = data["code"]

    u = session.query(UserCode).filter_by(user_id=user).first()

    if not u:
        u = UserCode(user_id=user, code=code)
        session.add(u)
    else:
        u.code = code

    session.commit()
    return "OK"

@app.route("/preview")
def preview():
    user = request.args.get("user")
    data = session.query(UserCode).filter_by(user_id=user).first()

    code = data.code if data else "<h1>No Code</h1>"

    return f"""
    <iframe style='width:100%;height:100vh;border:none'
    srcdoc='{code}'></iframe>
    """

# ================= BOT =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)

    # cek user
    u = session.query(UserCode).filter_by(user_id=uid).first()
    if not u:
        session.add(UserCode(user_id=uid, code="<h1>Hello</h1>"))
        session.commit()

    await update.message.reply_text(
        f"🚀 IDE siap!\n\n👉 {BASE_URL}/editor?user={uid}"
    )

# 🔥 PREMIUM LOCK
async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    u = session.query(UserCode).filter_by(user_id=uid).first()

    u.plan = "pro"
    session.commit()

    await update.message.reply_text("🔥 Kamu sekarang PRO!")

def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("upgrade", premium))
    app_bot.run_polling()

# ================= RUN =================

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))