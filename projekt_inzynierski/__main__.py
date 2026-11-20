from .core.config import config_instance
from .core.server import AppServer
from .core.database import DatabaseAccess
from .core.util import check_password, new_user

server = AppServer("projekt", ".")

server.run(host=config_instance["bind_address"], ssl_context=("cert.pem", "key.pem"))


# db = DatabaseAccess("test.db")
# new_user("test", "helllooo", 0, db)
# print(check_password("test", "helllooo", db))
#
#
# db.commit()
# db.close()
