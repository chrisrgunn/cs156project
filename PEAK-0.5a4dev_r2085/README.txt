PEAK Release 0.5 alpha 4

 Copyright (C) 1996-2004 by Phillip J. Eby and Tyler C. Sarna.
 All rights reserved.  This software may be used under the same terms
 as Zope or Python.  THERE ARE ABSOLUTELY NO WARRANTIES OF ANY KIND.
 Code quality varies between modules, from "beta" to "experimental
 pre-alpha".  :)

 Package Description

    PEAK is the "Python Enterprise Application Kit". If you develop
    "enterprise" applications with Python, or indeed almost any sort of
    application with Python, PEAK may help you do it faster, easier, on a
    larger scale, and with fewer defects than ever before. The key is
    component-based development, on a reliable infrastructure.

    PEAK tools can be used with other "Python Enterprise" frameworks such as
    Zope, Twisted, and the Python DBAPI to construct web-based, GUI, or
    command-line applications, interacting with any kind of storage, or with
    no storage at all.  Whatever the application type, PEAK can help you put
    it together.

 Package Features

   Far too many to list even briefly here: see FEATURES.txt for a very high
   level overview.















 Known Issues and Risks of this Version

   This is ALPHA software.  Although much of the system is extensively
   tested by a battery of automated tests, it may contain bugs, especially
   in areas not covered by the test suites.  Also, many system interfaces
   are still subject to change.

   PEAK includes early copies of Zope X3's 'ZConfig' and 'persistence'
   packages, which have had - and may continue to have - significant
   implementation changes.  We will be tracking Zope X3 periodically, but
   can't guarantee compatibility with arbitrary (e.g. CVS) versions of
   Zope X3.

   Documentation at present is limited, and scattered.  The principal
   documentation is an API reference generated from the code's lengthy
   docstrings (which usually contain motivating examples for using that
   class, method, or function).  The mailing list and its archives
   provide a wealth of information on actual usage scenarios,
   recommended approaches, etc.  There is also the beginnings of a
   tutorial on using the component binding package.





















 Third-Party Software Included with PEAK

     All third-party software included with PEAK are understood by PEAK's
     authors to be distributable under terms comparable to those PEAK is
     offered under.  However, it is up to you to understand any obligations
     those licenses may impose upon you.  For your reference, here are the
     third-party packages and where to find their license terms:

     The included 'pyexpat', 'doctest', 'optparse', and 'textwrap' modules in
     'peak.util' are from Python 2.4, and are included for backward
     compatibility in Python 2.2 and 2.3.  See the Python license for license
     details.

     The 'expat' XML parser is Copyright (c) 1998, 1999, 2000 Thai Open Source
     Software Center Ltd and Clark Cooper, and Copyright (c) 2001, 2002, 2003
     Expat maintainers.  See the 'COPYING' file in 'src/expat' for details of
     its license.

 Installation Instructions

    Please see the INSTALL.txt file.




















