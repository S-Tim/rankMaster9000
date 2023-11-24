import sys
import json
import boto3

BUCKET_NAME = "rankmaster9001"
FILENAME = "ratings.json"


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
    s3_client = boto3.client("s3")
    ratings_object = s3_client.get_object(Bucket=BUCKET_NAME, Key=FILENAME)
    content = ratings_object["Body"].read().decode("utf-8")
    ratings = json.loads(content)
    return ratings


def save_ratings(ratings):
    s3_client = boto3.client("s3")
    ratings_json = json.dumps(ratings).encode("utf-8")
    s3_client.put_object(Body=ratings_json, Bucket=BUCKET_NAME, Key=FILENAME)


def parse_payload(payload):
    loaded = json.loads(payload)
    return (loaded["player1"], loaded["player2"])


def lambda_handler(event, context):
    player1, player2 = parse_payload(event["body"])

    ratings = load_ratings()

    if player1 not in ratings:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": f"Player {player1} could not be found"}),
        }

    if player2 not in ratings:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": f"Player {player2} could not be found"}),
        }

    win_probabilities = [
        round(prob, 2) for prob in win_probability(ratings[player1], ratings[player2])
    ]

    adjustedA, adjustedB = adjust_ratings(ratings[player1], ratings[player2], 1)
    ratings[player1] = adjustedA
    ratings[player2] = adjustedB

    save_ratings(ratings)

    return {
        "statusCode": 200,
        "body": json.dumps(
            [
                {"name": player1, "rating": ratings[player1]},
                {"name": player2, "rating": ratings[player2]},
            ]
        ),
    }


def lambda_handler_show_ratings(event, context):
    ratings = load_ratings()
    mapped_ratings = sorted(
        [{"name": name, "rating": rating} for (name, rating) in ratings.items()],
        key=lambda entry: entry["rating"],
        reverse=True,
    )

    return {
        "statusCode": 200,
        "body": json.dumps(mapped_ratings),
    }


event = {"body": '{"player1": "Klaus", "player2": "Tim"}'}
print(lambda_handler_show_ratings(None, None))
lambda_handler(event, None)
print(lambda_handler_show_ratings(None, None))
