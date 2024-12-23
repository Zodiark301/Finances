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
            date_str = request.form.get('date')
            gross_income = float(request.form.get('gross_income'))
            net_income = float(request.form.get('net_income'))
            extra_income = float(request.form.get('extra_income'))
            cash_income = float(request.form.get('cash_income'))
            car_wash_expenses = float(request.form.get('car_wash_expenses'))
            # total = float(request.form.get('total'))

            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

            new_work_day = WorkDay(
                date=date_obj,
                gross_income=gross_income,
                net_income=net_income,
                extra_income=extra_income,
                cash_income=cash_income,
                car_wash_expenses=car_wash_expenses,
                # total=total
            )

            db.session.add(new_work_day)
            db.session.commit()

            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})

    work_days = WorkDay.query.order_by(WorkDay.date).all()
    return render_template('work_days.html', work_days=work_days)


@app.route('/work_days/<int:id>', methods=['PUT', 'DELETE'])
def modify_work_day(id):
    try:
        work_day = WorkDay.query.get(id)

        if not work_day:
            return jsonify({'status': 'error', 'message': 'Запись не найдена'}), 404

        if request.method == 'PUT':
            data = request.json
            work_day.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            work_day.gross_income = float(data['gross_income'])
            work_day.net_income = float(data['net_income'])
            work_day.extra_income = float(data['extra_income'])
            work_day.cash_income = float(data['cash_income'])
            work_day.car_wash_expenses = float(data['car_wash_expenses'])
            work_day.total = float(data['total'])
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Запись успешно обновлена'})

        elif request.method == 'DELETE':
            db.session.delete(work_day)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Запись успешно удалена'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
