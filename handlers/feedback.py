from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from config.database import get_db
from config.settings import settings

db = get_db()
FEEDBACK_WAITING = 1


async def start_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # ተጠቃሚው የትኛው ፖርትፎሊዮ ላይ አስተያየት እንደሰጠ ለማወቅ ID ውን እንይዛለን
    item_id = query.data.replace("give_fb_", "")
    context.user_data["feedback_item_id"] = item_id

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="✍️ **እባክዎን ለዚህ የዲዛይን ስራ ያለዎትን አስተያየት (Feedback) ይጻፉልን፦**\n\n_(ሂደቱን ለማቋረጥ /cancel ማለትን ይችላሉ)_",
        parse_mode="Markdown"
    )
    return FEEDBACK_WAITING


async def receive_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message
    chat_id = update.effective_chat.id
    username = update.effective_user.username or "No Username"
    full_name = update.effective_user.full_name or "Unknown"
    item_id = context.user_data.get("feedback_item_id", "Unknown")

    # ለአድሚኖች ማስተላለፊያ ሪፖርት
    feedback_report = (
        "💡 **አዲስ አስተያየት (New Feedback) ደርሷል!**\n\n"
        f"👤 **ከተጠቃሚ፦** {full_name} (@{username})\n"
        f"🆔 **የተጠቃሚ ID፦** `{chat_id}`\n"
        f"🖼️ **የስራው (Portfolio) ID፦** `{item_id}`\n\n"
        f"💬 **የተሰጠ አስተያየት፦**\n{user_msg.text}"
    )

    # በ .env ውስጥ ላሉት አድሚኖች በሙሉ መላክ
    for admin_id in settings.ADMIN_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=feedback_report, parse_mode="Markdown")
        except Exception as e:
            print(f"Failed to forward feedback to admin {admin_id}: {e}")

    await update.message.reply_text("🙏 ስላስተያየትዎ እጅግ እናመሰግናለን! አስተያየትዎ ለድርጅቱ አድሚን ተላልፏል።")
    context.user_data.clear()
    return ConversationHandler.END


async def cancel_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ የአስተያየት መስጫው ተቋርጧል።")
    context.user_data.clear()
    return ConversationHandler.END

# በ main.py ውስጥ "from handlers.feedback import feedback_conv" ተብሎ የሚጠራው ዋናው ተለዋዋጭ ይህ ነው፡
feedback_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_feedback, pattern="^give_fb_")],
    states={
        FEEDBACK_WAITING: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, receive_feedback)]
    },
    fallbacks=[CommandHandler("cancel", cancel_feedback)]
)
