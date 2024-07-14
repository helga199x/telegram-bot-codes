import telebot;
import dbConnector;
import addressSearch;
from telegram import ReplyKeyboardMarkup, KeyboardButton;
from telebot import types;

token = 'BOT_TOKEN'
admin_log_in = 'Я админ'
admin_log_out = 'Я больше не хочу быть админом'
bot = telebot.TeleBot(token)
admin_chats = {}
processing_adresses = {}
processing_house_num = {}

init_state = 1
set_address = 2
set_house_num = 3
set_code = 4

dbConnector.init_db()

@bot.message_handler(commands=['start'])
def handle_start(message):
    send_welcome_message(message.chat.id)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if is_admin_login(message):
        return
    if is_admin(message):
        admin_flow(message)
    else:
        compile_adress_btns(message, "get_code")

# Handler to process callback data from inline buttons
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.message:
        # Split the callback_data to identify the command and the address
        data_parts = call.data.split('|')
        if len(data_parts) == 2:
            if data_parts[0] == 'get_code':
                address = data_parts[1]
                result = dbConnector.get_code(address)
                if result:
                    text = ""
                    for row in result:
                        text += f"Дом {row[0]}, код {row[1]}\n"

                    bot.send_message(call.message.chat.id, f"Коды домофона для {address}:\n{text}")
                else:
                    bot.send_message(call.message.chat.id, f"По адресу {address} нет записей о кодах домофона.")
            if is_admin(call.message):
                if admin_chats[call.message.chat.id] == set_address and data_parts[0] == 'set_address':
                    address = data_parts[1]
                    processing_adresses[call.message.chat.id] = address
                    admin_chats[call.message.chat.id] = set_house_num
                    bot.send_message(call.message.chat.id, f"Введите номер дома:")

def is_admin(message):
    return message.chat.id in admin_chats.keys()

def is_admin_login(message):
    input_string = message.text[:100]
    if input_string == admin_log_in:
        admin_chats[message.chat.id] = init_state
        bot.send_message(message.chat.id, "Ну шо, теперь ты админ! Вводи адрес для которого нужно добавить/отредоктировать код.")
        return True
    elif input_string == admin_log_out:
        admin_chats.pop(message.chat.id)
        bot.send_message(message.chat.id, "Ну шо, гуляй тогда.")
        send_welcome_message(message.chat.id)
        return True
    return False

def admin_flow(message):
    chat_state = admin_chats[message.chat.id]
    if chat_state == init_state:
        admin_chats[message.chat.id] = set_address
        compile_adress_btns(message, "set_address")
    if chat_state == set_house_num:
        input_string = message.text[:10]
        processing_house_num[message.chat.id] = input_string
        bot.send_message(message.chat.id, f"Введите код домофона:")
        admin_chats[message.chat.id] = set_code
    if chat_state == set_code:
        input_string = message.text[:20]
        address = processing_adresses[message.chat.id]
        house_num = processing_house_num[message.chat.id]
        code = input_string
        dbConnector.add_address(address, house_num, code)
        bot.send_message(message.chat.id, f"Код '{code}' добавлен для: {address}. Введите ещё адрес для добавления нового кода или '{admin_log_out}' для выхода из режима админа.")
        admin_chats[message.chat.id] = init_state

def compile_adress_btns(message, action):
    input_string = message.text[:100]
    wrapper = addressSearch.OpenCageAPIWrapper()
    possible_addresses = wrapper.get_possible_addresses(input_string)
    if isinstance(possible_addresses, str):
        bot.send_message(message.chat.id, possible_addresses)
    else:
        keyboard_buttons = []
        for address in possible_addresses:
            if len(address) >= 57:
                address = address[:57] + "..."
            button = types.InlineKeyboardButton(text=f"{address}", callback_data=f"{action}|{address}")
            keyboard_buttons.append(button)

        markup = types.InlineKeyboardMarkup(row_width=1)
        for button in keyboard_buttons:
            markup.add(button)
        bot.send_message(message.chat.id, text="Вот найденные адреса по данному запросу:", reply_markup=markup)

def obtain_house_number(message):
    input_string = message.text[:5]

def send_welcome_message(chat_id):
    bot.send_message(chat_id, "Это бот для просмотра кодов домофона. Пожалуйста, введите адрес в формате 'Улица, Город', для которого вы хотите посмотреть код.")

bot.polling(none_stop=True, interval=0)