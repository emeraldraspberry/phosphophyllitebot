import logging
import io
import time
import sqlite3
import argparse
import datetime
import shlex

class Database():
    def __init__(self):
        # Establish connection to database.
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY)')

    def cell(self):
        row = self.cursor.fetchone()
        if row==None:
            return None
        if type(row[0])==str:
            cell = row[0]
            return cell
        cell = int(row[0])
        return cell

    def update(self, member):
        self.cursor.execute('SELECT EXISTS(SELECT 1 FROM users WHERE id=(?))', (member.id,))
        flag = self.cell()
        # Create new record if primary key doesn't exist.
        if flag==0:
            self.cursor.execute("INSERT INTO users VALUES (?,?,?,?)",
            (member.id, member.name, str(member.status), int(time.time())))
            self.connection.commit()
            self.cursor.execute("SELECT status_time FROM users WHERE id=(?)", (member.id,))
            logging.info(f'Creating new record: id={member.id} name={member.name} status={member.status} status_time={self.cell()}')
        # Update record by the primary key.
        else:
            self.cursor.execute('SELECT name from users where id=(?)', (member.id,))
            db_name = self.cell()
            logging.info(f'{db_name} {member.name}')
            if str(db_name)!=str(member.name):
                self.cursor.execute('UPDATE users SET name=(?) WHERE id=(?)', (member.name, member.id))
                self.connection.commit()
                logging.info(f'Updating {member.id}: old_name={db_name} new_name={member.name}')
            else:
                self.cursor.execute('SELECT status FROM users WHERE id=(?)', (member.id,))
                db_status = self.cell()
                logging.info(f'name: {member.name} db_status: {db_status} member.status{member.status}')
                # Only update if status has changed compared to database
                if str(db_status)!=str(member.status):
                    self.cursor.execute('UPDATE users SET name=(?), status=(?), status_time=(?) WHERE id=(?)',
                    (member.name, str(member.status), int(time.time()), member.id))
                    self.connection.commit()
                    self.cursor.execute("SELECT status_time FROM users WHERE id=(?)", (member.id,))
                    logging.info(f'Updating {member.id}: name={member.name} status={member.status} status_time={self.cell()}')
