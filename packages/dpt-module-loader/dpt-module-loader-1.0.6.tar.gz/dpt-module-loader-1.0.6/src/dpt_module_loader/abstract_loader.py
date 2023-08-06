# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;module_loader

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.0.6
dpt_module_loader/abstract_loader.py
"""

from weakref import proxy

from dpt_runtime.exceptions import NotImplementedException

class AbstractLoader(object):
    """
"AbstractLoader" provides common methods for module loaders.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: module_loader
:since:      v1.0.6
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = ( )
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _log_handler = None
    """
The log handler is called whenever debug messages should be logged or errors
happened.
    """

    @staticmethod
    def get_module(package_module, autoload = True):
        """
Get the module for the specified package and module name.

:param package_module: Package and module name
:param autoload: True to load the module automatically if not done already.

:return: (object) Python module; None on error
:since:  v1.0.6
        """

        raise NotImplementedException()
    #

    @staticmethod
    def is_defined(package_module, autoload = True):
        """
Checks if the specified package, module and class name is defined or can be
resolved after auto loading it.

:param package_module: Package and module name
:param autoload: True to load the class module automatically if not done
                 already.

:return: (bool) True if defined or resolvable
:since:  v1.0.6
        """

        raise NotImplementedException()
    #

    @staticmethod
    def reload(package_module, clear_caches = True):
        """
Reloads the the specified package module.

:param package_module: Package and module name
:param clear_caches: True to clear import caches before reloading

:return: (object) Reloaded module on success
:since:  v1.0.6
        """

        raise NotImplementedException()
    #

    @staticmethod
    def set_log_handler(log_handler):
        """
Sets the log handler.

:param log_handler: Log handler to use

:since: v1.0.6
        """

        AbstractLoader._log_handler = proxy(log_handler)
    #
#
