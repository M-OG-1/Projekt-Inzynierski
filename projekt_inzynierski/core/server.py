from flask import Flask

class AppServer(Flask):
    def __init__(self, import_name: str):
        super().__init__(import_name)

        @self.route("/")
        def root_route():
            return "test"