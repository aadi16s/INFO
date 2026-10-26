import os
import threading
from flask import Flask
import requests
import telebot

TOKEN = "8843876003:AAFe8Wm0SJfqqw61uhmzPMin_Gi4gl_q-Xg"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is running 24/7 successfully!"


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "Namaste! Give me any phone number"
      " i will fetch it for you.",
  )


@bot.message_handler(func=lambda message: True)
def get_number_info(message):
  query_number = message.text.strip()

  if not query_number.isdigit():
    bot.reply_to(
        message, "give an valid number(add a valid number)."
    )
    return

  bot.reply_to(
      message, "🔍 Fetching number for you...."
  )

  api_url = f"https://codex-num2info-v69.kesug.com/api.php?key=HarshitK-&num="

  try:
    response = requests.get(api_url, timeout=15)
    res_data = response.json()

    if res_data.get("status") == True:
      data_obj = res_data.get("data", {})
      alt_records = data_obj.get("alternative_records", [])

      if alt_records:
        text = f"📊 *Number Details Found:*\n\n"
        for i, rec in enumerate(alt_records, 1):
          text += f"📌 *Record {i}*\n"
          text += f"👤 *Name:* `{rec.get('full_name', 'N/A')}`\n"
          text += f"👨‍👦 *Father's Name:* `{rec.get('the_name_of_the_father', 'N/A')}`\n"
          text += f"📞 *Phone:* `{rec.get('phone', 'N/A')}`\n"
          text += f"🏠 *Address:* `{rec.get('address', 'N/A')}`\n"
          text += f"📄 *Doc Number:* `{rec.get('document_number', 'N/A')}`\n"
          text += f"🌐 *Region:* `{rec.get('region', 'N/A')}`\n\n"
        bot.reply_to(message, text, parse_mode="Markdown")
      else:
        bot.reply_to(
            message, "Is number ka koi record nahi mila (Records empty hain)."
        )
    else:
      bot.reply_to(message, "API se data fetch karne mein koi samasya aayi hai.")
  except Exception as e:
    bot.reply_to(message, f"Error aa gaya: {str(e)}")


def run_flask():
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
  # Flask server ko alag thread mein chalate hain taaki bot polling interrupt na ho
  t = threading.Thread(target=run_flask)
  t.start()
  bot.infinity_polling()
