from datetime import datetime as dt, timedelta

from settings import *
from Password_and_token import *
from models import Device
from bot import Bot


bot = Bot(TELEGRAM_TOKEN)


def delay_is_over(device):
    return dt.now() - device.last_alert_data > timedelta(minutes=DALEY_FOR_ALERT)


class AlertDispach:
    def __init__(self, alert_list: list):
        self.recovered_query = Device.select().where(Device.alert_is_send == 1).execute()
        self.device_alert_query = Device.select().where(Device.librenms_id.in_(tuple(alert_list)))

        self.device_is_recovered = [dev for dev in self.recovered_query
                                    if str(dev) not in alert_list]
        self.new_alerts = [dev for dev in self.device_alert_query if dev.last_alert_data is None]

        self.alerts_to_send = [dev for dev in self.device_alert_query
                               if dev not in self.new_alerts and dev.alert_is_send == 0]

    def send_alerts_to_users(self) -> None:
        for dev in self.alerts_to_send:
            if delay_is_over(dev):
                for user in dev.device_user:
                    bot.send_message(f'{DEVICE_ALERT} \n {dev.name} {dev.last_alert_data}', user.user)
                dev.alert_is_send = True
                dev.save()

    def sends_achive_to_users(self) -> None:
        for dev in self.device_is_recovered:
            for user in dev.device_user:
                bot.send_message(f'{ACHIVE} \n {dev.name} : {dev}', user.user)
            dev.last_alert_data = None
            dev.alert_is_send = False
            dev.save()

    def create_new_alerts(self):
        query = Device.update(last_alert_data=dt.now()).where(Device.librenms_id.in_(self.new_alerts))
        query.execute()


if __name__ == '__main__':
    print(TRY_RUN_MODULE)
