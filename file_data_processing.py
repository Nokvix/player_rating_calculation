from typing import Dict
import re

"""
Код обрабатывает файлы формата smw
"""


class Player:
    """
    Объект игрока:
    name - ФИО игрока;
    rating - Рейтинг игрока;
    new_rating - Рейтинг игрока после обсчёта;
    start_position - Стартовый номер игрока;
    player_id - Идентификационный номер игрока;
    points - Количество очков, набранных игроком в турнире;
    results - Словарь результатов партий:
    key - стартовый номер соперника, value - результат встречи (« - ничья)
    """

    def __init__(self, name, rating, start_position, player_id, points, results):
        self.name = name
        self.rating = rating
        self.new_rating = rating
        self.start_position = start_position
        self.player_id = player_id
        self.points = points
        self.results = results

    def __str__(self):
        return (f'name: {self.name}\nrating: {self.rating}\nstart_position: {self.start_position}\n'
                f'player_id: {self.player_id}\npoints: {self.points}\nresults: {self.results}')


def create_player(player_str: str) -> Player:
    """
    Функция создания объекта игрока

    :param player_str: строка данных игрока из файла
    :return: объект игрока
    """
    player_data = parse_data(player_str)
    results = reformat_results(player_data['results'])
    player = Player(
        name=player_data['name'],
        rating=player_data['rating'],
        start_position=player_data['start_position'],
        player_id=player_data['id'],
        points=player_data['points'],
        results=results
    )

    return player


def reformat_results(results: str) -> Dict[int, int]:
    """
    Функция преобразования результатов партий

    :param results: результаты партий из файла
    :return: словарь результатов. key - номер соперника, value - результат
    """
    pattern = re.compile(
        r"(?P<board_number>\d+)"
        r"(?P<color>[WB])"
        r"(?P<result>[\d«])#"
        r"(?P<opponent_number>\d+)"
    )

    results_dict = {}
    for result_match in pattern.finditer(results):
        result_groups = result_match.groupdict()
        results_dict[result_groups['opponent_number']] = result_groups['result']

    return results_dict


def parse_data(player_str: str) -> Dict[str, str]:
    """
    Функция разбиения данных

    :param player_str: строка данных игрока из файла
    :return: словарь с данными игрока
    """
    pattern = re.compile(
        r"^(?P<current_position>\d+)\s+"
        r"(?P<start_position>\d+)\s+"
        r"(?P<name>[a-zA-Zа-яА-ЯёЁ\s]+)\s+"
        r"(?P<rating>\d+)?\**\s+"
        r"(?P<title>[A-Z]*)\s+"
        r"(?P<id>\d+)?\s+"
        r"(?P<points>[0-9«]+)\s+"
        r"(?P<first_color>[WB])\s+"
        r"(?P<results>.+)$"
    )

    player_data = pattern.fullmatch(player_str)
    player_groups = player_data.groupdict()

    return player_groups


def get_player_data_from_file(path_to_file: str) -> Dict[int, Player]:
    """
    Функция читает файл формата smw,
    обращается к другим функциям и
    возвращает словарь объектов Player

    :param path_to_file: путь до файла
    :return: словарь игроков (Player)
    """
    with open(path_to_file, 'r') as file:
        split_data = file.readline().split()
        number_players, number_tours = map(int, [split_data[0], split_data[1]])
        file_lines = file.readlines()

    players = {}

    for i in range(number_players):
        player = create_player(file_lines[i].strip())
        players[player.start_position] = player

    return players

