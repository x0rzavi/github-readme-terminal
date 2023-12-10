# TODO
# [] resource intensive when 3 chars need to be chosen from large pool
import random


def generatePatternLines(
    outputTextLen: int,
    numChars: int,
    count: int,
) -> list:
    charsList = ["<", ">", "/", "*", " "]
    unwantedPatterns = None
    # unwantedPatterns = ["    ", "**", "<*>", "/ /"]
    outputTextLines = []
    prevOutputText = ""

    if outputTextLen < 5:
        return outputTextLines
    if numChars > outputTextLen - 1:  # need minimum 1 for space
        numChars = outputTextLen - 1

    for _ in range(count):
        while True:
            outputText = "".join(random.choice(charsList) for _ in range(outputTextLen))
            if unwantedPatterns and any(seq in outputText for seq in unwantedPatterns):
                continue
            numNonSpaceChars = len(outputText) - outputText.count(" ")

            if (
                (outputText.count("*") <= 2)
                and (outputText.count(" ") >= 1)
                and (outputText.count("/") >= 1)
                and (outputText.count("<") <= outputTextLen)
                and (outputText.count(">") <= outputTextLen)
                and (
                    prevOutputText[0:3] in outputText
                    or prevOutputText[1:4] in outputText
                )  # generate similar to last
                and numNonSpaceChars == numChars
            ):
                prevOutputText = outputText
                outputTextLines.append(outputText)
                break

    return outputTextLines


def textDecodeEffectLines(inputText: str, multiplier: int) -> list:
    linesList = []
    charsList = ["<", ">", "/", "*", " "]

    def randomReplace():
        numCharsToReplace = 2
        for _ in range(multiplier):  # randomly change consecutive chars
            charIndex = random.randint(0, len(inputText) - numCharsToReplace)
            # while " " in inputText[charIndex : charIndex + numCharsToReplace]: # only choose if space not in between
            #     charIndex = random.randint(0, len(inputText) - numCharsToReplace)
            outputText = (
                inputText[:charIndex]
                + "".join(random.choice(charsList) for _ in range(numCharsToReplace))
                + inputText[charIndex + numCharsToReplace :]
            )
            linesList.append(outputText)

        for _ in range(multiplier):
            linesList.append(inputText)

    # linesList += generatePatternLines(len(inputText), 3, multiplier)
    # linesList += generatePatternLines(
    #     len(inputText), ((len(inputText) - 3) // 2), multiplier
    # )
    # linesList += generatePatternLines(
    #     len(inputText), ((len(inputText) - 3) // 2) * 2, multiplier
    # )
    for i in range(len(inputText)):  # for each char
        for _ in range(multiplier):
            outputText = generatePatternLines(len(inputText), len(inputText), 1)
            outputText = inputText[0 : i + 1] + outputText[0][i + 1 :]
            linesList.append(outputText)

    randomReplace()
    randomReplace()

    return linesList
