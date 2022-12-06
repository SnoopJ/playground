import click


ROCK = object()
PAPER = object()
SCISSORS = object()

WIN_SCORE = 6
LOSS_SCORE = 0
DRAW_SCORE = 3

THEIR_MOVES = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
}

OUR_MOVES = {
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS,
}

MOVE_SCORES = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3,
}

# match-ups (theirs, ours) where we win
OUR_WINS = {
    (ROCK, PAPER),
    (PAPER, SCISSORS),
    (SCISSORS, ROCK),
}

# match-ups (theirs, ours) where we lose
OUR_LOSSES = {
    (ROCK, SCISSORS),
    (PAPER, ROCK),
    (SCISSORS, PAPER),
}


def moves(line: str) -> tuple:
    theirs, ours = line.split()
    their_move = THEIR_MOVES[theirs]
    our_move = OUR_MOVES[ours]

    return their_move, our_move


def score_round(line: str) -> tuple[int, int]:
    matchup = their_move, our_move = moves(line)

    # each player gets points for their move
    their_score = MOVE_SCORES[their_move]
    our_score = MOVE_SCORES[our_move]

    if matchup in OUR_WINS:
        their_score += LOSS_SCORE
        our_score += WIN_SCORE
    elif matchup in OUR_LOSSES:
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
#             print(f"Round #{roundnum} - won {our_score} points (total: {score})")

        print(f"Part 1 - total points: {score}")


if __name__ == '__main__':
    main()
