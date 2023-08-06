import re

from chordpro.constants import CHORD_SUFFIXES, ENGLISH_NOTES, GERMAN_NOTES, NEOLATIN_NOTES

_chord_cache = {}
_line_cache = {}


def _get_chord_regex(notes):
    """
    Create the regex for a particular set of notes

    :param notes: The regular expression for a set of valid notes
    :return: An expanded regular expression for valid chords
    """
    chord = notes + CHORD_SUFFIXES
    return '(' + chord + '(/' + chord + ')?)'


def _get_chord_match(notes):
    """
    Construct chord matching regular expression object

    :param notes: The regular expression for a set of valid notes
    :return: A compiled regular expression object
    """
    return re.compile(r'\[' + _get_chord_regex(notes) + r'\]')


def _get_line_match(notes):
    """
    Construct a chord line matching regular expression object

    :param notes: The regular expression for a set of valid notes
    :return: A compiled regular expression object
    """
    return re.compile(r'\[' + _get_chord_regex(notes) + r'\]([\u0080-\uFFFF,\w]*)'
                      r'([\u0080-\uFFFF\w\s\.\,\!\?\;\:\|\"\'\-\_]*)(\Z)?')


def _get_chords_for_notation(notation):
    """
    Get the right chord_match object based on the current chord notation
    """
    if notation not in _chord_cache.keys():
        if notation == 'german':
            _chord_cache[notation] = _get_chord_match(GERMAN_NOTES)
        elif notation == 'neo-latin':
            _chord_cache[notation] = _get_chord_match(NEOLATIN_NOTES)
        else:
            _chord_cache[notation] = _get_chord_match(ENGLISH_NOTES)
    return _chord_cache[notation]


def _get_line_for_notation(notation):
    """
    Get the right chord line match based on the current chord notation
    """
    if notation not in _line_cache.keys():
        if notation == 'german':
            _line_cache[notation] = _get_line_match(GERMAN_NOTES)
        elif notation == 'neo-latin':
            _line_cache[notation] = _get_line_match(NEOLATIN_NOTES)
        else:
            _line_cache[notation] = _get_line_match(ENGLISH_NOTES)
    return _line_cache[notation]
