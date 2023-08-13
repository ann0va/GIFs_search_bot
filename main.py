import requests
import telegram


from constant import TOKEN,giphy_api_key
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters,Application,ContextTypes

print('Starting up bot...')

BOT_USERNAME = '@thebestgifs_bot'

bot = telegram.Bot(token=TOKEN)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome to the GIF search bot! Send me a keyword to get GIFs.')

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Send a keyword to search for GIFs.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global response
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group' and BOT_USERNAME in text:
        new_text = text.replace(BOT_USERNAME, '').strip()
        response = handle_response(new_text)
    
    print('Bot:', response)
    await update.message.reply_text(response)

def handle_response(query):
    gifs = search_gifs(query)

    if gifs:
        return "Here are some GIFs for your search:\n" + "\n".join(gifs)
    else:
        return "No GIFs found for this search."

def search_gifs(query):
    base_url = "https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": giphy_api_key,  
        "q": query,
        "limit": 5
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        gif_urls = [gif["images"]["downsized"]["url"] for gif in data["data"]]
        return gif_urls
    else:
        return []

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
  
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)