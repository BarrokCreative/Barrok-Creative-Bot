import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from config.settings import settings
from handlers.user import start_command, handle_static_buttons, show_portfolio_categories, navigate_portfolio

# ---------------------------------------------------------
# አዳዲሶቹ የአድሚን ፋንክሽኖች ከነባሮቹ ጋር ተደምረው ኢምፖርት ተደርገዋል
# ---------------------------------------------------------
from handlers.admin import (
    start_add_portfolio, category_chosen, media_uploaded,
    topic_entered, description_entered, confirm_post, cancel_action,
    admin_toggle_main, admin_handle_toggle, admin_delete_main, admin_handle_delete, admin_back_button,
    CHOOSING_CATEGORY, UPLOADING_MEDIA, ENTERING_TOPIC, ENTERING_DESCRIPTION, CONFIRMING_POST,
    # አዳዲስ የገቡት የአድሚን ሎጅኮች
    admin_menu, verify_command, handle_admin_callbacks,
    broadcast_command, broadcast_start_btn, receive_broadcast_message, cancel_admin, BROADCAST_WAITING
)

from handlers.order import (
    start_order_flow, order_name_entered, order_phone_entered, order_type_chosen,
    order_location_entered, order_requirements_entered, order_quantity_chosen,
    order_custom_quantity_entered, order_confirmed, cancel_order,
    ORDER_NAME, ORDER_PHONE, ORDER_TYPE, ORDER_LOCATION, ORDER_REQUIREMENTS, ORDER_QUANTITY, ORDER_CUSTOM_QUANTITY, ORDER_CONFIRMATION
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main():
    application = Application.builder().token(settings.BOT_TOKEN).build()

    # --- USER COMMANDS & BUTTONS ---
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(
        handle_static_buttons, pattern="^user_(main_menu|contact|about)$"))
    application.add_handler(CallbackQueryHandler(
        show_portfolio_categories, pattern="^user_portfolio$"))
    application.add_handler(CallbackQueryHandler(
        navigate_portfolio, pattern="^view_cat_"))

    # --- PERFECT ORDER CONVERSATION HANDLER ---
    order_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                start_order_flow, pattern="^user_order_start$"),
            CallbackQueryHandler(start_order_flow, pattern="^order_item_")
        ],
        states={
            ORDER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_name_entered)],
            ORDER_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               order_phone_entered),
                CallbackQueryHandler(order_phone_entered,
                                     pattern="^back_to_name$")
            ],
            ORDER_TYPE: [CallbackQueryHandler(order_type_chosen, pattern="^(type_|back_to_phone)")],
            ORDER_LOCATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               order_location_entered),
                CallbackQueryHandler(order_location_entered,
                                     pattern="^back_to_type$")
            ],
            ORDER_REQUIREMENTS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               order_requirements_entered),
                CallbackQueryHandler(
                    order_requirements_entered, pattern="^back_from_req$")
            ],
            ORDER_QUANTITY: [CallbackQueryHandler(order_quantity_chosen, pattern="^(qty_|back_to_req)")],
            ORDER_CUSTOM_QUANTITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               order_custom_quantity_entered),
                CallbackQueryHandler(
                    order_custom_quantity_entered, pattern="^back_to_qty_opt$")
            ],
            ORDER_CONFIRMATION: [CallbackQueryHandler(
                order_confirmed, pattern="^(order_confirm_submit|back_to_qty_opt)")]
        },
        fallbacks=[
            CallbackQueryHandler(cancel_order, pattern="^order_cancel$"),
            CommandHandler("cancel", cancel_order)
        ]
    )
    application.add_handler(order_conv)

    # --- ADMIN CONVERSATION HANDLER (ADD PORTFOLIO) ---
    add_portfolio_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(
            start_add_portfolio, pattern="^admin_add_port$")],
        states={
            CHOOSING_CATEGORY: [CallbackQueryHandler(category_chosen, pattern="^add_cat_")],
            UPLOADING_MEDIA: [MessageHandler(filters.PHOTO | filters.VIDEO, media_uploaded)],
            ENTERING_TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, topic_entered)],
            ENTERING_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, description_entered)],
            CONFIRMING_POST: [CallbackQueryHandler(
                confirm_post, pattern="^admin_confirm_post")]
        },
        fallbacks=[
            CallbackQueryHandler(cancel_action, pattern="^admin_cancel$"),
            CommandHandler("cancel", cancel_action)
        ]
    )
    application.add_handler(add_portfolio_conv)

    # --- NEW: BROADCAST CONVERSATION HANDLER ---
    broadcast_conv = ConversationHandler(
        entry_points=[
            CommandHandler("broadcast", broadcast_command),
            CallbackQueryHandler(broadcast_start_btn,
                                 pattern="^admin_send_broadcast$")
        ],
        states={
            BROADCAST_WAITING: [MessageHandler(
                filters.ALL & ~filters.COMMAND, receive_broadcast_message)]
        },
        fallbacks=[CommandHandler("cancel", cancel_admin)]
    )
    application.add_handler(broadcast_conv)

    # --- ADMIN COMMANDS ---
    # ቀድሞ admin_command የነበረው በ admin_menu ተተክቷል
    application.add_handler(CommandHandler("admin", admin_menu))
    application.add_handler(CommandHandler("verify", verify_command))

    # --- ADMIN MANAGEMENT HANDLERS (PORTFOLIO CONTROL) ---
    application.add_handler(CallbackQueryHandler(
        admin_toggle_main, pattern="^admin_toggle_active$"))
    application.add_handler(CallbackQueryHandler(
        admin_handle_toggle, pattern="^adm_tg_"))
    application.add_handler(CallbackQueryHandler(
        admin_delete_main, pattern="^admin_delete_logic$"))  # አስተካክዬዋለሁ
    application.add_handler(CallbackQueryHandler(
        admin_handle_delete, pattern="^adm_del_"))
    application.add_handler(CallbackQueryHandler(
        admin_back_button, pattern="^admin_back_to_menu$"))

    # --- NEW: ADMIN VERIFY & EXPORT CALLBACKS ---
    # ፓተርኑ ከሌሎቹ ጋር እንዳይጋጭ (Specific) ሆኗል
    application.add_handler(CallbackQueryHandler(
        handle_admin_callbacks,
        pattern="^(admin_verify_orders|v_nav_|v_close_|admin_export_csv|back_to_admin_main)"
    ))

    print("🚀 Barrok Creative Bot is running... Press Ctrl+C to stop.")
    application.run_polling()


if __name__ == "__main__":
    main()
