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

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '3.3.1'
__CHEETAH_versionTuple__ = (3, 3, 1, 'final', 0)
__CHEETAH_genTime__ = 1721134725.743107
__CHEETAH_genTimestamp__ = 'Tue Jul 16 15:58:45 2024'
__CHEETAH_src__ = 'layout.tmpl'
__CHEETAH_srcLastModified__ = 'Tue Jul 16 15:57:52 2024'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class layout(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(layout, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def respond(self, trans=None):



        ## CHEETAH: main method generated for this template
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
        
        write(u'''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd">
<html>
<!-- THIS PAGE IS AUTOMATICALLY GENERATED USING CheetahTemplate. DO NOT EDIT. -->
<head>
<meta HTTP-Equiv="Content-Type" content="text/html; charset=utf-8">
<title>''')
        _v = VFFSL(SL,"title",True) # u'$title' on line 9, col 8
        if _v is not None: write(_filter(_v, rawExpr=u'$title')) # from line 9, col 8.
        write(u''' \u2014 m_Librarian</title>
<meta name="author" content="Oleg Broytman">
<meta name="copyright" content="&copy; 2018 PhiloSoft Design">
<link rev="made" href="mailto:phd@phdru.name">
<meta name="generator" content="CheetahTemplate">
<meta name="MSSmartTagsPreventParsing" content="TRUE"> <!-- MUST DIE -->
<link rel="stylesheet" type="text/css" media="screen" href="/static/style.css">
</head>
<body bgcolor="#FFFFFF" text="#000000"
      link="#0000bb"  vlink="#551a8b" alink="#ff0000">
<table class="long">
<tr class="long">
  <td style="width: 50%"><p><a href="/">m_Librarian</a></p></td>
  <td style="width: 50%; text-align: right"><a href="/quit">\u0412\u044b\u0445\u043e\u0434</a></td>
</tr>
</table>
''')
        _v = VFFSL(SL,"body",True) # u'$body' on line 25, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$body')) # from line 25, col 1.
        write(u'''
</body>
</html>
''')
        
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

    title = ''

    _mainCheetahMethod_for_layout = 'respond'

## END CLASS DEFINITION

if not hasattr(layout, '_initCheetahAttributes'):
    templateAPIClass = getattr(layout,
                               '_CHEETAH_templateClass',
                               Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(layout)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit https://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=layout()).run()


