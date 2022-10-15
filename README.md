# api_sp1_bot
Telegram-бот, который обращается к API сервиса Яндекс.Практикум.Домашка и узнавет статус отправленной домашней работы: взята ли домашняя работа в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.
# Install
1. Клонировать проект
```Python
git clone https://github.com/ZakonGyka/api_sp1_botgit.git
```
2. Создать новое вертуальное окружение
```Python
python -m venv env
```
3. Устноавить зависимости
```Python
pip install -r /path/to/requirements.txt
```
4. Запускить приложение
```Python
pip manage.py runserver
```
# Requirements
+ cryptography==3.3.2
+ python-dotenv==0.13.0
+ python-telegram-bot==12.7
