from datetime import datetime as dt
from Password_and_token import *

DALEY_FOR_ALERT = 1  # min
MORNING_TIME = '09:00:00'
EVENING_TIME = '23:50:00'

PLESE_LOGIN = 'Введите пароль....'
PLESE_ENTER_DEV_ID = 'введите уникальный идентификатор устройства'
LOGIN_INCORRECT = 'пароль не верный'
DEVICE_ADDED = 'Устройство добавлено'
DEVICE_NOT_ADDED = 'Устройство не обнаружено'
LOGIN = 'Вход выполнен'
DEVICE_LIST_IS_NULL = 'Устройства не обнаружены'
DATABASE_REFRESH = 'база данных успешно обнавлена'
DATABASE_REFRESH_ERROR = 'не удалось обновить базу данных'
ACHIVE = 'устройство восстановлено'
DEVICE_ALERT = 'Устройство недоступно:'
TRY_RUN_MODULE = 'you cannot run this file as a program'


URL = "https://api.telegram.org/bot{}/".format(TELEGRAM_TOKEN)
DATE_FORMAT = '%H:%M:%S'
MORNING = dt.strptime(MORNING_TIME, DATE_FORMAT)
EVENING = dt.strptime(EVENING_TIME, DATE_FORMAT)

REQUEST_HEADERS = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "X-Auth-Token": LIBRENMS_TOKEN,
    "Connection": "keep-alive"
}
