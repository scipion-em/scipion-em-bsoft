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

import pyworkflow.utils as pwutils
import pyworkflow.protocol.params as params
from pwem.protocols import ProtFilterParticles

import bsoft
from bsoft.constants import (FILTER_MEDIAN, FILTER_PEAK,
                             FILTER_DENOISE)

"""

-invert	            Invert density in the image.
-rescale -0.1,5.2	Rescale data to average and standard deviation after filtering.
-minmax -0.5,1.2	Rescale data to minimum and maximum.
-average 7,5,3	    Averaging/smoothing filter: kernel size.
-gaussian 11,2.6	Gaussian smoothing filter: kernel size and sigma.
-median 3	        Median filter: kernel edge size.
-peak 5	            Peak filter: kernel edge size.
-gradient	        Gradient filter (3x3x3).
-laplacian	        Laplacian filter (3x3x3).
-LoG 2.5	        Laplacian-of-Gaussian filter.
-DoG 1.5,3.1	    Difference-of-Gaussians filter.
-denoise 2,0.4	    Denoising filter: distance and density difference sigmas.
-rollingball 5,4.3	Rolling ball filter: radius and density scaling (default scaling=1).
-variance 11,1	    Calculate a local variance image using the given size kernel,
                    with a flag to indicate standard deviation rather than variance.
-extremes his	    Filter image extremes: his=histogram-based, mg=for micrograph.
-replacemaxima 1.5	Replace maxima above the given threshold with surrounding average.
-bandpass 25.3,200,0.02	Bandpass filter: resolution limits (angstrom) and band edge width (1/angstrom).
-amplitude 8.3	    Amplitude filter: setting all amplitudes below the threshold to zero.
-phasesonly	        Set all amplitudes to one.
-Bfactor 44,25.3	B-factor application: B-factor (A^2), high resolution limit (A,optional)
                    Multiplied in reciprocal space by exp(-B-factor/4 * s^2).

Parameters:
-verbose 1	        Verbosity of output.
-datatype u	        Force writing of a new data type.
-sampling 1.5,1.5,1.5	Sampling (A/pixel; default from input file; a single value can be given).
-wrap	            Turn wrapping on (default off, use with -denoise option).
"""


class BsoftProtBfilter(ProtFilterParticles):
    """ Wrapper around bfilter program of BSOFT. """
    _label = 'bfilter'

    def __init__(self, **kwargs):
        ProtFilterParticles.__init__(self, **kwargs)

    # --------------------------- DEFINE param functions ------------------------
    def _defineProcessParams(self, form):
        form.addParam('filterType', params.EnumParam,
                      choices=['median', 'peak', 'gradient',
                               'laplacian', 'denoise'],
                      label="Filter type", default=0,
                      help="Select what type of filter do you want to apply.")
        form.addParam('kernelEdgeSize', params.IntParam, default=3,
                      label='Kernel edge size',
                      condition='filterType==%d or filterType==%d' % (
                          FILTER_MEDIAN, FILTER_PEAK))

        line = form.addLine('Denoise',
                            condition='filterType==%d' % FILTER_DENOISE,
                            help="Denoising filter: distance and density difference sigmas.")
        line.addParam('denoiseDistance', params.IntParam, default=2,
                      label='distance')
        line.addParam('denoiseDensity', params.FloatParam, default=0.4,
                      label='density')
        form.addParam('wrap', params.BooleanParam, default=False,
                      condition='filterType==%d' % FILTER_DENOISE,
                      label='Wrap?',
                      help="Turn wrapping on ")

    # -denoise 2,0.4           Denoising filter: distance and density difference sigmas.

    #         line = form.addLine('Frequency',
    #                             condition='filterType > %d and filterType != %d' % (FILTER_SPACE_REAL,FILTER_FERMI),
    #                             help='Range to apply the filter. Expected values between 0 and 0.5.')
    #         line.addParam('lowFreq', DigFreqParam, condition='filterMode==%d' % FILTER_HIGHPASS, default=0.1,
    #                     label='Lowest')
    #         line.addParam('highFreq', DigFreqParam, condition='filterMode==%d' % FILTER_LOWPASS,
    #                     default=0.2, label='Highest')
    #
    #         form.addParam('temperature', FloatParam, default=0.3,
    #                       label='Temperature T:',
    #                       condition='filterType == %d' % FILTER_FERMI,
    #                       help='Enter a temperature parameter T The filter falls off roughly within \n'
    #                            'this reciprocal distance (in terms of frequency units).')

    # --------------------------- INSERT steps functions -----------------------
    def _insertAllSteps(self):
        # Insert processing steps
        self._insertFunctionStep('convertInputStep', self.inputParticles.get().strId())
        self._insertFunctionStep('filterStep', self.getFilterArgs())
        self._insertFunctionStep('createOutputStep')

    # --------------------------- STEPS functions ------------------------------
    def convertInputStep(self, strId):
        # we need to put all images into a single stack
        # to ease the call of bsoft programs
        self.inputParticles.get().writeStack(self._getPath('particles.spi:stk'))

    def getFilterArgs(self):
        """ Build the bfilter command line base on selected params. 
        Exclude only the input and output files"""
        filterText = self.getEnumText('filterType')
        filterType = self.filterType.get()

        # by default use always the filter type as first argument
        args = '-%s' % filterText

        if filterType in [FILTER_MEDIAN, FILTER_PEAK]:
            args += ' %d' % self.kernelEdgeSize
        elif filterType == FILTER_DENOISE:
            args += ' %d,%0.3f' % (self.denoiseDistance,
                                   self.denoiseDensity)

        return args

    def runFilter(self, inputStk, outputStk):
        """ Util function used by wizard. """
        self.setStepsExecutor()  # set default execution
        args = self.getFilterArgs()

        self.runJob(bsoft.Plugin.getProgram('bfilter'), args +
                    ' %s %s' % (inputStk, outputStk),
                    env=bsoft.Plugin.getEnviron())

    def filterStep(self, args):
        """ Apply the selected filter to particles. 
        Create the set of particles.
        """
        particlesStk = self._getPath('particles.spi')
        tmpStk = particlesStk.replace('.spi', '_tmp.spi')
        self.runJob(bsoft.Plugin.getProgram('bfilter'), args +
                    ' %s %s' % (particlesStk, tmpStk),
                    env=bsoft.Plugin.getEnviron())
        pwutils.moveFile(tmpStk, particlesStk.replace('.spi', '.stk'))
        # just we prefer stk as stack of spider images
        pwutils.cleanPath(particlesStk)

    def createOutputStep(self):
        particlesStk = self._getPath('particles.stk')
        inputSet = self.inputParticles.get()
        outputSet = self._createSetOfParticles()
        outputSet.copyInfo(inputSet)

        for i, img in enumerate(inputSet):
            img.setLocation(i + 1, particlesStk)
            outputSet.append(img)

        self._defineOutputs(outputParticles=outputSet)
        self._defineTransformRelation(inputSet, outputSet)

    # --------------------------- INFO functions ------------------------------
    def _validate(self):
        errors = []
        return errors

    def _summary(self):
        summary = []
        return summary

    def _methods(self):
        methods = []
        return methods
