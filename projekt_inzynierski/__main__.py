from .core.server import AppServer
from .core.database import DatabaseAccess
from .core.util import check_password, new_user

server = AppServer("projekt", ".")

server.run()


# db = DatabaseAccess("test.db")
# new_user("test", "helllooo", 0, db)
# print(check_password("test", "helllooo", db))
#
#
# db.commit()
# db.close()
