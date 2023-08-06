import os


def render(song, verse_upper=False):
    """Render a song to a text file"""
    nl = os.linesep
    bl = nl + nl
    rendered_verses = []
    for verse in song.verse_order:
        verse_title = verse.title.upper() if verse_upper else verse.title
        rendered_lines = [verse_title + ':']
        for line in verse.lines:
            rendered_chords = []
            rendered_syllables = []
            for word_counter, word in enumerate(line.words):
                is_last_word = (word_counter + 1) == len(line.words)
                for syll_counter, syllable in enumerate(word.syllables):
                    is_last_syllable = (syll_counter + 1) == len(word.syllables)
                    padding = max(len(syllable.syllable), len(syllable.chord or ''))
                    if is_last_syllable and not is_last_word:
                        padding += 1
                    elif syllable.chord and not syllable.syllable:
                        padding += 1
                    rendered_chords.append('{chord:^{padding}}'.format(chord=syllable.chord or '', padding=padding))
                    rendered_syllables.append('{syllable:<{padding}}'.format(syllable=syllable.syllable,
                                                                             padding=padding))
            rendered_lines.append(''.join(rendered_chords))
            rendered_lines.append(''.join(rendered_syllables))
        rendered_verses.append(nl.join(rendered_lines))
    title = song.metadata.get('title') or 'Song'
    artist = song.metadata.get('artist') or song.metadata.get('composer') or ''
    return nl.join([title, artist, '', bl.join(rendered_verses)]) + nl
