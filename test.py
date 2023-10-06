import requests, json, telebot, random, time



# Открываем файл config.json для чтения
with open('config_monitoring_bot.json', 'r') as file:
    # Загружаем данные из файла в формате JSON
    config_data = json.load(file)



api_key = config_data["api_key"]
bot_token = config_data["bot_token"]
url_server = config_data["url_server"]
headers = config_data["headers"]
timeout = config_data["timeout"]
long_polling_timeout = config_data["long_polling_timeout"]
good_code = config_data["good_code"]

bot = telebot.TeleBot(bot_token)

def send_to_server(data, headers, url):
    response = requests.post(url, data=json.dumps(data), headers=headers)

    # Проверяем успешность запроса
    if response.status_code == good_code:
        # Разбираем JSON-ответ
        data = response.json()
        return data
    else: return False

def get_message_text():
    url = url_server
    data = {"api_key": api_key}

    data = send_to_server(url=url, data=data, headers=headers)
    if data != False:
        text = ""

        status = data['status']
        if status == "succes":
            status = "Статус: ✅\n\n"
        else:
            status = "Статус: ❌\n\n"
        text += status


        if status == "Статус: ✅\n\n":
            cpu_total = "cpu total: " + str(data['data']['cpu']['total %']) + "%\n"
            cores_percent = data['data']['cpu']['cores %']
            number = 0
            cores = "   "
            for i in cores_percent:
                o = ""
                if number < 10: o = " "
                cores += f"{o}{number}: {i}%\n   "
                number += 1
            text += cpu_total
            text += cores
            text += "\nDisks:\n   "
            number = 0
            disks_percent = data['data']['disks']
            disk_logos = ["💿", "📀", "💽"]
            for data_ in disks_percent:
                text += f"{random.choice(disk_logos)} {number}: {data_['device']}: {data_['total Gb']} / {data_['used Gb']} Gb  ({data_['percent %']}%)\n   "
                number += 1
            memory_percent = data['data']['memory']['percent %']
            memory_total = data['data']['memory']['total Gb']
            memory_used = data['data']['memory']['used Gb']
            text += f"\n💾 memory 💾:\n   {memory_total} / {memory_used}Gb  ({memory_percent}%)"
        else:   
            text += f'data: {data}'
    return text

@bot.message_handler(commands=['start'])
def command_start(message):
    try:
        start_time = time.time()
        text = get_message_text()
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time_str = "{:.3f}".format(elapsed_time)
        text=f"⏱ {elapsed_time_str}.sec\n\n{text}"

        markup = telebot.types.InlineKeyboardMarkup()
        update = telebot.types.InlineKeyboardButton(text="update data 🔄", callback_data="update data 🔄")
        markup.add(update)

        bot.send_message(message.chat.id, text=text, reply_markup=markup)
    except:
        bot.reply_to(message, "Помилонька(")


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        start_time = time.time()
        text = get_message_text()
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time_str = "{:.3f}".format(elapsed_time)
        text=f"⏱ {elapsed_time_str}.sec\n\n{text}"

        markup = telebot.types.InlineKeyboardMarkup()
        update = telebot.types.InlineKeyboardButton(text="update data 🔄", callback_data="update data 🔄")
        markup.add(update)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text, reply_markup=markup)
    except:
         bot.send_message(call.message.chat.id, "Помилонька(")

    
bot.infinity_polling(timeout=timeout, long_polling_timeout = 5)