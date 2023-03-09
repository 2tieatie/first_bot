from random import choice
from random import randrange
from aiogram import executor
from all_texts import *
from game__life import *
import functions
import asyncio
import asyncpg
import datetime


async def db2_test():
    await db.set_bind(config.POSTGRES_URI)


# Запуск гри життя
@dp.message_handler(commands=['game_life'])
async def g_game_life(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    grid_1 = randomgrid(15)
    message_text = create_message_game_life(grid_1)
    last_message = await message.answer(message_text)
    for i in range(15):
        date = datetime.datetime.now() + timedelta(seconds=2 * i+1)
        scheduler.add_job(functions.edit_msg, "date", run_date=date, kwargs={"message": last_message})


# Команда для зміни ім'я
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    await message.answer(f'Hi, {message.from_user.first_name}')


# команда для виклику головного меню
@dp.message_handler(commands=['menu'])
async def m_main_menu(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    await message.answer('Обирай!', reply_markup=main_menu)


# Перейти до меню з іграми
@dp.callback_query_handler(lambda call: 'play_game' in call.data)
async def g_k(call):
    await call.message.edit_reply_markup(game_menu)


# Кнопка відправити серце
@dp.callback_query_handler(lambda call: 's_heart' in call.data)
async def h_k(call):
    await call.message.edit_reply_markup(heart_menu)


# Повернутися назад у меню
@dp.callback_query_handler(lambda call: 'back_to_menu' in call.data)
async def h_k(call):
    await call.message.edit_reply_markup(main_menu)


@dp.callback_query_handler(lambda call: 'help' in call.data)
async def h_help(call):
    file = open('ReadMe.txt', 'rb')
    chat_id = await functions.select_chat_id()
    await bot.send_document(chat_id, file)


# Ціле серце (з меню)
@dp.callback_query_handler(text='heart')
async def h_heart(call):
    chat_id = await functions.select_chat_id()
    message_text = heart[-1]
    last_message = await bot.send_message(chat_id, message_text)
    for i in range(len(heart)):
        date = datetime.datetime.now() + timedelta(seconds=1 * i + 1)
        scheduler.add_job(functions.edit_heart, "date", run_date=date, kwargs={"message": last_message, "i": i+1})


# Розбите серце (з меню)
@dp.callback_query_handler(text='heartbroken')
async def h_heartbroken(call):
    chat_id = await functions.select_chat_id()
    message_text = heart[0]
    last_message = await bot.send_message(chat_id, message_text)
    for i in range(len(heart)):
        date = datetime.datetime.now() + timedelta(seconds=1 * i + 1)
        scheduler.add_job(functions.edit_heart, "date", run_date=date, kwargs={"message": last_message, "i": -i})


# Голосове повідомлення російською
@dp.message_handler(commands=['voicen'])
async def send_voice_normal(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    text = message.text
    if len(text.replace(' ', '')) > 1:
        functions.delete_file('audio.ogg')
    text = text.replace('/voicen', '').replace('@ultradebik_bot', '')
    functions.create_audio(text, 'ru')
    await bot.send_chat_action(message.from_user.id, "upload_voice")
    audio = open('audio.ogg', 'rb')
    await bot.send_audio(message.chat.id, audio, reply_to_message_id=message.message_id)


# Голосове повідомлення польською
@dp.message_handler(commands=['voicef'])
async def send_voice_funny(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    text = message.text
    text = text.replace('/voicef', '').replace('@ultradebik_bot', '')
    if len(text.replace(' ', '')) > 1:
        functions.delete_file('audio.ogg')
    functions.create_audio(text, 'pl')
    await bot.send_chat_action(message.from_user.id, "upload_voice")
    audio = open('audio.ogg', 'rb')
    await bot.send_audio(message.chat.id, audio, reply_to_message_id=message.message_id)


# Голосове повідомлення україеською
@dp.message_handler(commands=['voiceu'])
async def send_voice_ukrainian(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    text = message.text
    if len(text.replace(' ', '')) > 1:
        functions.delete_file('audio.ogg')
    text = text.replace('/voiceu', '').replace('@ultradebik_bot', '')
    functions.create_audio(text, 'uk')
    await bot.send_chat_action(message.from_user.id, "upload_voice")
    audio = open('audio.ogg', 'rb')
    await bot.send_audio(message.chat.id, audio, reply_to_message_id=message.message_id)


# Надіслати перелік адмінів
@dp.message_handler(commands=['admins'])
async def send_admins(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    admins = 'Адміни:\n'
    for i in admins_id:
        user = await functions.select_user(i)
        admins += user.name + '\n'
    await message.answer(admins)


# Подивитись інформацію про себе
@dp.message_handler(commands=['profile'])
async def profile(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    user = await functions.select_user(message.from_user.id)
    text = message.text.split(' ')
    if message.from_user.id in admins_id and len(text) == 2:
        user = await functions.select_user_by_name(text[1])
        await message.answer((f'Нікнейм: {user.name}\n'
                         f'Ім\'я: {user.update_name}\n'
                         f'Кількість повідомлень: {user.n_messages}\n'
                         f'Любов Міші до {user.update_name}: {user.reputation}/10'))
    else:
        await message.answer(f'Твій нікнейм: {user.name}\n'
                             f'Твоє ім\'я: {user.update_name}\n'
                             f'Кількість повідомлень від тебе: {user.n_messages}\n'
                             f'Любов Міші до тебе: {user.reputation}/10')


# Змінити репутацію (лише для адмінів)
@dp.message_handler(commands=['change_reputation'])
async def change_reputation(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    if message.from_user.id in admins_id:
        text = message.text
        text = text.replace('/change_reputation', '').replace('@ultradebik_bot', '').split(' ')
        if text[0] == '':
            del text[0]
        user = await functions.select_user_by_name(text[0])
        reputation = int(text[1])

        await functions.update_user_reputation(user.name, None, reputation)

        await message.answer(f'Тепер любов Міші до @{user.name}: {reputation}/10')
    else:
        await message.answer('Ти що зудумав -_-')


# Відправка випадкового, готового заздалегідь, тексту
@dp.message_handler(commands=['pasta'])
async def button_test(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    await message.answer(choice(texts))


# Надіслати повідомлення з анімованим серцем (любов)
@dp.message_handler(commands=['heart'])
async def heart_h(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    message_text = heart[-1]
    last_message = await message.answer(message_text)
    for i in range(len(heart)):
        date = datetime.datetime.now() + timedelta(seconds=0.5 * i + 1)
        scheduler.add_job(functions.edit_heart, "date", run_date=date, kwargs={"message": last_message, "i": i+1})


# Надіслати повідомлення з анімованим серцем (розбите)
@dp.message_handler(commands=['heartbroken'])
async def heartbroken(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    message_text = heart[0]
    last_message = await message.answer(message_text)
    for i in range(len(heart)):
        date = datetime.datetime.now() + timedelta(seconds=0.5 * i + 1)
        scheduler.add_job(functions.edit_heart, "date", run_date=date, kwargs={"message": last_message, "i": -i})


# Надіслати картинку випадкового кота
@dp.message_handler(commands=['kitty', 'cat', 'kitten', 'котик'])
async def send_kitty(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    functions.save_picture('https://thiscatdoesnotexist.com/')
    photo = open('img.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo)
    functions.delete_file('img.jpg')


# Інші команди та повідомлення
@dp.message_handler(text_contains="/poll")
async def create_poll(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    text = message.text.replace('/poll', '').replace('@ultradebik_bot', '')
    text = text.split('-')
    text[1] = text[1].split('/')
    if len(text) == 3 and text[2].replace(' ', '').lower() in anon:

        await message.answer_poll(question=text[0], options=text[1], is_anonymous=True)
    else:
        await message.answer_poll(question=text[0], options=text[1], is_anonymous=False)


# Випадкове число
@dp.message_handler(text_contains='/random')
async def random_n(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    text = message.text
    text = text.replace('/random', '').replace('@ultradebik_bot', '')
    text_list = list(text.split(' '))
    # Випадкове число від 1 до обраного
    if len(text_list) == 2:
        num_2 = int(text_list[1])
        await message.answer(str(randrange(1, num_2)))
    # Випадкове число від обраного до обраного
    elif len(text_list) == 3:
        num_1 = int(text_list[1])
        num_2 = int(text_list[2])
        await message.answer((str(randrange(num_1, num_2))))
    # Випадкове число від 1 до 100
    else:
        await message.answer(str(randrange(1, 100)))


# Повідомлення з Інлвйн клавіатурою з іграми
@dp.message_handler(commands=['games'])
async def games(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    await message.answer('У яку гру бажаєш зіграти?', reply_markup=game_menu)

# Гра кістки
@dp.callback_query_handler(text='dice')
async def game_1(q):
    chat_id = await functions.select_chat_id()
    await bot.send_message(chat_id, 'Мій кубик')
    message = await bot.send_dice(chat_id)
    date = datetime.datetime.now() + timedelta(seconds=1)
    scheduler.add_job(functions.send_dice, 'date', run_date=date, kwargs={'chat_id': chat_id})
    date = datetime.datetime.now() + timedelta(seconds=5.2)
    scheduler.add_job(functions.check_game_value, 'date', run_date=date, kwargs={'bot_v': message.dice.value, 'chat_id': chat_id})

# Гра дартс
@dp.callback_query_handler(text='dart')
async def game_2(q):
    chat_id = await functions.select_chat_id()
    await bot.send_message(chat_id, 'Мій Дротик')
    message = await bot.send_dice(chat_id, emoji=types.dice.Dice(emoji='🎯'))
    date = datetime.datetime.now() + timedelta(seconds=1)
    scheduler.add_job(functions.send_game_, 'date', run_date=date, kwargs={'chat_id': chat_id, 'text': 'Твій дротик', 'emoji': '🎯'})
    date = datetime.datetime.now() + timedelta(seconds=4.2)
    scheduler.add_job(functions.check_game_value, 'date', run_date=date, kwargs={'bot_v': message.dice.value, 'chat_id': chat_id})


# Гра баскетбол
@dp.callback_query_handler(text='basketball')
async def game_3(q):
    chat_id = functions.select_chat_id()
    await bot.send_message(chat_id, 'Мій м\'яч')
    message = await bot.send_dice(chat_id, emoji=types.dice.Dice(emoji='🏀'))
    date = datetime.datetime.now() + timedelta(seconds=1)
    scheduler.add_job(functions.send_game_, 'date', run_date=date, kwargs={'chat_id': chat_id, 'text': 'Твій м\'яч', 'emoji': '🏀'})
    date = datetime.datetime.now() + timedelta(seconds=5.2)
    scheduler.add_job(functions.check_game_value, 'date', run_date=date, kwargs={'bot_v': message.dice.value, 'chat_id': chat_id})


# Гра футбол
@dp.callback_query_handler(text='football')
async def game_4(q):
    chat_id = await functions.select_chat_id()
    await bot.send_message(chat_id, 'Мій м\'яч')
    message = await bot.send_dice(chat_id, emoji=types.dice.Dice(emoji='⚽'))
    date = datetime.datetime.now() + timedelta(seconds=1)
    scheduler.add_job(functions.send_game_, 'date', run_date=date, kwargs={'chat_id': chat_id, 'text': 'Твій м\'яч', 'emoji': '⚽'})
    date = datetime.datetime.now() + timedelta(seconds=5.2)
    scheduler.add_job(functions.check_game_value, 'date', run_date=date, kwargs={'bot_v': message.dice.value, 'chat_id': chat_id})


# Гра слоти
@dp.callback_query_handler(text='slots')
async def game_5(q):
    chat_id = await functions.select_chat_id()
    await bot.send_message(chat_id, 'Мої слоти')
    message = await bot.send_dice(chat_id, emoji=types.dice.Dice(emoji='🎰'))
    date = datetime.datetime.now() + timedelta(seconds=1)
    scheduler.add_job(functions.send_game_, 'date', run_date=date, kwargs={'chat_id': chat_id, 'text': 'Твої слоти', 'emoji': '🎰'})
    date = datetime.datetime.now() + timedelta(seconds=3.5)
    scheduler.add_job(functions.check_game_value, 'date', run_date=date, kwargs={'bot_v': message.dice.value, 'chat_id': chat_id})


# Гра боулінг
@dp.callback_query_handler(text='bowling')
async def game_6(q):
    chat_id = await functions.select_chat_id()
    await bot.send_message(chat_id, 'Мій шар')
    message = await bot.send_dice(chat_id, emoji=types.dice.Dice(emoji='🎳'))
    date = datetime.datetime.now() + timedelta(seconds=1)
    scheduler.add_job(functions.send_game_, 'date', run_date=date, kwargs={'chat_id': chat_id, 'text': 'Твій шар', 'emoji': '🎳'})
    date = datetime.datetime.now() + timedelta(seconds=5.2)
    scheduler.add_job(functions.check_game_value, 'date', run_date=date, kwargs={'bot_v': message.dice.value, 'chat_id': chat_id})


# Команда для зміни ім'я
@dp.message_handler(text_contains='/change_name')
async def changing_name(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    text = message.text
    text = text.replace('/change_name', '').replace('@ultradebik_bot', '')
    # Для адмінів
    if message.from_user.id in admins_id and len(text.split('/')) == 2:
        text = text.split('/')
        user = await functions.select_user_by_name(text[0].replace(' ', ''))
        new_name = text[1]
        old_name = user.name
        await functions.update_user_name_admin(old_name, new_name)
        await message.answer(f'Тепер @{old_name} - {new_name}')
    # Для звичайних коричстувачів
    else:
        await functions.update_user_name(message.from_user.id, text)
        await message.reply(f'Твое имя обновлено на {text}!')


# Комада для перегляду пари
@dp.message_handler(text_contains='/para')
async def para_p(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    await message.answer(functions.para(message))


# Команда для перегляду розкладу
@dp.message_handler(text_contains='/time_t')
async def time_t_t(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    await message.answer(functions.time_t(message))


# Команда для створення цитати
@dp.message_handler(commands=['quote'])
async def reduce_rep(message: types.Message):
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    user = await functions.select_user(message.reply_to_message.from_user.id)
    name = user.update_name
    text = message.reply_to_message.text
    functions.create_quote_image(text, name)
    photo = open('quote.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo)
    functions.delete_file('quote.jpg')


#команда для відправки Wise_tree
@dp.message_handler(commands=['wise'])
async def wise_tree(message: types.Message):
    photo = open('wise_tree.png', 'rb')
    await bot.send_photo(message.chat.id, photo)


@dp.message_handler()
async def reduce_rep(message: types.Message):
    print(message)
    await functions.register_user(message)
    await functions.update_user_n_messages(message)
    user_id = message.from_user.id
    user = await functions.select_user(user_id)
    rep = user.reputation

    # Перевірка на погані слова
    for word in bad_words:
        if word in message.text.lower():
            print(word)
            await functions.update_user_reputation(None, user_id, rep - 1)
            await message.answer('Не ругайся, вафел')
            break

    # Перевірка на наявність слів, що підвищують репутацію
    for word in good_words:
        if word in message.text.lower():
            user = await functions.select_user(user_id)
            rep = user.reputation
            await functions.update_user_reputation(None, user_id, rep + 1)


# Запуск бота, якщо не виникло проблем під час ініціалізації
async def on_startup(dp: dp):
    await functions.on_startup_notify(dp)
    await functions.set_default_commands(dp)
    print('бот запущен')


# Якась фігня, боюсь її прибирати
async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(database=config.DATABASE,
    user=config.PGUSER,
    password=config.PGPASSWORD,
    max_inactive_connection_lifetime=100)

# Залупити бд
loop = asyncio.get_event_loop()
loop.run_until_complete(db2_test())

if __name__ == '__main__':
    try:
        executor.start_polling(dp, on_startup=on_startup)
    except Exception as ex:
        print(ex)
        executor.start_polling(dp, on_startup=on_startup)
