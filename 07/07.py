from functools import partial
from typing import Dict, List, Tuple

import utils

type Player = Tuple[str, int]
type Counts = Dict[str, int]

HIGH_CARD_VALUES = {card: val for val, card in enumerate('j23456789TJQKA')}
CARD_PLACE_MULT = [10 ** x for x in range(0, 10, 2)][::-1]


def get_hand_value(player: Player, variant=False):
    hand, _ = player
    if variant: hand = hand.replace('J', 'j')
    counts = get_card_count(hand)
    if joker_in_hand(hand) and len(counts) > 1: counts = convert_jokers(counts)
    return get_hand_type_value(counts) + get_card_placement_value(hand)


def get_card_count(hand: str) -> Counts:
    counts = {card: hand.count(card) for card in hand}
    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))


def joker_in_hand(hand: str) -> bool:
    return 'j' in hand


def convert_jokers(counts: Counts) -> Counts:
    counts[[key for key in counts.keys() if key != 'j'][0]] += counts['j']
    del counts['j']
    return counts


def get_hand_type_value(counts: Counts) -> int:
    for i, f in enumerate([
        is_five_of_a_kind,
        is_four_of_a_kind,
        is_full_house,
        is_three_of_a_kind,
        is_two_pair,
        is_one_pair,
        is_high_card
    ]):
        if f(counts): return (7 - i) * 10 ** 10


def get_card_placement_value(hand: str) -> int:
    return sum([HIGH_CARD_VALUES[card] * CARD_PLACE_MULT[i] for i, card in enumerate(hand)])


def is_five_of_a_kind(counts: Counts) -> bool:
    return len(counts) == 1


def is_four_of_a_kind(counts: Counts) -> bool:
    return 4 in set(counts.values())


def is_full_house(counts: Counts) -> bool:
    vals = set(counts.values())
    return 3 in vals and 2 in vals


def is_three_of_a_kind(counts: Counts) -> bool:
    vals = set(counts.values())
    return 3 in vals and 2 not in vals


def is_two_pair(counts: Counts) -> bool:
    if len(counts) != 3: return False
    first, second, *rest = sorted(counts.values(), reverse=True)
    return first == second == 2


def is_one_pair(counts: Counts) -> bool:
    if len(counts) != 4: return False
    first, *rest = sorted(counts.values(), reverse=True)
    return first == 2 and all([v == 1 for v in rest])


def is_high_card(counts: Counts) -> bool:
    return all([v == 1 for v in counts.values()])


def get_winnings(players: List[Player]) -> int:
    return sum([(i + 1) * bid for i, (_, bid) in enumerate(players)])


def main():
    players: List[Player] = [(hand, int(bid)) for hand, bid in [line.split() for line in utils.read_str_lines()]]

    # Part 1
    sorted_players = sorted(players, key=get_hand_value)
    print('Part 1:', get_winnings(sorted_players))

    # Part 2
    differently_sorted_players = sorted(players, key=partial(get_hand_value, variant=True))
    print('Part 2:', get_winnings(differently_sorted_players))


if __name__ == "__main__":
    timer = utils.Timer()

    timer.start()
    main()
    timer.stop()  #  8.32ms
