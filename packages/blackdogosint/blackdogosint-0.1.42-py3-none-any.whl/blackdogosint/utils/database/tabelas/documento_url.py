# coding=utf-8

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from blackdogosint.utils.database.db import Base


class DocumentUrls(Base):
    __tablename__ = "Documenturls_pdf"

    id = Column(Integer, primary_key=True)
    Documenturls = Column(String)

    def __init__(self, Documenturls):
        self.Documenturls = Documenturls
