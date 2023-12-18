"""This module initializes the gifos.effects package and provides access to its
functions.

The gifos.effects package contains functions for generating text effects.
These functions include `text_decode_effect_lines` and `text_scramble_effect_lines`.

Functions:
    text_decode_effect_lines: Generate a list of text lines with a decoding effect.
    text_scramble_effect_lines: Generate a list of text lines with a scramble effect.
"""

from gifos.effects.text_decode_effect import text_decode_effect_lines
from gifos.effects.text_scramble_effect import text_scramble_effect_lines

__all__ = ["text_decode_effect_lines", "text_scramble_effect_lines"]
