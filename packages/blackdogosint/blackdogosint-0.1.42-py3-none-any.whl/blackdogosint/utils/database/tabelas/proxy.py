# coding=utf-8

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from blackdogosint.utils.database.db import Base


class ProxyTable(Base):
    __tablename__ = "proxy_list"

    id = Column(Integer, primary_key=True)
    proxy_address = Column(String)

    def __init__(self, proxy_address):
        self.proxy_address = proxy_address
