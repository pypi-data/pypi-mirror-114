python-chordpro
===============

``python-chordpro`` is a ChordPro parser, written in Python. The main difference between this module
and other similar libraries is that ``python-chordpro`` parses ChordPro files down to the syllable
level, enabling finer-grained control of the formatted output.

.. warning::

   This package is still in development. Only a subset of ChordPro is currently supported, and
   some key features are missing, like displaying song metadata.

Installation
------------

You can use ``pip`` to install ``python-chordpro``::

   $ pip install python-chordpro

Example Usage
-------------

.. code-block:: python

   from chordpro import Song

   song = Song('path/to/song.chordpro')

   for verse in song.verses:
       print(verse.title)

Rendering
---------

``python-chordpro`` comes with two renders, HTML and Text.

.. code-block:: python

   from chordpro.renderers.html import render

   print(render(song))


Command Line Interface
----------------------

``python-chordpro`` also ships with a built-in command line interface which will read a ChordPro
file and then render it using either the text or HTML renderer.

For example::

   $ python-chordpro path/to/song.chordpro -f text -o song.txt

License
-------

``python-chordpro`` is licensed under the MIT license. See the LICENSE file for more information.
