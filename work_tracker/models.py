from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WorkDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    gross_income = db.Column(db.Float, nullable=False, default=0.0)  # Грязные деньги
    net_income = db.Column(db.Float, nullable=False, default=0.0)  # Чистый заработок (рассчитывается автоматически)
    extra_income = db.Column(db.Float, nullable=False, default=0.0)
    cash_income = db.Column(db.Float, nullable=False, default=0.0)
    car_wash_expenses = db.Column(db.Float, nullable=False, default=0.0)
    total = db.Column(db.Float, nullable=False, default=0.0)  # Итог за день
