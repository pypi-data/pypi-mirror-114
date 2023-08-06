CHORD = '<td class="chord">{}</td>'
SYLLB = '<td class="syllable">{}</td>'
LINE = '<table class="line" border="0" cellpadding="0" cellspacing="0"><tr class="chords-line">{}</tr><tr ' \
    'class="lyrics-line">{}</tr></table>'
VERSE = '''<section class="verse">
<h4 class="verse-name {verse_type}">{verse_name}</h4>
<div class="verse-body">
{verse_body}
</div>
</section>'''
TITLE = '<section class="metadata"><h1 class="title">{title}</h1><h3 class="artist">{artist}</h3></section>'
HTML = '''<html>
<head>
  <title>{title}</title>
  <style>
  h4.verse-name {{ font-weight: normal; }}
  .verse-name {{ margin-bottom: 0; }}
  .verse-body {{ padding-left: 2rem; }}
  .chord {{ text-align: center; }}
  {styles}
  </style>
</head>
<body>
{body}
</body>
</html>'''
STYLES = {
    'verse_name_bold': '.verse-name { font-weight: bold !important; }',
    'verse_upper': '.verse-name { text-transform: uppercase; }',
    'chord_bold': '.chord { font-weight: bold; }'
}


def render(song, verse_upper=False, verse_name_bold=False, chord_bold=False):
    """Render a song to HTML"""
    rendered_verses = []
    for verse in song.verse_order:
        rendered_lines = []
        for line in verse.lines:
            rendered_chords = []
            rendered_syllables = []
            for word_counter, word in enumerate(line.words):
                is_last_word = (word_counter + 1) == len(line.words)
                for syll_counter, syllable in enumerate(word.syllables):
                    is_last_syllable = (syll_counter + 1) == len(word.syllables)
                    rendered_chords.append(CHORD.format(syllable.chord or '&nbsp;'))
                    rendered_syllables.append(SYLLB.format(
                        syllable.syllable + ('&nbsp;' if is_last_syllable and not is_last_word else '')))
            rendered_lines.append(LINE.format(''.join(rendered_chords), ''.join(rendered_syllables)))
        rendered_verses.append(VERSE.format(verse_type=verse.type_ or '', verse_name=verse.title,
                                            verse_body='\n'.join(rendered_lines)))
    title = song.metadata.get('title') or 'Song'
    metadata = TITLE.format(title=title, artist=song.metadata.get('artist') or song.metadata.get('composer') or '')
    body = metadata + '\n' + '\n'.join(rendered_verses)
    styles = ''
    if verse_name_bold:
        styles += STYLES['verse_name_bold'] + '\n'
    if verse_upper:
        styles += STYLES['verse_upper'] + '\n'
    if chord_bold:
        styles += STYLES['chord_bold'] + '\n'
    return HTML.format(title=title, body=body, styles=styles)
