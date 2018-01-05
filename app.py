from telebot import TeleBot as tb # Telegram API
import bot_config
from googletrans import Translator #GooGle Translate lib


bot = tb(bot_config.token) #  API token
translator = Translator()

class Bthelper:
    def __init__(self):
        self.handler = 'en'

    def set_handler(self,handler):
        self.handler = handler

    def get_handler(self):
        return self.handler
bt_help = Bthelper()

# handler for cases with '/start" command wahere user gets to know about bot.
@bot.message_handler(commands=['start']) 
def message_start(message):
    if message.from_user.username in bot_config.known_users:
        bot.send_message(message.from_user.id,'Salamlar. Hal - hazirda movcud olan komandalar \n /entoaz - Ingilis -> Azerbaycan tercumecisi. \n /aztoen - Azerbaycan -> Ingilis tercumecisi. \n /translate - Istenilen dil -> Ingilis tercumecisi')
    else:
        bot.send_message(message.from_user.id,'Bot-dan istifade etmek huququnuz yoxdur.') #bot_config faylinda known_users listine elave edilmelidir

# /aztoen 
@bot.message_handler(commands=['aztoen'])
def message_aztoen(message):
    if message.from_user.username in bot_config.known_users:
        msg = bot.reply_to(message, "Sizden tercume edilecek sozu gozleyirem...") #Istifadeciye gonderilecek cavab
        bt_help.set_handler('en')
        bot.register_next_step_handler(msg,do_trans) #Tercumeci funksiyamiza kecid
    else:
        bot.send_message(message.from_user.id,'Bot-dan istifade etmek huququnuz yoxdur.') #bot_config faylinda known_users listine elave edilmelidir


# /entoaz
@bot.message_handler(commands=['entoaz'])
def message_entoaz(message):
    if message.from_user.username in bot_config.known_users:
        msg = bot.reply_to(message, "Send me something for translating...") #Istifadeciye gonderilecek cavab
        bt_help.set_handler('az')
        bot.register_next_step_handler(msg,do_trans) #Tercumeci funksiyamiza kecid
    else:
        bot.send_message(message.from_user.id,'Bot-dan istifade etmek huququnuz yoxdur.') #bot_config faylinda known_users listine elave edilmelidir

# /translate
@bot.message_handler(commands=['translate'])
def message_translate(message):
    if message.from_user.username in bot_config.known_users:
        msg = bot.reply_to(message, "Sizden tercume edilecek sozu gozleyirem...") #Istifadeciye gonderilecek cavab
        bot.register_next_step_handler(msg,do_trans) #Tercumeci funksiyamiza kecid
    else:
        bot.send_message(message.from_user.id,'Bot-dan istifade etmek huququnuz yoxdur.') #bot_config faylinda known_users listine elave edilmelidir

def do_trans(message):
    try:
        handler = bt_help.get_handler()
        translated = translator.translate(message.text,handler)
        bot.send_message(message.from_user.id,translated.text)
    except Exception  as e:
        bot.send_message(message.from_user.id,e)

bot.polling(none_stop=True)
