"""Telegram bot to create a playlist"""
import logging
import os
from telegram import Update
from telegram.ext import  MessageHandler, ApplicationBuilder,filters
from spotify import search_song, add_song_to_playlist

# Replace 'YOUR_TOKEN' with the token you got from BotFather
TOKEN = os.environ.get('BOT_TOKEN')

# This list will act as a simple playlist
playlist = []

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update, context):
    """Function to handle the /start command"""
    await update.message.reply_text('Hi! Send me a song name and I will add it to your playlist.')

async def add_song(update, context):
    """Function to handle regular messages"""
    if update and update.message:
        msg : str = update.message.text
        if msg and msg.startswith(('Поставь', 'Включи', 'Хочу песню', "Хочу")):
            song_name = msg.replace('Поставь', '').replace('Включи', '').replace('Хочу песню', '').replace('Хочу', '').strip()
            song_id = search_song(song_name)
            if song_id:
                add_song_to_playlist(song_id)
                await update.message.reply_text(f'"{song_name}" added to your playlist!')
            else:
                await update.message.reply_text(f'"{song_name}" not found on Spotify.')

async def show_playlist(update, context):
    """Function to show the playlist"""
    if playlist:
        message = "Your playlist:\n" + "\n".join(playlist)
    else:
        message = "Your playlist is empty."
    await update.message.reply_text(message)

def main():
    """Start the bot."""
    app = ApplicationBuilder().token(TOKEN).build()
    # Register handlers
    app.add_handler(MessageHandler(filters.ALL, add_song))

    # Start the Bot
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()