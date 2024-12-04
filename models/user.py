from db import db
from werkzeug.security import generate_password_hash, check_password_hash

# Оголошуємо клас UserModel
class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    @staticmethod
    def create_user(username, password):
        # Хешування пароля
        hashed_password = generate_password_hash(password)
        # Створення нового користувача
        user = UserModel(username=username, password=hashed_password)
        # Додавання користувача в сесію
        db.session.add(user)
        # Підтвердження змін у базі даних
        db.session.commit()

    def check_password(self, password):
        # Перевірка пароля
        return check_password_hash(self.password, password)



