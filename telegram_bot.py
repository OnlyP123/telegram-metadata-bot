import os
import ffmpeg
import telebot
from telebot.types import Message

# Telegram Bot Token (replace with your actual bot token)
TOKEN = "7859533119:AAE7kChxwWhdZHQu7IMw2G0P_5Q2X4yS_0s"
bot = telebot.TeleBot(TOKEN)

# Folder to store videos
if not os.path.exists("videos"):
    os.makedirs("videos")

@bot.message_handler(content_types=['video'])
def handle_video(message: Message):
    try:
        # Download video
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        input_path = f"videos/input_{message.chat.id}.mp4"
        output_path = f"videos/output_{message.chat.id}.mp4"
        
        with open(input_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Remove metadata and add custom metadata
        ffmpeg.input(input_path).output(output_path,
            map_metadata='-1',
            c="copy",
            **{
                "metadata": "title=Optimized Video",
                "metadata": "artist=Telegram Bot",
                "metadata": "description=Instagram-ready",
                "metadata": "comment=No social media stamps"
            }).run()

        # Send back optimized video
        with open(output_path, "rb") as output_file:
            bot.send_video(message.chat.id, output_file, caption="Here is your optimized video! 🚀")

        # Cleanup
        os.remove(input_path)
        os.remove(output_path)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error processing video: {str(e)}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Send me a video, and I'll optimize it for Instagram! 🚀")

bot.polling()

