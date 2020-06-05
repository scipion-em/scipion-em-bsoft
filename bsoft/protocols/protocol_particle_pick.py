# **************************************************************************
# *
# * Authors:     Jose Gutierrez Tabuenca (jose.gutierrez@cnb.csic.es) [1]
# *              J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se) [2]
# *
# * [1] Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# * [2] SciLifeLab, Stockholm University
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

from os.path import abspath, basename

from pwem.protocols import ProtParticlePicking
from pyworkflow.protocol.params import FloatParam
from pyworkflow.utils.properties import Message
from pyworkflow.gui.dialog import askYesNo

import bsoft
from bsoft.convert import readSetOfCoordinates


class BsoftProtParticlePicking(ProtParticlePicking):
    """Protocol to pick particles in a set of micrographs using bsoft"""
    _label = 'particle picking'

    def __init__(self, **args):
        ProtParticlePicking.__init__(self, **args)
        # The following attribute is only for testing

    def _defineParams(self, form):
        ProtParticlePicking._defineParams(self, form)
        form.addParam('memory', FloatParam, default=2,
                      label='Memory to use (In Gb)', expertLevel=2)

    def _insertAllSteps(self):
        """The Particle Picking process is realized for a set of micrographs"""
        # Get pointer to input micrographs
        self.inputMics = self.inputMicrographs.get()
        # Launch Particle Picking GUI
        self._insertFunctionStep('launchParticlePickGUIStep',
                                 interactive=True)

    def launchParticlePickGUIStep(self):
        # Launch the particle picking GUI
        outputdir = self._getExtraPath()
        for mic in self.inputMics:
            micfile = abspath(mic.getFileName())
            args = "%s %s" % (micfile, outputdir)
            self.runJob("ln -sf", args)

        self._enterDir(outputdir)
        for mic in self.inputMics:
            self.runJob(bsoft.Plugin.getProgram('bshow'), basename(mic.getFileName()),
                        env=bsoft.Plugin.getEnviron())

        # Open dialog to request confirmation to create output
        if askYesNo(Message.TITLE_SAVE_OUTPUT,
                    Message.LABEL_SAVE_OUTPUT, None):
            self._leaveDir()  # going back to project dir
            self._createOutput(outputdir)

    def readSetOfCoordinates(self, workingDir, coordSet):
        readSetOfCoordinates(workingDir, self.inputMics, coordSet)

    def _methods(self):
        return ProtParticlePicking._methods(self)

    def _summary(self):
        return ProtParticlePicking._summary(self)

    def __str__(self):
        """ String representation of a Supervised Picking run """
        if not hasattr(self, 'outputCoordinates'):
            picked = 0
        else:
            picked = self.outputCoordinates.getSize()
        return "Particles picked: %d (from %d micrographs)" % (
            picked, self.inputMicrographs.get().getSize())
