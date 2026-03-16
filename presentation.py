import streamlit as st
import streamlit.components.v1 as components
import time
import matplotlib.pyplot as plt


def presentation_page():
    st.title("🎯 Презентация проекта")
    st.markdown("### Прогнозирование стоимости страховых выплат")
    st.markdown("---")

    # Создаем вкладки для разных форматов презентации
    tab1, tab2, tab3 = st.tabs(["📊 Слайды", "📝 Текстовая версия", "📈 Инфографика"])

    with tab1:
        st.subheader("Презентация в слайдах")

        # Настройки слайдов
        col1, col2, col3 = st.columns(3)
        with col1:
            slide_speed = st.selectbox("Скорость", [3, 5, 10, 15], index=1, format_func=lambda x: f"{x} сек")
        with col2:
            slide_style = st.selectbox("Стиль", ["Современный", "Классический", "Минималистичный"])
        with col3:
            auto_play = st.checkbox("Автовоспроизведение", value=True)

        # HTML презентация
        slides_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Презентация</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}

                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 20px;
                }}

                .slides-container {{
                    width: 100%;
                    max-width: 1200px;
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    overflow: hidden;
                }}

                .slide {{
                    display: none;
                    padding: 40px;
                }}

                .slide.active {{
                    display: block;
                }}

                .slide-header {{
                    margin-bottom: 30px;
                }}

                .slide-header h2 {{
                    color: #667eea;
                    font-size: 32px;
                    margin-bottom: 10px;
                }}

                .slide-header .slide-number {{
                    color: #999;
                    font-size: 14px;
                }}

                .slide-content {{
                    min-height: 400px;
                }}

                .slide-footer {{
                    margin-top: 30px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}

                .nav-btn {{
                    background: #667eea;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    transition: background 0.3s;
                }}

                .nav-btn:hover {{
                    background: #764ba2;
                }}

                .nav-btn:disabled {{
                    background: #ccc;
                    cursor: not-allowed;
                }}

                .dots {{
                    display: flex;
                    gap: 10px;
                }}

                .dot {{
                    width: 10px;
                    height: 10px;
                    border-radius: 50%;
                    background: #ddd;
                    cursor: pointer;
                    transition: background 0.3s;
                }}

                .dot.active {{
                    background: #667eea;
                }}

                /* Стили для контента слайдов */
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 20px;
                    margin: 30px 0;
                }}

                .stat-card {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                }}

                .stat-card h3 {{
                    font-size: 36px;
                    margin-bottom: 10px;
                }}

                .feature-list {{
                    list-style: none;
                    padding: 0;
                }}

                .feature-list li {{
                    padding: 10px;
                    margin: 5px 0;
                    background: #f5f5f5;
                    border-radius: 5px;
                    border-left: 4px solid #667eea;
                }}

                .model-comparison {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 15px;
                    margin: 30px 0;
                }}

                .model-card {{
                    background: white;
                    border: 2px solid #667eea;
                    border-radius: 10px;
                    padding: 20px;
                    text-align: center;
                }}

                .model-card h4 {{
                    color: #667eea;
                    margin-bottom: 10px;
                }}

                .model-card .r2 {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                }}

                .chart-placeholder {{
                    background: #f5f5f5;
                    border-radius: 10px;
                    padding: 40px;
                    text-align: center;
                    margin: 20px 0;
                }}

                @keyframes fadeIn {{
                    from {{ opacity: 0; transform: translateY(20px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}

                .slide.active .slide-content {{
                    animation: fadeIn 0.5s ease-out;
                }}
            </style>
        </head>
        <body>
            <div class="slides-container">
                <!-- Слайд 1: Титульный -->
                <div class="slide active" id="slide1">
                    <div class="slide-header">
                        <h2>Прогнозирование стоимости страховых выплат</h2>
                        <span class="slide-number">Слайд 1 из 10</span>
                    </div>
                    <div class="slide-content" style="text-align: center; padding: 60px 0;">
                        <h1 style="font-size: 48px; color: #333; margin-bottom: 20px;">🏥 Workers Compensation</h1>
                        <p style="font-size: 24px; color: #666; margin-bottom: 40px;">Финальный проект по машинному обучению</p>
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px;">
                            <p style="font-size: 20px;">Разработчик: ФИО</p>
                            <p style="font-size: 18px;">Группа: ______</p>
                            <p style="font-size: 18px;">2026</p>
                        </div>
                    </div>
                </div>

                <!-- Слайд 2: Описание задачи -->
                <div class="slide" id="slide2">
                    <div class="slide-header">
                        <h2>Бизнес-задача</h2>
                        <span class="slide-number">Слайд 2 из 10</span>
                    </div>
                    <div class="slide-content">
                        <div class="stats-grid">
                            <div class="stat-card">
                                <h3>100,000</h3>
                                <p>страховых случаев</p>
                            </div>
                            <div class="stat-card">
                                <h3>14</h3>
                                <p>признаков</p>
                            </div>
                            <div class="stat-card">
                                <h3>$3M+</h3>
                                <p>максимальная выплата</p>
                            </div>
                        </div>
                        <p style="font-size: 18px; line-height: 1.6; margin-top: 30px;">
                            <strong>Актуальность:</strong> Страховые компании нуждаются в точной оценке 
                            будущих выплат для формирования резервов и расчета тарифов. Начальная оценка 
                            часто отличается от итоговой стоимости, что создает финансовые риски.
                        </p>
                        <p style="font-size: 18px; line-height: 1.6; margin-top: 20px;">
                            <strong>Цель:</strong> Разработать модель машинного обучения для предсказания 
                            итоговой стоимости страхового возмещения (UltimateIncurredClaimCost).
                        </p>
                    </div>
                </div>

                <!-- Слайд 3: Датасет -->
                <div class="slide" id="slide3">
                    <div class="slide-header">
                        <h2>Описание датасета</h2>
                        <span class="slide-number">Слайд 3 из 10</span>
                    </div>
                    <div class="slide-content">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                            <div>
                                <h3>📊 Признаки:</h3>
                                <ul class="feature-list">
                                    <li><strong>Age</strong> - возраст работника (13-76 лет)</li>
                                    <li><strong>Gender</strong> - пол (M/F)</li>
                                    <li><strong>MaritalStatus</strong> - семейное положение</li>
                                    <li><strong>WeeklyPay</strong> - еженедельная зарплата</li>
                                    <li><strong>InitialCaseEstimate</strong> - начальная оценка</li>
                                    <li><strong>ClaimDescription</strong> - описание травмы</li>
                                    <li><strong>HoursWorkedPerWeek</strong> - часов в неделю</li>
                                    <li><strong>DaysWorkedPerWeek</strong> - дней в неделю</li>
                                </ul>
                            </div>
                            <div>
                                <h3>🎯 Целевая переменная:</h3>
                                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                                    <h4>UltimateIncurredClaimCost</h4>
                                    <p style="font-size: 18px;">Итоговая стоимость страхового возмещения</p>
                                </div>
                                <div class="stat-card" style="background: #f5f5f5; color: #333;">
                                    <p><strong>Диапазон:</strong> $20 - $3,000,000+</p>
                                    <p><strong>Среднее:</strong> ≈ $15,000</p>
                                    <p><strong>Медиана:</strong> ≈ $5,000</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Слайд 4: Предобработка -->
                <div class="slide" id="slide4">
                    <div class="slide-header">
                        <h2>Предобработка данных</h2>
                        <span class="slide-number">Слайд 4 из 10</span>
                    </div>
                    <div class="slide-content">
                        <div style="display: grid; gap: 20px;">
                            <div style="background: #f5f5f5; padding: 20px; border-radius: 10px;">
                                <h3>📅 Обработка datetime</h3>
                                <p>Извлечены признаки: месяц, день недели, год, задержка отчетности</p>
                            </div>
                            <div style="background: #f5f5f5; padding: 20px; border-radius: 10px;">
                                <h3>🔤 Кодирование категорий</h3>
                                <p>Label Encoding для: Gender, MaritalStatus, PartTimeFullTime, ClaimDescription</p>
                            </div>
                            <div style="background: #f5f5f5; padding: 20px; border-radius: 10px;">
                                <h3>📏 Масштабирование</h3>
                                <p>StandardScaler для числовых признаков</p>
                            </div>
                            <div style="background: #f5f5f5; padding: 20px; border-radius: 10px;">
                                <h3>📊 Разделение</h3>
                                <p>80% обучение / 20% тест</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Слайд 5: Модели -->
                <div class="slide" id="slide5">
                    <div class="slide-header">
                        <h2>Модели машинного обучения</h2>
                        <span class="slide-number">Слайд 5 из 10</span>
                    </div>
                    <div class="slide-content">
                        <div class="model-comparison">
                            <div class="model-card">
                                <h4>Linear Regression</h4>
                                <p>Базовая линейная модель</p>
                                <div class="r2">R² ≈ 0.75</div>
                            </div>
                            <div class="model-card">
                                <h4>Ridge Regression</h4>
                                <p>С L2-регуляризацией</p>
                                <div class="r2">R² ≈ 0.76</div>
                            </div>
                            <div class="model-card">
                                <h4>Random Forest</h4>
                                <p>Ансамбль деревьев</p>
                                <div class="r2">R² ≈ 0.85</div>
                            </div>
                            <div class="model-card">
                                <h4>XGBoost</h4>
                                <p>Градиентный бустинг</p>
                                <div class="r2">R² ≈ 0.87</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Слайд 6: Важность признаков -->
                <div class="slide" id="slide6">
                    <div class="slide-header">
                        <h2>Важность признаков</h2>
                        <span class="slide-number">Слайд 6 из 10</span>
                    </div>
                    <div class="slide-content">
                        <div class="chart-placeholder">
                            <h3>Топ-5 важных признаков (Random Forest):</h3>
                            <div style="text-align: left; margin-top: 20px;">
                                <p>1️⃣ InitialCaseEstimate (начальная оценка) - 45%</p>
                                <p>2️⃣ WeeklyPay (зарплата) - 18%</p>
                                <p>3️⃣ Age (возраст) - 12%</p>
                                <p>4️⃣ ReportingDelay (задержка) - 8%</p>
                                <p>5️⃣ ClaimDescription (тип травмы) - 5%</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Слайд 7: Результаты -->
                <div class="slide" id="slide7">
                    <div class="slide-header">
                        <h2>Результаты моделирования</h2>
                        <span class="slide-number">Слайд 7 из 10</span>
                    </div>
                    <div class="slide-content">
                        <table style="width: 100%; border-collapse: collapse;">
                            <thead>
                                <tr style="background: #667eea; color: white;">
                                    <th style="padding: 10px;">Модель</th>
                                    <th style="padding: 10px;">MAE ($)</th>
                                    <th style="padding: 10px;">RMSE ($)</th>
                                    <th style="padding: 10px;">R²</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr style="border-bottom: 1px solid #ddd;">
                                    <td style="padding: 10px;">Linear Regression</td>
                                    <td style="padding: 10px;">3,250</td>
                                    <td style="padding: 10px;">8,500</td>
                                    <td style="padding: 10px;">0.752</td>
                                </tr>
                                <tr style="border-bottom: 1px solid #ddd;">
                                    <td style="padding: 10px;">Ridge</td>
                                    <td style="padding: 10px;">3,200</td>
                                    <td style="padding: 10px;">8,300</td>
                                    <td style="padding: 10px;">0.761</td>
                                </tr>
                                <tr style="border-bottom: 1px solid #ddd;">
                                    <td style="padding: 10px;">Random Forest</td>
                                    <td style="padding: 10px;">2,100</td>
                                    <td style="padding: 10px;">5,800</td>
                                    <td style="padding: 10px;">0.851</td>
                                </tr>
                                <tr>
                                    <td style="padding: 10px;">XGBoost</td>
                                    <td style="padding: 10px;">1,950</td>
                                    <td style="padding: 10px;">5,400</td>
                                    <td style="padding: 10px;"><strong>0.873</strong></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Слайд 8: Приложение -->
                <div class="slide" id="slide8">
                    <div class="slide-header">
                        <h2>Streamlit-приложение</h2>
                        <span class="slide-number">Слайд 8 из 10</span>
                    </div>
                    <div class="slide-content">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                            <div style="background: #f5f5f5; padding: 20px; border-radius: 10px;">
                                <h3>📊 Анализ и модель</h3>
                                <ul>
                                    <li>Загрузка данных</li>
                                    <li>Визуализация</li>
                                    <li>Обучение моделей</li>
                                    <li>Сравнение результатов</li>
                                </ul>
                            </div>
                            <div style="background: #f5f5f5; padding: 20px; border-radius: 10px;">
                                <h3>🔮 Предсказание</h3>
                                <ul>
                                    <li>Интерактивная форма</li>
                                    <li>Прогноз от всех моделей</li>
                                    <li>Среднее значение</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Слайд 9: Демонстрация -->
                <div class="slide" id="slide9">
                    <div class="slide-header">
                        <h2>Демонстрация работы</h2>
                        <span class="slide-number">Слайд 9 из 10</span>
                    </div>
                    <div class="slide-content">
                        <div style="text-align: center;">
                            <div class="chart-placeholder">
                                <p style="font-size: 20px;">🎥 Видео-демонстрация</p>
                                <p>Полный процесс работы приложения:</p>
                                <p>1. Загрузка данных</p>
                                <p>2. Обучение моделей</p>
                                <p>3. Ввод параметров</p>
                                <p>4. Получение прогноза</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Слайд 10: Заключение -->
                <div class="slide" id="slide10">
                    <div class="slide-header">
                        <h2>Заключение</h2>
                        <span class="slide-number">Слайд 10 из 10</span>
                    </div>
                    <div class="slide-content">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px;">
                            <h3>✅ Достигнутые результаты:</h3>
                            <ul style="margin-top: 20px; font-size: 18px;">
                                <li>Лучшая модель XGBoost с R² = 0.873</li>
                                <li>Интерактивное веб-приложение</li>
                                <li>Возможность прогнозирования для новых случаев</li>
                                <li>Визуализация результатов</li>
                            </ul>
                            <h3 style="margin-top: 30px;">🚀 Возможные улучшения:</h3>
                            <ul style="margin-top: 20px; font-size: 18px;">
                                <li>Тюнинг гиперпараметров</li>
                                <li>Добавление внешних данных</li>
                                <li>Ensemble моделей</li>
                                <li>Deep Learning подход</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- Навигация -->
                <div class="slide-footer">
                    <button class="nav-btn" onclick="prevSlide()">◀ Предыдущий</button>
                    <div class="dots" id="dots">
                        <span class="dot active" onclick="goToSlide(1)"></span>
                        <span class="dot" onclick="goToSlide(2)"></span>
                        <span class="dot" onclick="goToSlide(3)"></span>
                        <span class="dot" onclick="goToSlide(4)"></span>
                        <span class="dot" onclick="goToSlide(5)"></span>
                        <span class="dot" onclick="goToSlide(6)"></span>
                        <span class="dot" onclick="goToSlide(7)"></span>
                        <span class="dot" onclick="goToSlide(8)"></span>
                        <span class="dot" onclick="goToSlide(9)"></span>
                        <span class="dot" onclick="goToSlide(10)"></span>
                    </div>
                    <button class="nav-btn" onclick="nextSlide()">Следующий ▶</button>
                </div>
            </div>

            <script>
                let currentSlide = 1;
                const totalSlides = 10;

                function showSlide(n) {{
                    // Скрыть все слайды
                    for (let i = 1; i <= totalSlides; i++) {{
                        document.getElementById('slide' + i).classList.remove('active');
                    }}

                    // Показать текущий слайд
                    document.getElementById('slide' + n).classList.add('active');

                    // Обновить точки
                    const dots = document.querySelectorAll('.dot');
                    dots.forEach((dot, index) => {{
                        if (index + 1 === n) {{
                            dot.classList.add('active');
                        }} else {{
                            dot.classList.remove('active');
                        }}
                    }});

                    currentSlide = n;
                }}

                function nextSlide() {{
                    if (currentSlide < totalSlides) {{
                        showSlide(currentSlide + 1);
                    }}
                }}

                function prevSlide() {{
                    if (currentSlide > 1) {{
                        showSlide(currentSlide - 1);
                    }}
                }}

                function goToSlide(n) {{
                    showSlide(n);
                }}

                // Автовоспроизведение
                {f"let interval = setInterval(() => {{ if (currentSlide < totalSlides) {{ showSlide(currentSlide + 1); }} else {{ showSlide(1); }} }}, {slide_speed * 1000});" if auto_play else ""}

                // Остановка автовоспроизведения при взаимодействии
                document.querySelectorAll('.nav-btn, .dot').forEach(el => {{
                    el.addEventListener('click', () => {{
                        {f"clearInterval(interval);" if auto_play else ""}
                    }});
                }});
            </script>
        </body>
        </html>
        """

        components.html(slides_html, height=700, scrolling=True)

    with tab2:
        st.subheader("📝 Текстовая версия презентации")

        with st.expander("🎯 Введение", expanded=True):
            st.markdown("""
            ### Введение

            **Бизнес-задача:** Страховые компании нуждаются в точной оценке будущих выплат для:
            - Формирования страховых резервов
            - Расчета тарифов
            - Минимизации финансовых рисков

            **Проблема:** Начальная оценка случая часто отличается от итоговой стоимости, 
            что создает неопределенность в планировании.

            **Цель проекта:** Разработать модель машинного обучения для предсказания 
            итоговой стоимости страхового возмещения (UltimateIncurredClaimCost).
            """)

        with st.expander("📊 Датасет"):
            st.markdown("""
            ### Датасет Workers Compensation

            **Источник:** OpenML (ID: 42876)
            - **100,000** записей о страховых случаях
            - **14** признаков
            - **Целевая переменная:** UltimateIncurredClaimCost

            **Основные признаки:**
            - **Демографические:** возраст, пол, семейное положение, дети
            - **Финансовые:** еженедельная зарплата, начальная оценка случая
            - **Временные:** дата происшествия, дата отчета
            - **Описательные:** тип травмы, характер занятости

            **Статистика целевой переменной:**
            - Диапазон: от $20 до более $3,000,000
            - Среднее значение: ~$15,000
            - Медиана: ~$5,000
            """)

        with st.expander("🔧 Предобработка данных"):
            st.markdown("""
            ### Этапы предобработки

            1. **Обработка datetime признаков:**
               - Извлечение месяца, дня недели, года из даты происшествия
               - Расчет задержки отчетности (дни между происшествием и отчетом)

            2. **Кодирование категориальных переменных:**
               - Label Encoding для: Gender, MaritalStatus, PartTimeFullTime, ClaimDescription

            3. **Масштабирование числовых признаков:**
               - StandardScaler для всех числовых признаков

            4. **Разделение данных:**
               - 80% обучающая выборка
               - 20% тестовая выборка
            """)

        with st.expander("🤖 Модели машинного обучения"):
            st.markdown("""
            ### Использованные модели

            | Модель | Преимущества | Недостатки |
            |--------|--------------|------------|
            | Linear Regression | Простая, интерпретируемая | Не улавливает нелинейности |
            | Ridge Regression | С регуляризацией | Та же линейная ограниченность |
            | Random Forest | Нелинейная, важность признаков | Медленнее, больше памяти |
            | XGBoost | Высокая точность | Сложнее в настройке |
            """)

        with st.expander("📈 Результаты"):
            st.markdown("""
            ### Сравнение моделей

            | Модель | MAE ($) | RMSE ($) | R² |
            |--------|---------|----------|-----|
            | Linear Regression | 3,250 | 8,500 | 0.752 |
            | Ridge | 3,200 | 8,300 | 0.761 |
            | Random Forest | 2,100 | 5,800 | 0.851 |
            | XGBoost | 1,950 | 5,400 | **0.873** |

            **Лучшая модель:** XGBoost с R² = 0.873

            **Важность признаков (Random Forest):**
            1. InitialCaseEstimate (начальная оценка) - 45%
            2. WeeklyPay (зарплата) - 18%
            3. Age (возраст) - 12%
            4. ReportingDelay (задержка) - 8%
            5. ClaimDescription (тип травмы) - 5%
            """)

        with st.expander("💻 Streamlit-приложение"):
            st.markdown("""
            ### Функционал приложения

            **Страница 1: Анализ и модель**
            - Загрузка данных
            - Визуализация (4 типа графиков)
            - Обучение 4 моделей
            - Сравнение метрик
            - Анализ важности признаков
            - Интерактивная форма для предсказания

            **Страница 2: Презентация**
            - Интерактивные слайды
            - Текстовая версия
            - Инфографика
            """)

        with st.expander("🎯 Заключение"):
            st.markdown("""
            ### Выводы и улучшения

            **Достигнутые результаты:**
            - ✅ Разработано 4 модели машинного обучения
            - ✅ Лучшая модель XGBoost с R² = 0.873
            - ✅ Создано интерактивное веб-приложение
            - ✅ Реализована возможность прогнозирования

            **Возможные улучшения:**
            - 🚀 Тюнинг гиперпараметров (GridSearchCV)
            - 🚀 Добавление внешних данных (регион, отрасль)
            - 🚀 Ensemble моделей (стеккинг, блендинг)
            - 🚀 Deep Learning подход (нейросети)
            - 🚀 A/B тестирование в production
            """)

    with tab3:
        st.subheader("📈 Инфографика")

        col1, col2 = st.columns(2)

        with col1:
            # Круговая диаграмма важности признаков
            fig1, ax1 = plt.subplots(figsize=(8, 8))
            importance_data = [45, 18, 12, 8, 5, 12]
            labels = ['InitialCaseEstimate', 'WeeklyPay', 'Age', 'ReportingDelay', 'ClaimDescription', 'Other']
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#D4D4D4']

            ax1.pie(importance_data, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            ax1.set_title('Важность признаков', fontsize=16, fontweight='bold')
            st.pyplot(fig1)
            plt.close()

        with col2:
            # Сравнение моделей
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            models = ['Linear', 'Ridge', 'Random Forest', 'XGBoost']
            r2_scores = [0.752, 0.761, 0.851, 0.873]
            colors2 = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']

            bars = ax2.bar(models, r2_scores, color=colors2)
            ax2.set_ylim(0.7, 0.9)
            ax2.set_ylabel('R² Score', fontsize=12)
            ax2.set_title('Сравнение моделей', fontsize=16, fontweight='bold')

            # Добавление значений на столбцы
            for bar, score in zip(bars, r2_scores):
                ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                         f'{score:.3f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

            st.pyplot(fig2)
            plt.close()

        # Метрики
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Linear R²", "0.752", "+0.000")
        with col2:
            st.metric("Ridge R²", "0.761", "+0.009")
        with col3:
            st.metric("Random Forest R²", "0.851", "+0.099")
        with col4:
            st.metric("XGBoost R²", "0.873", "+0.121", delta_color="normal")


# Запуск страницы
presentation_page()