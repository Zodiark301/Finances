from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WorkDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный ID для каждой записи
    date = db.Column(db.Date, nullable=False)  # Дата работы
    gross_income = db.Column(db.Float, nullable=False, default=0.0)  # Грязные деньги
    net_income = db.Column(db.Float, nullable=False, default=0.0)  # Чистый заработок
    extra_income = db.Column(db.Float, nullable=False, default=0.0)  # Левак (дополнительный заработок)
    cash_income = db.Column(db.Float, nullable=False, default=0.0)  # Наличные за день
    car_wash_expenses = db.Column(db.Float, nullable=False, default=0.0)  # Расходы на мойку
    total = db.Column(db.Float, nullable=False, default=0.0)  # Итог за день
