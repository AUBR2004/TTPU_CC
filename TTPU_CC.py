import telebot
from telebot import types

bot = telebot.TeleBot("YOUR TOKEN")

user_data = {}

car_options = ["NEXIA", "COBALT", "GENTRA"] 
part_options = ["Свечи 🕯️", "Колодки ⚙", "Масло 🛢️", "Антифриз(Охл. сис.) ❄️"]


main_menu_button = types.InlineKeyboardButton("📤Назад", callback_data="main_menu")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Выберите марку вашей машины 🚘:", reply_markup=car_keyboard())

def car_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=3)
    for car in car_options:
        markup.add(types.InlineKeyboardButton(car, callback_data=car))
    return markup

@bot.callback_query_handler(func=lambda call: call.data in car_options)
def car_selected(call):
    user_data['car'] = call.data
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    for part in part_options:
        markup.add(types.InlineKeyboardButton(part, callback_data=part))
    
    markup.add(main_menu_button)
    bot.send_message(call.message.chat.id, f'Ваша машина: {user_data["car"]}🌟\n'
                                           'Что вы хотите заменить/починить?🔧', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in part_options)
def part_selected(call):
    user_data['part'] = call.data
    bot.send_message(call.message.chat.id, "Введите пробег при последней замене")
    bot.register_next_step_handler(call.message, get_last_replaced_mileage)

def get_last_replaced_mileage(message):
    try:
        user_data['last_replaced_mileage'] = int(message.text)
        if user_data['last_replaced_mileage'] < 2000:
            bot.send_message(message.chat.id, "Ошибка,пробег при последней замене должен быть минимум 2000КМ")
            return
        bot.send_message(message.chat.id, "Введите нынешний пробег")
        bot.register_next_step_handler(message, get_current_mileage)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка,введите пробег цифрами!")
        
def get_current_mileage(message):
    try:
        user_data['current_mileage'] = int(message.text)
        
        min_value = 0

        if user_data['car'] == 'GENTRA':
            if user_data['part'] == 'Свечи 🕯️':
                min_value = 30000
            elif user_data['part'] == 'Колодки ⚙':
                min_value = 40000
            elif user_data['part'] == 'Масло 🛢️':
                min_value = 7000
            elif user_data['part'] == 'Антифриз(Охл. сис.) ❄️':
                min_value = 150000
        elif user_data['car'] == 'COBALT':
            if user_data['part'] == 'Свечи 🕯️':
                min_value = 30000
            elif user_data['part'] == 'Колодки ⚙':
                min_value = 40000
            elif user_data['part'] == 'Масло 🛢️':
                min_value = 7000
            elif user_data['part'] == 'Антифриз(Охл. сис.) ❄️':
                min_value = 150000
        elif user_data['car'] == 'NEXIA':
            if user_data['part'] == 'Свечи 🕯️':
                min_value = 20000
            elif user_data['part'] == 'Колодки ⚙':
                min_value = 40000
            elif user_data['part'] == 'Масло 🛢️':
                min_value = 7000
            elif user_data['part'] == 'Антифриз(Охл. сис.) ❄️':
                min_value = 40000

        result = f'Настало время замены {user_data["part"]} ❌' if user_data['current_mileage'] - user_data['last_replaced_mileage'] >= min_value else f'Ваша машина ещё в исправности {user_data["part"]} ✅'

        bot.send_message(message.chat.id, result)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка,введите пробег цифрами!")

@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def return_to_main_menu(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Выберите марку вашей машины:", reply_markup=car_keyboard())

if __name__ == "__main__":
    bot.polling(none_stop=True)

