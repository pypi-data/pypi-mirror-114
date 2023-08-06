import re

from hyphen import Hyphenator

from chordpro.constants import KNOWN_DIRECTIVES, KNOWN_VERSE_TYPES

DIRECTIVE = re.compile(r'\{(.*?): *(.*?)\}')
START_OF = re.compile(r'\{start_of_(' + '|'.join(KNOWN_VERSE_TYPES) + r')(: *(.*?))?\}')
END_OF = re.compile(r'\{end_of_(' + '|'.join(KNOWN_VERSE_TYPES) + r')\}')
CHORUS_MARKER = re.compile(r'\{chorus(: *(.*?))?\}')
CHORD_WORD = re.compile(r'(.*?)\[(.*?)\]')
HYPHEN_CACHE = {}
SYLLABLE_EXCEPTIONS = {
    'outer': ['out', 'er']
}


class MismatchedVerseType(Exception):

    def __init__(self, line_number, expected_type):
        super().__init__('Mismatched verse type on line {}, expected {}'.format(line_number, expected_type))


class Directive(object):

    def __init__(self, line=None):
        self.directive = None
        self.info = None
        if line:
            self.parse(line)

    def parse(self, line):
        """Parse a directive line and return a Directive object"""
        match = DIRECTIVE.match(line)
        if not match:
            return None
        for known_directive in KNOWN_DIRECTIVES:
            if match.group(1) in known_directive:
                self.directive = match.group(1)
                self.info = match.group(2)

    @staticmethod
    def is_directive(line):
        """Check if a line in a file contains a directive"""
        match = DIRECTIVE.match(line)
        if match:
            for known_directive in KNOWN_DIRECTIVES:
                if match.group(1) in known_directive:
                    return True
        return False


class Syllable(object):
    def __init__(self, syllable, chord=None):
        self.syllable = syllable
        self.chord = chord


class Word(object):

    def __init__(self, word=None):
        self.syllables = []
        if word:
            self.parse(word)

    def parse(self, word):
        """Parse a word into syllables with chords.

        1. Split word by chords
        2. Rejoin word, split into syllables
        3. Track down syllable before chord
        4. Add chord to syllable
        """
        word_parts = []
        chords = ['']
        match = CHORD_WORD.match(word)
        while match:
            word_parts.append(match.group(1))
            chords.append(match.group(2))
            word = word.replace(match.group(0), '')
            match = CHORD_WORD.match(word)
        # If there are any left over portions, just add them as the rest of the word
        word_parts.append(word)
        whole_word = ''.join(word_parts)
        self.syllables = []
        if whole_word in SYLLABLE_EXCEPTIONS:
            # words with a 2-letter ending syllable currently do not get recognised by PyHyphen
            sylls = SYLLABLE_EXCEPTIONS[whole_word]
        else:
            if 'en_US' not in HYPHEN_CACHE:
                HYPHEN_CACHE['en_US'] = Hyphenator('en_US')
            if 'en_GB' not in HYPHEN_CACHE:
                HYPHEN_CACHE['en_GB'] = Hyphenator('en_GB')
            hyphenator = HYPHEN_CACHE['en_US']
            # Do a fallback for en_GB
            if not hyphenator.pairs(whole_word):
                if HYPHEN_CACHE['en_GB'].pairs(whole_word):
                    hyphenator = HYPHEN_CACHE['en_GB']
            sylls = hyphenator.syllables(whole_word)
        if not sylls:
            sylls = [whole_word]
        for syll in sylls:
            syllable = Syllable(syll)
            can_consume = False
            for idx, part in enumerate(word_parts):
                if part.startswith(syll):
                    can_consume = True
                    syllable.chord = chords[idx]
                    break
            self.syllables.append(syllable)
            if can_consume:
                word_parts = word_parts[idx + 1:]
                chords = chords[idx + 1:]
        # Process any left over chords, they're trailing chords
        for chord in chords:
            self.syllables.append(Syllable('', chord))


class Line(object):

    def __init__(self, line=None):
        if line:
            words = line.split(' ')
            # Split trailing chords into their own "words"
            last_word = words[-1]
            trailing_chords = []
            for part in last_word.split('['):
                if not part:
                    continue
                if part.split(']')[-1] == '':
                    trailing_chords.append('[{}]'.format(part.split(']')[0]))
            # remove chords from last word
            for chord in trailing_chords:
                last_word = last_word.replace(chord, '')
            # replace last word, and append trailing chords as separate words
            words[-1] = last_word
            words.extend(trailing_chords)
            self.words = [Word(word) for word in words]
        else:
            self.words = []


class Verse(object):

    def __init__(self, type_, title=None, content=None):
        self.type_ = type_
        self.title = title or type_.title()
        self.lines = [Line(line) for line in content.splitlines()] if content else []

    def add_line(self, line):
        self.lines.append(Line(line))

    @classmethod
    def parse(cls, line):
        """Parse the line into a verse type"""
        match = START_OF.match(line)
        verse = cls(match.group(1))
        if len(match.groups()) > 1:
            verse.title = match.group(3) or match.group(1).title()
        return verse

    @staticmethod
    def is_start_of_verse(line):
        return START_OF.match(line) is not None

    @staticmethod
    def is_end_of_verse(line, type_=None):
        match = END_OF.match(line)
        if not type_:
            return match is not None
        return match.group(1) == type_

    @staticmethod
    def is_chorus_marker(line):
        return line.strip().startswith('{chorus')

    @staticmethod
    def get_chorus_from_marker(line):
        match = CHORUS_MARKER.match(line)
        if not match:
            return None
        if len(match.groups()) > 1:
            return match.group(2)


class Metadata(object):

    def __init__(self):
        self._directives = {}

    def add(self, directive):
        self._directives[directive.directive] = directive

    def get(self, key):
        """Grab the title from the title directive"""
        return self._directives[key].info if self._directives.get(key) else None


class Song(object):

    def __init__(self, filename=None):
        self.filename = filename
        if self.filename:
            self.parse(self.filename)

    def parse(self, filename):
        self.metadata = Metadata()
        self.verses = []
        self.verse_order = []
        with open(filename) as song_file:
            is_verse = False
            current_verse = None
            for line_number, line in enumerate(song_file):
                if Directive.is_directive(line):
                    self.metadata.add(Directive(line))
                elif Verse.is_start_of_verse(line):
                    is_verse = True
                    current_verse = Verse.parse(line)
                    self.verse_order.append(current_verse)
                elif Verse.is_end_of_verse(line):
                    if not Verse.is_end_of_verse(line, current_verse.type_):
                        raise MismatchedVerseType(line_number, current_verse.type_)
                    self.verses.append(current_verse)
                    is_verse = False
                    current_verse = None
                elif is_verse:
                    current_verse.add_line(line.strip())
                elif Verse.is_chorus_marker(line):
                    chorus_name = Verse.get_chorus_from_marker(line)
                    for verse in self.verses[::-1]:
                        if verse.title == chorus_name or verse.type_ == "chorus":
                            self.verse_order.append(verse)
                            break
