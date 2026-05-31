import random

from test_data.spam import spam_profile_descriptions
from test_data.gibberish import gibberish_profile_descriptions
from test_data.inappropriate import inappropriate_profile_descriptions
from test_data.unsupported_languages import unsupported_language_profile_descriptions
from test_data.valid import valid_profile_descriptions


def get_all_test_data():
    categories = [
        "valid",
        "spam",
        "gibberish",
        "inappropriate",
        "language",
    ]

    test_data = []

    for category in categories:
        if category == "valid":
            for description in valid_profile_descriptions:
                test_data.append((description, "is_valid"))
        elif category == "spam":
            for description in spam_profile_descriptions:
                test_data.append((description, "is_spam"))
        elif category == "gibberish":
            for description in gibberish_profile_descriptions:
                test_data.append((description, "is_gibberish"))
        elif category == "inappropriate":
            for description in inappropriate_profile_descriptions:
                test_data.append((description, "is_inappropriate"))
        elif category == "language":
            for description in unsupported_language_profile_descriptions:
                test_data.append((description, "language"))

    # print(f"Total test data count: {len(test_data)}")

    return test_data


def get_random_test_data(count=2):
    all_test_data = get_all_test_data()

    random.shuffle(all_test_data)

    return all_test_data[:count]
