# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se)
# *
# * SciLifeLab, Stockholm University
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
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

import pwem
from pyworkflow.utils import Environ

from bsoft.constants import BSOFT_HOME, V2_0_7, V1_9_0

__version__ = '3.0.5'
_logo = "bsoft_logo.png"
_references = ['Heymann2007', 'Heymann2018']


class Plugin(pwem.Plugin):
    _homeVar = BSOFT_HOME
    _pathVars = [BSOFT_HOME]
    _supportedVersions = [V2_0_7]

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar(BSOFT_HOME, 'bsoft-2.0.7')

    @classmethod
    def getEnviron(cls, bsoftVersion=None):
        """ Setup the environment variables needed to launch bsoft.
        :param bsoftVersion (optional) pass a version to be used,
        otherwise will choose default value for BSOFT_HOME"""
        environ = Environ(os.environ)

        home = cls.getHomeFromVersion(bsoftVersion)

        environ.update({
            'PATH': os.path.join(home, 'bin'),
            'BSOFT': home
        }, position=Environ.BEGIN)
        return environ

    @classmethod
    def getHomeFromVersion(self, bsoftVersion):

        return Plugin.getHome() if bsoftVersion is None else os.path.join(pwem.Config.EM_HOME, bsoftVersion)

    @classmethod
    def getProgram(cls, program, bsoftVersion=None):
        """ Return the program binary that will be used. """
        return os.path.join(cls.getHomeFromVersion(bsoftVersion),"bin", program)

    @classmethod
    def defineBinaries(cls, env):

        env.addPackage('bsoft', version='1.9.0',
                       tar='bsoft1_9_0_Fedora_20.tgz',
                       default=True)

        env.addPackage('bsoft', version='2.0.7',
			            url="https://lsbr.niams.nih.gov/bsoft/bsoft2_0_7_CentOS_7.7.1908.tgz",
                        buildDir = "bsoft",
                        default=True)

