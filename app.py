import streamlit as st

# Настройка страницы
st.set_page_config(
    page_title="Workers Compensation Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Инициализация состояния сессии
if 'df' not in st.session_state:
    st.session_state['df'] = None
if 'models' not in st.session_state:
    st.session_state['models'] = {}
if 'metrics' not in st.session_state:
    st.session_state['metrics'] = {}
if 'feature_importance' not in st.session_state:
    st.session_state['feature_importance'] = None
if 'X_test' not in st.session_state:
    st.session_state['X_test'] = None
if 'y_test' not in st.session_state:
    st.session_state['y_test'] = None

# Создание страниц
page1 = st.Page(
    "analysis_and_model.py",
    title="Анализ данных и обучение модели",
    icon="📊",
    default=True
)

page2 = st.Page(
    "presentation.py",
    title="Презентация проекта",
    icon="📝"
)

# Навигация (исправлено - передаем список страниц)
pg = st.navigation([page1, page2], position="sidebar")

# Боковая панель с информацией
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/insurance.png", width=80)
    st.title("🏥 Workers Comp")
    st.markdown("---")
    st.markdown("### О проекте")
    st.info(
        "Предсказание итоговой стоимости страховых выплат "
        "на основе характеристик работника и начальной оценки случая."
    )
    st.markdown("---")
    st.markdown("### Разработчик")

    # Поля для ввода информации о студенте
    name = st.text_input("ФИО", value="", placeholder="Иванов Иван Иванович")
    group = st.text_input("Группа", value="", placeholder="ИВТ-201")

    st.markdown(f"**Дата:** 2026")

    # Индикатор загрузки данных
    if st.session_state['df'] is not None:
        st.success("✅ Данные загружены")
        st.write(f"Записей: {st.session_state['df'].shape[0]:,}")
        st.write(f"Признаков: {st.session_state['df'].shape[1]}")
    else:
        st.warning("⏳ Данные не загружены")
        st.info("Перейдите на страницу 'Анализ и модель' для загрузки")

    st.markdown("---")
    st.caption("© 2026 | Финальный проект")

# Запуск выбранной страницы
pg.run()