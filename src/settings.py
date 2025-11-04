# src/settings.py
# Минимально: загрузка .env и чтение двух переменных с простым парсингом bool.

from dotenv import load_dotenv #импорт функции, которая читает пары ключ=значение из файла .env
import os # модуль для работы с переменными окружения.

TRUE_SET = ("1", "true", "yes", "y", "on")

def load_settings():
    # 1) загрузить переменные из .env (если файл есть)
    load_dotenv()

    # 2) прочитать из окружения
    credentials = os.getenv("GIGACHAT_CREDENTIALS")
    verify_ssl = os.getenv("GIGACHAT_VERIFY_SSL_CERTS", "True").strip().lower() in TRUE_SET
    #Берём строку из окружения (или "True" по умолчани)
    #Приводим к нижнему регистру(lover) и убираем пробелы(strip).
    #Сравниваем со списком “истинных” значений. В итоге получаем булево:

    return credentials, verify_ssl