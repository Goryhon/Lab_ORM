from config import db
from app import app  # Добавляем импорт приложения
from sqlalchemy import func

class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Страна', db.String(100), nullable=False)
    cities = db.relationship("City", back_populates="country", cascade='all, delete')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'id: {self.id}, Страна: {self.name}'


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('Город', db.String(100))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship("Country", back_populates="cities")
    buildings = db.relationship("Building", back_populates="city", cascade='all, delete')

    def __init__(self, name, country_id):
        self.name = name
        self.country_id = country_id

    def __repr__(self):
        return f'id: {self.id}, Город: {self.name}, country_id: {self.country_id}'


class TypeBuilding(db.Model):
    __tablename__ = 'type_building'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('Тип', db.String(50), nullable=False)
    buildings = db.relationship("Building", back_populates="type_building", cascade='all, delete')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'id: {self.id}, Тип: {self.name}'


class Building(db.Model):
    __tablename__ = 'building'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column('Название', db.String(200))
    type_building_id = db.Column(db.Integer, db.ForeignKey('type_building.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    year = db.Column(db.Integer)
    height = db.Column(db.Integer)
    type_building = db.relationship("TypeBuilding", back_populates="buildings")
    city = db.relationship("City", back_populates="buildings")

    def __init__(self, title, type_building_id, city_id, year, height):
        self.title = title
        self.type_building_id = type_building_id
        self.city_id = city_id
        self.year = year
        self.height = height

    def __repr__(self):
        return f'id: {self.id}, Здание: {self.title}, type_building_id: {self.type_building_id}, city_id: {self.city_id}, Год: {self.year}, Высота: {self.height}'


def get_all_buildings():
    """
    Функция для получения всех зданий с связанными данными
    Возвращает:
    - список заголовков столбцов
    - список кортежей с данными о зданиях
    """
    query = (
        db.session.query(
            Building.title.label("Здание"),
            TypeBuilding.name.label("Тип"),
            Country.name.label("Страна"),
            City.name.label("Город"),
            Building.year.label("Год"),
            Building.height.label("Высота (м)")
        )
        .select_from(Building)
        .join(TypeBuilding)
        .join(City)
        .join(Country)
        .order_by(Building.height.desc())
    )
    return [query.statement.columns.keys(), query.all()]

def get_buildings_by_type():
    query = (
        db.session.query(
            TypeBuilding.name.label("Тип здания"),
            func.count(Building.id).label("Количество"),
            func.max(Building.height).label("Максимальная высота"),
            func.min(Building.height).label("Минимальная высота"),
            func.round(func.avg(Building.height), 1).label("Средняя высота")
        )
        .join(Building, TypeBuilding.id == Building.type_building_id)
        .group_by(TypeBuilding.name)
        .order_by(func.count(Building.id).desc())
    )
    return [query.statement.columns.keys(), query.all()]

def get_buildings_by_country():
    query = (
        db.session.query(
            Country.name.label("Страна"),
            func.count(Building.id).label("Количество"),
            func.max(Building.height).label("Максимальная высота"),
            func.min(Building.height).label("Минимальная высота"),
            func.round(func.avg(Building.height), 1).label("Средняя высота")
        )
        .join(City, Building.city_id == City.id)
        .join(Country, City.country_id == Country.id)
        .group_by(Country.name)
        .order_by(func.max(Building.height).desc())
    )
    return query.all()

def get_buildings_by_year():
    return (
        db.session.query(
            Building.year.label("Год"),
            func.count(Building.id).label("Количество"),
            func.max(Building.height).label("Максимальная_высота"),
            func.min(Building.height).label("Минимальная_высота"),
            func.round(func.avg(Building.height), 1).label("Средняя_высота")
        )
        .group_by(Building.year)
        .order_by(Building.year)
        .all()
    )


def get_buildings_by_year_range(start_year, end_year):
    results = (
        db.session.query(
            Building.title.label("Название"),
            TypeBuilding.name.label("Тип"),
            Country.name.label("Страна"),
            City.name.label("Город"),
            Building.year,
            Building.height
        )
        .join(TypeBuilding)
        .join(City)
        .join(Country)
        .filter(Building.year.between(start_year, end_year))
        .order_by(Building.year)
        .all()
    )

    # Преобразуем в список словарей с правильными ключами
    return [{
        "Название": r[0],
        "Тип": r[1],
        "Страна": r[2],
        "Город": r[3],
        "Год": r[4],
        "Высота": r[5]
    } for r in results]

# Создание таблиц (если они ещё не созданы)
with app.app_context():
    db.create_all()