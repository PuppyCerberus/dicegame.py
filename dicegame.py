import telebot
import datetime
import time
import logging as log
from Tokens import TOKEN_MIYA
from sqlite3 import IntegrityError, connect
from sqlite3.dbapi2 import Connection, Cursor

today = datetime.datetime.now().date()
hour = datetime.datetime.now().minute

miya_bot = telebot.TeleBot(TOKEN_MIYA)

# Connect to database
conn: Connection = connect("PuppyAdventure_Game.db", check_same_thread=False)
# Create a cursor object
c: Cursor = conn.cursor()

c.execute(
    "CREATE TABLE IF NOT EXISTS dice_game (tg_username TEXT UNIQUE, points INTEGER NOT NULL,\
    date TEXT, time TEXT)"
)


def dice_entry(tg_username: str, dice_point: int) -> None:
    c.execute(
        """INSERT INTO dice_game (tg_username, points, date, time)
        VALUES (?, ?, datetime('now'), datetime('now', 'localtime'))""",
        (tg_username, dice_point),
    )
    conn.commit()


@miya_bot.message_handler(content_types=["dice"])
def dice_bot(message):
    rolling_dice = message.dice.value
    username = message.from_user.username
    c.execute("SELECT points FROM dice_game WHERE tg_username = ?", (username,))
    a_list = c.fetchall()  # give a list of tuple data from table
    list_exts = [item[0] for item in a_list]  # convert the list of tuple to a list
    string = [str(list_ext) for list_ext in list_exts]  # convert the list into string
    a_string = "".join(string)
    an_integer = int(a_string)  # existing data from the table
    final_points = rolling_dice + an_integer

    try:
        if final_points >= 144:
            miya_bot.send_message(message.chat.id, "You busted LOL")
        else:
            dice_entry(tg_username=username, dice_point=rolling_dice)
            miya_bot.send_message(message.chat.id, "Your 1st entry is registered" + " \
                            You now have " + rolling_dice + "points")
    except IntegrityError:

        c.execute("SELECT points FROM dice_game WHERE tg_username = ?", (username,))
        a_list = c.fetchall()  # give a list of tuple data from table
        list_exts = [item[0] for item in a_list]  # convert the list of tuple to a list
        string = [str(list_ext) for list_ext in list_exts]  # convert the list into string
        a_string = "".join(string)
        an_integer = int(a_string)  # existing data from the table
        final_points = rolling_dice + an_integer
        c.execute("UPDATE dice_game SET points = ? WHERE tg_username = ?", (final_points, username), )
        conn.commit()

        print(str(rolling_dice) + " This is what you roll")
        print(str(an_integer) + " This is the existing points from database")
        print(str(rolling_dice + an_integer) + " This is the final points updated on database")
        miya_bot.send_message(message.chat.id, "Your total points are " + final_points)


telebot.apihelper.RETRY_ON_ERROR = True

cerberus_bot.polling(none_stop=True)
