# Проект приложение для анализа банковских транзакций

## Описание:
Приложение для анализа транзакций, которые находятся в Excel-файле. В приложении генерируется JSON-данные для веб-страниц, формировать Excel-отчеты, а также предоставлять другие сервисы.

## Структура проекта
1. src\utils.py - модуль с функциями для чтения и обработки полученных данных. 
2. src\views.pу - модуль с функцией для формирования JSON-файла
3. src\reports.py - модуль, в котором реализована функция сортировки трат по категории 
4. src\services.pу - модуль, в котором реализован простой поиск по слову


## Зависимости
1. python = "^3.12"
2. requests = "^2.32.3"
3. python-dotenv = "^1.0.1"
4. pandas = "^2.2.3"
5. openpyxl = "^3.1.5"

## Тестирование
Было проведено тестирование всех функций и было покрыто 84%

### Важное:
[Skypro](https://my.sky.pro)
