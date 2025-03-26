from flask_sqlalchemy import SQLAlchemy
from app import app

# Создаем расширение
db = SQLAlchemy()

# Конфигурируем базу данных SQLite в папке instance приложения
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///structure.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем приложение с расширением
db.init_app(app)