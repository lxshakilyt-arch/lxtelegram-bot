import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- কনফিগারেশন ও ক্রেন্ডেনশিয়ালস ---
API_ID = 30761712
API_HASH = "6f1240a3461b12a7eacd1b5b65d89bec"
BOT_TOKEN = "9094898339:AAFlXuEuMxxkexU1gliFDgWgXydgR0JnrqU"
ADMIN_ID = 7741441989  # আপনার টেলিগ্রাম আইডি

# বাধ্যতামূলক চ্যানেলগুলোর সঠিক চ্যাট আইডি (মাইনাস চিহ্নসহ পূর্ণসংখ্যা)
REQUIRED_CHANNELS = [
    -1002573110861,
    -1002571498580,
    -1003969824749
]

# ডিফল্ট অ্যাপ ডেটা (অ্যাডমিন কমান্ড দিয়ে এগুলো লাইভ পরিবর্তন করতে পারবেন)
app_data = {
    "username": "LxShakil_App",
    "password": "SecurePassword123",
    "link": "https://t.me"
}

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# --- মেম্বারশিপ চেক করার ফাংশন ---
async def check_user_membership(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            logger.error(f"Error checking membership for channel {channel}: {e}")
            return False
    return True

# --- /start কমান্ড ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    is_joined = await check_user_membership(user_id, context)
    
    if is_joined:
        content = (
            f"🎉 **স্বাগতম! আপনার সব চ্যানেলে জয়েন করা নিশ্চিত হয়েছে।**\n\n"
            f"📦 **আপনার কাঙ্ক্ষিত অ্যাপ ও তথ্য নিচে দেওয়া হলো:**\n"
            f"👤 **Username:** `{app_data['username']}`\n"
            f"🔑 **Password:** `{app_data['password']}`\n"
            f"📥 **Download Link:** {app_data['link']}"
        )
        await update.message.reply_text(content, parse_mode="Markdown")
    else:
        keyboard = [
            [InlineKeyboardButton("📢 জয়েন চ্যানেল ১", url="https://t.me/+oialIN5nGMpmYzU1")],
            [InlineKeyboardButton("📢 জয়েন চ্যানেল ২", url="https://t.me/+0XtG3hTk1QNlZGZl")],
            [InlineKeyboardButton("📢 জয়েন চ্যানেল ৩", url="https://t.me/+hbnMRX43ciU3MDBl")],
            [InlineKeyboardButton("✅ আমি জয়েন করেছি (Check)", callback_data="check_join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "⚠️ **বট ব্যবহারের আগে আপনাকে অবশ্যই আমাদের ৩টি চ্যানেলে জয়েন করতে হবে!**\n\n"
            "সবগুলোতে জয়েন করার পর নিচের **✅ আমি জয়েন করেছি (Check)** বাটনে ক্লিক করুন:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

# --- বাটন ক্লিক হ্যান্ডলার (Check Join) ---
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "check_join":
        user_id = query.from_user.id
        is_joined = await check_user_membership(user_id, context)
        
        if is_joined:
            content = (
                f"🎉 **ধন্যবাদ! আপনার জয়েন করা নিশ্চিত হয়েছে।**\n\n"
                f"📦 **আপনার কাঙ্ক্ষিত অ্যাপ ও তথ্য নিচে দেওয়া হলো:**\n"
                f"👤 **Username:** `{app_data['username']}`\n"
                f"🔑 **Password:** `{app_data['password']}`\n"
                f"📥 **Download Link:** {app_data['link']}"
            )
            await query.message.edit_text(content, parse_mode="Markdown")
        else:
            await query.answer("❌ আপনি এখনো সবকটি চ্যানেলে জয়েন করেননি! দয়া করে সবগুলোতে জয়েন করে আবার চেক করুন।", show_alert=True)

# --- অ্যাডমিন কমান্ড: ইউজারনেম সেট করতে (/setuser) ---
async def set_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if context.args:
        new_user = " ".join(context.args)
        app_data['username'] = new_user
        await update.message.reply_text(f"✅ সফলভাবে ইউজারনেম আপডেট করা হয়েছে:\n`{new_user}`", parse_mode="Markdown")
    else:
        await update.message.reply_text("⚠️ ব্যবহার: `/setuser [নতুন ইউজারনেম]`", parse_mode="Markdown")

# --- অ্যাডমিন কমান্ড: পাসওয়ার্ড সেট করতে (/setpass) ---
async def set_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if context.args:
        new_pass = context.args[0]
        app_data['password'] = new_pass
        await update.message.reply_text(f"✅ সফলভাবে পাসওয়ার্ড আপডেট করা হয়েছে:\n`{new_pass}`", parse_mode="Markdown")
    else:
        await update.message.reply_text("⚠️ ব্যবহার: `/setpass [নতুন পাসওয়ার্ড]`", parse_mode="Markdown")

# --- অ্যাডমিন কমান্ড: লিংক সেট করতে (/setlink) ---
async def set_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if context.args:
        new_link = context.args[0]
        app_data['link'] = new_link
        await update.message.reply_text(f"✅ সফলভাবে ডাউনলোড লিংক আপডেট করা হয়েছে:\n{new_link}")
    else:
        await update.message.reply_text("⚠️ ব্যবহার: `/setlink [নতুন লিংক]`")

# --- মেইন ফাংশন ---
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(CommandHandler("setuser", set_username))
    application.add_handler(CommandHandler("setpass", set_password))
    application.add_handler(CommandHandler("setlink", set_link))

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
