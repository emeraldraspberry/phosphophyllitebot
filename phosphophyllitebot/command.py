import logging
import io
import time
import sqlite3
import argparse
import datetime
import shlex

class Command():
    def __init__(self):
        self.cooldown_time = time.time()
        # Amount of seconds to wait before updating ability with on_seen()
        self.cooldown = 60

    def convert_time(self, seconds):
        min, sec = divmod(seconds, 60)
        hour, min = divmod(min, 60)
        day, hour = divmod(hour, 24)
        week, day = divmod(day, 7)
        if week != 0:
            return(f'{week} week(s), {day} day(s), {hour} hour(s), {min} min(s), and {sec} second(s)')
        elif day != 0:
            return(f'{day} day(s), {hour} hour(s), {min} min(s), and {sec} second(s)')
        elif hour != 0:
            return(f'{hour} hour(s), {min} min(s), and {sec} second(s)')
        elif min != 0:
            return(f'{min} min(s), and {sec} second(s)')
        else:
            return(f'{sec} second(s)')

    def check_cooldown(self):
        # When off cooldown (after elapsed time), return true
        if (time.time()-self.cooldown_time)>self.cooldown:
            return True
        else:
            return False

    def get_elapsed_cooldown_time(self):
        return(str(time.time()-self.cooldown_time))

    def on_seen(self, message, database):
        if self.check_cooldown()==True:
            for member in message.guild.members:
                database.update(member=member)
            self.cooldown_time = time.time()
        else:
            logging.info(f'Update cooldown: {self.get_elapsed_cooldown_time()}')

        logging.info(f'Received command:seen {message.content}')
        parser = argparse.ArgumentParser(description="Example goes here")
        parser.add_argument("--user", help="User name")
        logging.info(f'{shlex.split(message.content)}')
        name, unknown = parser.parse_known_args(shlex.split(message.content))
        try:
            database.cursor.execute('SELECT status_time from users where name=(?)', (vars(name)["user"],))
            num = database.cell()
            # Run if a matching name was found.
            if num!=None:
                status_time = self.convert_time(int(time.time())-num)
                if status_time!=False:
                    logging.info("Processing string...")
                    logging.info(name)
                    uname = vars(name)["user"]
                    database.cursor.execute('SELECT status from users where name=(?)', (uname,))
                    status = database.cell()
                    logging.info(f'{uname} {status} {status_time}')
                    return(f'{uname} has been {status} for {status_time}.')
            if num==None:
                logging.error(f'{vars(name)["user"]} was not found within the database!')
        except Exception as e:
            logging.error("Exception occured.")
            logging.error(f"{e}")
            return False
