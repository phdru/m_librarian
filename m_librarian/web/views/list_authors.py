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
from m_librarian.translations import translations
from views.layout import layout
from views.search_authors_form import search_authors_form

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '3.3.1'
__CHEETAH_versionTuple__ = (3, 3, 1, 'final', 0)
__CHEETAH_genTime__ = 1718725815.054143
__CHEETAH_genTimestamp__ = 'Tue Jun 18 18:50:15 2024'
__CHEETAH_src__ = 'list_authors.tmpl'
__CHEETAH_srcLastModified__ = 'Tue Jun 18 18:50:12 2024'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class list_authors(layout):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(list_authors, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def body(self, **KWS):



        ## CHEETAH: generated from #def body at line 5, col 1.
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
        
        write(u'''<h1>\u041f\u043e\u0438\u0441\u043a \u0430\u0432\u0442\u043e\u0440\u043e\u0432</h1>
''')
        _v = VFFSL(SL,"search_authors_form",False)(searchList=VFFSL(SL,"searchList",True)) # u'$search_authors_form(searchList=$searchList)' on line 8, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$search_authors_form(searchList=$searchList)')) # from line 8, col 1.
        write(u'''

<h1>''')
        _v = VFFSL(SL,"title",True) # u'$title' on line 10, col 5
        if _v is not None: write(_filter(_v, rawExpr=u'$title')) # from line 10, col 5.
        write(u'''</h1>

''')
        if VFFSL(SL,"authors",True): # generated from line 12, col 1
            _orig_filter_63533534 = _filter
            filterName = u'WebSafe'
            if "WebSafe" in self._CHEETAH__filters:
                _filter = self._CHEETAH__currentFilter = self._CHEETAH__filters[filterName]
            else:
                _filter = self._CHEETAH__currentFilter = \
			self._CHEETAH__filters[filterName] = getattr(self._CHEETAH__filtersLib, filterName)(self).filter
            write(u'''  <table>
  <tr>
  ''')
            if False:
                _
            _ = VFFSL(SL,"getattr",False)(VFFSL(SL,"translations",True), 'ugettext', None) or VFFSL(SL,"translations.gettext",True)
            for column in VFFSL(SL,"columns",True): # generated from line 17, col 3
                write(u'''    <td style="text-align: center">''')
                if False:
                    _(VFFSL(SL,"column",True))
                _v = VFFSL(SL,"_",False)(VFFSL(SL,"column",True)) # u'$_($column)' on line 18, col 36
                if _v is not None: write(_filter(_v, rawExpr=u'$_($column)')) # from line 18, col 36.
                write(u'''</td>
''')
            write(u'''  </tr>
''')
            for author in VFFSL(SL,"authors",True): # generated from line 21, col 3
                write(u'''  <tr>
''')
                for column in VFFSL(SL,"columns",True): # generated from line 23, col 3
                    if VFFSL(SL,"column",True) == 'count': # generated from line 24, col 5
                        style = ' style="text-align: right; width: 5ex"'
                    else: # generated from line 26, col 5
                        style = ''
                    write(u'''    <td''')
                    _v = VFFSL(SL,"style",True) # u'$style' on line 29, col 8
                    if _v is not None: write(_filter(_v, rawExpr=u'$style')) # from line 29, col 8.
                    write(u'''><a href="/books-by-author/''')
                    _v = VFFSL(SL,"author.id",True) # u'$author.id' on line 29, col 41
                    if _v is not None: write(_filter(_v, rawExpr=u'$author.id')) # from line 29, col 41.
                    write(u'''/">
    ''')
                    _v = VFFSL(SL,"unicode",False)(VFFSL(SL,"getattr",False)(VFFSL(SL,"author",True), VFFSL(SL,"column",True)) or '') # u"$unicode($getattr($author, $column) or '')" on line 30, col 5
                    if _v is not None: write(_filter(_v, rawExpr=u"$unicode($getattr($author, $column) or '')")) # from line 30, col 5.
                    write(u'''
    </a></td>
''')
                write(u'''  </tr>
''')
            write(u'''  </table>
''')
            _filter = self._CHEETAH__currentFilter = _orig_filter_63533534
        else: # generated from line 37, col 1
            write(u'''  <p>\u041d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u043e \u043d\u0438 \u043e\u0434\u043d\u043e\u0433\u043e \u0430\u0432\u0442\u043e\u0440\u0430!</p>
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

    title = 'Список авторов'

    _mainCheetahMethod_for_list_authors = 'writeBody'

## END CLASS DEFINITION

if not hasattr(list_authors, '_initCheetahAttributes'):
    templateAPIClass = getattr(list_authors,
                               '_CHEETAH_templateClass',
                               Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(list_authors)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit https://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=list_authors()).run()


