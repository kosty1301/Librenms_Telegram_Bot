from peewee import *
db = SqliteDatabase('models.db')


class Device(Model):
    librenms_id = PrimaryKeyField()
    name = CharField(null=True)
    last_alert_data = DateTimeField(null=True)
    alert_is_send = BooleanField(default=False)

    class Meta:
        database = db

    def __int__(self):
        return self.librenms_id


class User(Model):
    chat_id = PrimaryKeyField()
    login = BooleanField(default=False)

    class Meta:
        database = db

    def __int__(self):
        return self.chat_id


class UserDevice(Model):
    user = ForeignKeyField(User, backref='user_device')
    device = ForeignKeyField(Device, backref='device_user')

    class Meta:
        database = db


def get_devices_or_false(chat_id):
    query = (Device
             .select()
             .join(UserDevice)
             .join(User)
             .where(User.chat_id == chat_id).execute())
    return [i for i in query] if len(query) > 0 else False


if __name__ == '__main__':
    Device.create_table()
    User.create_table()
    UserDevice.create_table()
