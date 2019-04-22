# -*- coding:utf8 -*- 

#Отображать кирилицу в коде, при выводе информации
#Если вы её не укажете, то при print("привет"), если кодировка не поддерживающая кирилицу , то там будет вопросики, на месте русских букв или в бинарном коде будет текст выводиться


import telebot  
#Подключить модуль можно с помощью инструкции import. К примеру, подключим модуль config,keyboards, weath, datetime для получения текущей директории
from config import * #Вы можете использовать любой питоновский файл как модуль в другом файле, выполнив в нем команду import. 
from keyboards import * 
from weath import * #В Python так же возможно импортировать всё (переменные, функции, классы) за раз из модуля, для этого используется конструкция from ... import *
from datetime import datetime #Команда from ... import позволяет нам импортировать не весь модуль целиком, а только определенное его содержимое.
bot = telebot.TeleBot(token)

coords={} #{user_id:[lat,long]}
ask_geo={} 

@bot.message_handler(commands=['start'])
def start_message(message):
    ask_geo[message.from_user.id]=1
    bot.send_message(message.from_user.id,hello_text,reply_markup=geo())

@bot.message_handler(content_types=['location'],func=lambda message:ask_geo.get(message.from_user.id,0)==1)
def location(message):
    latit=message.location.latitude
    longit=message.location.longitude
    coords[message.from_user.id]=[latit,longit]
    bot.send_message(message.from_user.id,coords_ok,reply_markup=weather())
    ask_geo[message.from_user.id]=0
#Прогнозы на сегодня
@bot.message_handler(func=lambda message:message.text=="Прогноз на сегодня")
def daily(message):
    c=coords.get(message.from_user.id,-1)
    if c!=-1:
        status=get_weather_five(c)
        city=status['city'].get("name","Неизвестно")
        dt_now=datetime.now()
        now_day=weekdays[dt_now.weekday()]
        mes_text=f"<b>Город: {city}</b>\n\n<b>{now_day}</b>\n"      
        for data in status['list']:
            dt=str(data['dt_txt'].split(" ")[0])
            day=datetime.strptime(dt,r"%Y-%m-%d")
            if (dt_now.year==day.year) and (dt_now.month==day.month) and (dt_now.day==day.day):
                humid=data['main']['humidity']
                date="".join(data['dt_txt'].split(" ")[1:])
                temp=str(data['main']['temp_min'])
                press=data['main']['pressure']
                descr=data['weather'][0]['description']
                ws=data['wind']['speed']
                mes_text+=weath_text_day.format(date,temp,descr,humid,press,ws)
            else:
                continue
        bot.send_message(message.from_user.id,mes_text,parse_mode="HTML")
    else:
        ask_geo[message.from_user.id]=1
        bot.send_message(message.from_user.id,hello_text,reply_markup=geo())

#Прогнозы на завтра 
@bot.message_handler(func=lambda message:message.text=="Прогноз на завтра")
def tomorrow(message):
    c=coords.get(message.from_user.id,-1)
    if c!=-1:
        status=get_weather_five(c)
        city=status['city'].get("name","Неизвестно")
        dt_now=datetime.now()
        now_day=weekdays[(dt_now.weekday()+1)%7]
        mes_text=f"<b>Город: {city}</b>\n\n<b>{now_day}</b>\n"      
        for data in status['list']:
            dt=str(data['dt_txt'].split(" ")[0])
            day=datetime.strptime(dt,r"%Y-%m-%d")
            if (dt_now.year==day.year) and (dt_now.month==day.month) and (dt_now.day+1==day.day):
                humid=data['main']['humidity']
                date="".join(data['dt_txt'].split(" ")[1:])
                temp=str(data['main']['temp_min'])
                press=data['main']['pressure']
                descr=data['weather'][0]['description']
                ws=data['wind']['speed']
                mes_text+=weath_text_day.format(date,temp,descr,humid,press,ws)
            else:
                continue
        bot.send_message(message.from_user.id,mes_text,parse_mode="HTML")
    else:
        ask_geo[message.from_user.id]=1
        bot.send_message(message.from_user.id,hello_text,reply_markup=geo())
#Прогнозы на 5 дней 
@bot.message_handler(func=lambda message:message.text=="Прогноз на 5 дней")
def five_day(message):
    c=coords.get(message.from_user.id,-1)
    if c!=-1:
        status=get_weather_five(c)
        city=status['city'].get("name","Неизвестно")
        dt=status['list'][0]['dt_txt'].split(" ")[0]
        day=datetime.strptime(dt,r"%Y-%m-%d")
        now_day=weekdays[day.weekday()]
        mes_text=f"<b>Город: {city}</b>\n\n<b>{now_day}</b>\n"
        for data in status['list']:
            dt_now=data['dt_txt'].split(" ")[0]
            if dt_now!=dt:
                day=datetime.strptime(dt_now,r"%Y-%m-%d")
                now_day=weekdays[day.weekday()]
                mes_text+=f"<b>{now_day}</b>\n"
                dt=dt_now
            humid=data['main']['humidity']
            date="".join(data['dt_txt'].split(" ")[1:])
            temp=str(data['main']['temp_min'])
            descr=data['weather'][0]['description']
            mes_text+=weath_text_weak.format(date,temp,descr,humid)
        bot.send_message(message.from_user.id,mes_text,parse_mode="HTML")
    else:
        ask_geo[message.from_user.id]=1
        bot.send_message(message.from_user.id,hello_text,reply_markup=geo())
            

@bot.message_handler(func=lambda message:message.text=="Сменить координаты")
def reset(message):
    ask_geo[message.from_user.id]=1
    bot.send_message(message.from_user.id,"Пожалуйста, пришлите новые координаты",reply_markup=geo())

bot.polling()
