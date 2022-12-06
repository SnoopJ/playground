from enum import IntEnum, auto

import click


class Move(IntEnum):
    ROCK = 1
    PAPER = auto()
    SCISSORS = auto()


WIN_SCORE = 6
LOSS_SCORE = 0
DRAW_SCORE = 3


# if opponent chose [key], then [val] wins the matchup
WINS = {
    Move.ROCK: Move.PAPER,
    Move.PAPER: Move.SCISSORS,
    Move.SCISSORS: Move.ROCK,
}

WIN_PAIRS = WINS.items()


# if opponent chose [key], then [val] loses the matchup
LOSSES = {
    Move.ROCK: Move.SCISSORS,
    Move.PAPER: Move.ROCK,
    Move.SCISSORS: Move.PAPER,
}

LOSS_PAIRS = LOSSES.items()


THEIR_MOVES = {
    "A": Move.ROCK,
    "B": Move.PAPER,
    "C": Move.SCISSORS,
}


def moves(line: str) -> tuple:
    theirs, ours = line.split()
    their_move = THEIR_MOVES[theirs]

    print(f"Opponent played {their_move=}")

    if ours == "X":
        print("we need to lose")
        our_move = LOSSES[their_move]
    elif ours == "Y":
        print("we need to draw")
        our_move = their_move
    elif ours == "Z":
        print("we need to win")
        our_move = WINS[their_move]
    else:
        raise ValueError(f"Unknown strategy {ours=}")

    print(f"We will play {our_move=}")
    return their_move, our_move


def score_round(line: str) -> tuple[int, int]:
    print(f"Matchup: {line}")
    matchup = their_move, our_move = moves(line)

    # each player gets points for their move
    their_score = their_move.value
    our_score = our_move.value

    if matchup in WIN_PAIRS:
        their_score += LOSS_SCORE
        our_score += WIN_SCORE
    elif matchup in LOSS_PAIRS:
        their_score += WIN_SCORE
        our_score += LOSS_SCORE
    else:
        # draw
        their_score += DRAW_SCORE
        our_score += DRAW_SCORE


    return their_score, our_score


@click.command()
@click.option('--input', required=True, help="Input file for this day")
def main(input):
    with open(input, "r") as f:
        score = 0

        for roundnum, line in enumerate(f, 1):
            _, our_score = score_round(line)
            score += our_score
            print(f"Round #{roundnum} - won {our_score} points (total: {score})\n")

        # 13073 is too low
        print(f"Part 2 - total points: {score}")


if __name__ == '__main__':
    main()
