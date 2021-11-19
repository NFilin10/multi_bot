import telebot
from covid import Covid
from telebot import types
from bs4 import BeautifulSoup
import requests
import config

#info about covid
covid = Covid()

#token
bot = telebot.TeleBot(config.token)

#start message
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'hello, user')

#covid message
@bot.message_handler(commands=['covid'])
def start1(message):
    bot.send_message(message.chat.id, 'choose a country', reply_markup=markup)


#link message
@bot.message_handler(commands=['link'])
def messages1(message):
        bot.send_message(message.chat.id, 'insert a link')
        bot.register_next_step_handler(message, reg_name)
        bot.register_next_step_handler(message, parse)



def reg_name(message):
    global name
    name = message.text


#index message
@bot.message_handler(commands=['index'])
def mass(message):
    bot.send_message(message.chat.id, 'Insert your data')
    bot.send_message(message.chat.id, 'Your weight (kg):')
    bot.register_next_step_handler(message, reg_weight)



def reg_weight(message):
    global weight1
    weight1 = message.text
    bot.send_message(message.chat.id, 'Your height (cm):')
    bot.register_next_step_handler(message, reg_height)

def reg_height(message):
    global height1
    height1 = message.text
    try:
        height2 = float(height1.replace(',', '.')) / 100
        index = float(weight1.replace(',', '.')) / (float(height2) ** 2)
        index = round(index, 2)
        if index < 16:
            a = 'Острый дефицит массы'
        elif 16 <= index <= 18.5  :
            a = 'Недостаточная масса тела'
        elif 18.6 <=index <=25:
            a = 'Норма'
        elif 25.1 <= index <= 30:
            a = 'Избыточная масса тела'
        elif 30.1 <= index <= 35:
            a = 'Ожирение первой степени'
        elif 35.1 <= index <= 40:
            a = 'Ожирение второй степени'
        elif index > 40.1:
            a = 'ООжирение третьей степени'
        bot.send_message(message.chat.id, 'Your weight (kg): ' + weight1.replace(',', '.') + '\n' + 'Your height (cm): ' + str(height1.replace(',', '.')) + '\n' + str(index) + ' ' + a +
                         '\n' + '' '\n' + 'Острый дефицит массы < 16' + '\n' + 'Недостаточная масса тела 16 - 18.5' + '\n' + 'Норма 18.6 - 25'  + '\n' + 'Избыточная масса тела 25.1 - 30' +
                         '\n' + 'Ожирение первой степени 30.1 - 35' + '\n' + 'Ожирение второй степени	35.1 - 40' + '\n' + 'Ожирение третьей степени > 40.1')
    except:
        bot.send_message(message.chat.id, 'Error: Please input correct data')
#parser
def parse(message):
    HEADERS1 = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.310'}
    response1 = requests.get(name, headers=HEADERS1)
    soup1 = BeautifulSoup(response1.content, 'html.parser')
    items1 = soup1.findAll('div', class_='col-1-1 bg-white extra-offers-offer')
    comps1 = []
    for item in items1:
        comps1.append({
            'shop': item.find('a', 'regular-link').get_text().upper(),
            'price': item.find('p',
                               'bold roboto red text-24 extra-offers-price nomargin curr_change').get_text().replace(
                u'\xa0', ''),
            'link': item.find('a', 'btn blue-bg white rounded roboto bold').get('href')
        })
    for title in comps1:
        bot.send_message(message.chat.id, title['shop'] + ' - ' + title['price'] + '  ' + title['link'], disable_web_page_preview=True)


#flags
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
world = types.KeyboardButton('🌎')
est = types.KeyboardButton('🇪🇪')
rus = types.KeyboardButton('🇷🇺')
fin = types.KeyboardButton('🇫🇮')
lv = types.KeyboardButton('🇱🇻')
usa = types.KeyboardButton('🇺🇸')
fr = types.KeyboardButton('🇫🇷')
es = types.KeyboardButton('🇪🇸')
it = types.KeyboardButton('🇮🇹')
uk = types.KeyboardButton('🇬🇧')
de = types.KeyboardButton('🇩🇪')
lt = types.KeyboardButton('🇱🇹')
markup.add(world, est, rus, fin, lv, usa, fr, es, it, uk, de, lt)

flags = {"🇪🇪": ["58", "estonia"], "🇷🇺": ["142", "russia"], "🇫🇮": ["62", "finland"], "🇱🇻": ["97", "latvia"], "🇺🇸": ["178", "usa"], "🇫🇷": ["63", "france"], "🇪🇸": ["162", "spain"], "🇮🇹": ["86", "italy"], "🇬🇧": ["181", "uk"], "🇩🇪": ["67", "germany"], "🇱🇹": ["103", "lithuania"]}

def cov(id, country, message):
    covid = Covid()
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.310'}
    response = requests.get("https://coronavirus-monitor.info/country/" + country, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='info_blk stat_block confirmed')
    comps = []
    print(id)
    location = covid.get_status_by_country_id(id)
    try:
        for item in items:
            comps.append({
                'cases': item.find('sup').get_text()
            })
        for title in comps:
            a = (title['cases'])

        bot.send_message(message.chat.id, str(location['country']) + '\n' + "Confirmed: " + str(
            location['confirmed']) + '\n' + 'Active: '
                         + str(location['active']) + '\n' + 'Recovered: ' + str(
            location['recovered']) + '\n' + 'Deaths: ' + str(
            location['deaths']) + '\n' + 'New cases: ' + a)
    except AttributeError:
        bot.send_message(message.chat.id, str(location['country']) + '\n' + "Confirmed: " + str(
            location['confirmed']) + '\n' + 'Active: '
                         + str(location['active']) + '\n' + 'Recovered: ' + str(
            location['recovered']) + '\n' + 'Deaths: ' + str(
            location['deaths']) + '\n' + 'New cases: ' + 'no data yet')


#flag function
@bot.message_handler(content_types=['text'])
def messages(message):
    if message.text in flags:
        users_input = message.text
        cov(flags[users_input][0], flags[users_input][1], message)
    elif message.text == '🌎':
        active = covid.get_total_active_cases()
        confirmed = covid.get_total_confirmed_cases()
        recovered = covid.get_total_recovered()
        deaths = covid.get_total_deaths()
        bot.send_message(message.chat.id, 'World:' + '\n' + "Confirmed: " + str(confirmed) + '\n' + 'Active: '
                         + str(active) + '\n' + 'Recovered: ' + str(recovered) + '\n' + 'Deaths: ' + str(
            deaths) + '\n')
    else:
        bot.send_message(message.chat.id, "Try again")


#start bot
if  __name__ == '__main__':
    bot.polling(none_stop=True)






