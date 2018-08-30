# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se)
# *
# * SciLifeLab, Stockholm University
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import os

import pyworkflow.em
from pyworkflow.utils import Environ

from constants import BSOFT_HOME

_logo = "bsoft_logo.png"
_references = ['Heymann2007']


class Plugin(pyworkflow.em.Plugin):
    _homeVar = BSOFT_HOME
    _pathVars = [BSOFT_HOME]
    _supportedVersions = ['1.9.0']

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar(BSOFT_HOME, 'bsoft-1.9.0')

    @classmethod
    def getEnviron(cls, xmippFirst=True):
        """ Setup the environment variables needed to launch bsoft. """
        environ = Environ(os.environ)
        pos = Environ.BEGIN if xmippFirst else Environ.END
        environ.update({
            'PATH': os.path.join(os.environ[BSOFT_HOME], 'bin'),
            'BSOFT': os.environ[BSOFT_HOME]
        }, position=pos)
        return environ

    @classmethod
    def getProgram(cls, program):
        """ Return the program binary that will be used. """
        if BSOFT_HOME not in os.environ:
            return None
        cmd = cls.getHome('bin', program)
        return str(cmd)


pyworkflow.em.Domain.registerPlugin(__name__)
