from .views import (index_bp, add_note_bp, login_bp, auth_bp,
                    register_bp, logout_bp, edit_note_bp, request_reset_form_bp,
                    delete_note_bp, note_detail_bp, about_bp, profile_bp,
                    reset_password_form_bp)
from .views.api import edit_profile_bp, check_data_bp, request_reset_password_bp, reset_password_bp, registrate_bp, confirm_email_bp

def register_routes(app):
    # Главная
    app.register_blueprint(index_bp)
    # Вход через Google
    app.register_blueprint(auth_bp)
    # Вход по логину и паролю
    app.register_blueprint(login_bp)
    # Форма регистрации по логину и паролю
    app.register_blueprint(register_bp)
    # Профиль
    app.register_blueprint(profile_bp)
    # Добавление записи
    app.register_blueprint(add_note_bp)
    # Просмотр записи
    app.register_blueprint(note_detail_bp)
    # Редактирование записи
    app.register_blueprint(edit_note_bp)
    # Удаление записи
    app.register_blueprint(delete_note_bp)
    # Выход
    app.register_blueprint(logout_bp)
    # Раздел "О нас"
    app.register_blueprint(about_bp)
    # Форма для восстановления пароля
    app.register_blueprint(request_reset_form_bp)
    # Регистрация пользователя
    app.register_blueprint(registrate_bp)


    # api
    # Редактировать профиль
    app.register_blueprint(edit_profile_bp)
    # Валидация регистрации
    app.register_blueprint(check_data_bp)
    # Запрос на смену пароля и отправка сообщения на email
    app.register_blueprint(request_reset_password_bp)
    # Смена пароля
    app.register_blueprint(reset_password_bp)
    # Восстановить пароль
    app.register_blueprint(reset_password_form_bp)
    # Подтверждение email при регистрации
    app.register_blueprint(confirm_email_bp)
