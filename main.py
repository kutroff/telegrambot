import telegram
import struct
import random
import encode
import os

questions = ""

# Загружаем вопросы и ответы из файла test.txt
encode.decode("test.txt.bin")#Декодируем бинарный файл
with open("test.txt.bin.txt", "r", encoding="utf-8") as f:#Считываем текстовый файл
    questions = f.read().splitlines()
os.remove("test.txt.bin.txt")#Удаляем файл, который декодировали

# Создаем список вариантов ответа для каждого вопроса
options = []
for i in range(1, len(questions), 6):
    options.append(questions[i:i+5])

# Создаем словарь правильных ответов для каждого вопроса
answers = []
for i in range(0, len(questions), 6):
    a = questions[i+1:i+5]
    for j in range(len(a)):
        if a[j][0] == questions[i+5][0]:
            answers.append(j)
            
# Создаем телеграм-бота
TOKEN = '6280094652:AAH6mZYnYzzEWz_xG4mZ5VbwZ5iazRxPtag'
bot = telegram.Bot(token=TOKEN)

# Функция для отправки приветствия и первого вопроса
async def start(update, context):
    #ниже представлен вывод сообщений
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Это тест на знание раздела объектно-ориентированного программирования в C++. Отвечайте на вопросы, выбирая кнопки а, б, в или г.")

    # Случайным образом выбираем первый вопрос
    current_question = random.randint(0, len(options)-1)

    # Отправляем первый вопрос и варианты ответа
    context.user_data['current_question'] = current_question#Индекс нынешнего вопроса
    context.user_data['score'] = 0#Счет пользователя
    context.user_data['answered'] = [current_question]#Список с вопросами, которые уже пользователь видел
    text1 = (questions[current_question*6])#Вопрос
    text2 = (options[current_question][0])#Первый вариант
    text3 = (options[current_question][1])#Второй вариант
    text4 = (options[current_question][2])#Третий вариант
    text5 = (options[current_question][3])#Четвертый вариант
    #выводим
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text1)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text2)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text3)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text4)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text5)

# Функция для обработки ответов пользователя
async def answer(update, context):
    # Получаем ответ пользователя
    user_answer = update.message.text

    # Получаем текущий вопрос
    current_question = context.user_data['current_question']
    # Проверяем ответ пользователя
    if  user_answer == 'А' or user_answer == 'а':
        user_answer_index = 0
    elif user_answer == 'Б' or user_answer == 'б':
        user_answer_index = 1
    elif user_answer == 'В' or user_answer == 'в':
        user_answer_index = 2
    elif user_answer == 'Г' or user_answer == 'г':
        user_answer_index = 3
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, выберите один из вариантов ответа: а, б, в или г.")
        return

    # Получаем правильный ответ на текущий вопрос
    correct_answer_index = answers[current_question]

    # Проверяем, был ли ответ пользователя правильным
    if user_answer_index == correct_answer_index:
        context.user_data['score'] += 1

    # Если было задано 20 вопросов, выводим результаты
    if len(context.user_data['answered']) == 20:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Тест завершен! Вы ответили правильно на " + str(context.user_data['score']) + " из 20 вопросов.")
        # Определяем оценку пользователя
        score = context.user_data['score']
        if score >= 15:
            grade = "Поздравляю, экзамен автоматом"
        elif score >= 12:
            grade = "4"
        elif score >= 9:
            grade = "3"
        else:
            grade = "2"

        # Отправляем оценку пользователю
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Ваша оценка: " + grade)
        context.user_data['score'] = 0
        context.user_data['answered'] = []
        return
    # Выбираем следующий вопрос случайным образом
    current_question = random.randint(0, len(options)-1)
    while current_question in context.user_data['answered']:#Находим такой случайный индекс вопроса, который мы не выводили пользователю
        current_question = random.randint(0, len(options)-1)

    context.user_data['answered'].append(current_question)

    # Отправляем следующий вопрос и варианты ответа
    context.user_data['current_question'] = current_question
    text1 = (questions[current_question*6])
    text2 = (options[current_question][0])
    text3 = (options[current_question][1])
    text4 = (options[current_question][2])
    text5 = (options[current_question][3])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text1)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text2)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text3)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text4)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text5)
from telegram.ext import Updater
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
application = ApplicationBuilder().token(TOKEN).build()
start_handler = CommandHandler('start', start)
application.add_handler(start_handler)


from telegram.ext import MessageHandler, filters
answer_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, answer)
application.add_handler(answer_handler)

application.run_polling()