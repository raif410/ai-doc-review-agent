from gigachat import GigaChat #импорт клиента SDK GigaChat.
from .settings import load_settings

def main() -> None:
    credentials, verify_ssl = load_settings()

    if not credentials:
        print("Не найден GIGACHAT_CREDENTIALS. Укажите его в .env или переменных окружения.")
        return

    #Инициализирует клиента GigaChat, передавая ваши авторизационные данные и флаг проверки SSL.
    with GigaChat(credentials=credentials, verify_ssl_certs=verify_ssl) as giga:
        response = giga.chat("Как мне сравнить документацию с точки зрения аналитика, сопровождения, безопастности, архитектуры?")
        print(response.choices[0].message.content)

if __name__ == "__main__":
    main()