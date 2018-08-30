# **************************************************************************
# *
# * Authors:     Grigory Sharov (gsharov@mrc-lmb.cam.ac.uk)
# *
# * MRC Laboratory of Molecular Biology (MRC-LMB)
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

from collections import OrderedDict

import pyworkflow.em.metadata as md

BSOFT_HOME = 'BSOFT_HOME'

# Bfilter constants
FILTER_MEDIAN = 0
FILTER_PEAK = 1
FILTER_GRADIENT = 2
FILTER_LAPLACIAN = 3
FILTER_DENOISE = 4

# Blocres constants
FN_HALF1 = 'half1'
FN_HALF2 = 'half2'
FN_MASKVOL = 'maskvol'
FN_RESOLMAP = 'resolutionMap'


# Map from Xmipp labels to Bsoft labels names
XMIPP_BSOFT_LABELS = {
    md.MDL_MICROGRAPH: 'micrograph.file_name',
    md.MDL_MICROGRAPH_ID: 'micrograph.id',
    md.MDL_IMAGE: 'particle.filename',
    md.MDL_PARTICLE_ID: 'particle.id',
    md.MDL_XCOOR: 'particle.x',
    md.MDL_YCOOR: 'particle.y',
    md.MDL_ZCOOR: 'particle.z',
    md.MDL_SHIFT_X: 'particle.origin_x',
    md.MDL_SHIFT_Y: 'particle.origin_y',
    md.MDL_SHIFT_Z: 'particle.origin_z',
    md.MDL_ENABLED: 'particle.select',
    md.MDL_PICKING_PARTICLE_SIZE: 'particle.origin_x',
    md.MDL_MAGNIFICATION: 'particle.magnification'
}

COOR_DICT = OrderedDict([
             ("_x", md.MDL_XCOOR),
             ("_y", md.MDL_YCOOR)
             ])

COOR_EXTRA_LABELS = [
    # Additional autopicking-related metadata
    md.RLN_PARTICLE_AUTOPICK_FOM,
    md.RLN_PARTICLE_CLASS,
    md.RLN_ORIENT_PSI
    ]
