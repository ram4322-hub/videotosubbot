import os
import whisper
from moviepy.editor import VideoFileClip
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters

# Load the Whisper model
model = whisper.load_model("base")

# Get the bot token from environment variables
TOKEN = os.getenv('7370676670:AAEraeZ4BZw4G2TJAT-TMRFn9SwRCISmdPg')

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Send me a video and I'll provide English subtitles.")

async def handle_video(update: Update, context: CallbackContext):
    file = await update.message.video.get_file()
    file.download('video.mp4')

    # Extract audio from video
    clip = VideoFileClip('video.mp4')
    audio = clip.audio
    audio.write_audiofile('audio.wav')

    # Perform speech-to-text using Whisper
    result = model.transcribe('audio.wav')
    subtitles = result['text']

    # Send subtitles to user
    await update.message.reply_text(subtitles)

async def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Add command handler and message handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Video, handle_video))

    # Run the bot until Ctrl-C is pressed
    await application.start_polling()
    await application.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
