from telegram import InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, SuccessfulPayment
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, PreCheckoutQueryHandler, MessageHandler, Filters
import os

# Функция-обработчик команды /start
def start(update, context):

    # Создаем кнопку "Купить"
    keyboard = [[InlineKeyboardButton("Купить", callback_data='buy')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем приветственное сообщение

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('hello.jpg', 'rb'), caption="Добро пожаловать!\nПолучите гайд «Планировка без дизайнера интерьера»\nПервые 100 человек могут приобрести со скидкой!‌\nДалее скидка исчезнет. \nДля оплаты нажмите 'Купить'.", reply_markup=reply_markup)
    # Отправляем кнопку пользователю
    # context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите действие:", reply_markup=reply_markup)

# Функция-обработчик нажатия на кнопку "Купить"
def button_click(update, context):
    query = update.callback_query
    if query.data == 'buy':
        # Генерируем счет с деталями платежа
        invoice_text = "Это руководство позволит Вам самостоятельно создать грамотную и комфортную планировку и расстановку мебели."
        invoice_amount = 1800.0
        invoice_currency = "RUB"
        invoice_payload = "some_payload"

        # Отправляем счет пользователю
        # Отправляем счет пользователю
        context.bot.send_invoice(chat_id=query.message.chat_id,
                                title="Оплата за гайд Linii Interior",
                                description=invoice_text,
                                payload=invoice_payload,
                                provider_token='390540012:LIVE:37855',
                                currency=invoice_currency,
                                start_parameter='start_parameter',
                                prices=[LabeledPrice('Руб', 180000)])

# Функция-обработчик PreCheckoutQuery
def pre_checkout_query(update, context):
    query = update.pre_checkout_query

    # В данном примере всегда принимаем платеж
    context.bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)

# Функция-обработчик SuccessfulPayment
def successful_payment(update, context):
    message = update.message

    # Проверяем, что платеж успешен
    if message.successful_payment.total_amount == 180000 and message.successful_payment.currency == 'RUB':
        # Определяем путь к файлу course.pdf
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, 'guide.pdf')
        # Отправляем файл course.pdf пользователю
        context.bot.send_document(chat_id=message.chat_id, document=open(file_path, 'rb'))

def main():
    # Создаем экземпляр Updater и передаем токен вашего бота
    updater = Updater(token='6379158900:AAGDp0gr4He7u08qBnAIusUwMvILc3d-JbY', use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем обработчики
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button_click))
    dispatcher.add_handler(PreCheckoutQueryHandler(pre_checkout_query))
    dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
