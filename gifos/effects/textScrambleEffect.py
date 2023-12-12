import random
import string

upperCase = string.ascii_uppercase
lowerCase = string.ascii_lowercase
specialChars = string.punctuation


def textScrambleEffectLines(
    inputText: str,
    multiplier: int,
    onlyUpper: bool = False,
    includeSpecial: bool = True,
) -> list:
    linesList = list()
    if onlyUpper:
        totalChars = upperCase
    else:
        totalChars = upperCase + lowerCase
    if includeSpecial:
        totalChars += specialChars

    for i in range(len(inputText) * multiplier):  # no of lines
        outputText = ""
        for j in range(len(inputText)):  # for each char
            if i < multiplier or inputText[j] == " ":
                outputText += " " if inputText[j] == " " else random.choice(totalChars)
            elif i // multiplier >= j:
                outputText += inputText[j]
            else:
                outputText += random.choice(totalChars)
        linesList.append(outputText)

    def randomReplace():
        numCharsToReplace = 2
        for _ in range(multiplier):  # randomly change consecutive chars
            charIndex = random.randint(0, len(inputText) - numCharsToReplace)
            # while " " in inputText[charIndex : charIndex + numCharsToReplace]: # only choose if space not in between
            #     charIndex = random.randint(0, len(inputText) - numCharsToReplace)
            outputText = (
                inputText[:charIndex]
                + "".join(random.choice(totalChars) for _ in range(numCharsToReplace))
                + inputText[charIndex + numCharsToReplace :]
            )
            linesList.append(outputText)

        for _ in range(multiplier):
            linesList.append(inputText)

    randomReplace()
    randomReplace()

    return linesList
