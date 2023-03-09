import numpy as np
from variables import *
import functions
from datetime import datetime, timedelta


game_chat_id = -1001849084434


# Створення випадкового поля для гри життя
def randomgrid(N):
    return np.random.choice(vals, N * N, p=[0.2, 0.8]).reshape(N, N)


# Ініціалізація змінної з полем
grid_1 = randomgrid(15)


# Оновлення поля гри життя
def updategrid(grid, N):
    global grid_1
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            total = int((grid[i, (j - 1) % N] + grid[i, (j + 1) % N] +
                         grid[(i - 1) % N, j] + grid[(i + 1) % N, j] +
                         grid[(i - 1) % N, (j - 1) % N] + grid[(i - 1) % N, (j + 1) % N] +
                         grid[(i + 1) % N, (j - 1) % N] + grid[(i + 1) % N, (j + 1) % N]) / 255)

            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON

    grid[:] = newGrid[:]
    grid_1[:] = grid[:]


# Створення текствого повідомлення з матриці поля гри життя
def create_message_game_life(grid):
    message_text = ''
    for row in list(grid):
        for pos, i in enumerate(list(row)):
            message_text += str(i)
            if pos == 14:
                message_text += '\n'
    message_text = message_text.replace('0', '□').replace('255', '■')
    return message_text


# Виклик гри життя з меню
@dp.callback_query_handler(text='g_life')
async def g_g_life(call):
    chat_id = game_chat_id
    grid_1 = randomgrid(15)
    message_text = create_message_game_life(grid_1)
    last_message = await bot.send_message(chat_id, message_text)
    for i in range(15):
        date = datetime.datetime.now() + timedelta(seconds=2 * i + 1)
        scheduler.add_job(functions.edit_msg, "date", run_date=date, kwargs={"message": last_message})


