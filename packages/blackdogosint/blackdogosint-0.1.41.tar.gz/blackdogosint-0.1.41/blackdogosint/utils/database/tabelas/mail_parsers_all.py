# coding=utf-8

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from blackdogosint.utils.database.db import Base


class MaiParses(Base):
    __tablename__ = "mail_parses"

    id = Column(Integer, primary_key=True)
    mail_parses = Column(String)

    def __init__(self, mail_parses):
        self.mail_parses = mail_parses
