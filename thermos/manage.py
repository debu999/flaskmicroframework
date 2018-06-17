import sys

from thermos import application, db
from thermos.models import User, Bookmark, Tag
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
import random

manager = Manager(app=application)
migrate = Migrate(app=application, db=db)

manager.add_command("db", MigrateCommand)

@manager.command
def insert_data():
    u1 = User(username="debu999", email="debabrata.patnaik@live.com", password="123456")
    u2 = User(username="priyu999", email="priyabrata.patnaik@live.com", password="abcdef")
    u3 = User(username="Debabrata Patnaik", email="debu999@gmail.com", password="456789")
    u4 = User(username="Jigyansa", email="jigyansa@infosys.com", password="jigi123")
    ulist = [u1, u2, u3, u4]
    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)
    db.session.add(u4)

    def add_bookmark(url, desc, tags):
        bkm = Bookmark(url=url, description=desc, user=random.choice(ulist), tags=tags)
        # tglist = list()
        # for t in tags.split(","):
        #     tg = Tag.query.filter_by(name=t).first()
        #     if not tg:
        #         tg = Tag(name=t)
        #         db.session.add(tg)
        #     tglist.append(tg)
        # for tgs in tglist:
        #     bkm._tags.append(tgs)
        db.session.add(bkm)

    for name in ["python", "flask", "programming", "werkzeug", "news", "training", "orm"]:
        db.session.add(Tag(name=name))

    add_bookmark("https://www.nike.com", "Just Do It", "python,programming,orm,news,bigdata")
    add_bookmark("https://www.Apple.com", "Think Different", "programming")
    add_bookmark("https://www.Dollar Shave Club.com", "Shave Time. Shave Money.", "news,werkzeug,flask,training")
    add_bookmark("https://www.L'Oréal.com", "Because You're Worth It", "python,training")
    add_bookmark("https://www.California Milk Processor Board.com", "Got Milk?", "python,flask")
    add_bookmark("https://www.MasterCard.com",
                 "There are some things money can't buy. For everything else, there's MasterCard.", "orm")
    add_bookmark("https://www.BMW.com", "Designed for Driving Pleasure", "news,werkzeug,training,programming")
    add_bookmark("https://www.Tesco.com", "Every Little Helps", "flask")
    add_bookmark("https://www.M&M.com", "Melts in Your Mouth, Not in Your Hands", "news,orm,training")
    add_bookmark("https://www.Bounty.com", "The Quicker Picker Upper", "orm,flask,training,programming")
    add_bookmark("https://www.De Beers.com", "A Diamond is Forever", "python,orm")
    add_bookmark("https://www.Lay's.com", "Betcha Can't Eat Just One", "python,orm,werkzeug,flask")
    add_bookmark("https://www.Audi.com", "Vorsprung durch technik ('Advancement Through Technology')",
                 "orm,news,programming")
    add_bookmark("https://www.Dunkin' Donuts.com", "America Runs on Dunkin", "news")
    add_bookmark("https://www.Meow Mix.com", "Tastes So Good, Cats Ask for It by Name", "python,orm,news")
    add_bookmark("https://www.McDonald's.com", "I'm Lovin' It", "news,orm,werkzeug,flask")
    add_bookmark("https://www.The New York Times.com", "All the News That's Fit to Print", "orm,werkzeug")
    add_bookmark("https://www.General Electric.com", "Imagination at Work", "programming,training")
    add_bookmark("https://www.Verizon.com", "Can You Hear Me Now? Good.", "news,werkzeug,programming")
    add_bookmark("https://www.State Farm.com", "Like a Good Neighbor, State Farm is There", "python,flask")
    add_bookmark("https://www.Maybelline.com", "Maybe she's born with it. Maybe it's Maybelline.", "flask,training")
    db.session.commit()
    print("Inserted records to database.")


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to loose all your data"):
        db.drop_all()
        print("Dropped all DB objects using db.drop_all command")


if __name__ == "__main__":
    manager.run()
