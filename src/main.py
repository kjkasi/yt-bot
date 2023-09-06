import logging
from os import path, environ, remove, listdir, stat

from yt_dlp import YoutubeDL
from telegram import ForceReply, Update, constants
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ydl_opts = {
        #'format': 'worstvideo[ext=mp4][height<=?1080]+worstaudio[ext=m4a]/worst',
        "format": "worstaudio[ext=m4a]/worst",
        "outtmpl": "/app/src/%(id)s.%(ext)s"
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(update.message.text, download=False)
        ydl.download(update.message.text)
        file = path.join(f"/app/src/{info['id']}.{info['ext']}")
        #logger.info(listdir("/app/src/"))

        file_size = stat(file).st_size
        try:
           if file_size >= constants.FileSizeLimit.FILESIZE_UPLOAD:
               await update.message.reply_text(f"File {file} too large, size {file_size / (1024 * 1024)}")
           else:                            
               await update.message.reply_audio(open(file, "rb"), title=info['title'])
        except Exception as e:
            await update.message.reply_text(e.strerror)
        finally:
            remove(file)




def main() -> None:
    token: str = environ.get("TELEGRAM_TOKEN")

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
