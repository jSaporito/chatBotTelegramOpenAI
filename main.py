from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
from openai import OpenAI
from json import dumps



load_dotenv()

TOKEN_TELEGRAM: Final = os.getenv("TOKEN_TELEGRAM")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")


client = OpenAI()

async def start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello world")
    print(update.message.text)    
    
async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am cambrian creature")


async def custom_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("custom command")

async def quit_command(update:Update,context: ContextTypes.DEFAULT_TYPE):
    quit_text =  update.message.text.replace('/', '').strip()
    if 'quit' in quit_text:
        return  False
    else:
        return True


    
def handle_response (prompt:str) -> str:
   text : str | None = None
   
   try:
        response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                        "role": "user",
                        "content": prompt
                        }
                    ],
                    temperature=1,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    )
        text = response.choices[0].message.content
        return text
   except Exception as e:
            print("ERROR:", e)
            return None



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text:str  = update.message.text   
    
    print(f'User:({update.message.chat.id}) in {message_type}:"{text}"') 

    if message_type == 'private':
            new_text: str = text.strip()
            response: str = handle_response(new_text)
    else:
            response:str = handle_response(text)    
            
    await update.message.reply_text(response)
    


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")



if __name__ == '__main__':
    app = Application.builder().token(TOKEN_TELEGRAM).build()    
    
    #Commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))
    app.add_handler(CommandHandler('quit',quit_command))
    
    
    
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.TEXT, quit_command))
    
    
    
    # Erros
    app.add_error_handler(error)
    
    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
    