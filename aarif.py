#!/usr/bin/python
# -*- coding: utf-8 -*-

from telegram import File
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from keys import aarif_telegram_token, clarifai_key_id, clarifai_key_secret
import logging
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp(clarifai_key_id, clarifai_key_secret)

updater = Updater(token=aarif_telegram_token)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    update.message.reply_text("Started")

def photo(bot, update):
    update.message.reply_text("Photo: Calismaya Basladim")
    idi = update.message.photo[-1]["file_id"]
    photo_file = bot.getFile(idi)
    photo_file.download(str(idi)+".jpg")
    model = app.models.get("general-v1.3")
    image = ClImage(file_obj=open(str(idi)+".jpg", 'rb'))
    result = model.predict([image])
    output = ""
    for i in result["outputs"][0]["data"]["concepts"]:
        output = output + i["name"].encode(encoding="utf-8") + " | value: " + str(i["value"]) + "\n"
    update.message.reply_text(output)

def file(bot, update):
    update.message.reply_text("File/Document: Calismaya Basladim")

photo_handler = MessageHandler(Filters.photo, photo)
file_handler = MessageHandler(Filters.document, file)
start_handler = CommandHandler("start", start)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(photo_handler)
dispatcher.add_handler(file_handler)

updater.start_polling()