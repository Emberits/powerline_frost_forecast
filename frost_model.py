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


def predict_shedding_probability(frost_thickness, temperature, wind_speed):
    """
    Прогноз вероятности самопроизвольного сброса изморози.
    Увеличивается с ростом температуры, ветра и толщины изморози.
    """
    if frost_thickness < 1.0:
        return 0.0

    # Температурный фактор: при T > -5 вероятность растет
    temp_factor = max(0, (temperature + 10) / 10)
    wind_factor = min(1, wind_speed / 10)
    thickness_factor = min(1, frost_thickness / 25)

    prob = 0.3 * temp_factor + 0.5 * wind_factor + 0.2 * thickness_factor
    return min(prob, 1.0)
