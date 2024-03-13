# рассчитываем функцию принадлежности
def f_membership(canon_value, value):
    x = float(1.0 / (1.0 + (value - canon_value) ** 4))
    return x

# проверяем выходит ли введенное значение за рамки диапазона
# это нужно, так как у нас кусочно заданная функция
def f_check_diapazon(sympt, current_value):
    if sympt == 'пульс':
        # если значение слишком высокое
        if current_value > 120:
            current_value = 120
        # если значение слишком низкое
        elif current_value < 30:
            current_value = 30
    elif sympt == 'верхнее давление':
        if current_value > 150:
            current_value = 150
        elif current_value < 90:
            current_value = 90
    elif sympt == 'нижнее давление':
        if current_value > 110:
            current_value = 110
        elif current_value < 50:
            current_value = 50
    elif sympt == "температура":
        if current_value > 38:
            current_value = 38
        elif current_value < 35:
            current_value = 35
    return current_value

# проверяем принадлежность классу
def f_is_in_class(sympt, current_value, bz_value):
    # проверяем текущее значение симптома
    current_value = f_check_diapazon(sympt, current_value)

    # если формула из БЗ содержит какую-либо лингвистическую переменную
    if bz_value.count('высок') > 0:
        if sympt == 'пульс':
            canon_value = 120
            # чем больше число, на котрое делим, тем шире диапазон
            canon_value = canon_value / 15
            current_value = current_value / 15
        elif sympt == 'верхнее давление':
            canon_value = 150
            canon_value = canon_value / 10
            current_value = current_value / 10
        elif sympt == 'нижнее давление':
            canon_value = 110
            canon_value = canon_value / 10
            current_value = current_value / 10
        else:
            canon_value = 38
            # уменьшаем диапазон, у температуры должно быть точное значение
            canon_value = canon_value * 2
            current_value = current_value * 2

    elif bz_value.count('норм') > 0:
        if sympt == 'пульс':
            canon_value = 75
            canon_value = canon_value / 15
            current_value = current_value / 15
        elif sympt == 'верхнее давление':
            canon_value = 120
            canon_value = canon_value / 10
            current_value = current_value / 10
        elif sympt == 'нижнее давление':
            canon_value = 80
            canon_value = canon_value / 10
            current_value = current_value / 10
        else:
            canon_value = 36.6
            canon_value = canon_value * 2
            current_value = current_value * 2

    elif bz_value.count('низк') > 0:
        if sympt == 'пульс':
            canon_value = 35
            canon_value = canon_value / 15
            current_value = current_value / 15
        elif sympt == 'верхнее давление':
            canon_value = 90
            canon_value = canon_value / 10
            current_value = current_value / 10
        elif sympt == 'нижнее давление':
            canon_value = 60
            canon_value = canon_value / 10
            current_value = current_value / 10
        else:
            canon_value = 35.2
            canon_value = canon_value * 2
            current_value = current_value * 2

    # если значение ФП больше порогового значения, то считаем, что введенное число принадлежит классу
    if f_membership(float(canon_value), current_value) >= 0.2:
        return True
    else:
        return False
