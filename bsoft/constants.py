# **************************************************************************
# *
# * Authors:     Grigory Sharov (gsharov@mrc-lmb.cam.ac.uk)
# *
# * MRC Laboratory of Molecular Biology (MRC-LMB)
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

from collections import OrderedDict

BSOFT_HOME = 'BSOFT_HOME'

# Supported Versions
V2_0_7 = '2.0.7'

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


COOR_DICT = OrderedDict([
             ("_x", "particle.x"),
             ("_y", "particle.y")
             ])
