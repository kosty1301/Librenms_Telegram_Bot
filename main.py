from functools import wraps
from loguru import logger

from alert_dispach import AlertDispach
from settings import *
from Password_and_token import *
from bot import Bot
from models import User, Device, UserDevice, get_devices_or_false
from librenms import LibreNMSAPI
from exceptions import *


logger.add('log.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
           level="DEBUG"
           )

librenms_api = LibreNMSAPI(auth_token=LIBRENMS_TOKEN,
                           request_headers=REQUEST_HEADERS,
                           api_url=LIBRENMS_URL
                           )

print_info = logger.info
print_error = logger.error
bot = Bot(TELEGRAM_TOKEN)
next_step = {}


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        text, chat = bot.context(*args)
        user = User.get_or_none(User.chat_id == chat)
        if not user or not user.login:
            return start(*args)
        return func(*args, **kwargs)
    return inner


def start(update):
    text, chat = bot.context(update)
    user = User.get_or_none(User.chat_id == chat)
    if user:
        bot.send_message(LOGIN, chat)
        return
    bot.send_message(PLESE_LOGIN, chat)
    next_step.update({chat: auth})


def auth(update):
    text, chat = bot.context(update)
    if text.isdigit() and text == PASSWORD:
        User.create(chat_id=chat, login=True)
        bot.send_message(LOGIN, chat)
        return next_step.pop(chat)
    bot.send_message(LOGIN_INCORRECT, chat)


@login_required
def add_device_step_one(update):
    text, chat = bot.context(update)
    bot.send_message(PLESE_ENTER_DEV_ID, chat)
    next_step.update({chat: add_device})


def add_device(update):
    text, chat = bot.context(update)
    user = User.get_or_none(User.chat_id == chat)
    device = Device.get_or_none(Device.librenms_id == text)
    if device and user:
        UserDevice.get_or_create(user=user, device=device)
        return bot.send_message(DEVICE_ADDED, chat)
    bot.send_message(DEVICE_NOT_ADDED, chat)


@login_required
def device_list(update):
    text, chat = bot.context(update)
    dev_list = get_devices_or_false(chat)
    result = 'name:   ' + 'id:' + '\n'
    if dev_list:
        for i in dev_list:
            name = Device.get_or_none(librenms_id=i).name
            result += name + ': ' + str(i) + '\n'
        return bot.send_message(result, chat)
    bot.send_message(DEVICE_LIST_IS_NULL, chat)


@login_required
def refresh_device_list(update):
    text, chat = bot.context(update)
    message = DATABASE_REFRESH
    try:
        devices = librenms_api.get_id_and_name_list()
        for dev_id, name in devices.items():
            device = Device.get_or_none(Device.librenms_id == dev_id)
            if not device:
                Device.get_or_create(librenms_id=dev_id, name=name)

    except LibrenmsApiError:
        message = DATABASE_REFRESH_ERROR
    bot.send_message(message, chat)


comands = {'/start': start,
           '/add_device': add_device_step_one,
           '/device_list': device_list,
           '/refresh_database': refresh_device_list}


def handler(updates):
    for update in updates["result"]:
        text, chat = bot.context(update)
        if text in comands:
            comands[text](update)
            continue
        if chat in next_step:
            next_step[chat](update)


def main():
    last_update_id = None
    while True:
        updates = bot.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = bot.get_last_update_id(updates) + 1
            handler(updates)

        try:
            alerts = librenms_api.get_alert_devices()
        except LibrenmsApiError as error:
            print_error(f'{error}, LIBRENMS_URL: {LIBRENMS_URL}, please check it')
            continue
        alert_dispach = AlertDispach(alerts.keys())
        alert_dispach.create_new_alerts()
        alert_dispach.send_alerts_to_users()
        alert_dispach.sends_achive_to_users()


if __name__ == "__main__":
    print_info('bot has started')
    main()

