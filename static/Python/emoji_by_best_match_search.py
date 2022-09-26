from operator import indexOf
from emoji_dictionary import emoji_dictionary


def emoji_by_best_match_search(item: str, dict: dict = emoji_dictionary) -> str:
    total_num_of_char: int = 0
    similar_key: str = ""
    total_num_of_not_char: int = 0
    similarity_percent: int = 0
    list_of_keys: list[str] = list(dict.keys())

    # loop to remove any numerical/ white spaces from the item (basically clean up item of unnessary str values)
    for character in item:
        if character.isnumeric():
            if item[indexOf(item, character) + 1] == " ":
                item = item.replace(" ", "", (indexOf(item, character) + 1))
                item = item.replace(character, "")
                break
            elif item[indexOf(item, character) + 2] == " ":
                item = item.replace(item[indexOf(item, character) + 1], "")
                item = item.replace(" ", "", (indexOf(item, character) + 1))
                item = item.replace(character, "")
                break

            item = item.replace(character, "")
            continue

    if item in list_of_keys:
        return dict[item]

    # below is the actual part of the code that does the searching
    for key in list_of_keys:
        # key = key.lower()
        total_num_of_char = 0
        total_num_of_not_char = 0
        for char in item:
            # char = char.lower()
            if char.lower() in key.lower():
                total_num_of_char += 1

            if char not in key:
                total_num_of_not_char += 1

            # edit below decimal to increase or decrease accurracy
            if similarity_percent == 0:
                if 0.5 < float((total_num_of_char - total_num_of_not_char) / len(key)):
                    similarity_percent = float(
                        (total_num_of_char - total_num_of_not_char) / len(key))
                    similar_key = key

            if 0 < similarity_percent:
                if similarity_percent < float((total_num_of_char - total_num_of_not_char) / len(key)):
                    similarity_percent = float(
                        (total_num_of_char - total_num_of_not_char) / len(key))
                    similar_key = key

    return dict[similar_key] if similar_key else "🛍️"
