import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import time
import warnings

warnings.filterwarnings('ignore')

# Настройка стиля графиков
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def load_data():
    """Загрузка данных из OpenML"""
    with st.spinner("🔄 Загрузка данных... Это может занять 10-20 секунд"):
        try:
            data = fetch_openml(data_id=42876, as_frame=True, parser='auto')
            df = data.frame
            st.success(f"✅ Данные успешно загружены! {df.shape[0]} записей, {df.shape[1]} признаков")
            return df
        except Exception as e:
            st.error(f"❌ Ошибка загрузки: {e}")
            return None


def preprocess_data(df):
    """Предобработка данных"""
    with st.expander("🔧 Детали предобработки", expanded=False):
        st.write("**Шаг 1:** Копирование данных")
        data = df.copy()

        st.write("**Шаг 2:** Обработка datetime признаков")
        # Преобразование datetime
        data['DateTimeOfAccident'] = pd.to_datetime(data['DateTimeOfAccident'])
        data['DateReported'] = pd.to_datetime(data['DateReported'])

        # Создание новых признаков
        data['AccidentMonth'] = data['DateTimeOfAccident'].dt.month
        data['AccidentDayOfWeek'] = data['DateTimeOfAccident'].dt.dayofweek
        data['AccidentYear'] = data['DateTimeOfAccident'].dt.year
        data['ReportingDelay'] = (data['DateReported'] - data['DateTimeOfAccident']).dt.days

        st.write(
            f"  - Диапазон задержки отчетности: {data['ReportingDelay'].min()} - {data['ReportingDelay'].max()} дней")

        # Удаление исходных datetime
        data = data.drop(columns=['DateTimeOfAccident', 'DateReported'])

        st.write("**Шаг 3:** Кодирование категориальных признаков")
        label_encoders = {}
        categorical_columns = ['Gender', 'MaritalStatus', 'PartTimeFullTime', 'ClaimDescription']

        for col in categorical_columns:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col].astype(str))
            label_encoders[col] = le
            st.write(f"  - {col}: {len(le.classes_)} уникальных значений")

        st.write("**Шаг 4:** Проверка пропусков")
        missing = data.isnull().sum().sum()
        st.write(f"  - Всего пропусков: {missing}")

        st.write("**Шаг 5:** Проверка выбросов")
        negative_target = (data['UltimateIncurredClaimCost'] < 0).sum()
        st.write(f"  - Отрицательных значений в целевой переменной: {negative_target}")

        if negative_target > 0:
            data = data[data['UltimateIncurredClaimCost'] >= 0]
            st.write(f"  - Удалено {negative_target} записей с отрицательной ценой")

        return data


def scale_features(data, numerical_features):
    """Масштабирование числовых признаков"""
    scaler = StandardScaler()
    data[numerical_features] = scaler.fit_transform(data[numerical_features])
    return data, scaler


def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """Обучение и оценка моделей"""

    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(alpha=1.0, random_state=42),
        'Random Forest': RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1
        ),
        'XGBoost': XGBRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42,
            verbosity=0
        )
    }

    results = {}
    trained_models = {}

    progress_bar = st.progress(0)
    for i, (name, model) in enumerate(models.items()):
        with st.spinner(f"🔄 Обучение {name}..."):
            # Обучение
            start_time = time.time()
            model.fit(X_train, y_train)
            train_time = time.time() - start_time

            # Предсказание
            y_pred = model.predict(X_test)

            # Метрики
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)

            # Кросс-валидация
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')

            results[name] = {
                'MAE': mae,
                'RMSE': rmse,
                'R2': r2,
                'CV_R2_mean': cv_scores.mean(),
                'CV_R2_std': cv_scores.std(),
                'Train_Time': train_time,
                'Predictions': y_pred
            }

            trained_models[name] = model

        progress_bar.progress((i + 1) / len(models))

    return results, trained_models


def plot_results(y_test, y_pred_dict, model_name):
    """Построение графиков результатов"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # График 1: Предсказания vs Реальные значения
    ax1 = axes[0, 0]
    ax1.scatter(y_test, y_pred_dict[model_name], alpha=0.3, s=10)
    ax1.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    ax1.set_xlabel('Реальные значения ($)')
    ax1.set_ylabel('Предсказанные значения ($)')
    ax1.set_title(f'{model_name}: Предсказания vs Реальные')
    ax1.grid(True, alpha=0.3)

    # График 2: Распределение ошибок
    ax2 = axes[0, 1]
    errors = y_test - y_pred_dict[model_name]
    ax2.hist(errors, bins=50, edgecolor='black', alpha=0.7)
    ax2.axvline(x=0, color='r', linestyle='--', lw=2)
    ax2.set_xlabel('Ошибка предсказания ($)')
    ax2.set_ylabel('Частота')
    ax2.set_title('Распределение ошибок')
    ax2.grid(True, alpha=0.3)

    # График 3: Сравнение распределений
    ax3 = axes[1, 0]
    ax3.hist(y_test, bins=50, alpha=0.5, label='Реальные', color='blue', density=True)
    ax3.hist(y_pred_dict[model_name], bins=50, alpha=0.5, label='Предсказанные', color='red', density=True)
    ax3.set_xlabel('Цена ($)')
    ax3.set_ylabel('Плотность')
    ax3.set_title('Распределение реальных и предсказанных цен')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # График 4: Остатки vs Предсказанные
    ax4 = axes[1, 1]
    ax4.scatter(y_pred_dict[model_name], errors, alpha=0.3, s=10)
    ax4.axhline(y=0, color='r', linestyle='--', lw=2)
    ax4.set_xlabel('Предсказанные значения ($)')
    ax4.set_ylabel('Остатки ($)')
    ax4.set_title('Остатки vs Предсказанные')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_feature_importance(model, feature_names, model_name):
    """Построение графика важности признаков"""
    if hasattr(model, 'feature_importances_'):
        importance = model.feature_importances_
    elif hasattr(model, 'coef_'):
        importance = np.abs(model.coef_)
    else:
        return None

    # Создаем DataFrame
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': importance
    }).sort_values('importance', ascending=True)

    # Берем топ-15
    top_15 = feature_importance.tail(15)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(top_15['feature'], top_15['importance'])
    ax.set_xlabel('Важность')
    ax.set_title(f'{model_name}: Топ-15 важных признаков')
    ax.grid(True, alpha=0.3, axis='x')

    return fig, feature_importance


def analysis_and_model_page():
    st.title("📊 Анализ данных и прогнозирование")
    st.markdown("---")

    # Боковая панель управления
    with st.sidebar:
        st.header("🎮 Управление")

        if st.button("📥 Загрузить данные", use_container_width=True):
            df = load_data()
            if df is not None:
                st.session_state['df'] = df

        if st.session_state['df'] is not None:
            if st.button("🔄 Обработать и обучить модели", use_container_width=True, type="primary"):
                with st.spinner("🔄 Обработка данных..."):
                    # Предобработка
                    data = preprocess_data(st.session_state['df'])

                    # Масштабирование
                    numerical_features = ['Age', 'DependentChildren', 'DependentsOther',
                                          'WeeklyPay', 'HoursWorkedPerWeek', 'DaysWorkedPerWeek',
                                          'InitialCaseEstimate', 'AccidentMonth', 'AccidentDayOfWeek',
                                          'AccidentYear', 'ReportingDelay']

                    data, scaler = scale_features(data, numerical_features)

                    # Разделение данных
                    X = data.drop(columns=['UltimateIncurredClaimCost'])
                    y = data['UltimateIncurredClaimCost']

                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y, test_size=0.2, random_state=42
                    )

                    st.session_state['X_train'] = X_train
                    st.session_state['X_test'] = X_test
                    st.session_state['y_train'] = y_train
                    st.session_state['y_test'] = y_test
                    st.session_state['feature_names'] = X.columns.tolist()

                    st.success(f"✅ Данные подготовлены! Train: {X_train.shape}, Test: {X_test.shape}")

                    # Обучение моделей
                    results, models = train_and_evaluate_models(X_train, X_test, y_train, y_test)

                    st.session_state['results'] = results
                    st.session_state['models'] = models

                    st.success("✅ Модели обучены!")

    # Основной контент
    if st.session_state['df'] is None:
        st.info("👈 Нажмите **'Загрузить данные'** в боковой панели для начала работы")

        # Превью датасета
        st.subheader("📋 О датасете")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Записей", "100,000", "≈ 100к")
        with col2:
            st.metric("Признаков", "14", "после обработки +4")
        with col3:
            st.metric("Целевая", "UltimateIncurredClaimCost", "до $3M")

        st.markdown("""
        ### 🏥 Workers Compensation Dataset

        Датасет содержит информацию о страховых случаях компенсации работникам:

        **Признаки:**
        - 👤 **Демография**: возраст, пол, семейное положение, дети
        - 💰 **Финансы**: еженедельная зарплата, начальная оценка случая
        - 📅 **Время**: дата происшествия, дата отчета
        - 📝 **Описание**: тип травмы, характер занятости

        **Целевая переменная:** `UltimateIncurredClaimCost` - итоговая стоимость страхового возмещения
        """)

    else:
        # Вкладки для организации контента
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Данные",
            "📈 Визуализация",
            "🤖 Модели",
            "🔮 Предсказание"
        ])

        with tab1:
            st.subheader("Загруженные данные")
            st.dataframe(st.session_state['df'].head(100), use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Информация о данных")
                buffer = st.session_state['df'].info(buf=None)
                st.text(f"Размер: {st.session_state['df'].shape}")
                st.text(f"Типы данных:\n{st.session_state['df'].dtypes.value_counts()}")

            with col2:
                st.subheader("Статистика")
                st.dataframe(st.session_state['df'].describe(), use_container_width=True)

        with tab2:
            if 'X_train' in st.session_state:
                st.subheader("Визуализация данных")

                chart_type = st.selectbox(
                    "Выберите тип графика",
                    ["Распределение целевой переменной",
                     "Корреляционная матрица",
                     "Зависимость от зарплаты",
                     "Зависимость от возраста"]
                )

                fig, ax = plt.subplots(figsize=(10, 6))

                if chart_type == "Распределение целевой переменной":
                    ax.hist(st.session_state['y_train'], bins=50, edgecolor='black', alpha=0.7)
                    ax.set_xlabel('Итоговая стоимость ($)')
                    ax.set_ylabel('Частота')
                    ax.set_title('Распределение UltimateIncurredClaimCost')
                    ax.grid(True, alpha=0.3)

                elif chart_type == "Корреляционная матрица":
                    # Берем выборку для корреляции
                    df_sample = st.session_state['X_train'].select_dtypes(include=[np.number]).iloc[:5000]
                    df_sample['Target'] = st.session_state['y_train'].iloc[:5000]
                    corr = df_sample.corr()
                    sns.heatmap(corr, annot=False, cmap='coolwarm', ax=ax)
                    ax.set_title('Корреляционная матрица')

                elif chart_type == "Зависимость от зарплаты":
                    ax.scatter(
                        st.session_state['X_train']['WeeklyPay'].iloc[:5000],
                        st.session_state['y_train'].iloc[:5000],
                        alpha=0.3, s=5
                    )
                    ax.set_xlabel('Еженедельная зарплата ($)')
                    ax.set_ylabel('Итоговая стоимость ($)')
                    ax.set_title('Зависимость от зарплаты')
                    ax.grid(True, alpha=0.3)

                elif chart_type == "Зависимость от возраста":
                    ax.scatter(
                        st.session_state['X_train']['Age'].iloc[:5000],
                        st.session_state['y_train'].iloc[:5000],
                        alpha=0.3, s=5
                    )
                    ax.set_xlabel('Возраст')
                    ax.set_ylabel('Итоговая стоимость ($)')
                    ax.set_title('Зависимость от возраста')
                    ax.grid(True, alpha=0.3)

                st.pyplot(fig)
                plt.close()
            else:
                st.info("Сначала обучите модели для визуализации")

        with tab3:
            if 'results' in st.session_state:
                st.subheader("📊 Результаты моделей")

                # Таблица с результатами
                results_df = pd.DataFrame(st.session_state['results']).T
                st.dataframe(
                    results_df[['MAE', 'RMSE', 'R2', 'CV_R2_mean', 'Train_Time']].round(4),
                    use_container_width=True
                )

                # Выбор лучшей модели
                best_model = results_df['R2'].idxmax()
                st.success(f"🏆 Лучшая модель: **{best_model}** с R² = {results_df.loc[best_model, 'R2']:.4f}")

                # Графики для выбранной модели
                st.subheader("Графики для лучшей модели")

                col1, col2 = st.columns(2)
                with col1:
                    selected_model = st.selectbox(
                        "Выберите модель для визуализации",
                        list(st.session_state['results'].keys())
                    )

                with col2:
                    show_importance = st.checkbox("Показать важность признаков", value=True)

                # Графики предсказаний
                fig = plot_results(
                    st.session_state['y_test'],
                    {name: res['Predictions'] for name, res in st.session_state['results'].items()},
                    selected_model
                )
                st.pyplot(fig)
                plt.close()

                # Важность признаков
                if show_importance and selected_model in st.session_state['models']:
                    model = st.session_state['models'][selected_model]
                    fig_imp, imp_df = plot_feature_importance(
                        model,
                        st.session_state['feature_names'],
                        selected_model
                    )
                    if fig_imp:
                        st.pyplot(fig_imp)
                        plt.close()

                        st.subheader("Топ-10 важных признаков")
                        st.dataframe(
                            imp_df.sort_values('importance', ascending=False).head(10),
                            use_container_width=True
                        )
            else:
                st.info("Обучите модели для просмотра результатов")

        with tab4:
            st.subheader("🔮 Предсказание стоимости для нового случая")

            if 'models' in st.session_state and 'X_train' in st.session_state:
                with st.form("prediction_form"):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        age = st.number_input("Возраст", min_value=18, max_value=80, value=35)
                        gender = st.selectbox("Пол", ["M", "F"])
                        marital = st.selectbox("Семейное положение", ["Single", "Married", "Divorced", "Widowed"])
                        children = st.number_input("Количество детей", min_value=0, max_value=10, value=0)

                    with col2:
                        dependents = st.number_input("Другие иждивенцы", min_value=0, max_value=10, value=0)
                        weekly_pay = st.number_input("Еженедельная зарплата ($)", min_value=0, value=800)
                        employment = st.selectbox("Тип занятости", ["Full Time", "Part Time"])
                        hours_week = st.number_input("Часов в неделю", min_value=0, max_value=80, value=40)

                    with col3:
                        days_week = st.number_input("Дней в неделю", min_value=0, max_value=7, value=5)
                        claim_desc = st.selectbox(
                            "Описание случая",
                            ["Back injury", "Fall", "Repetitive strain", "Accident", "Other"]
                        )
                        initial_estimate = st.number_input("Начальная оценка ($)", min_value=0, value=5000)
                        delay = st.number_input("Задержка отчетности (дни)", min_value=0, value=2)

                    # Дополнительные параметры
                    with st.expander("📅 Дополнительные параметры"):
                        accident_month = st.slider("Месяц происшествия", 1, 12, 6)
                        accident_day = st.slider("День недели", 0, 6, 2)
                        accident_year = st.slider("Год", 2010, 2024, 2023)

                    submitted = st.form_submit_button("🚀 Предсказать стоимость", use_container_width=True)

                    if submitted:
                        # Создаем DataFrame с введенными данными
                        input_data = pd.DataFrame([{
                            'Age': age,
                            'Gender': 0 if gender == 'M' else 1,
                            'MaritalStatus': ['Single', 'Married', 'Divorced', 'Widowed'].index(marital),
                            'DependentChildren': children,
                            'DependentsOther': dependents,
                            'WeeklyPay': weekly_pay,
                            'PartTimeFullTime': 0 if employment == 'Full Time' else 1,
                            'HoursWorkedPerWeek': hours_week,
                            'DaysWorkedPerWeek': days_week,
                            'ClaimDescription': ['Back injury', 'Fall', 'Repetitive strain', 'Accident', 'Other'].index(
                                claim_desc),
                            'InitialCaseEstimate': initial_estimate,
                            'AccidentMonth': accident_month,
                            'AccidentDayOfWeek': accident_day,
                            'AccidentYear': accident_year,
                            'ReportingDelay': delay
                        }])

                        # Убеждаемся, что колонки в правильном порядке
                        input_data = input_data[st.session_state['feature_names']]

                        st.markdown("---")
                        st.subheader("📊 Результаты предсказания")

                        # Предсказания от всех моделей
                        cols = st.columns(len(st.session_state['models']))

                        for idx, (name, model) in enumerate(st.session_state['models'].items()):
                            with cols[idx]:
                                pred = model.predict(input_data)[0]

                                # Стилизованный вывод
                                st.markdown(f"""
                                <div style="
                                    padding: 10px;
                                    border-radius: 10px;
                                    background-color: #f0f2f6;
                                    text-align: center;
                                    margin: 5px;
                                ">
                                    <h4>{name}</h4>
                                    <h2 style="color: #0066cc;">${pred:,.0f}</h2>
                                    <p style="color: #666;">R²: {st.session_state['results'][name]['R2']:.3f}</p>
                                </div>
                                """, unsafe_allow_html=True)

                        # Среднее предсказание
                        avg_pred = np.mean([
                            model.predict(input_data)[0]
                            for model in st.session_state['models'].values()
                        ])

                        st.markdown(f"""
                        <div style="
                            padding: 20px;
                            border-radius: 10px;
                            background-color: #e8f4fd;
                            text-align: center;
                            margin-top: 20px;
                            border: 2px solid #0066cc;
                        ">
                            <h3>📈 Среднее предсказание всех моделей</h3>
                            <h1 style="color: #0066cc; font-size: 48px;">${avg_pred:,.0f}</h1>
                        </div>
                        """, unsafe_allow_html=True)

            else:
                st.warning("⚠️ Сначала загрузите данные и обучите модели!")


# Запуск страницы
analysis_and_model_page()