# coding=utf-8
from blackdogosint.utils.database.db import *
from blackdogosint.utils.database.tabelas.proxy import ProxyTable
data=[i for i in range(100000000000000000000)]

def populate_database():
    session = session_factory()
    for item in data:
        ed_user = ProxyTable(proxy_address='{}'.format(item))

        # Let's add the user and its addresses we've created to the DB and commit.
        session.add(ed_user)
        session.commit()
        session.close()

        # Now let's query the user that has the e-mail address ed@google.com
        # SQLAlchemy will construct a JOIN query automatically.






populate_database()
