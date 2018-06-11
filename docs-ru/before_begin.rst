
Прежде чем вы начнёте
=====================

Прежде чем вы начнёте, вам потребуются некоторые приготовления.


.. contents::
   :local:

.. highlight:: none

Программное обеспечение
-----------------------

m_Librarian написан на языке Python, так что вам нужно скачать и
установить Python (2.7 или 3.4+). Нужны также библиотеки SQLObject и
m_lib.defenc.


Архивы библиотек
----------------

Данный программный комплекс работает с локальными файлами библиотек, так
что предварительно скачайте некоторые библиотеки. Вот краткий и совсем
не исчерпывающий список для скачивания:

|   Библиотека Flibusta.net [fb2]
|      https://booktracker.org/viewtopic.php?t=46979
|      https://nnm-club.me/forum/viewtopic.php?t=521962
|      http://rus-tor.com/torrent/542970
|   Библиотека Flibusta.net [fb2, usr]
|      https://booktracker.org/viewtopic.php?t=49016
|      https://nnm-club.me/forum/viewtopic.php?t=353958
|      http://rus-tor.com/torrent/543084
|   Библиотека Либрусек (lib.rus.ec) + MyHomeLib [FB2]
|      https://booktracker.org/viewtopic.php?t=1198
|      https://nnm-club.me/forum/viewtopic.php?t=510054
|      http://rus-tor.com/torrent/212528
|   Библиотека Либрусек (lib.rus.ec) [ALL]
|      https://booktracker.org/viewtopic.php?t=79829
|      https://nnm-club.me/forum/viewtopic.php?t=877707

Кроме самих библиотек вам понадобиться найти для них индексы INPX —
m_Librarian пока не научился индексировать архивы библиотек.

Индексы INPX обычно распространяются вместе с программами для работы с
библиотеками, и такие программы есть в архивах по ссылкам выше.
Некоторые индексы можно скачать с сайта одной из таких программ
`MyHomeLib <http://myhomelib.org/>`_:

| http://myhomelib.org/download/inpx/librusec_local_fb2.inpx
| http://myhomelib.org/download/inpx/librusec_local_usr.inpx (не обновляется)
| http://myhomelib.org/download/inpx/librusec_local_all.inpx (не обновляется)
| https://booktracker.org/viewtopic.php?t=64690
| https://booktracker.org/viewtopic.php?t=74487
| https://nnm-club.me/forum/viewtopic.php?t=875907
| http://rus-tor.com/torrent/543085

Файл конфигурации
-----------------

Файл конфигурации по умолчанию ищется в $HOME/.config/ (если у вас
POSIX-совместимая ОС). Файл должен называться ``m_librarian.conf``. Это
должен быть файл в формате ``ini``. В настоящий момент m_librarian
понимает следующие секции и ключи в них::

    [database]
    URI = "DB URI"

    [library]
    path = "путь к архивам библиотеки"

    [download]
    format = "формат имён сохраняемых файлов"

Большинство программ имею опцию `-C|--config config`, которая позволяет
использовать файл произвольный конфигурации.

База данных
-----------

Для работы m_Librarian требуется база данных. m_Librarian может работать
с любой БД, поддерживаемой библиотекой SQLObject. Предпочтительные
варианты: MySQL, PostgreSQL или SQLite. При использовании сервера SQL БД
вам придётся создать самим. Для SQLite файл БД будет создан программой,
так что это наиболее простой способ использования m_Librarian,

Database URI
^^^^^^^^^^^^

Чтобы m_Librarian использовал сервер SQL в файле конфигурации должна
быть секция ``[database]`` с единственным ключом ``URI``. Значением
ключа должно быть Database URI в формате, который понимает SQLObject.
Вот несколько примеров::

   [database]
   URI = mysql://user:password@host/database

   [database]
   URI = postgres://user@host/database

   [database]
   URI = sqlite:///full/path/to/database

Больше примеров есть в файле m_librarian.conf.sample. Детальное описание
DB URI есть в `документации на SQLObject
<http://sqlobject.org/SQLObject.html#declaring-a-connection>`_.

.. vim: set tw=72 :
