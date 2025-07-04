def assess_failure_risk(frost_thickness, shedding_probability, bounce_height):
    """
    Интегральная оценка риска аварии.
    Категории риска:
    - Низкий: толщина <5 мм и вероятность сброса <0.3 и высота <0.5 м
    - Средний: толщина 5-15 мм или вероятность 0.3-0.6 или высота 0.5-1.0 м
    - Высокий: толщина 15-25 мм или вероятность 0.6-0.85 или высота 1.0-2.0 м
    - Критический: толщина >25 мм или вероятность >0.85 или высота >2.0 м
    """
    risk_score = 0

    # Толщина изморози
    if frost_thickness < 5:
        risk_score += 0
    elif frost_thickness < 15:
        risk_score += 1
    elif frost_thickness < 25:
        risk_score += 2
    else:
        risk_score += 3

    # Вероятность сброса
    if shedding_probability < 0.3:
        risk_score += 0
    elif shedding_probability < 0.6:
        risk_score += 1
    elif shedding_probability < 0.85:
        risk_score += 2
    else:
        risk_score += 3

    # Высота подскока
    if bounce_height < 0.5:
        risk_score += 0
    elif bounce_height < 1.0:
        risk_score += 1
    elif bounce_height < 2.0:
        risk_score += 2
    else:
        risk_score += 3

    # Итоговая классификация
    if risk_score <= 2:
        return "Низкий"
    elif risk_score <= 4:
        return "Средний"
    elif risk_score <= 6:
        return "Высокий"
    else:
        return "Критический"
