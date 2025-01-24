def get_development_coefficient(player_rating: int) -> int:
    """
    Получает рейтинг и возвращает коэффициент развития,
    согласно диапазону рейтинга

    :param player_rating: рейтинг игрока
    :return: коэффициент развития
    """
    if player_rating < 1200:
        coefficient = 60
    elif player_rating < 1400:
        coefficient = 50
    elif player_rating < 1600:
        coefficient = 40
    elif player_rating < 1800:
        coefficient = 35
    elif player_rating < 2000:
        coefficient = 30
    elif player_rating < 2200:
        coefficient = 25
    elif player_rating < 2400:
        coefficient = 20
    else:
        coefficient = 10

    return coefficient
