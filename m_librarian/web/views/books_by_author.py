#!/usr/bin/env python
# -*- coding: utf-8 -*-




##################################################
## DEPENDENCIES
import sys
import os
import os.path
try:
    import builtins as builtin
except ImportError:
    import __builtin__ as builtin
from os.path import getmtime, exists
import time
import types
from Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion
from Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple
from Cheetah.Template import Template
from Cheetah.DummyTransaction import *
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers
from Cheetah.compat import unicode
from views.layout import layout

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_genTime__ = 1523141375.719046
__CHEETAH_genTimestamp__ = 'Sun Apr  8 01:49:35 2018'
__CHEETAH_src__ = 'books_by_author.tmpl'
__CHEETAH_srcLastModified__ = 'Sun Apr  8 01:49:05 2018'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class books_by_author(layout):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(books_by_author, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def body(self, **KWS):



        ## CHEETAH: generated from #def body at line 4, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''<h1>''')
        _v = VFFSL(SL,"title",True) # u'$title' on line 5, col 5
        if _v is not None: write(_filter(_v, rawExpr=u'$title')) # from line 5, col 5.
        write(u'''</h1>

''')
        if VFFSL(SL,"books",True): # generated from line 7, col 1
            write(u'''  <table>
''')
            series = None
            for book in VFFSL(SL,"books",True): # generated from line 10, col 3
                if VFFSL(SL,"book.series",True) != VFFSL(SL,"series",True): # generated from line 11, col 3
                    series = VFFSL(SL,"book.series",True)
                    if VFFSL(SL,"book.series",True): # generated from line 13, col 3
                        write(u'''  <tr>
    <td colspan=2>\u0421\u0435\u0440\u0438\u044f: ''')
                        _v = VFFSL(SL,"series",True) # u'$series' on line 15, col 26
                        if _v is not None: write(_filter(_v, rawExpr=u'$series')) # from line 15, col 26.
                        write(u'''</td>
  </tr>
''')
                    else: # generated from line 17, col 3
                        write(u'''  <tr>
    <td colspan=2>\u0412\u043d\u0435 \u0441\u0435\u0440\u0438\u0439</td>
  </tr>
''')
                write(u'''  <tr>
    <td class="numeric">''')
                _v = VFFSL(SL,"book.ser_no",True) # u'$book.ser_no' on line 24, col 25
                if _v is not None: write(_filter(_v, rawExpr=u'$book.ser_no')) # from line 24, col 25.
                write(u'''</td>
    <td><a href="/download/''')
                _v = VFFSL(SL,"book.id",True) # u'$book.id' on line 25, col 28
                if _v is not None: write(_filter(_v, rawExpr=u'$book.id')) # from line 25, col 28.
                write(u'''/">''')
                _v = VFFSL(SL,"book.title",True) # u'$book.title' on line 25, col 39
                if _v is not None: write(_filter(_v, rawExpr=u'$book.title')) # from line 25, col 39.
                write(u'''</a></td>
  </tr>
''')
            write(u'''  </table>
''')
        else: # generated from line 29, col 1
            write(u'''  <p>\u041d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u043e \u043d\u0438 \u043e\u0434\u043d\u043e\u0439 \u043a\u043d\u0438\u0433\u0438!</p>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def writeBody(self, **KWS):



        ## CHEETAH: main method generated for this template
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## CHEETAH GENERATED ATTRIBUTES


    _CHEETAH__instanceInitialized = False

    _CHEETAH_version = __CHEETAH_version__

    _CHEETAH_versionTuple = __CHEETAH_versionTuple__

    _CHEETAH_genTime = __CHEETAH_genTime__

    _CHEETAH_genTimestamp = __CHEETAH_genTimestamp__

    _CHEETAH_src = __CHEETAH_src__

    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__

    title = 'Список книг автора $author.fullname'

    _mainCheetahMethod_for_books_by_author = 'writeBody'

## END CLASS DEFINITION

if not hasattr(books_by_author, '_initCheetahAttributes'):
    templateAPIClass = getattr(books_by_author,
                               '_CHEETAH_templateClass',
                               Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(books_by_author)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=books_by_author()).run()


