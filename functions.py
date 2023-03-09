from asyncpg import UniqueViolationError
from datetime import time
from aiogram.utils import exceptions
from gtts import gTTS
from all_texts import *
from PIL import Image, ImageDraw, ImageFont
from classes import *
import asyncio
import logging
import game__life
import httplib2
import textwrap


# Завантажити картинку за юрл
def save_picture(url):
    h = httplib2.Http('.cache')
    response, content = h.request(url)
    with open('img.jpg', 'wb') as f:
        f.write(content)


# Видалити файл за назвою
def delete_file(file):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file)
    os.remove(path)


# Створити голосове повідомлення
def create_audio(text, language):
    audio = gTTS(text=text, lang=language, slow=False)
    audio.save('audio.ogg')


# Створити картинку за цитатою
def create_quote_image(text, name):
    offset = 150
    text = '    ' + text
    if len(text) <= 28:
        offset = 85
        margin = 200
        font1 = ImageFont.truetype("arial.ttf", 95, encoding="unic")
        width1 = 11
    elif len(text) in range(29, 54):
        margin = 130
        font1 = ImageFont.truetype("arial.ttf", 70, encoding="unic")
        width1 = 17
    elif len(text) in range(55, 105):
        margin = 120
        font1 = ImageFont.truetype("arial.ttf", 45, encoding="unic")
        width1 = 28
    elif len(text) in range(105, 154):
        font1 = ImageFont.truetype("arial.ttf", 35, encoding="unic")
        margin = 100
        width1 = 39
    elif len(text) in range(154, 200):
        font1 = ImageFont.truetype("arial.ttf", 25, encoding="unic")
        offset = 120
        margin = 100
        width1 = 51
    else:
        font1 = ImageFont.truetype("arial.ttf", 18, encoding="unic")
        offset = 120
        margin = 100
        width1 = 70
    img = Image.open('quote_image_.png')
    font2 = ImageFont.truetype("arial.ttf", 10, encoding="unic")
    draw_text = ImageDraw.Draw(img)
    for line in textwrap.wrap(text, width=width1):
        draw_text.text((margin, offset), line, font=font1, fill="#000000")
        offset += font1.getsize(line)[1]
    draw_text.text((150, 420), name, font=font2, fill="#000000")
    img.save('quote.jpg')


def photo_in_symbols(file):
    tile = int(input('Введите разрешение фотографии от (1 до 100, где меньше - лучше): '))
    photo = input('Введите путь к фотографии: ').replace('\'', '').replace('\"', '')
    symbols = [i for i in '@$0B#NGWM8RDHPOKZ96khEPXS2wmeyjufF]}{tx1zv7lciL/\\|?*>r^;:_\"~,\'-.`']
    font2 = ImageFont.truetype("arial.ttf", tile, encoding="unic")
    img = Image.open(photo)
    width = img.size[0] // tile
    height = img.size[1] // tile
    goal = width * height
    symb_image = Image.new('RGB', (width * tile, height * tile), 'white')
    img = img.resize((width, height))
    draw = ImageDraw.Draw(symb_image)
    pix = img.load()
    process = 0
    for x in range(width):
        for y in range(height):
            draw.text((x * tile, y * tile),
                      symbols[(pix[x, y][0] + pix[x, y][1] + pix[x, y][2]) // 12],
                      font=font2, fill="#000000")
            process += 1
            print(f'{process}/{goal}')
    symb_image.save('qqqq.png')

# Час для функцій з парсингом таблиці
def time_in(time_s):
    if time_s is None:
        time_1 = datetime.datetime.now().time()
    else:
        time_1 = time_s.split('.')
        for i, i1 in enumerate(time_1):
            time_1[i] = int(i1)
        time_1 = datetime.time(time_1[0], time_1[1])
    return time_1


# Дата для функції з парсингом таблиці
def date_in(date_s):
    if date_s is None:
        date_1 = datetime.datetime.now().date()
    else:
        date_1 = date_s.split('.')
        for i, i1 in enumerate(date_1):
            date_1[i] = int(i1)
        date_1 = datetime.datetime(date_1[0], date_1[1], date_1[2])
    return date_1


# Переглянути пару за датою та чосом
def now_para(group, subgroup, date_s, time_s):
    group -= 1
    first_day = datetime.datetime(2022, 9, 12)
    date_1 = date_in(date_s)
    time_1 = time_in(time_s)
    dt = datetime.datetime.combine(date_1, time_1)
    start = datetime.datetime.combine(date_1, time(8))
    d_dif = (dt - first_day).days // 7
    week_day = date_1.weekday()
    h_dif = dt - start
    seconds = h_dif.seconds
    minutes = seconds // 60
    les_n = minutes // 95 + 1
    if d_dif % 2 == 0:
        chisel_znam = 1
    else:
        chisel_znam = 0
    if les_n in range(1, 6):
        collumn = let[3 + group * 2 + subgroup // 2]
        row = 2 + week_day * 10 + les_n * 2 - chisel_znam
        less = ws[collumn + str(row)].value
        if less is not None:
            return less
        else:
            return 'Нема пар, кукарача'
    else:
        return 'Не час для пар'


# Підготувати повідомлення для функції з парою
def para(message: types.Message):
    text = message.text
    text = text.replace('/para', '').replace('@ultradebik_bot', '').lower()
    text = text.split(' ')
    if '' in text:
        del text[0]
    if 'пт' in text and len(text) == 1:
        subgroup = 1
        group = 6
        date_s = None
        time_s = None
    else:
        if 'пт' in text:
            subgroup = 1
            group = 6
            if text[1] == '-':
                date_s = None
            else:
                date_s = text[1]

            if text[2] == '-':
                time_s = None
            else:
                time_s = text[2]
        else:
            group = groups.index(text[0]) + int(text[1])
            subgroup = int(text[2])
            if len(text) == 3:
                date_s = None
                time_s = None
            else:
                if text[3] == '-':
                    date_s = None
                else:
                    date_s = text[3]

                if text[4] == '-':
                    time_s = None
                else:
                    time_s = text[4]
    para_d = now_para(group, subgroup, date_s, time_s)
    return para_d


# Переглянути розклад за датою
def timetable(group, subgroup, date_s):
    group -= 1
    first_day = datetime.datetime(2022, 9, 12)
    date_1 = date_in(date_s)
    time_1 = time(4, 20)
    dt = datetime.datetime.combine(date_1, time_1)
    d_dif = (dt - first_day).days // 7
    week_day = date_1.weekday()
    if d_dif % 2 == 0:
        chisel_znam = 1
    else:
        chisel_znam = 0
    time_table = ''
    if week_day not in [5, 6]:
        for i in range(1, 6):
            column = let[3 + group * 2 + subgroup // 2]
            row = 2 + week_day * 10 + i*2 - chisel_znam
            less = ws[column + str(row)].value
            if less is not None:
                time_table += times[i - 1] + '| ' + less + '\n'
            else:
                time_table += times[i - 1] + '| Нема пари' + '\n'
        return time_table
    else:
        return 'Це вихідний, бовдуре'


# Підготувати повідомлення для функції з розкладом
def time_t(message: types.Message):
    text = message.text
    text = text.replace('/time_t', '').replace('@ultradebik_bot', '').lower()
    text = text.split(' ')
    if '' in text:
        del text[0]

    if text[0] == 'пт':
        group = 6
        subgroup = 1
        if len(text) == 2:
            date_s = text[1]
        else:
            date_s = None
    else:
        group = groups.index(text[0]) + int(text[1])
        subgroup = int(text[2])
        if len(text) == 3:
            date_s = None

        else:
            date_s = text[3]
    timetable_1 = timetable(group, subgroup, date_s)
    return timetable_1


# Розсилка усім адмінам повідомлення про запуск бота
async def on_startup_notify(dp: dp):
    for admin in admins_id:
        try:
            await dp.bot.send_message(chat_id=admin, text='Бот запущен')
        except Exception as ex:
            logging.exception(ex)


# Команди бота
async def set_default_commands(dp: dp):
    await dp.bot.set_my_commands([
        types.BotCommand('/start', 'Привітання'),
        types.BotCommand('/profile', 'Профіль'),
        types.BotCommand('/change_name', 'Змінити ім\'я'),
        types.BotCommand('/menu', 'переглянути деякі доступні команди'),
        types.BotCommand('/game_life', 'Гра життя'),
        types.BotCommand('/poll', 'Створити опитування /poll Питання -> Відп./Відп.'),
        types.BotCommand('/pasta', 'Велике, випадкове повідомлення'),
        types.BotCommand('/random', 'Випадкове число'),
        types.BotCommand('/kitty', 'Котик'),
        types.BotCommand('/para', 'Яка пара /para "Назва спец. (пз/пт та ін.)" "Номер групи" "Підгрупа" "Дата" "Час" (для ПТ лише /para "ПТ" "Дата" "Час")'),
        types.BotCommand('/time_t', 'Розклад за датою /time_t "Назва спец. (пз/пт та ін.)" "Номер групи" "Підгрупа" "Дата" (для ПТ лише /para "ПТ" "Дата")'),
        types.BotCommand('/voicen', 'Озвуче текст після /voicen жіночим голосом'),
        types.BotCommand('/games', 'Надішле перелік доступних ігор'),
        types.BotCommand('/quote', ' Створити фото - цитату (відповісти на повідомлення і увести комнду)'),
        types.BotCommand('/heart ', '<3'),
        types.BotCommand('/heartbroken', '</3'),
        types.BotCommand('/wise', 'Мудре дерево..')
    ])


# Під'єднання до бази даних
async def startup_database(disotcher: dp):
    print('устанавливается связь с базой данных')
    await db.set_bind(config.POSTGRES_URI)


async def db2_test():
    await db.set_bind(config.POSTGRES_URI)


# Додавання юзера у бд
async def add_user(user_id: int, name: str, update_name: str, n_messages: int, reputation: int):
    try:
        user = User(user_id=user_id, name=name, update_name=update_name, n_messages=n_messages, reputation=reputation)
        await user.create()
    except UniqueViolationError:
        print('пользователь не добавлен')


# Завантажити список усіх існуючих у бд юзерів
async def select_all_users():
    users = await User.query.gino.all()
    return users


# Підрахувати кількість юзерів у бд
async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count


# Завантажити дані про юзера, обраного за айді
async def select_user(user_id):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


# Завантажити дані про юзера, обраного за нікнеймом
async def select_user_by_name(name):
    name = name.replace(' ', '')
    user = await User.query.where(User.name == name).gino.first()
    return user


# Змінити ім'я обраного користувача
async def update_user_name_admin(old_name, new_name):
    user = await select_user_by_name(old_name)
    await user.update(update_name=new_name).apply()


# Змінити ім'я юзера
async def update_user_name(user_id, new_name):
    user = await select_user(user_id)
    await user.update(update_name=new_name).apply()


# Збільшити кількість відправлених повідомлень від певного юзера
async def update_user_n_messages(message: types.Message):
    user_id = message.from_user.id
    user = await select_user(user_id)
    new_n_messages = user.n_messages + 1
    await user.update(n_messages=new_n_messages).apply()


# Оновити репутацію юзера
async def update_user_reputation(name, user_id, new_reputation):
    if user_id is None:
        user = await select_user_by_name(name)
    else:
        user = await select_user(user_id)
    await user.update(reputation=new_reputation).apply()


# Записати id чату (використовується лише для відправки повідомлень з головного меню)
async def update_chat_id(chat_id):
    with open('ci.txt', 'w') as file:
        file.write(str(chat_id))


# Обрати id чату (використовується лише для відправки повідомлень з головного меню)
async def select_chat_id():
    with open('ci.txt', 'r') as file:
        chat_id = file.read()
    return int(chat_id)


# Перевірка реєстрації/реєстрація користувача у бд
async def register_user(message: types.Message):
    await update_chat_id(message.chat.id)
    count_of_registered_users = await db.func.count(User.user_id).gino.scalar()
    selected_user_id = message.from_user.id
    if count_of_registered_users != amount_of_users_in_group:
        users = await select_all_users()
        selected_user_nickname = message.from_user.username
        selected_user_first_name = message.from_user.first_name
        user_in_db = False
        for user in users:
            if selected_user_id == user.user_id:
                user_in_db = True
                break
        if not user_in_db:
            if message.from_user.username is None:
                selected_user_nickname = 'unknown' + str(count_of_registered_users)
            await add_user(selected_user_id, selected_user_nickname, selected_user_first_name, 0, 0)


# Оновлення повідомлення з полем гри життя
async def edit_msg(message: types.Message):
    try:
        game__life.updategrid(game__life.grid_1, 15)
        text =game__life.create_message_game_life(game__life.grid_1)
        await message.edit_text(text)
    except exceptions.RetryAfter as ex:
        print(ex.timeout)
        await message.answer(f'botyara занадто часто викликався і йому потрібно відбочити {ex.timeout} секунд')
        await asyncio.sleep(ex.timeout)


# Змінити повідомлення з анімованим серцем
async def edit_heart(message: types.Message, i):
    try:
        text = heart[-i]
        await message.edit_text(text)
    except exceptions.RetryAfter as ex:
        print(ex.timeout)
        await message.answer(f'botyara занадто часто викликався і йому потрібно відбочити {ex.timeout} секунд')
        await asyncio.sleep(ex.timeout)


# Перевірка переможця у грі
async def check_game_value(bot_v, chat_id):
    user_v = value
    if bot_v > user_v:
        await bot.send_message(chat_id, 'botyara переміг!')
    elif bot_v < user_v:
        await bot.send_message(chat_id, 'Пощастило, botyara програв!')
    elif bot_v == user_v:
        await bot.send_message(chat_id, 'Нічия!')


# Надіслати гру кістки (користвувач)
async def send_dice(chat_id):
    global value
    await bot.send_message(chat_id, 'Твій кубик')
    dice = await bot.send_dice(chat_id)
    value = dice.dice.value


# Надіслати гру (користувач)
async def send_game_(chat_id, text, emoji):
    global value
    await bot.send_message(chat_id, text)
    dice = await bot.send_dice(chat_id, emoji=types.dice.Dice(emoji=emoji))
    value = dice.dice.value




# __all__ = ['BaseModel', 'TimedBaseModel', 'User', 'save_picture', 'delete_file', 'create_audio', 'create_quote_image', 'time_in', 'date_in', 'now_para', 'para', 'timetable', 'time_t', 'randomgrid', 'create_message_game_life', 'updateGrid', 'on_startup_notify', 'set_default_commands', 'startup_database', 'db2_test', 'add_user', 'select_all_users', 'count_users', 'select_user', 'select_user_by_name', 'update_user_name_admin', 'update_user_name', 'update_user_n_messages', 'update_user_reputation', 'register_user', 'edit_msg', 'edit_heart', 'check_game_value', 'send_dice']
