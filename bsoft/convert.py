# **************************************************************************
# *
# * Authors:     Airen Zaldivar Peraza (azaldivar@cnb.csic.es)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
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

import pwem.emlib.metadata as md
from pwem.objects import Coordinate
from pyworkflow.object import String, ObjectWrap
from pyworkflow.utils import join, replaceBaseExt, createLink, exists

from bsoft.constants import *


def readSetOfCoordinates(outputDir, micSet, coordSet):
    """ Read from Bsoft .star files.
    Params:
        outputDir: the directory where the .star files are.
           
        micSet: the SetOfMicrographs to associate the .star, which 
            name should be the same of the micrographs.
        coordSet: the SetOfCoordinates that will be populated.
    """
    boxSize = 100
    for mic in micSet:
        outputFile = join(outputDir, replaceBaseExt(mic.getFileName(), 'star'))
        if exists(outputFile):
            posMd = md.MetaData(outputFile)

            for objId in posMd:
                coordRow = rowFromMd(posMd, objId)
                coord = rowToCoordinate(coordRow)
                boxSize = 2 * float(coordRow.getValue("particle.x_origin", 50))
                coord.setMicrograph(mic)
                coord.setX(coord.getX())
                coord.setY(coord.getY())

                coordSet.append(coord)
                # Add an unique ID that will be propagated to particles
                # posMd.setValue(md.MDL_PARTICLE_ID, long(coord.getObjId()), objId)

    # reading origin.x value and converting to particle
    # size, can change, we take last value
    coordSet.setBoxSize(boxSize)


def rowToCoordinate(coordRow):
    """ Create a Coordinate from a row of a metadata. """
    # Check that all required labels are present in the row
    if _containsAll(coordRow, COOR_DICT):
        coord = Coordinate()
        rowToObject(coordRow, coord, COOR_DICT)  # , extraLabels=COOR_EXTRA_LABELS)
        # TODO: switch back on extra labels when
        # sqlite mapper can tolerate dots in label names
    else:
        coord = None

    return coord


def rowToObject(row, obj, attrDict, extraLabels=[]):
    """ This function will convert from a md Row to an EMObject.
    Params:
        row: the Row instance (input)
        obj: the EMObject instance (output)
        attrDict: dictionary with the map between obj attributes(keys) and
            row MDLabels in Bsoft (values).
    """
    # Bsoft does not have analogous label for MDL_ENABLED
    obj.setEnabled(True)

    for attr, label in attrDict.iteritems():
        # all Bsoft labels are strings, so convert to float
        value = float(row.getValue(label))
        if not hasattr(obj, attr):
            setattr(obj, attr, ObjectWrap(value))
        else:
            getattr(obj, attr).set(value)

    attrLabels = attrDict.values()

    for label in extraLabels:
        if label not in attrLabels and row.hasLabel(label):
            labelStr = md.label2Str(label)
            setattr(obj, '_' + labelStr, row.getValueAsObject(label))


def rowFromMd(mdata, objId):
    row = md.Row()
    row.readFromMd(mdata, objId)
    return row


def _containsAll(row, labels):
    """ Check if the labels (values) in labelsDict
    are present in the row.
    """
    values = labels.values() if isinstance(labels, dict) else labels
    return all(row.containsLabel(l) for l in values)


def writeSetOfParticles(imgSet, starFile, stackFile):
    """ This function will write a SetOfImages as Bsoft metadata.
    Params:
        imgSet: the SetOfImages instance.
        starFile: the filename where to write the metadata.
    """
    mdata = md.MetaData()
    mdata.setColumnFormat(False)
    imgRow = mdata.Row()
    imgRow.setValue("micrograph.id", int(1))
    imgRow.setValue("particle.x_origin", str(stackFile))
    imgRow.writeToMd(mdata, mdata.addObject())
    imgSet._bsoftStar = String(starFile)


def createBsoftInputParticles(imgSet, starFile, stackFile):
    """ Ensure that 'starFile' is a valid STAR files with particles.
    If the imgSet comes from Bsoft, just create a link.
    If not, then write the proper file.
    """
    imgsStar = getattr(imgSet, '_bsoftStar', None)
    if imgsStar is None:
        writeSetOfParticles(imgSet, starFile, stackFile)
    else:
        imgsFn = imgsStar.get()
        createLink(imgsFn, imgsStar.get())
