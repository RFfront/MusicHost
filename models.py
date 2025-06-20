from peewee import *

sqlite_db = SqliteDatabase('app.db')


class BaseModel(Model):
    class Meta:
        database = sqlite_db


class VKMessages(BaseModel):
    message_id = IntegerField()
    flags = IntegerField()
    minor_id = IntegerField()
    other = TextField()


if __name__ == '__main__':
    VKMessages.create_table()
