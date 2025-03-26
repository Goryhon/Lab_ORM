from app import app
from config import db
from models import TypeBuilding

# Добавляем контекст приложения
with app.app_context():
    # Добавление типов зданий
    building_types = [
        'Антенная мачта',
        'Бетонная башня',
        'Радиомачта',
        'Гиперболоидная башня',
        'Дымовая труба',
        'Решётчатая мачта',
        'Башня',
        'Мост'
    ]

    for bt in building_types:
        item = TypeBuilding(name=bt)
        db.session.add(item)

    db.session.commit()
    print("Типы зданий успешно добавлены!")

    # Пример чтения данных (можно раскомментировать)
    # query = TypeBuilding.query.all()
    # print(query)