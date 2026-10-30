import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Your Credentials
API_ID = 30761712
API_HASH = "6f1240a3461b12a7eacd1b5b65d89bec"
BOT_TOKEN = "9094898339:AAFlXuEuMxxkexU1gliFDgWgXydgR0JnrqU"

# আপনার টেলিগ্রাম আইডি (অ্যাডমিন)
ADMIN_ID = 7741441989

# ৪টি বাধ্যতামূলক গ্রুপ/চ্যানেলের লিংক বা ইউজারনেম
# (বটকে অবশ্যই এই চ্যানেলগুলোতে Admin করে রাখতে হবে)
CHANNELS = [
    "@publicchat084",
    "https://t.me/+oialIN5nGMpmYzU1",
    "https://t.me/+0XtG3hTk1QNlZGZl",
    "https://t.me/+hbnMRX43ciU3MDBl"
]

# অ্যাপের তথ্য (বট থেকে এগুলো পরিবর্তন করা যাবে)
app_data = {
    "username": "LxShakil_App",
    "password": "SecurePassword123",
    "link": "https://t.me"
}

# ইউজারদের লিস্ট সেভ রাখার জন্য
users_set = set()

async def check_user_membership(user_id, context: ContextTypes.DEFAULT_TYPE):
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            print(f"Error checking channel {channel}: {e}")
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users_set.add(user_id)
    
    # মেম্বারশিপ চেক করা
    is_joined = await check_user_membership(user_id, context)
    
    if is_joined:
        content = (
            f"🎉 অভিনন্দন! আপনি সফলভাবে সবগুলোতে জয়েন করেছেন।\n\n"
            f"🔐 বর্তমান অ্যাপের তথ্য নিচে দেওয়া হলো:\n"
            f"- Username: `{app_data['username']}`\n"
            f"- Password: `{app_data['password']}`\n"
            f"- Download Link: {app_data['link']}"
        )
        await update.message.reply_text(content, parse_mode="Markdown")
    else:
        keyboard = [
            [InlineKeyboardButton("🔗 জয়েন চ্যানেল ১", url="https://t.me/+oialIN5nGMpmYzU1")],
            [InlineKeyboardButton("🔗 জয়েন চ্যানেল ২", url="https://t.me/publicchat084")],
            [InlineKeyboardButton("🔗 জয়েন চ্যানেল ৩", url="https://t.me/+0XtG3hTk1QNlZGZl")],
            [InlineKeyboardButton("🔗 জয়েন চ্যানেল ৪", url="https://t.me/+hbnMRX43ciU3MDBl")],
            [InlineKeyboardButton("✅ আমি জয়েন করেছি (Check)", callback_data="check_join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "⚠️ বট ব্যবহারের আগে আপনাকে অবশ্যই আমাদের ৪টি টেলিগ্রাম গ্রুপ/চ্যানেলে জয়েন করতে হবে!\n\n"
            "সবগুলোতে জয়েন করার পর নিচের **✅ আমি জয়েন করেছি (Check)** বাটনে ক্লিক করুন:",
            reply_markup=reply_markup
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "check_join":
        user_id = query.from_user.id
        is_joined = await check_user_membership(user_id, context)
        
        if is_joined:
            content = (
                f"🎉 ধন্যবাদ! আপনার জয়েন করা নিশ্চিত হয়েছে।\n\n"
                f"🔐 বর্তমান অ্যাপের তথ্য নিচে দেওয়া হলো:\n"
                f"- Username: `{app_data['username']}`\n"
                f"- Password: `{app_data['password']}`\n"
                f"- Download Link: {app_data['link']}"
            )
            await query.message.edit_text(content, parse_mode="Markdown")
        else:
            await query.answer("❌ আপনি এখনো সবকটি গ্রুপ/চ্যানেলে জয়েন করেননি! দয়া করে সবগুলোতে জয়েন করে আবার চেক করুন।", show_alert=True)

# অ্যাডমিন কমান্ড: ইউজারনেম পরিবর্তনের জন্য (/setuser নতুন_নাম)
async def set_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ আপনার এই কমান্ড ব্যবহারের অনুমতি নেই!")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ ব্যবহার: /setuser [নতুন ইউজারনেম]")
        return
    
    new_user = " ".join(context.args)
    app_data["username"] = new_user
    await update.message.reply_text(f"✅ সফলভাবে ইউজারনেম আপডেট করা হয়েছে: `{new_user}`", parse_mode="Markdown")

# অ্যাডমিন কমান্ড: পাসওয়ার্ড পরিবর্তনের জন্য (/setpass নতুন_পাসওয়ার্ড)
async def set_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ আপনার এই কমান্ড ব্যবহারের অনুমতি নেই!")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ ব্যবহার: /setpass [নতুন পাসওয়ার্ড]")
        return
    
    new_pass = " ".join(context.args)
    app_data["password"] = new_pass
    await update.message.reply_text(f"✅ সফলভাবে পাসওয়ার্ড আপডেট করা হয়েছে: `{new_pass}`", parse_mode="Markdown")

# অ্যাডমিন ব্রডকাস্ট সিস্টেম
async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    message_text = update.message.text
    success_count = 0
    
    for uid in users_set:
        try:
            await context.bot.send_message(chat_id=uid, text=message_text)
            success_count += 1
        except Exception as e:
            print(f"Error sending to {uid}: {e}")
            
    await update.message.reply_text(f"📢 ব্রডকাস্ট সফল! মোট {success_count} জন ইউজারের কাছে মেসেজ পাঠানো হয়েছে।")

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setuser", set_username))
    application.add_handler(CommandHandler("setpass", set_password))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast_message))

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
