# from model import StyleTransferModel
# from telegram_token import token
from io import BytesIO
from PIL import Image
import telegram
import os
from skeleton import Skeletonizer

token = os.getenv("TOKEN", '1449221385:AAFaE6J7hYNINWvVyGhKY6SekV_tqQHuJrQ')  # Получаем из переменных Heroku
FIRST = range(1)
skeletonizer = Skeletonizer()

def send_gif_on_photo(update, context):
    chat_id = update.message.chat_id
    print("Got image from {}".format(chat_id))

    # получаем информацию о картинке
    image_info = update.message.photo[-1]
    image_file = context.bot.get_file(image_info)

    content_image_stream = BytesIO()
    image_file.download(out=content_image_stream)
    skeletonizer.skeletonize(content_image_stream)
    # output = fast_model.stylize(model_list[chat_id], content_image_stream)

    # теперь отправим назад фото
    output = skeletonizer.skeletonize(content_image_stream)
    output_stream = BytesIO()
    output.save(output_stream, format='PNG')
    output_stream.seek(0)
    context.bot.send_photo(chat_id, photo=output_stream)

def start(update, context):
    update.message.reply_text(main_menu_message())
    return FIRST

def main_menu_message():
    return 'Upload image for skeleton creation'


def help_callback(update, context):
    '''Обработчик команды /help'''
    update.message.reply_text(
        "This bot creates GIF, illustrating the proccess of image skeleton making. Use /start")

if __name__ == '__main__':
    from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, MessageHandler, Filters, ConversationHandler
    import logging

    # Включим самый базовый логгинг, чтобы видеть сообщения об ошибках
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [MessageHandler(Filters.photo, send_gif_on_photo)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("help", help_callback))
    PORT = int(os.environ.get("PORT", "8443"))  ###Избегаем ошибки Heroku R10
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=token)
    if HEROKU_APP_NAME is None:
        updater.bot.set_webhook("https://16e6404716b7.ngrok.io/{}".format(token)) #вставить сюда для локального запуска ngrok http -p 8443
    else:
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, token))

    
