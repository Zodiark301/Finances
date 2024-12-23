from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from models import db, WorkDay
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workdays.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

@app.route('/work_days', methods=['GET', 'POST'])
def work_days():
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            date_str = request.form.get('date')
            gross_income = float(request.form.get('gross_income', 0))
            extra_income = float(request.form.get('extra_income', 0))
            cash_income = float(request.form.get('cash_income', 0))
            car_wash_expenses = float(request.form.get('car_wash_expenses', 0))

            # Проверяем, что все поля корректны
            if not date_str:
                return jsonify({'status': 'error', 'message': 'Дата не указана'}), 400

            # Чистый заработок (40% от грязных денег)
            net_income = gross_income * 0.4

            # Скорректированные наличные (наличные - мойка)
            corrected_cash_income = cash_income - car_wash_expenses

            # Итоговый доход (чистый + левак)
            total = net_income + extra_income

            # Преобразуем дату из формата YYYY-MM-DD
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            new_work_day = WorkDay(
                date=date_obj,
                gross_income=gross_income,
                net_income=net_income,
                extra_income=extra_income,
                cash_income=corrected_cash_income,
                car_wash_expenses=car_wash_expenses,
                total=total
            )

            # Сохраняем запись в БД
            db.session.add(new_work_day)
            db.session.commit()

            return jsonify({'status': 'success'})
        except ValueError as e:
            return jsonify({'status': 'error', 'message': 'Некорректные данные: ' + str(e)})
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'Ошибка сервера: ' + str(e)}), 500

    # GET-запрос для отображения
    work_days = WorkDay.query.order_by(WorkDay.date).all()

    # Форматируем даты в нужный формат
    for work_day in work_days:
        work_day.formatted_date = work_day.date.strftime('%d.%m.%Y')

    return render_template('work_days.html', work_days=work_days)



@app.route('/work_days/<int:id>', methods=['PUT', 'DELETE'])
def modify_work_day(id):
    try:
        work_day = WorkDay.query.get(id)

        if not work_day:
            return jsonify({'status': 'error', 'message': 'Запись не найдена'}), 404

        if request.method == 'PUT':
            data = request.json

            # Обновляем только те поля, которые имеют смысл редактировать
            work_day.date = datetime.strptime(data.get('date', ''), '%d.%m.%Y').date()
            work_day.gross_income = float(data.get('gross_income', 0))
            work_day.extra_income = float(data.get('extra_income', 0))
            work_day.cash_income = float(data.get('cash_income', 0))  # Оригинальная сумма наличных
            work_day.car_wash_expenses = float(data.get('car_wash_expenses', 0))

            # Пересчёт чистого заработка (40% от грязного дохода)
            work_day.net_income = work_day.gross_income * 0.4

            # Пересчёт наличных с учётом мойки
            work_day.cash_income = work_day.cash_income - work_day.car_wash_expenses

            # Пересчёт итогового дохода (чистый + левак)
            work_day.total = work_day.net_income + work_day.extra_income

            # Сохраняем изменения
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Запись успешно обновлена'})

        if request.method == 'DELETE':
            db.session.delete(work_day)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Запись успешно удалена'})
    except ValueError as e:
        return jsonify({'status': 'error', 'message': 'Некорректные данные: ' + str(e)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Ошибка сервера: ' + str(e)}), 500

from sqlalchemy import func

@app.route('/work_days/summary', methods=['GET'])
def work_days_summary():
    try:
        # Используем агрегатные функции для получения итоговых значений
        summary = db.session.query(
            func.sum(WorkDay.gross_income).label('total_gross_income'),
            func.sum(WorkDay.net_income).label('total_net_income'),
            func.sum(WorkDay.extra_income).label('total_extra_income'),
            func.sum(WorkDay.cash_income).label('total_cash_income'),
            func.sum(WorkDay.car_wash_expenses).label('total_car_wash_expenses'),
            func.sum(WorkDay.total).label('total_total')  # Итоговый столбец
        ).first()

        # Возвращаем итоговые суммы для каждого столбца отдельно
        return jsonify({
            'total_gross_income': round(summary.total_gross_income or 0, 2),
            'total_net_income': round(summary.total_net_income or 0, 2),
            'total_extra_income': round(summary.total_extra_income or 0, 2),
            'total_cash_income': round(summary.total_cash_income or 0, 2),
            'total_car_wash_expenses': round(summary.total_car_wash_expenses or 0, 2),
            'total_total': round(summary.total_total or 0, 2)  # Итог по отдельному столбцу
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
