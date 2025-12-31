import pandas as pd
import random
from pathlib import Path

OUTPUT_PATH = Path("../data/login_data_augmented.csv")

rows = []

def normal_hour():
    return random.randint(7, 23)

def unusual_hour():
    return random.randint(0, 6)

TOTAL_ROWS = 1000

for _ in range(TOTAL_ROWS):

    case = random.choice([
        "low_normal_usual_usual",
        "low_normal_usual_new",
        "low_normal_new_usual",
        "low_unusual_usual_usual",
        "medium_normal_new_new",
        "medium_unusual_new_usual",
        "medium_unusual_usual_new",
        "high_unusual_new_new"
    ])

    if case == "low_normal_usual_usual":
        rows.append([normal_hour(), 0, 0, 0])

    elif case == "low_normal_usual_new":
        rows.append([normal_hour(), 0, 1, 0])

    elif case == "low_normal_new_usual":
        rows.append([normal_hour(), 1, 0, 0])

    elif case == "low_unusual_usual_usual":
        rows.append([unusual_hour(), 0, 0, 0])

    elif case == "medium_normal_new_new":
        rows.append([normal_hour(), 1, 1, 1])

    elif case == "medium_unusual_new_usual":
        rows.append([unusual_hour(), 1, 0, 1])

    elif case == "medium_unusual_usual_new":
        rows.append([unusual_hour(), 0, 1, 1])

    elif case == "high_unusual_new_new":
        rows.append([unusual_hour(), 1, 1, 2])

df = pd.DataFrame(
    rows,
    columns=["login_hour", "device", "country", "label"]
)

df.to_csv(OUTPUT_PATH, index=False)

print("Dataset generated")
print(df["label"].value_counts())
