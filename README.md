# 🏥 Прогнозирование стоимости страховых выплат

## 📋 Описание проекта

Разработка модели машинного обучения для предсказания итоговой стоимости страхового возмещения (UltimateIncurredClaimCost) на основе характеристик работника и начальной оценки случая.

**Датасет:** Workers Compensation (OpenML ID: 42876)
- 100,000 записей
- 14 признаков
- Целевая переменная: UltimateIncurredClaimCost

## 🚀 Функционал

- 📊 Загрузка и анализ данных
- 🔧 Предобработка (datetime, кодирование, масштабирование)
- 🤖 Обучение 4 моделей (Linear Regression, Ridge, Random Forest, XGBoost)
- 📈 Визуализация результатов
- 🔮 Интерактивное предсказание для новых случаев
- 🎯 Презентация проекта

Демонстрация функционала доступна по ссылке:
https://disk.yandex.ru/i/YJ1zYev3cnRyQw

## 🛠️ Установка и запуск

```bash
# Клонирование репозитория
git clone https://github.com/dekstop4/DigitalKAIFinalWork
cd workers_compensation_project

# Установка зависимостей
pip install -r requirements.txt

# Запуск приложения
streamlit run app.py
