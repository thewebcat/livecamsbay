# coding=utf-8
"""
Пакет: Авторизации

Основной функционал:
 -- регистрация
 -- активация пользователя по ссылке
 -- авторизация
 -- восстановление пароля
 -- возможность быстрого переключения между пользователями(при DEBUG=True)

Дополнительные файлы добавленные в пакет:
cms_app.py - нужен для django cms
cms_toolbar.py - нужен для django cms toolbar, чтобы править Meta теги с клиентской стороны.
tasks.py - задания для celery. Функция sent_email при регистрации нового пользователя, отправляет письмо с инструкцией для активациии
"""