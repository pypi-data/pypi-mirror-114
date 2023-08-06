from telegram import (ParseMode, InputFile, InputMediaPhoto, ReplyKeyboardMarkup, ReplyKeyboardRemove,
                      KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Poll, Update, CallbackQuery)
from telegram.ext import CallbackContext, ConversationHandler
from PIL import Image
import re

import base64
from io import BytesIO
import yaml

import logging
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class callback_query_handler():
    def __init__(self, actions_dict):
        self.actions_dict = actions_dict

    def __call__(self, update: Update, context: CallbackContext):
        query = update.callback_query

        query.answer()
        query.edit_message_reply_markup(InlineKeyboardMarkup([]))
        if query.data.split(":")[0] == "action":
            return self.actions_dict[query.data.split(":")[1]](query, context)
        else:
            raise ValueError(
                "This type of operation ({}) is not supported in a callback query handler".format(query.data))


def read_action_yaml(filename, action_functions={}):
    with open(filename) as file:
        yaml_dict = yaml.load(file)

    actions_dict = {}

    for key, value in yaml_dict.items():
        actions_dict[key] = Action(value, action_functions=action_functions)

    return actions_dict


class Action():
    def __init__(self, actions, action_functions={}):
        self.actions = actions
        self.action_functions = action_functions

    def __call__(self, update: Update, context: CallbackContext):
        if "daten" in context.user_data and context.user_data["daten"]:
            logger.info(update)

        for item in self.actions:
            if "InlineKeyboard" in item:
                keyboard = [[]]
                for button in item["InlineKeyboard"]:
                    if "data" in button:
                        callback_data = button["data"]
                    else:
                        callback_data = None

                    if "url" in button:
                        callback_url = button["url"]
                    else:
                        callback_url = None

                    keyboard[0].append(InlineKeyboardButton(
                        button["text"], callback_data=callback_data, url=callback_url))

                reply_markup = InlineKeyboardMarkup(keyboard)

            elif "ReplyKeyboardMarkup" in item:
                keyboard = [[]]
                for button in item["ReplyKeyboardMarkup"]:
                    if "request_location" in button:
                        request_location = button["request_location"]
                    else:
                        request_location = False

                    keyboard[0].append(KeyboardButton(text=button["text"], request_location=request_location))

                reply_markup = ReplyKeyboardMarkup(
                    keyboard, one_time_keyboard=True)
            else:
                reply_markup = ReplyKeyboardRemove()

            if item["type"] == "message":
                parse_mode = None
                if "parse_mode" in item:
                    parse_mode = item["parse_mode"]

                if type(update) != CallbackQuery and update.poll_answer:
                    update.poll_answer.user.send_message(item["text"].format(
                        **{"echo": update.message.text, "name": context.user_data["name"]}), reply_markup=reply_markup, parse_mode=parse_mode)
                else:
                    update.message.reply_text(item["text"].format(
                        **{"echo": update.message.text, "name": context.user_data["name"]}), reply_markup=reply_markup, parse_mode=parse_mode)
            elif item["type"] == "photo":
                if type(update) != CallbackQuery and update.poll_answer:
                    update.poll_answer.user.send_photo(
                        open(item["file"], 'rb'), reply_markup=reply_markup)
                else:
                    update.message.reply_photo(
                        open(item["file"], 'rb'), reply_markup=reply_markup)
            elif item["type"] == "audio":
                update.message.reply_audio(open(
                    item["file"], 'rb'), title=item["title"], performer=item["performer"], reply_markup=reply_markup)
            elif item["type"] == "contact":
                update.message.reply_contact(phone_number=item["phone_number"],
                                            first_name=item["first_name"],
                                            last_name=item["last_name"],
                                            reply_markup=reply_markup)
            elif item["type"] == "poll":
                update.message.reply_poll(question=item["question"],
                                          options=item["options"],
                                          type=Poll.QUIZ,
                                          correct_option_id=item["correct_option_id"],
                                          is_anonymous=False
                                          )

            elif item["type"] == "media_group":
                photoGroup = [InputMediaPhoto(media=open(
                    photo, 'rb')) for photo in item["files"]]
                update.message.reply_media_group(media=photoGroup)
            elif item["type"] == "sticker":
                if type(update) != CallbackQuery and update.poll_answer:
                    update.poll_answer.user.send_sticker(item["id"])
                else:
                    update.message.reply_sticker(item["id"])
            
            ## type: venue
            # latitude: 52.4090401
            # longitude: 12.9724552
            # address: Bahnhof Golm
            # title: Start der Rallye

            elif item["type"] == "venue":
                if type(update) != CallbackQuery and update.poll_answer:
                    update.poll_answer.user.send_venue(
                        latitude=item["latitude"], longitude=item["longitude"], address=item["address"], title=item["title"])
                else:
                    update.message.reply_venue(
                        latitude=item["latitude"], longitude=item["longitude"], address=item["address"], title=item["title"])

            elif item["type"] == "return":
                if item["state"] == "END":
                    return ConversationHandler.END
                return item["state"]
            elif item["type"] == "callback":
                query = update.callback_query

                query.answer()
                query.edit_message_reply_markup(InlineKeyboardMarkup([]))
                for case in item["conditions"]:
                    if query.data == case["condition"]:
                        return Action(case["action"])(query, context)
            elif item["type"] == "function":
                arguments = {i:item[i] for i in item if i!='type' and i!='func'}
                self.action_functions[item["func"]](update, context, **arguments)
