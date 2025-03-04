from sqladmin import ModelView

from app.bookings.models import Bookings
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]    # столбцы которые отображаются на главной странице
    column_details_exclude_list = [Users.hashed_password]    # не показывает пароль в просмотре
    can_delete = False    # запрет на удаление через админку
    name = "Пользователь"    # имя модели в админке
    name_plural = "Пользователи"    # имя модели в админке
    icon = "fa-solid fa-user"    # иконка

class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user]    # отобразить все столбцы
    name = "Бронь"    # имя модели в админке
    name_plural = "Брони"    # имя модели в админке