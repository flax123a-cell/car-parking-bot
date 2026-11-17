import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, ConversationHandler, filters

# تحديد حالات المحادثة
GET_EMAIL, GET_PASSWORD = range(2)

# دالة البداية /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك يا بطل في بوت Car Parking Multiplayer!\nالرجاء إرسال **الإيميل** الخاص بك أولاً:"
    )
    return GET_EMAIL

# استقبال الإيميل وطلب الباسورد
async def receive_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['email'] = update.message.text
    await update.message.reply_text("تم حفظ الإيميل بنجاح ✅\nالآن، أدخل **كلمة المرور (الباسورد)**:")
    return GET_PASSWORD

# استقبال الباسورد وعرض قائمة الخدمات والـ ID
async def receive_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['password'] = update.message.text
    
    # جلب الـ ID الخاص بالمستخدم على تيليجرام
    user_id = update.effective_user.id
    
    success_message = (
        f"🎉 **تم تسجيل الدخول بنجاح!**\n\n"
        f"👤 **معلومات الحساب:**\n"
        f"• الإيميل: {context.user_data['email']}\n"
        f"• الـ ID الخاص بك: `{user_id}`\n\n"
        f"اختر الخدمة المطلوبة من القائمة أدناه:"
    )
    
    # أزرار القائمة الرئيسية للخدمات
    keyboard = [
        [InlineKeyboardButton("💰 زيادة الفلوس (Money)", callback_data="money")],
        [InlineKeyboardButton("🪙 زيادة الكوينز (Coins)", callback_data="coins")],
        [InlineKeyboardButton("🏎️ ترقية الموتور (Engine)", callback_data="engine")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(success_message, reply_markup=reply_markup, parse_mode="Markdown")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم إلغاء العملية.")
    return ConversationHandler.END

# إعداد البوت وتشغيله
if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GET_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_email)],
            GET_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_password)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()
