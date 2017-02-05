#!/usr/bin/python
# -*- coding: utf-8 -*-

from telegram import File
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from keys import maarif_telegram_token, clarifai_key_id, clarifai_key_secret
import logging
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp(clarifai_key_id, clarifai_key_secret)

betim = []

updater = Updater(token=maarif_telegram_token)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    global betim
    update.message.reply_text(betim)
    betim = []

def train(bot, update):
    update.message.reply_text("training")
    #model = app.models.create('vidi-v1', concepts=["white cane", "folded white cane", "braille", "book", "notebook", "pen", "telephone", "headphone", "box", "people"])
    model = app.models.get("vidi-v1")
    model.train()

def entry(bot, update):
    update.message.reply_text("Entry: Çalışmaya başladım")
    betim.append(update.message.text)
    print(betim)

def photo(bot, update):
    global betim
    update.message.reply_text(betim)
    idi = update.message.photo[-1]["file_id"]
    photo_file = bot.getFile(idi)
    photo_file.download(str(idi) + ".jpg")
    print(app.inputs.create_image_from_filename(str(idi) + ".jpg", image_id=None, concepts=betim))
    betim = []

def file(bot, update):
    update.message.reply_text("File/Document: Calismaya Basladim")

photo_handler = MessageHandler(Filters.photo, photo)
file_handler = MessageHandler(Filters.document, file)
start_handler = CommandHandler("start", start)
train_handler = CommandHandler("train", train)
entry_handler = MessageHandler(Filters.text, entry)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(photo_handler)
dispatcher.add_handler(file_handler)
dispatcher.add_handler(entry_handler)
dispatcher.add_handler(train_handler)

updater.start_polling()