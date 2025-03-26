from app import app
from flask import render_template
from models import *

@app.route('/')
def index():
    [buildings_head, buildings_body] = get_all_buildings()
    return render_template(
        'index.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body,
        title="Самые высокие здания и сооружения"
    )


@app.route('/building-stats')
def building_stats():
    headers, data = get_buildings_by_type()

    # Преобразуем в список словарей для удобства работы в шаблоне
    buildings = []
    for row in data:
        buildings.append({
            "Тип_здания": row[0],
            "Количество": row[1],
            "Максимальная_высота": row[2],
            "Минимальная_высота": row[3],
            "Средняя_высота": row[4]
        })

    return render_template(
        'building_stats.html',
        title='Статистика по типам зданий',
        headers=headers,
        buildings=buildings
    )


@app.route('/country-stats')
def country_stats():
    stats = get_buildings_by_country()
    headers = ["Страна", "Количество", "Максимальная высота", "Минимальная высота", "Средняя высота"]

    return render_template(
        'country_stats.html',
        headers=headers,
        stats=stats
    )


@app.route('/year-stats')
def year_stats():
    stats = get_buildings_by_year()
    headers = ["Год", "Количество", "Максимальная высота", "Минимальная высота", "Средняя высота"]

    return render_template(
        'year_stats.html',
        headers=headers,
        stats=stats,
        title="Статистика по годам"
    )


@app.route('/buildings-by-years')
def buildings_by_years():
    start_year = 2000
    end_year = 2018

    buildings = get_buildings_by_year_range(start_year, end_year)
    headers = ["Название", "Тип", "Страна", "Город", "Год", "Высота (м)"]

    return render_template(
        'buildings_by_years.html',
        headers=headers,
        buildings=buildings,
        title=f"Здания {start_year}-{end_year} годов",
        start_year=start_year,
        end_year=end_year
    )