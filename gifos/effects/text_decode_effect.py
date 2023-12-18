# TODO
# [] resource intensive when 3 chars need to be chosen from large pool
import random


def generate_pattern_lines(
    output_text_len: int,
    num_chars: int,
    count: int,
) -> list:
    chars_list = ["<", ">", "/", "*", " "]
    unwanted_patterns = None
    # unwanted_patterns = ["    ", "**", "<*>", "/ /"]
    output_text_lines = list()
    prev_output_text = ""

    if output_text_len < 5:
        return output_text_lines
    if num_chars > output_text_len - 1:  # need minimum 1 for space
        num_chars = output_text_len - 1

    for _ in range(count):
        while True:
            output_text = "".join(
                random.choice(chars_list) for _ in range(output_text_len)
            )
            if unwanted_patterns and any(
                seq in output_text for seq in unwanted_patterns
            ):
                continue
            num_non_space_chars = len(output_text) - output_text.count(" ")

            if (
                (output_text.count("*") <= 2)
                and (output_text.count(" ") >= 1)
                and (output_text.count("/") >= 1)
                and (output_text.count("<") <= output_text_len)
                and (output_text.count(">") <= output_text_len)
                and (
                    prev_output_text[0:3] in output_text
                    or prev_output_text[1:4] in output_text
                )  # generate similar to last
                and num_non_space_chars == num_chars
            ):
                prev_output_text = output_text
                output_text_lines.append(output_text)
                break

    return output_text_lines


def text_decode_effect_lines(input_text: str, multiplier: int) -> list:
    """Generate a list of text lines with a decoding effect.

    This function generates a list of text lines that simulate a decoding effect. The
    function takes an input text and a multiplier as parameters. The multiplier
    determines the number of times each line is repeated in the output. The function
    randomly replaces characters in the input text with characters from a list to create
    the decoding effect.

    :param input_text: The text to apply the decoding effect to.
    :type input_text: str
    :param multiplier: The number of times each line is repeated in the output.
    :type multiplier: int
    :return: A list of text lines with the decoding effect.
    :rtype: list
    """
    lines_list = list()
    chars_list = ["<", ">", "/", "*", " "]

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
                        random.choice(chars_list) for _ in range(num_chars_to_replace)
                    )
                    + input_text[char_index + num_chars_to_replace :]
                )
                lines_list.append(output_text)

            for _ in range(multiplier):
                lines_list.append(input_text)

    # lines_list += generate_pattern_lines(len(input_text), 3, multiplier)
    # lines_list += generate_pattern_lines(
    #     len(input_text), ((len(input_text) - 3) // 2), multiplier
    # )
    # lines_list += generate_pattern_lines(
    #     len(input_text), ((len(input_text) - 3) // 2) * 2, multiplier
    # )

    for i in range(len(input_text)):  # for each char
        for _ in range(multiplier):
            output_text = generate_pattern_lines(len(input_text), len(input_text), 1)
            output_text = input_text[0 : i + 1] + output_text[0][i + 1 :]
            lines_list.append(output_text)

    random_replace(2)

    return lines_list
