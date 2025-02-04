readmdict.py
------------
readmdict.py is an example implementation in Python. This program can read/extract mdx/mdd files.

.. note:: python-lzo is required to read mdx files created with engine 1.2.
   Get Windows version from http://www.lfd.uci.edu/~gohlke/pythonlibs/#python-lzo

It can be used as a command line tool. Suppose one has oald8.mdx and oald8.mdd::

    $ python readmdict.py -x oald8.mdx

This will creates *oald8.txt* dictionary file and creates a folder *data* for images, pronunciation audio files.

On Windows, one can also double click it and select the file in the popup dialog.

Or as a module::

    In [1]: from readmdict import MDX, MDD

Read MDX file and print the first entry::

    In [2]: mdx = MDX('oald8.mdx')

    In [3]: items = mdx.items()

    In [4]: items.next()
    Out[4]:
    ('A',
     '<span style=\'display:block;color:black;\'>.........')
``mdx`` is an object having all info from a MDX file. ``items`` is an iterator producing 2-item tuples.
Of each tuple, the first element is the entry text and the second is the explanation. Both are UTF-8 encoded strings.

Read MDD file and print the first entry::

    In [5]: mdd = MDD('oald8.mdd')

    In [6]: items = mdd.items()

    In [7]: items = mdd.next()
    Out[7]: 
    (u'\\pic\\accordion_concertina.jpg',
    '\xff\xd8\xff\xe0\x00\x10JFIF...........')

``mdd`` is an object having all info from a MDD file. ``items`` is an iterator producing 2-item tuples. 
Of each tuple, the first element is the file name and the second element is the corresponding file content.
The file name is encoded in UTF-8. The file content is a plain bytes array.
