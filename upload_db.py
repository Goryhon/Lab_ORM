from app import app
from config import db
from models import Country, City, Building
import csv


def country_upload():
    with open("data/country.csv", encoding='windows-1251') as f:  # Изменили кодировку
        reader = csv.reader(f)
        next(reader)  # Пропускаем заголовок
        for item in reader:
            new_entry = Country(name=item[0])
            db.session.add(new_entry)
        db.session.commit()
    print("Данные стран успешно загружены!")


def city_upload():
    with open("data/city.csv", encoding='windows-1251') as f:  # Изменили кодировку
        reader = csv.reader(f)
        next(reader)
        for item in reader:
            new_entry = City(name=item[0], country_id=int(item[1]))
            db.session.add(new_entry)
        db.session.commit()
    print("Данные городов успешно загружены!")


def building_upload():
    with open("data/building.csv", encoding='windows-1251') as f:  # Изменили кодировку
        reader = csv.reader(f)
        next(reader)
        for item in reader:
            height = float(item[4]) if '.' in item[4] else int(item[4])
            new_entry = Building(
                title=item[0],
                type_building_id=int(item[1]),
                city_id=int(item[2]),
                year=int(item[3]),
                height=height
            )
            db.session.add(new_entry)
        db.session.commit()
    print("Данные зданий успешно загружены!")


if __name__ == '__main__':
    with app.app_context():
        # Создаем таблицы (если они ещё не созданы)
        db.create_all()

        # Загружаем данные (можно раскомментировать нужные)
        country_upload()
        city_upload()
        building_upload()

        # Проверка
        print("Страны:", Country.query.count())
        print("Города:", City.query.count())
        print("Здания:", Building.query.count())