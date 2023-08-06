import socket
import sys
import threading
import pickle
import sqlite3
import os
import importlib.resources as importlib_resources

from bin.user import User
from bin.event import Event
from bin.group import Group
from bin._calendar import GroupCalendar
from bin.option import Option
from bin.message import Message


# TODO: Use CamelCase for class names


# TODO: Implementing compression on blobs may be needed if object sizes become large.
# TODO: Remove traceback from exception handlers before release. Useful for testing right now.  Logging instead?
# TODO: Change tables to use primary keys and possibly relationships between object types.
# TODO: Specify object type/name in message header so we don't have to unpickle in Receiver thread.
# TODO: Pass info from header to generic methods that interact with database, instead of separate methods for each type. 
#       For easier maintenance, the different classes for adding objects could be combined into a single class.
# TODO: Create methods for cases where the local database is recieveing an update to information
# TODO: Exists function

class Data(threading.local):
    """
    Using name as primary key, stores serialized class objects as blobs (Binary Large Objects) in a sqlite3 database.

    Each method uses a new database connection because sqlite throws an error if a single connection is accessed by more
    than one thread.

    For testing, each client instance has to opened from its own directory so that they are each using their own
    database file.
    """
    with importlib_resources.path("bin", "circles.ui") as p:
        path = p
    path = os.path.dirname(path)
    DB_FILENAME = str(path) + "/db.db"  # Constant for database filename.
    update_UI = False

    # Method to create tables if they don't already exist in file.
    @staticmethod
    def create_tables():
        try:
            db_connection = sqlite3.connect(Data.DB_FILENAME)
            cursor = db_connection.cursor()
            # Wrapping identifiers in `` prevents conflicts with SQLite keywords i.e. GROUP
            cursor.execute('''CREATE TABLE `users` (`name` TEXT, `user` BLOB)''')
            cursor.execute('''CREATE TABLE `events` (`name` TEXT, `group` TEXT, `event` BLOB)''')
            cursor.execute('''CREATE TABLE `groups` (`name` TEXT, `group` BLOB)''')
            cursor.execute('''CREATE TABLE `calendars` (`name` TEXT, `calendar` BLOB)''')
            cursor.execute('''CREATE TABLE `options` (`name` TEXT, `option` BLOB)''')
            cursor.execute('''CREATE TABLE `messages` (`name` TEXT, `group` TEXT, `message` BLOB)''')
            db_connection.commit()
            db_connection.close()
        except Exception as e:
            print(e)

    # Deletes database file. Useful if corrupted.
    @staticmethod
    def db_reset():
        try:
            os.remove(Data.DB_FILENAME)  # Dangerous :)
            Data.create_tables()
        except Exception as e:
            print(e.with_traceback())

    # Requests a copy of database from server.  Fulfilled by other clients.
    @staticmethod
    def db_request():
        sender = Client.Send(bytes(), 2)  # Second parameter specifies fifth byte in message header
        sender.start()
        print("Request for db sent from new client")

    # Replaces local database using file received from server.
    @staticmethod
    def db_reload(db):
        Data.db_reset()
        try:
            with open(Data.DB_FILENAME, "wb") as file:  # Write bytes back to file
                file.write(db)
        except Exception as e:
            print(e.with_traceback())

    # Sends db file to server when Receiver thread gets request.
    @staticmethod
    def db_send():
        print("Sending db to server.")
        try:
            with open(Data.DB_FILENAME, "rb") as file:
                db_file = file.read()
                sender = Client.Send(db_file, 1)
                sender.start()
        except Exception as e:
            print(e)

    # Adds an object to database if it doesn't exist.
    @staticmethod
    def add_user(user):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()
            if Data.get_users(user.name) is None:
                cursor.execute("INSERT INTO `users` VALUES (?, ?)", (user.name, pickle.dumps(user)))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(user))
                sender.start()
            db_connection.close()
        except Exception as e:
            print(e.with_traceback())  # Can't have duplicate name.

    # Updates users by replacing it with passed class object
    @staticmethod
    def update_user(user):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()
            if Data.get_users(user.name) is None:
                print("Does not exist")
            # Only perform update if new object is different from current object.
            elif user != Data.get_users(user.name):
                cursor.execute("UPDATE `users` SET user = ? WHERE name = ?", (pickle.dumps(user), user.name))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(Data.get_users(user.name)), 4)
                sender.start()
            db_connection.close()
        except:
            pass  # Can't have duplicate name.

    # Deletes user based on primary key. Parameter is not a full user object.
    @staticmethod
    def delete_user(user):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()
            if Data.get_users(user.name).name == user.name:
                cursor.execute("DELETE FROM `users` WHERE name = ?", (user.name,))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(user), 5)
                sender.start()
            db_connection.close()
        except Exception as e:  # Fails when object doesn't exist because it won't have name attribute for comparison.
            pass

    # Returns User object if parameter is given, otherwise returns list of all users
    # Returns None if nothing is found.
    @staticmethod
    def get_users(name=None):
        try:
            if name is None:
                db_connection = sqlite3.connect(Data().DB_FILENAME)
                cursor = db_connection.cursor()
                cursor.execute("SELECT `user` FROM `users`")
                users = cursor.fetchall()  # fetchall() returns a list of rows returned from executed SQL query 
                db_connection.commit()
                db_connection.close()

                # Unpickle each object into new list to return.
                unpickled_users = []
                for user in users:
                    # Attributes for each row returned by fetchall() are accessed through a tuple.
                    # We are only selecting for one attribute (the pickled object), so we access with user[0]
                    unpickled_users.append(pickle.loads(user[0]))
                return unpickled_users

            else:
                db_connection = sqlite3.connect(Data().DB_FILENAME)
                cursor = db_connection.cursor()
                cursor.execute("SELECT `user` FROM `users` WHERE `name`=?", (name,))  # Parameter must be tuple
                user = cursor.fetchone()  # Returns None if nothing found, otherwise one object in a tuple.
                db_connection.commit()
                db_connection.close()
                # TODO: This if statement is not working correctly.  Handled with exception for now
                if user is not None:
                    user = pickle.loads(user[0])  # Get object out of tuple and pickle before returning.
                return user
        except Exception as e:
            return None

    # Adds an object to database if it doesn't exist.
    @staticmethod
    def add_event(event):
        #try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()
            if Data.get_events(event.name, event.group) is None:
                cursor.execute("INSERT INTO `events` VALUES (?, ?, ?)", (event.name, event.group, pickle.dumps(event)))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(event))
                sender.start()
            db_connection.close()
        #except Exception as e:
            #print(e.with_traceback())  # Can't have duplicate name.

    # deletes event based on primary key.
    @staticmethod
    def delete_event(event):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()
            if Data.get_events(event.name, event.group) is None:
                pass
            else:
                cursor.execute("DELETE FROM `events` WHERE `name` = ? and `group` = ?", (event.name, event.group))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(event), 5)
                sender.start()
            db_connection.close()
        except Exception as e:
            print(e.with_traceback())  # Can't have duplicate name.

    # Updates events by replacing it with passed class object
    @staticmethod
    def update_event(event):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()
            if Data.get_events(event.name, event.group) is None:
                pass
            elif event != Data.get_events(event.name, event.group):
                cursor.execute("UPDATE `events` SET event = ? WHERE `name` = ? and `group` = ?", (pickle.dumps(event), event.name, event.group))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(Data.get_events(event.name, event.group)), 4)
                sender.start()
            db_connection.close()
        except Exception as e:
            print(e.with_traceback())  # Can't have duplicate name.

    # Returns User object if parameter is given, otherwise returns list of all events
    # Returns None if nothing is found.
    @staticmethod
    def get_events(name=None, group=None):
        try:
            if name is None and group is None:
                db_connection = sqlite3.connect(Data().DB_FILENAME)
                cursor = db_connection.cursor()
                cursor.execute("SELECT `event` FROM `events`")
                events = cursor.fetchall()  # fetchall() returns a list of rows returned from executed SQL query 
                db_connection.commit()
                db_connection.close()

                # Unpickle each object into new list to return.
                unpickled_events = []
                for event in events:
                    # Attributes for each row returned by fetchall() are accessed through a tuple.
                    # We are only selecting for one attribute (the pickled object), so we access with event[0]
                    unpickled_events.append(pickle.loads(event[0]))
                return unpickled_events

            elif name is None and group is not None:
                db_connection = sqlite3.connect(Data().DB_FILENAME)
                cursor = db_connection.cursor()
                cursor.execute("SELECT `event` FROM `events` WHERE `group` = ?" ,(group,))
                events = cursor.fetchall()  # fetchall() returns a list of rows returned from executed SQL query
                db_connection.commit()
                db_connection.close()

                # Unpickle each object into new list to return.
                unpickled_events = []
                for event in events:
                    # Attributes for each row returned by fetchall() are accessed through a tuple.
                    # We are only selecting for one attribute (the pickled object), so we access with event[0]
                    unpickled_events.append(pickle.loads(event[0]))
                return unpickled_events

            else:
                db_connection = sqlite3.connect(Data().DB_FILENAME)
                cursor = db_connection.cursor()
                cursor.execute("SELECT `event` FROM `events` WHERE `name`=? and `group`=?", (name,group))  # Parameter must be tuple
                event = cursor.fetchone()  # Returns None if nothing found, otherwise one object in a tuple.
                db_connection.commit()
                db_connection.close()
                # TODO: This if statement is not working correctly.  Handled with exception for now
                if event is not None:
                    event = pickle.loads(event[0])  # Get object out of tuple and pickle before returning.
                return event
        except Exception as e:
            return None

    # Adds an object to database if it doesn't exist.
    @staticmethod
    def add_group(group):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()
            if Data.get_groups(group.name) is None:
                cursor.execute("INSERT INTO `groups` VALUES (?, ?)", (group.name, pickle.dumps(group)))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(group))
                sender.start()
            db_connection.close()
        except Exception as e:
            print(e.with_traceback())  # Can't have duplicate name.

    # Updates group by replacing it with passed class object.
    @staticmethod
    def update_group(group):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()

            if Data.get_groups(group.name) is None:
                pass
            elif group != Data.get_groups(group.name):
                cursor.execute("UPDATE `groups` SET `group` = ? WHERE name = ?", (pickle.dumps(group), group.name))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(Data.get_groups(group.name)), 4)
                sender.start()

            db_connection.close()
        except Exception as e:
            print(e.with_traceback())  # Can't have duplicate name.

    # Deletes group based on primary key.
    @staticmethod
    def delete_group(group):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()

            if Data.get_groups(group.name) is None:
                pass
            elif group != Data.get_groups(group.name):
                cursor.execute("DELETE FROM `groups` WHERE name = ?", (group.name,))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(group), 5)
                sender.start()

            db_connection.close()
        except Exception as e:
            print(e.with_traceback())  # Can't have duplicate name.

    # Returns User object if parameter is given, otherwise returns list of all groups
    # Returns None if nothing is found.
    @staticmethod
    def get_groups(name=None):
        try:
            if name is None:
                db_connection = sqlite3.connect(Data().DB_FILENAME)
                cursor = db_connection.cursor()
                cursor.execute("SELECT `group` FROM `groups`")
                groups = cursor.fetchall()  # fetchall() returns a list of rows returned from executed SQL query 
                db_connection.commit()
                db_connection.close()

                # Unpickle each object into new list to return.
                unpickled_groups = []
                for group in groups:
                    # Attributes for each row returned by fetchall() are accessed through a tuple.
                    # We are only selecting for one attribute (the pickled object), so we access with group[0]
                    unpickled_groups.append(pickle.loads(group[0]))
                return unpickled_groups

            else:
                db_connection = sqlite3.connect(Data().DB_FILENAME)
                cursor = db_connection.cursor()
                cursor.execute("SELECT `group` FROM `groups` WHERE `name`=?", (name,))  # Parameter must be tuple
                group = cursor.fetchone()  # Returns None if nothing found, otherwise one object in a tuple.
                db_connection.commit()
                db_connection.close()
                # TODO: This if statement is not working correctly.  Handled with exception for now
                if group is not None:
                    group = pickle.loads(group[0])  # Get object out of tuple and pickle before returning.
                return group
        except Exception as e:
            return None

    # Adds an object to database if it doesn't exist.
    @staticmethod
    def add_calendar(calendar):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()
            if Data.get_calendars(calendar.name) is None:
                cursor.execute("INSERT INTO `calendars` VALUES (?, ?)", (calendar.name, pickle.dumps(calendar)))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(calendar))
                sender.start()
            db_connection.close()
        except Exception as e:
            print(e.with_traceback())  # Can't have duplicate name.

    # Returns User object if parameter is given, otherwise returns list of all calendars
    # Returns None if nothing is found.

    # updates calendar by replacing it with passed class object
    @staticmethod
    def update_calendar(calendar):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()

            if Data.get_calendars(calendar.name) is None:
                pass
            elif calendar != Data.get_calendars(calendar.name):
                cursor.execute("UPDATE `calendars` SET `calendar` = ? WHERE name = ?", (pickle.dumps(calendar), calendar.name))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(Data.get_calendars(calendar.name)), 4)
                sender.start()

            db_connection.close()
        except Exception as e:
            print(e.with_traceback())  # Can't have duplicate name.

    @staticmethod
    def get_calendars(name=None):
        try:
            if name is None:
                db_connection = sqlite3.connect(Data().DB_FILENAME)
                cursor = db_connection.cursor()
                cursor.execute("SELECT `calendar` FROM `calendars`")
                calendars = cursor.fetchall()  # fetchall() returns a list of rows returned from executed SQL query 
                db_connection.commit()
                db_connection.close()

                # Unpickle each object into new list to return.
                unpickled_calendars = []
                for calendar in calendars:
                    # Attributes for each row returned by fetchall() are accessed through a tuple.
                    # We are only selecting for one attribute (the pickled object), so we access with calendar[0]
                    unpickled_calendars.append(pickle.loads(calendar[0]))
                return unpickled_calendars

            else:
                db_connection = sqlite3.connect(Data().DB_FILENAME)
                cursor = db_connection.cursor()
                cursor.execute("SELECT `calendar` FROM `calendars` WHERE `name`=?", (name,))  # Parameter must be tuple
                calendar = cursor.fetchone()  # Returns None if nothing found, otherwise one object in a tuple.
                db_connection.commit()
                db_connection.close()
                # TODO: This if statement is not working correctly.  Handled with exception for now
                if calendar is not None:
                    calendar = pickle.loads(calendar[0])  # Get object out of tuple and pickle before returning.
                return calendar
        except Exception as e:
            return None

    # deletes calendar based on primary key
    @staticmethod
    def delete_calendar(calendar):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()

            if Data.get_calendars(calendar.name) is None:
                pass
            else:
                cursor.execute("DELETE FROM `calendars` WHERE name = ?", (calendar.name,))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(calendar), 5)
                sender.start()

            db_connection.close()
        except Exception as e:
            print(e.with_traceback())  # Can't have duplicate name.

    # Adds an object to database if it doesn't exist.
    @staticmethod
    def add_option(option):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()
            if Data.get_options(option.name) is None:
                cursor.execute("INSERT INTO `options` VALUES (?, ?)", (option.name, pickle.dumps(option)))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(option))
                sender.start()
            db_connection.close()
        except Exception as e:
            print(e.with_traceback())  # Can't have duplicate name.

    # Updates Option by replacing it with passed class object
    @staticmethod
    def update_option(option):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()

            if Data.get_options(option.name) is None:
                pass
            elif option != Data.get_options(option.name):
                cursor.execute("UPDATE `options` SET `option` = ? WHERE name = ?", (pickle.dumps(option), option.name))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(Data.get_options(option.name)), 4)
                sender.start()

            db_connection.close()
        except Exception as e:
            print(e.with_traceback())  # Can't have duplicate name.

    # Returns User object if parameter is given, otherwise returns list of all options
    # Returns None if nothing is found.
    @staticmethod
    def get_options(name=None):
        try:
            if name is None:
                db_connection = sqlite3.connect(Data().DB_FILENAME)
                cursor = db_connection.cursor()
                cursor.execute("SELECT `option` FROM `options`")
                options = cursor.fetchall()  # fetchall() returns a list of rows returned from executed SQL query 
                db_connection.commit()
                db_connection.close()

                # Unpickle each object into new list to return.
                unpickled_options = []
                for option in options:
                    # Attributes for each row returned by fetchall() are accessed through a tuple.
                    # We are only selecting for one attribute (the pickled object), so we access with option[0]
                    unpickled_options.append(pickle.loads(option[0]))
                return unpickled_options

            else:
                db_connection = sqlite3.connect(Data().DB_FILENAME)
                cursor = db_connection.cursor()
                cursor.execute("SELECT `option` FROM `options` WHERE `name`=?", (name,))  # Parameter must be tuple
                option = cursor.fetchone()  # Returns None if nothing found, otherwise one object in a tuple.
                db_connection.commit()
                db_connection.close()
                # TODO: This if statement is not working correctly.  Handled with exception for now
                if option is not None:
                    option = pickle.loads(option[0])  # Get object out of tuple and pickle before returning.
                return option
        except Exception as e:
            return None
    # deletes option based on primary key
    @staticmethod
    def delete_option(option):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()

            if Data.get_options(option.name) is None:
                pass
            else:
                cursor.execute("DELETE FROM `options` WHERE name = ?", (option.name,))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(option), 5)
                sender.start()

            db_connection.close()
        except Exception as e:
            print(e.with_traceback())  # Can't have duplicate name.

# Adds an object to database if it doesn't exist.
    @staticmethod
    def add_message(message):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()
            if Data.get_messages(message.name, message.group) is None:
                cursor.execute("INSERT INTO `messages` VALUES (?, ?, ?)", (message.name, message.group, pickle.dumps(message)))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(message))
                sender.start()
            db_connection.close()
        except Exception as e:
            print("# Can't have duplicate name.")
            print(e.with_traceback())  # Can't have duplicate name.

    # Updates message by replacing it with passed class object
    @staticmethod
    def update_message(message):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()
            
            if Data.get_messages(message.name) is None:
                pass
            elif message != Data.get_messages(message.name):
                cursor.execute("UPDATE `messages` SET `message` = ? WHERE name = ?", (pickle.dumps(message), message.name))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(Data.get_messages(message.name)), 4)
                sender.start()
                
            db_connection.close()
        except:
            pass  # Can't have duplicate name.

    # Deletes message based on primary key. Parameter is not a full message object.
    @staticmethod
    def delete_message(message):
        try:
            db_connection = sqlite3.connect(Data().DB_FILENAME)
            cursor = db_connection.cursor()

            if Data.get_messages(message.name) is None:
                pass
            else:
                cursor.execute("DELETE FROM `messages` WHERE name = ?", (message.name,))
                db_connection.commit()
                sender = Client.Send(pickle.dumps(message), 5)
                sender.start()

        except Exception as e:  # Fails when object doesn't exist because it won't have name attribute for comparison.
            pass

    # Returns Message object if parameter is given, otherwise returns list of all messages
    # Returns None if nothing is found.
    @staticmethod
    def get_messages(name=None, group=None):
        #try:
            if name is None and group is None:
                db_connection = sqlite3.connect(Data().DB_FILENAME)
                cursor = db_connection.cursor()
                cursor.execute("SELECT `message` FROM `messages`")
                messages = cursor.fetchall()  # fetchall() returns a list of rows returned from executed SQL query
                db_connection.commit()
                db_connection.close()

                # Unpickle each object into new list to return.
                unpickled_messages = []
                for message in messages:
                    # Attributes for each row returned by fetchall() are accessed through a tuple.
                    # We are only selecting for one attribute (the pickled object), so we access with user[0]
                    unpickled_messages.append(pickle.loads(message[0]))
                return unpickled_messages

            elif name is None and group is not None:
                db_connection = sqlite3.connect(Data().DB_FILENAME)
                cursor = db_connection.cursor()
                cursor.execute("SELECT `message` FROM `messages` WHERE `group` = ?", (group,))
                messages = cursor.fetchall()  # fetchall() returns a list of rows returned from executed SQL query
                db_connection.commit()
                db_connection.close()

                # Unpickle each object into new list to return.
                unpickled_messages = []
                for message in messages:
                    # Attributes for each row returned by fetchall() are accessed through a tuple.
                    # We are only selecting for one attribute (the pickled object), so we access with user[0]
                    unpickled_messages.append(pickle.loads(message[0]))
                return unpickled_messages
            elif name is not None and group is None:
                pass
            else:
                db_connection = sqlite3.connect(Data().DB_FILENAME)
                cursor = db_connection.cursor()
                cursor.execute("SELECT `message` FROM `messages` WHERE `name`=? AND `group` = ?", (name, group))  # Parameter must be tuple
                message = cursor.fetchone()  # Returns None if nothing found, otherwise one object in a tuple.
                db_connection.commit()
                db_connection.close()
                # TODO: This if statement is not working correctly.  Handled with exception for now
                if message is not None:
                    message = pickle.loads(message[0])  # Get object out of tuple and pickle before returning.
                return message
        #except Exception as e:
           # return None

class Receive(threading.Thread):
    """
    A class to create a thread and listen on socket passed as parameter.
    Parses the data type and calls appropriate Data method.
    """

    def __init__(self, sock):
        super().__init__(daemon=True)
        self._sock = sock

    # If a message is received from server, unpickle it.  Otherwise, keep listening until the connection is closed.
    def run(self):
        while True:
            try:
                length = int.from_bytes(self._sock.recv(4), "big")  # Get length of message from first 4 bytes
                msg_type = int.from_bytes(self._sock.recv(1), "big")
                msg = self._sock.recv(length)

                # Detect update msg_type and set flag in Data class so UI can be updated.
                if msg_type == 6:
                    print("update header detected.")
                    Data.update_UI = True
                    msg = None

                if msg_type == 2:
                    print("Request for database received")
                    Data.db_send()

                if msg_type == 1:
                    print("Fresh db received")
                    Data.db_reload(msg)

                if msg:
                    try:  # Parse for string commands received from server.
                        cmd = msg.decode()
                        #if cmd == "request_db()":  # Send db if requested
                        #    print("Request for database file received. Sending.")
                        #    Data.db_send()
                    except UnicodeDecodeError:
                        try:  # Try to unpickle if you can't decode
                            unpickled_message = pickle.loads(msg)
                            # Add received user to local db.
                            if type(unpickled_message) is User:
                                if msg_type == 4:
                                    Data.update_user(unpickled_message)
                                elif msg_type == 5:
                                    Data.delete_user(unpickled_message)
                                else:
                                    Data.add_user(unpickled_message)
                            elif type(unpickled_message) is Event:
                                if msg_type == 4:
                                    Data.update_event(unpickled_message)
                                elif msg_type == 5:
                                    Data.delete_event(unpickled_message)
                                else:
                                    Data.add_event(unpickled_message)
                            elif type(unpickled_message) is Group:
                                if msg_type == 4:
                                    Data.update_group(unpickled_message)
                                elif msg_type == 5:
                                    Data.delete_group(unpickled_message)
                                else:
                                    Data.add_group(unpickled_message)
                            elif type(unpickled_message) is GroupCalendar:
                                if msg_type == 4:
                                    Data.update_calendar(unpickled_message)
                                elif msg_type == 5:
                                    Data.delete_calendar(unpickled_message)
                                else:
                                    Data.add_calendar(unpickled_message)
                            elif type(unpickled_message) is Option:
                                if msg_type == 4:
                                    Data.update_option(unpickled_message)
                                elif msg_type == 5:
                                    Data.delete_option(unpickled_message)
                                else:
                                    Data.add_option(unpickled_message)
                            elif type(unpickled_message) is Message:
                                if msg_type == 4:
                                    Data.update_message(unpickled_message)
                                elif msg_type == 5:
                                    Data.delete_message(unpickled_message)
                                else:
                                    Data.add_message(unpickled_message)

                        except pickle.PickleError as e:
                            pass

            except OSError as e:  # Catch exception when loop trys to connect after program closes socket.
                print(e)
                break


# Client class calls listener thread to run perpetually and sender method as needed to send data.
# Changed so that connection is stored as class variable and can be accessed from other classes we define.
class Client(threading.Thread):
    sock = socket.socket()  # Store connection info outside of instances.

    def __init__(self, addr):
        super().__init__(daemon=True)
        self._address = addr
        Data()
        self.srv = socket.create_connection(self._address)
        self.rcv = Receive(self.srv)

    def run(self):
        with self.srv as srv:
            Client.sock = srv

            # Start Receive thread to listen for data from server.
            self.rcv.start()

            print("Connected to server: %s:%d\n" % self._address)

            # TODO: Delete or hide before release.
            # Create and send dummy class objects for testing.
            # If there are other clients connected, they should receive what is sent with their receive thread.
            selection = input()
            while selection != "exit()":
                if selection == "0":  # Deletes database and reinitializes.
                    Data.db_reset()
                """
                if selection == "-1010":
                    Data.delete_option(Option("Option1", "", "", votes=[]))
                if selection == "-10":
                    Data.update_option(Option("Option1", "newActivity1", "newlocation", votes=["newVote1", "newVote2"]))

                if selection == "-88":
                    Data.delete_calendar(GroupCalendar("Calendar1", ["Event1", "Event2"]))
                if selection == "-8":
                    Data.update_calendar(GroupCalendar("Calendar1", ["newEvent1", "newEvent2"]))

                if selection == "-66":
                    Data.delete_group(Group("Group1", "", ["", ""], ["", ""]))
                if selection == "-6":
                    Data.update_group(Group("Group1", "newCalendar1", ["newUser1", "newUser2"], ["newEvent1", "newEvent2"]))

                if selection == "-44":
                    Data.delete_event(Event(name="Event1", description="", options=["", ""]))
                if selection == "-4":
                    Data.update_event(Event(name="Event1", description="new Description1", options=["new Option1", "new Option2"], status=False))

                if selection == "-22":
                    Data.delete_user(User(name="User1"))

                if selection == "-2":
                    Data.update_user(User(name="User1", password="pw", constraints=["C", "C"], groups=["Group", "Group"]))

                if selection == "-1":  # Request database from server.
                    Data.db_request()

                elif selection == "0":  # Deletes database and reinitializes.
                    Data.db_reset()

                elif selection == "1":  # Add different users for testing
                    Data.add_user(User(name="User1", password="pw", constraints=["C1", "C2"], groups=["Group1", "Group2"]))
                elif selection == "11":
                    Data.add_user(User("User2", "pw", ["Constraint1", "Constraint2"], ["Group2"]))
                elif selection == "111":
                    Data.add_user(User("User3", "pw", ["Constraint12"], ["Group12", "Group22"]))

                elif selection == "2":  # Print users from local database
                    for user in Data().get_users():
                        print(user.name, user.constraints, user.groups)

                if selection == "3":  # Add different events for testing
                    Data.add_event(Event(name="Event1", description="Description1", options=["Option1", "Option2"], status=True))
                elif selection == "33":
                    Data.add_event(Event("Event2", "Description2", "no group2", ["Option11", "Option22"]))
                elif selection == "333":
                    Data.add_event(Event("Event3", "Description3", "no group3", ["Option111", "Option222"]))

                elif selection == "4":  # Print events from local database
                    for event in Data().get_events():
                        print(event.name, event.description, event.options, event.status)

                if selection == "5":  # Add different groups for testing
                    Data.add_group(Group("Group1", "Calendar1", ["User1", "User2"], ["Event1", "Event2"]))
                elif selection == "55":
                    Data.add_group(Group("Group2", "Calendar2", ["User11", "User22"], ["Event11", "Event22"]))
                elif selection == "555":
                    Data.add_group(Group("Group3", "Calendar3", ["User111", "User222"], ["Event111", "Event222"]))

                elif selection == "6":  # Print groups from local database
                    for group in Data().get_groups():
                        print(group.name, group.calendar, group.users, group.events)

                if selection == "7":  # Add different calendars for testing
                    Data.add_calendar(GroupCalendar("Calendar1", ["Event1", "Event2"]))
                elif selection == "77":
                    Data.add_calendar(GroupCalendar("Calendar2", ["Event11", "Event22"]))
                elif selection == "777":
                    Data.add_calendar(GroupCalendar("Calendar3", ["Event111", "Event222"]))

                elif selection == "8":  # Print calendars from local database
                    for calendar in Data().get_calendars():
                        print(calendar.name, calendar.events)

                if selection == "9":  # Add different options for testing
                    Data.add_option(Option("Option1", "Activity1", "location", votes=["Vote1", "Vote2"]))
                elif selection == "99":
                    Data.add_option(Option("Option2", "Activity2", ["Vote11", "Vote22"]))
                elif selection == "999":
                    Data.add_option(Option("Option3", "Activity3", ["Vote1111", "Vote2222"]))

                elif selection == "10":  # Print options from local database
                    for option in Data().get_options():
                        print(option.name, option.activity, option.time, option.chosen, option.votes)

                elif selection == "69":
                    #name, description, options=[], group="", status=False:
                    Data.add_event(Event("Event1", "description1", "options1", "group1"))
                    Data.add_event(Event("Event1", "description1", "options1", "group2"))
                    Data.add_event(Event("Event2", "description1", "options1", "group1"))
                    Data.add_event(Event("Event1", "description1", "options1", "group3"))
                    Data.add_event(Event("Event2", "description1", "options1", "group3"))
                    Data.add_event(Event("Event3", "description1", "options1", "group1"))
                    Data.add_event(Event("Event3", "description1", "options1", "group2"))
                    #Data.delete_message(Message("message5", "Hi rebecca I hate you", "Hazel", "RebeccaHaters"))
                    for event in Data().get_events(None, "group1"):
                        print(event.name, event.description, event.options, event.group)"""

                selection = input()

            Client.exit()

    @staticmethod
    def exit():
        ex = Client.Send("exit()", 3)  # Send exit command to server.
        ex.start()
        sys.exit(0)

    # Creates a thread to accept an object and then encode or pickle before sending to server, depending on object type.
    # Attaches a 4 byte header to the object that specifies size
    # If msg_type is added to header, let's server know to only request from newest connection

    class Send(threading.Thread):
        def __init__(self, obj, msg_type=0):
            super().__init__()
            self.obj = obj
            self.msg_type = msg_type
            print("msg_type: ", msg_type)

        def run(self):
            if self.msg_type == 2:
                Client.sock.sendall(bytes([0, 0, 0, 0, 2]))
            else:
                try:
                    if type(self.obj) is str:
                        self.obj = self.obj.encode()

                    self.attach_header()
                    Client.sock.sendall(self.obj)
                except Exception as e:
                    print(e)

        # Appends length of object being sent to beginning of it's byte string
        # Also adds a byte to specify if this is a database file.
        def attach_header(self):
            prefix = sys.getsizeof(self.obj)  # Get length of message so we can create header.
            prefix = prefix.to_bytes(4, "big")  # Convert length to bytes

            self.msg_type = bytes([self.msg_type])
            # Create bytearray to add header then convert back to bytes.
            self.obj = bytes(bytearray(prefix + self.msg_type + self.obj))




if __name__ == '__main__':
    # TODO: Make host IP configurable by user.
    address = ("localhost", 55557)
    client = Client(address)
    client.start()
    print("Client started.")
