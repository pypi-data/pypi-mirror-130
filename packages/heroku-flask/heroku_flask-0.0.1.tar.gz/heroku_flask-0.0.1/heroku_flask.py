"""

Created by abhimanyu at 07/12/21

"""
import platform

APP_CONTENT = """from flask import Flask

app = Flask(__name__)


@app.route("/")
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"
"""

WSGI_CONTENT = """from app import app

if __name__ == "__main__":
    app.run()
"""


class FlaskSetup:

    def create(self):
        self.create_procfile()
        self.create_runtime()
        self.create_app()
        self.create_wsgi()

    def create_app(self):
        content = """from flask import Flask
        app = Flask(__name__)
        
        @app.route("/")
        def home_view():
            return "<h1>Welcome to Geeks for Geeks</h1>"
        """
        self.create_file("app.py", APP_CONTENT)

    def create_wsgi(self):
        content = """from app.main import app
        
        if __name__ == "__main__":
            app.run()
        """
        self.create_file("wsgi.py", WSGI_CONTENT)

    def create_procfile(self):
        self.create_file("Procfile", "web: gunicorn wsgi:app")

    def create_runtime(self):
        self.create_file("runtime.txt", "python-{}".format(platform.python_version()))

    @staticmethod
    def create_file(file_name, content):
        print(f"Creating {file_name}", end="\r")
        temp_file = open(file_name, "w")
        temp_file.write(content)
        temp_file.close()
        print(f"Created {file_name}")


if __name__ == "__main__":
    FlaskSetup().create()
