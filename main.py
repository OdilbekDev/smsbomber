import telebot
import requests
from telebot import types

bot = telebot.TeleBot('5961553974:AAFuAUUMsavrtf1mT2bGGLS1V2XaHMJYYag')


url = 'https://api.express24.uz/client/v4/authentication/code'

user_dict = {}
class User:
    def __init__(self, phone) -> None:
        self.phone = phone
        self.msgnum = None

def start_markup():
    markup = types.InlineKeyboardMarkup(row_width=True)
    line_keyboard = types.InlineKeyboardButton(text='1-Kanal', url='https://t.me/shavkatov_bio')
    check_keyboard = types.InlineKeyboardButton(text='Tekshirish', callback_data='check')
    markup.add(line_keyboard, check_keyboard)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    bot.send_message(chat_id, f'Assalomu Aleykum {first_name} ! \n'
                     f"Botdan to'liq foydalanish uchun kanalimizga azo bo'ling", reply_markup=start_markup())

def check(call):
    status = ['member']
    for i in status:
        if i == bot.get_chat_member(chat_id='-1001526960093', user_id=call.message.chat.id).status:
            sent = bot.send_message(call.message.chat.id, 'Telefon raqam kiriting' + '\n Namuna 998901234567')
            bot.register_next_step_handler(sent, getphone)
        else:
            bot.send_message(call.message.chat.id, "Kanalimizga azo bo'ling")


@bot.callback_query_handler(func= lambda call: True)
def callback(call):
    if call.data == 'check':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        check(call)





def getphone(message):
    chat_id = message.chat.id
    phone = message.text
    user = User(phone)
    user_dict[chat_id] = user
    msg = bot.reply_to(message, 'Xabarlar sonini kiriting')
    bot.register_next_step_handler(message, getmsgnum)

def getmsgnum(message):
    chat_id = message.chat.id
    num = message.text
    user = user_dict[chat_id]
    user.msgnum = num
    print(user.msgnum)
    bot.send_message(chat_id, 'Xabarlar yuborilmoqda...')
    for i in range(int(user.msgnum)):
        print(user.phone)
        response = requests.post(url, json = {"phone": user.phone})
        print(response.status_code)

    bot.send_message(chat_id, "Xabarlar yuborildi! Qayta xabar yuborish uchun /start buyrug'ini yuboring")


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)