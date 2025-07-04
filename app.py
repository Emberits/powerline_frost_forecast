import streamlit as st
from frost_model import predict_frost_thickness, predict_shedding_probability
from wire_dynamics import calculate_wire_bounce_height
from risk_assessment import assess_failure_risk

st.set_page_config(page_title="Прогноз аварий на ЛЭП", layout="centered")

st.title("Прогнозирование аварий на линиях электропередачи")

st.header("Входные параметры")

col1, col2 = st.columns(2)

with col1:
    temperature = st.number_input("Температура воздуха (°C)", min_value=-50.0, max_value=10.0, value=-15.0, step=0.1)
    humidity = st.slider("Относительная влажность (%)", 0, 100, 85)
    wind_speed = st.number_input("Скорость ветра (м/с)", min_value=0.0, max_value=30.0, value=2.0, step=0.1)
    time_hours = st.number_input("Время воздействия (ч)", min_value=0.1, max_value=24.0, value=3.0, step=0.1)

with col2:
    wire_length = st.number_input("Длина пролета провода (м)", min_value=10.0, max_value=1000.0, value=200.0, step=1.0)
    wire_tension = st.number_input("Натяжение провода (Н)", min_value=1000.0, max_value=100000.0, value=15000.0, step=100.0)
    wire_mass_per_m = st.number_input("Масса провода на метр (кг/м)", min_value=0.1, max_value=5.0, value=1.2, step=0.01)

if st.button("Прогнозировать"):
    frost_thickness = predict_frost_thickness(temperature, humidity, wind_speed, time_hours)
    shedding_prob = predict_shedding_probability(frost_thickness, temperature, wind_speed)
    bounce_height = calculate_wire_bounce_height(frost_thickness, wire_length, wire_tension, wire_mass_per_m)
    failure_risk = assess_failure_risk(frost_thickness, shedding_prob, bounce_height)

    st.subheader("Результаты прогноза")
    st.write(f"Толщина изморози: **{frost_thickness:.2f} мм**")
    st.write(f"Вероятность самопроизвольного сброса изморози: **{shedding_prob*100:.1f}%**")
    st.write(f"Высота подскока провода после сброса (м): **{bounce_height:.2f}**")
    st.write(f"Оценка риска аварии: **{failure_risk}**")

def predict_frost_thickness(temperature, humidity, wind_speed, time_hours):
    """
    Прогноз толщины изморози (мм) по упрощенной модели.
    Образование изморози возможно при T <= -11°C, влажности >= 80%, ветре <= 3 м/с.
    """
    if temperature > -11 or humidity < 80 or wind_speed > 3:
        return 0.0

    # Коэффициенты модели (условные)
    alpha = 0.05  # коэффициент захвата пара
    beta = 0.1    # коэффициент намерзания
    d = 1.0       # плотность пара (условно)
    W = humidity / 100.0
    V = max(0, 3 - wind_speed)  # уменьшается с ростом ветра

    frost_thickness = alpha * beta * d * W * V * time_hours * 10  # умножаем на 10 для масштаба мм
    return frost_thickness
