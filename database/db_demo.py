from tortoise.models import Model
from tortoise import fields, Tortoise, run_async


class Tournament(Model):
    # Defining `id` field is optional, it will be defined automatically
    # if you haven't done it yourself
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    # Defining ``__str__`` is also optional, but gives you pretty
    # represent of model in debugger and interpreter
    def __str__(self):
        return self.name


class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    # References to other models are defined in format
    # "{app_name}.{model_name}" - where {app_name} is defined in tortoise config
    tournament = fields.ForeignKeyField('models.Tournament', related_name='events')
    participants = fields.ManyToManyField('models.Team', related_name='events', through='event_team')

    def __str__(self):
        return self.name


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['database.db_demo']}
    )
    # Generate the schema
    await Tortoise.generate_schemas(safe=True)


# Create instance by save
async def create_v1():
    tournament = Tournament(name='New Tournament')
    a = await tournament.save()
    return a


# Or by .create()
async def create_v2():
    await Tournament.create(name='Another Tournament')


# Now search for a record
async def search_v1():
    tour = await Tournament.filter(name__contains='Another').first()
    print(tour.name)


if __name__ == '__main__':
    # run_async(init()) # 创建表
    create_v1()
