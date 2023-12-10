import random
import string

upperCase = string.ascii_uppercase
lowerCase = string.ascii_lowercase
specialChars = string.punctuation


def hackedTextEffectLines(
    inputIext: str, multiplier: int, onlyUpper: bool = True
) -> list:
    linesList = list()
    if onlyUpper:
        totalChars = upperCase + specialChars
    else:
        totalChars = upperCase + lowerCase + specialChars

    for i in range(len(inputIext) * multiplier):  # no of lines
        outputText = ""
        for j in range(len(inputIext)):  # for each char
            if i < 3 or inputIext[j] == " ":
                outputText += " " if inputIext[j] == " " else random.choice(totalChars)
            elif i // multiplier >= j:
                outputText += inputIext[j]
            else:
                outputText += random.choice(totalChars)
        linesList.append(outputText)

    numCharsToReplace = 2
    for _ in range(multiplier):  # randomly change consecutive chars
        charIndex = random.randint(0, len(inputIext) - numCharsToReplace)
        # while " " in inputIext[charIndex : charIndex + numCharsToReplace]: # only choose if space not in between
        #     charIndex = random.randint(0, len(inputIext) - numCharsToReplace)
        outputText = (
            inputIext[:charIndex]
            + "".join(random.choice(totalChars) for _ in range(numCharsToReplace))
            + inputIext[charIndex + numCharsToReplace :]
        )
        linesList.append(outputText)

    for _ in range(multiplier):
        linesList.append(inputIext)

    return linesList
