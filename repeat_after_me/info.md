# Руководство: создание и запуск проекта с виртуальным окружением (Windows)

Ниже — пошаговая инструкция в Markdown, по которой любой сможет повторить ваш путь: от создания venv до запуска кода с разнесением по файлам.

#### Зачем виртуальное окружение
- Виртуальное окружение — это изолированная от системы среда с собственными пакетами.
- Зачем: чтобы не засорять глобальный Python и избежать конфликтов версий между проектами.

#### Предпосылки
- Установлен Python 3.10+ (в Windows обычно доступен через команду `py` или `python`).
- Терминал: PowerShell или CMD (Command Prompt). Команды активации для них разные.

---

#### Шаг 1. Создать виртуальное окружение
```bash
python -m venv .venv
```
- В проекте появится папка `.venv` с интерпретатором и скриптами.

#### Шаг 2. Активировать окружение
- PowerShell:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- CMD (Command Prompt):
  ```bat
  .venv\Scripts\activate.bat
  ```

После успешной активации в начале строки появится префикс вида `(.venv)`:
```
(.venv) PS C:\git\new>
```

---

#### Если возникла ошибка безопасности при активации (PowerShell)
Сообщение вида: «выполнение сценариев отключено... PSSecurityException».

1) Посмотреть текущие политики:
```powershell
Get-ExecutionPolicy -List
```
Часто вывод такой:
```
MachinePolicy    Undefined
UserPolicy       Undefined
Process          Undefined
CurrentUser      Undefined
LocalMachine     Undefined
```

2) Разрешить запуск локальных скриптов для текущего пользователя (рекомендуется):
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
- Это безопасный минимум для разработки.
- Перезапустите PowerShell и снова активируйте:
  ```
  .\.venv\Scripts\Activate.ps1
  ```

Альтернативы:
- Только на текущую сессию (сбросится при закрытии окна):
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
- Как вернуть, «как было» (убрать пользовательское переопределение):
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Undefined
  ```

3) Проверить, что политика применилась:
```powershell
Get-ExecutionPolicy -List
```
Ожидаемо:
```
MachinePolicy    Undefined
UserPolicy       Undefined
Process          Undefined
CurrentUser      RemoteSigned
LocalMachine     Undefined
```

4) Активировать окружение:
```powershell
.\.venv\Scripts\Activate.ps1
```

---

#### Проверка, что окружение активно
- По префиксу `(.venv)` в приглашении терминала.
- Дополнительно:
  - CMD:
    ```
    where python
    ```
  - PowerShell:
    ```
    Get-Command python
    ```
  - Универсально:
    ```
    python -c "import sys; print(sys.executable); print(sys.prefix); print(sys.base_prefix)"
    ```
    При активном venv `sys.prefix` указывает на путь к `.venv`, а `sys.base_prefix` — на базовый Python.

- Деактивация окружения:
  ```
  deactivate
  ```

---

#### Шаг 3. Установить зависимости
```bash
pip install gigachat python-dotenv
```
(Опционально обновить pip перед этим: `python -m pip install --upgrade pip`)

#### Шаг 4. Зафиксировать версии
Создать/перезаписать файл зависимостей:
```bash
pip freeze > requirements.txt
```

---

#### Шаг 5. Добавить .gitignore
Создайте `.gitignore` в корне проекта:
```
# виртуальные окружения
.venv/
venv/
env/

# кэш Python
__pycache__/
*.pyc

# локальные переменные окружения/секреты
.env
```
Примечание: файл `__init__.py` НЕ нужно добавлять в .gitignore — это часть исходников.

---

#### Шаг 6. Структура проекта
```
your_project/
  src/
    __init__.py      # делает src пакетом (может быть пустым)
    main.py
    settings.py
  .env               # локально, не коммитить
  .env.example       # можно коммитить (шаблон)
  requirements.txt
  .gitignore
  README.md
```

- `src/__init__.py` — пустой файл, который «пакетизирует» каталог `src`. Благодаря этому работают пакетные импорты и запуск через `python -m src.main`.

---

#### Шаг 7. Разнести код по файлам

Было (в одном файле):
```python
from dotenv import load_dotenv
import os
from gigachat import GigaChat

load_dotenv()

credentials = os.getenv("GIGACHAT_CREDENTIALS")
verify_ssl = os.getenv("GIGACHAT_VERIFY_SSL_CERTS", "True").strip().lower() in ("1", "true", "yes", "y")

with GigaChat(credentials=credentials, verify_ssl_certs=verify_ssl) as giga:
    response = giga.chat("Какие факторы влияют на стоимость страховки на дом?")
    print(response.choices[0].message.content)
```

Стало (разнесено):

- src/__init__.py
```python
# пустой файл
```

- src/settings.py
```python
# Минимально: загрузка .env и чтение двух переменных с простым парсингом bool.
from dotenv import load_dotenv  # читает пары ключ=значение из .env
import os

TRUE_SET = ("1", "true", "yes", "y", "on")

def load_settings():
    # 1) загрузить переменные из .env (если файл есть)
    load_dotenv()
    # 2) прочитать из окружения
    credentials = os.getenv("GIGACHAT_CREDENTIALS")
    verify_ssl = os.getenv("GIGACHAT_VERIFY_SSL_CERTS", "True").strip().lower() in TRUE_SET
    return credentials, verify_ssl
```

- src/main.py
```python
from gigachat import GigaChat
from .settings import load_settings

def main() -> None:
    credentials, verify_ssl = load_settings()

    if not credentials:
        print("Не найден GIGACHAT_CREDENTIALS. Укажите его в .env или переменных окружения.")
        return

    with GigaChat(credentials=credentials, verify_ssl_certs=verify_ssl) as giga:
        response = giga.chat("Какие факторы влияют на стоимость страховки на дом?")
        print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
```

- .env.example (шаблон, можно коммитить)
```env
GIGACHAT_CREDENTIALS=put-your-token-here
GIGACHAT_VERIFY_SSL_CERTS=True
# GIGACHAT_SCOPE=GIGACHAT_API_PERS
```

- .env (локально, не коммитить)
```env
GIGACHAT_CREDENTIALS="..."
GIGACHAT_VERIFY_SSL_CERTS=False
```

---

#### Шаг 8. Запуск
- Вариант А (предпочтительный для пакетной структуры):
  ```bash
  python -m src.main
  ```
- Вариант Б (как скрипт):
  ```bash
  python src/main.py
  ```

Если при запуске через `-m` увидите `ModuleNotFoundError: No module named 'settings'`, убедитесь, что:
- у вас есть файл `src/__init__.py`;
- импорт в `main.py` пакетный: `from .settings import load_settings` или `from src.settings import load_settings`;
- вы запускаете команду из корня проекта (там, где лежит папка `src`).

---

#### Полезные команды
- Установка зависимостей из файла:
  ```
  pip install -r requirements.txt
  ```
- Проверка активного Python:
  ```
  where python            # в CMD
  Get-Command python      # в PowerShell
  ```
- Проверка путей внутри Python:
  ```
  python -c "import sys; print(sys.executable); print(sys.prefix); print(sys.base_prefix)"
  ```
- Деактивация окружения:
  ```
  deactivate
  ```

---

#### Типичные проблемы и решения
- Ошибка безопасности в PowerShell (PSSecurityException):
  - Решение: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, затем `.\.venv\Scripts\Activate.ps1`.
- Окружение «не активно»:
  - Убедитесь, что активируете в корректной оболочке: PowerShell — `Activate.ps1`, CMD — `activate.bat`.
  - Проверьте префикс `(.venv)` или выполните проверочные команды из раздела «Проверка».
- `ModuleNotFoundError` при `python -m src.main`:
  - Добавить `src/__init__.py`; исправить импорт на `from .settings import load_settings`.
- Политики выполнения нужно вернуть «как было»:
  - `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Undefined` (или явное значение, например, `Restricted`).