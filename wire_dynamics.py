def calculate_wire_bounce_height(frost_thickness_mm, wire_length_m, wire_tension_N, wire_mass_per_m_kg):
    """
    Расчет высоты подскока провода после сброса изморози.
    Используется упрощенная формула провисания и кинетической энергии.
    """
    # Масса изморози на проводе (кг) на метр (условно, плотность льда ~0.9 г/см3)
    frost_density = 900  # кг/м3
    frost_thickness_m = frost_thickness_mm / 1000
    frost_mass_per_m = frost_density * frost_thickness_m * 0.01  # сечение изморози ~1 см ширина

    total_mass_per_m = wire_mass_per_m_kg + frost_mass_per_m

    # Дополнительное провисание s (м)
    s = (total_mass_per_m * wire_length_m ** 2) / (8 * wire_tension_N)

    # Упругая энергия провода (Дж)
    E = 0.5 * wire_tension_N * s ** 2

    # Масса провода на длину (кг)
    m = wire_mass_per_m_kg * wire_length_m

    if m == 0:
        return 0.0

    # Высота подскока (м), из энергии потенциальной = кинетической
    h = (2 * E / m) ** 0.5
    return h
