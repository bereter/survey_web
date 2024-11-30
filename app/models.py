from app.db import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import DateTime, TIMESTAMP, ForeignKey, String
from datetime import datetime, timezone


class Admin(Base):
    __tablename__ = 'admins'

    username: Mapped[str]
    password: Mapped[str]
    user_email: Mapped[str] = mapped_column(unique=True)
    datetime: Mapped[DateTime] = mapped_column(TIMESTAMP, default=datetime.now())
    verification_email: Mapped[bool] = mapped_column(default=False)

    questionnaires: Mapped[list['Questionnaire']] = relationship(back_populates='admin')


    def __str__(self):
        return f'{self.__class__.__name__} (id={self.id}, username={self.username})'

    def __repr__(self):
        return str(self)


class Questionnaire(Base):
    __tablename__ = 'questionnaires'

    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str]
    date_start: Mapped[datetime] = mapped_column(default=datetime.now())
    date_end: Mapped[datetime] = mapped_column(nullable=True)
    user: Mapped[int | None]

    questions: Mapped[list['Question']] = relationship(back_populates='questionnaire')

    admin_id: Mapped[int] = mapped_column(ForeignKey('admins.id', ondelete='CASCADE'))
    admin: Mapped['Admin'] = relationship(back_populates='questionnaires')

    def __str__(self):
        return f'{self.__class__.__name__} (id={self.id}, title={self.title}, admin={self.admin.username})'

    def __repr__(self):
        return str(self)


class Question(Base):
    __tablename__ = 'questions'

    question_text: Mapped[str]
    question_type: Mapped[str] = mapped_column(String(2))
    user_answer_text: Mapped[str | None]

    questionnaire_id: Mapped[int] = mapped_column(ForeignKey('questionnaires.id', ondelete='CASCADE'))
    questionnaire: Mapped['Questionnaire'] = relationship(back_populates='questions')

    admin_answer_list: Mapped[list['AnswerAdmin']] = relationship(back_populates='question_admin')
    user_answer_list: Mapped[list['AnswerUser']] = relationship(back_populates='question_user')

    def __str__(self):
        return f'{self.__class__.__name__} (id={self.id}, questionnaire={self.questionnaire.title})'

    def __repr__(self):
        return str(self)


class AnswerAdmin(Base):
    __tablename__ = 'answers_admins'

    text: Mapped[str]

    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id', ondelete='CASCADE'))
    question_admin: Mapped['Question'] = relationship(back_populates='admin_answer_list')

    def __str__(self):
        return f'{self.__class__.__name__} (question_id={self.question_id})'

    def __repr__(self):
        return str(self)


class AnswerUser(Base):
    __tablename__ = 'answers_users'

    text: Mapped[str]

    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id', ondelete='CASCADE'))
    question_user: Mapped['Question'] = relationship(back_populates='user_answer_list')

    def __str__(self):
        return f'{self.__class__.__name__} (question_id={self.question_id})'

    def __repr__(self):
        return str(self)

