import random
import string

upper_case = string.ascii_uppercase
lower_case = string.ascii_lowercase
special_chars = string.punctuation


def text_scramble_effect_lines(
    input_text: str,
    multiplier: int,
    only_upper: bool = False,
    include_special: bool = True,
) -> list:
    """Generate a list of text lines with a scramble effect.

    This function generates a list of text lines that simulate a scramble effect. The
    function takes an input text and a multiplier as parameters. The multiplier
    determines the number of times each line is repeated in the output. The function
    randomly replaces characters in the input text with characters from a list of upper
    case, lower case, and special characters to create the scramble effect.

    :param input_text: The text to apply the scramble effect to.
    :type input_text: str
    :param multiplier: The number of times each line is repeated in the output.
    :type multiplier: int
    :param only_upper: A boolean that determines whether to only use upper case
        characters for the scramble effect. Defaults to False.
    :type only_upper: bool, optional
    :param include_special: A boolean that determines whether to include special
        characters in the scramble effect. Defaults to True.
    :type include_special: bool, optional
    :return: A list of text lines with the scramble effect.
    :rtype: list
    """
    lines_list = list()
    if only_upper:
        total_chars = upper_case
    else:
        total_chars = upper_case + lower_case
    if include_special:
        total_chars += special_chars

    for i in range(len(input_text) * multiplier):  # no of lines
        output_text = ""
        for j in range(len(input_text)):  # for each char
            if i < multiplier or input_text[j] == " ":
                output_text += (
                    " " if input_text[j] == " " else random.choice(total_chars)
                )
            elif i // multiplier >= j:
                output_text += input_text[j]
            else:
                output_text += random.choice(total_chars)
        lines_list.append(output_text)

    def random_replace(count: int = 1):
        num_chars_to_replace = 2
        for _ in range(count):
            for _ in range(multiplier):  # randomly change consecutive chars
                char_index = random.randint(0, len(input_text) - num_chars_to_replace)
                # while " " in input_text[char_index : char_index + num_chars_to_replace]: # only choose if space not in between
                #     char_index = random.randint(0, len(input_text) - num_chars_to_replace)
                output_text = (
                    input_text[:char_index]
                    + "".join(
                        random.choice(total_chars) for _ in range(num_chars_to_replace)
                    )
                    + input_text[char_index + num_chars_to_replace :]
                )
                lines_list.append(output_text)

            for _ in range(multiplier):
                lines_list.append(input_text)

    random_replace(2)

    return lines_list
