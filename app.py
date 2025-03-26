from flask import Flask

app = Flask(__name__)

# Импорт маршрутов после создания app чтобы избежать circular import
from structures.views import *

if __name__ == '__main__':
    app.run(debug=True)