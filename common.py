#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      7810AK
#
# Created:     26/09/2018
# Copyright:   (c) 7810AK 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import datetime
##from dateutil.relativedelta import relativedelta
import os.path

##try:
##    arcpy
##except NameError:
##    start = datetime.datetime.now()
##    import arcpy
##    end = datetime.datetime.now()
##    diff = relativedelta(end, start)
##    print "arcpy loaded in {0} minutes, {1} seconds".format(diff.minutes, diff.seconds )

##def _removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def removeNonAscii(s): return ''.join([i if ord(i) < 128 else '.' for i in s])

##return ''.join([i if ord(i) < 128 else ' ' for i in text])

def getdatetime():
    d = datetime.datetime.now()
    return d.strftime("%y") + d.strftime("%m") + d.strftime("%d") + "_" + d.strftime("%H") + d.strftime("%M")

def getdate():
    d = datetime.datetime.now()
    return d.strftime("%y") + d.strftime("%m") + d.strftime("%d")

##def getSpatialDimension(featureClass):
##    spatial_dim = 0
##    geometries = arcpy.CopyFeatures_management(featureClass, arcpy.Geometry())
##
##    for geometry in geometries:
##
##        try:
##            if geometry.type == 'polygon':
##                spatial_dim += geometry.area
##            elif geometry.type == 'polyline':
##                spatial_dim += geometry.length
##            elif geometry.type == 'point':
##                spatial_dim += geometry.pointCount
##            elif geometry.type == 'multipoint':
##                spatial_dim += geometry.pointCount
##
##        except AttributeError:
##            print 'NULL geom!'
##            pass
##
##    return spatial_dim

def writeError(fe, path, filename, errorstring, header):
    if fe is None:
        if os.path.isfile(path + "/" + filename):
            fe = open(path + "/" + filename, 'a')
        else:
            fe = open(path + "/" + filename, 'w')
            #write header of output file
            fe.write(header)

    fe.write(errorstring)
    fe.close()
    return True

def writeData(fo, path, filename, linestring, header):
    if fo is None:
        if os.path.isfile(path + "/OUTPUT/" + filename):
            fo = open(path + "/OUTPUT/" + filename, 'a')
        else:
            fo = open(path + "/OUTPUT/" + filename, 'w')
            #write header of output file
            fo.write(header)

    fo.write(linestring)
    fo.close()
    return True

##def getDomainLU(domainList, domain):
##    try:
##        ddesc_lu = [d.codedValues for d in domainList if d.name == domain][0]
##    except IndexError:
##        ddesc_lu = None
##        pass
##
##    return ddesc_lu

def getFileNames(folder, extension):
    items = os.listdir(folder)
    newlist = []
    for names in items:
        if names.endswith(extension):
            newlist.append(names)

    return newlist


def xldate_to_date(xldate):
	temp = datetime.date(1899, 12, 30)
	delta = datetime.timedelta(days=xldate)
	return temp+delta

##def FieldExist(featureclass, fieldname):
##    fieldList = arcpy.ListFields(featureclass, fieldname)
##
##    fieldCount = len(fieldList)
##
##    if (fieldCount == 1):
##        return True
##    else:
##        return False

##def test_for_GDB(path, name):
##    arcpy.env.workspace = path
##    workspaces = arcpy.ListWorkspaces("*", "FileGDB")
##    found = 0
####    print path
####    print name
##    for workspace in workspaces:
####        print workspace
##        if workspace.lower().find(name.lower()) > 0:
##            found = 1
##            break
####        if workspace.lower() == path.lower() + name.lower() or workspace.lower() == path.lower() + "/" + name.lower():
####            found = 1
####            break
##
##    if found == 1:
##        return True
##    else:
##        return False


def getChangeReason(objIDnum, obArr= []):
    for ob in obArr:
##        print ob
        if ob[0] == objIDnum:
            return ob[1]

    return 'NA'















