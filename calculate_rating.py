from file_data_processing import get_player_data_from_file, Player
from get_development_coefficient import get_development_coefficient
from typing import Dict
from path import PATH_TO_FILE
from rating_differential import RATING_DIFFERENTIAL
import csv
import datetime


def calculate_single_person_rating(player: Player, players: Dict[int, Player]) -> None:
    """
    Функция обсчёта рейтинга одного игрока

    :param player: игрок, для которого обсчитываем рейтинг
    :param players: слоаварь всех игроков турнира
    """
    new_rating = player.rating
    player_coefficient = get_development_coefficient(player.rating)

    for opponent, result in player.results.items():
        opponent_rating = players.get(opponent).rating
        rating_diff = abs(opponent_rating - player.rating)

        if rating_diff > 392:
            rating_diff = 392

        probability_victory = RATING_DIFFERENTIAL.get(rating_diff)[0] \
            if player.rating > opponent_rating \
            else RATING_DIFFERENTIAL.get(rating_diff)[1]

        new_rating += (result - probability_victory) * player_coefficient

    new_rating = round(new_rating)
    player.set_new_rating(new_rating)


def calculate_all_people_rating(players: Dict[int, Player]) -> None:
    """
    Обсчитывает рейтинг всех игроков по очереди

    :param players: слоаварь всех игроков турнира
    """
    for player in players.values():
        calculate_single_person_rating(player, players)


def write_to_csv(players: Dict[int, Player]) -> None:
    """
    Записывает данные в файл csv в кодировке cp1251,
    с разделителем точка с запятой (;)

    :param players:
    :return:
    """
    with open(f'rating_{datetime.date.today()}.csv', 'w', encoding='cp1251', newline='') as file:
        writer = csv.writer(file, delimiter=';', )

        for player in players.values():
            writer.writerow(
                (
                    player.player_id,
                    player.name,
                    player.new_rating
                )
            )


def main():
    players = get_player_data_from_file(PATH_TO_FILE)

    calculate_all_people_rating(players)
    write_to_csv(players)


main()
