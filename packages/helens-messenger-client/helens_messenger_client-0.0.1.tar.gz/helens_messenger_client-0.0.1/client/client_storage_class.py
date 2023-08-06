"""
Модуль класса базы данных клиента
"""

import datetime

from sqlalchemy import Column, create_engine, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import default_comparator


class ClientStorage:
    """
    Класс базы данных клиента
    """

    Base = declarative_base()

    class KnownUsers(Base):
        """
        Класс таблицы известных пользователей
        """
        __tablename__ = 'known_users'
        id = Column(Integer, primary_key=True)
        username = Column(String)

    class MessageHistory(Base):
        """
        Класс таблицы истории сообщений
        """
        __tablename__ = 'message_history'
        id = Column(Integer, primary_key=True)
        destination = Column(String)
        user = Column(String)
        message = Column(Text)
        date = Column(DateTime)

    class Contacts(Base):
        """
        Класс таблицы контактов пользователя
        """
        __tablename__ = 'contacts'
        id = Column(Integer, primary_key=True)
        name = Column(String)

    def __init__(self, username):
        """
        Метод инициализации. Создаётся объект движка базы данных, таблицы в базе данных
        на базе описанных классов таблиц, объект сессии. Очищается таблица контактов.
        """
        self.username = username
        self.engine = create_engine(f'sqlite:///client_{username}.db3', echo=False, pool_recycle=7200,
                                    connect_args={'check_same_thread': False})
        self.Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        self.session.query(self.Contacts).delete()
        self.session.commit()

    def add_contact(self, contact):
        """
        Метод добавления контакта
        """
        if not self.session.query(self.Contacts).filter_by(name=contact).count():
            contact_row = self.Contacts(name=contact)
            self.session.add(contact_row)
            self.session.commit()

    def del_contact(self, contact):
        """
        Метод удаления контакта
        """
        self.session.query(self.Contacts).filter_by(name=contact).delete()

    def add_users(self, users_list):
        """
        Метод добавления пользователя
        """
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            user_row = self.KnownUsers(username=user)
            self.session.add(user_row)
        self.session.commit()

    def save_message(self, destination, user, message):
        """
        Метод сохранения сообщения
        """
        message_row = self.MessageHistory(
            destination=destination,
            user=user,
            message=message,
            date=datetime.datetime.now()
        )
        self.session.add(message_row)
        self.session.commit()

    def get_contacts(self):
        """
        Метод получения списка контактов пользователя
        """
        return [contact[0] for contact in self.session.query(self.Contacts.name).all()]

    def get_users(self):
        """
        Метод получения списка известных пользователей
        """
        return [user[0] for user in self.session.query(self.KnownUsers.username).all()]

    def check_user(self, user):
        """
        Метод проверки существования пользователя в таблице известных пользователей
        """
        if self.session.query(self.KnownUsers).filter_by(username=user).count():
            return True
        else:
            return False

    def check_contact(self, contact):
        """
        Метод проверки существования контакта в таблице контактов
        """
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:
            return False

    def get_user_history(self, user):
        """
        Метод получения истории сообщений с пользователем
        """
        query = self.session.query(self.MessageHistory).filter_by(user=user)
        return [(history_row.user, history_row.destination, history_row.message, history_row.date)
                for history_row in query.all()]

    def contacts_clear(self):
        """
        Метод очищения таблицы контактов
        """
        self.session.query(self.Contacts).delete()
