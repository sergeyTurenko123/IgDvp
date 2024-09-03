У консолі команд:
docker-compose up - запуск служб, визначених у файлі docker-compose.yml.
alembic revision --autogenerate -m 'Init' - створюємо міграцію.
alembic upgrade head - застосуємо створену міграцію
створіть файл .env та додайте свої данні
DB_URL: str = 
SECRET_KEY_JWT: str = 
ALGORITHM: str = 
MAIL_USERNAME: EmailStr = 
MAIL_PASSWORD: str = "
MAIL_PORT: int = 
MAIL_SERVER: str = "postgress"
REDIS_DOMAIN: str = 'localhost'
REDIS_PORT: int = 
REDIS_PASSWORD: str | None = None
CLD_NAME: str = '
CLD_API_KEY: int = 
CLD_API_SECRET: str = "secret"
uvicorn main:app --host localhost --reload - запуск FastAPI.

В браузері:
http://127.0.0.1:8000/docs
Проходите аутентіфікацію та підтверджуєте свій ємейл. 
Авторезуєтесь. Перший користувач є адмін. 
Адмін має право визначити модератора.
Користувачі можуть добавляти світлини з описом та тегами.
Користувачі можуть виконувати базові операції з сервісу cloudinary з випадаючого списку
Користувачі можуть створювати посилання на трансформоване зображення для перегляду світлини в вигляді URL та QR-code
Користувачі можуть добавляти коментарії до світлин. Адмін може видаляти.
Незареєстрований користувач може продивитися ці світлини.
