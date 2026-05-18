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

    """
        Particle Picking (BsoftProtParticlePicking) — User Manual

            Overview

            The Particle Picking protocol provides an interactive framework
            for manually selecting particles from cryo-EM micrographs using
            the BSOFT visualization tools. Its main purpose is to generate
            particle coordinate datasets through direct visual inspection
            of experimental micrographs.

            Inputs and General Workflow

            The protocol requires a set of input micrographs that will be
            inspected during the picking session. Before execution, the
            micrographs are linked into the working directory to allow
            direct access from the BSOFT graphical environment. An optional
            memory parameter can also be adjusted to optimize performance
            when processing large datasets.

            Interactive Particle Picking

            During execution, the protocol launches the BSOFT `bshow`
            graphical interface for each micrograph. Users manually inspect
            the images and identify particle positions interactively,
            allowing direct evaluation of particle quality, contamination,
            aggregation, or structural heterogeneity.

            From a biological perspective, manual picking remains especially
            useful for challenging cryo-EM datasets where automated methods
            may fail because of low contrast, flexible particles, or noisy
            backgrounds. The interactive workflow allows users to apply
            biological knowledge and visual criteria when selecting
            meaningful particles for downstream analysis.

            Outputs and Interpretation

            After the picking session is completed and confirmed, the
            protocol generates a set of particle coordinates associated
            with the original micrographs. These coordinates can be used
            directly in downstream extraction, classification, and
            reconstruction workflows.

            Final Perspective

            BsoftProtParticlePicking provides a practical framework for
            interactive particle selection in cryo-EM workflows. By
            combining direct visualization with user-guided coordinate
            assignment, the protocol helps generate reliable particle
            datasets for downstream structural analysis.
        """
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
