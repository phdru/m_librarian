
Прежде чем вы начнёте
=====================

Прежде чем вы начнёте, вам потребуются некоторые приготовления.


.. contents::
   :local:


Программное обеспечение
-----------------------

m_Librarian написан на языке Python, так что вам нужно скачать и
установить Python 2.7. Нужны также библиотеки SQLObject и m_lib.


Архивы библиотек
----------------

Данный программный комплекс работает с локальными файлами библиотек, так
что предварительно скачайте некоторые библиотеки. Вот краткий и совсем
не исчерпывающий список для скачивания:

| http://torrent.rus.ec/index.php?c=3
| http://booktracker.org/index.php?c=18
| https://nnm-club.me/forum/viewtopic.php?t=353958
| https://nnm-club.me/forum/viewtopic.php?t=510054
| https://nnm-club.me/forum/viewtopic.php?t=521962
| https://nnm-club.me/forum/viewtopic.php?t=877707

Кроме самих библиотек вам понадобиться найти для них индексы INPX —
m_Librarian пока не научился индексировать архивы библиотек.

Индексы INPX обычно распространяются вместе с программами для работы с
библиотеками, и такие программы есть в архивах по ссылкам выше.
Некоторые индексы можно скачать с сайта одной из таких программ
`MyHomeLib <http://home-lib.net/>`_:

| http://home-lib.net/download/inpx/librusec_local_fb2.inpx
| http://home-lib.net/download/inpx/librusec_local_usr.inpx
| http://home-lib.net/download/inpx/librusec_local_all.inpx


База данных
-----------

Для работы m_Librarian требуется база данных. m_Librarian может работать
с любой БД, поддерживаемой библиотекой SQLObject. Предпочтительные
варианты: MySQL, PostgreSQL или SQLite. При использовании сервера SQL БД
вам придётся создать самим. Для SQLite файл БД будет создан программой,
так что это наиболее простой способ использования m_Librarian,


.. vim: set tw=72 :
