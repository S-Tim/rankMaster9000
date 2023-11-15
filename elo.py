import sys


def win_probability(ratingA, ratingB):
    scale = 200
    return (
        1 / (1 + 10 ** ((ratingB - ratingA) / scale)),
        1 / (1 + 10 ** ((ratingA - ratingB) / scale)),
    )


def adjust_ratings(ratingA, ratingB, scoreA):
    k = 15
    scoreB = 1 - scoreA
    probabilities = win_probability(ratingA, ratingB)

    adjustedA = ratingA + k * (scoreA - probabilities[0])
    adjustedB = ratingB + k * (scoreB - probabilities[1])

    return int(round(adjustedA, 0)), int(round(adjustedB, 0))


def load_ratings():
    with open("ratings.txt") as f:
        lines = f.read().splitlines()
        lines = [line.split(",") for line in lines]
        ratings = {line[0]: int(line[1]) for line in lines}
    return ratings


def save_ratings():
    with open("ratings.txt", "w") as f:
        lines = [f"{name},{rating}" for name, rating in ratings.items()]
        f.write("\n".join(lines))


if __name__ == "__main__":
    ratings = load_ratings()

    if len(sys.argv) == 1:
        sorted_ratings = sorted(
            ratings.items(), key=lambda entry: entry[1], reverse=True
        )
        for player, rating in sorted_ratings:
            print(f"{player}, {rating}")
        exit()

    if len(sys.argv) != 3:
        print("Please provide the players as arguments in the form: 'winner loser'")
        exit()

    player1 = sys.argv[1]
    player2 = sys.argv[2]

    if player1 not in ratings:
        print(f"Player {player1} could not be found")
        exit()

    if player2 not in ratings:
        print(f"Player {player2} could not be found")
        exit()

    print(f"{sys.argv[1]} vs. {sys.argv[2]}")
    win_probabilities = [
        round(prob, 2) for prob in win_probability(ratings[player1], ratings[player2])
    ]
    print(f"Win probabilities: {win_probabilities[0]}, {win_probabilities[1]}")
    print(f"Previous ratings:  {ratings[player1]}, {ratings[player2]}")

    adjustedA, adjustedB = adjust_ratings(ratings[player1], ratings[player2], 1)
    ratings[player1] = adjustedA
    ratings[player2] = adjustedB

    print(f"New ratings:       {ratings[player1]}, {ratings[player2]}")

    save_ratings()
