#-------------------------------------------------------------------------------
# Name:         Shapefile to JSON
# Purpose:      The purpose of this script is to download a zip file that
#               contains a shapefile(s), unzip it, buffer where needed,
#               merge all the shapefiles together into one coverage polygon,
#               merge all the polygons together with a dissolve, then single
#               part to multipart the results.  Amounts of polygons and amounts
#               of vertices will be calculated to make sure that the amounts
#               are not too high, to be checked against later when scripts are
#               merged.
#
# Author:       Sean Eagles
#
# Created:      31-05-2021
# Copyright:    (c) seagles 2021
# Licence:      <your licence>
#-------------------------------------------------------------------------------

import urllib2
from contextlib import closing
import zipfile
import arcpy
import os

# module to download zip files
def download_url(url, save_path):
    with closing(urllib2.urlopen(url)) as dl_file:
        with open(save_path, 'wb') as out_file:
            out_file.write(dl_file.read())

def extract_zipfile(save_path, folder):
    with zipfile.ZipFile(save_path, 'r') as zip_ref:
        zip_ref.extractall(folder)
    print "Zip file folder extracted to: " + folder

# module for listing all feature classes within a given geodatabase
def listFcsInGDB(gdb):
    arcpy.env.workspace = gdb
    print 'Processing ', arcpy.env.workspace

    fcs = []
    for fds in arcpy.ListDatasets('','feature') + ['']:
        for fc in arcpy.ListFeatureClasses('','',fds):
            #yield os.path.join(fds, fc)
            fcs.append(os.path.join(fds, fc))
    return fcs

def create_shapefile(folder, ShapefileName):
    # Create a shapefile to merge everything
    print("Creating master Shapefile " + str(folder) + "\\" + str(ShapefileName))
    arcpy.env.workspace = folder
    arcpy.CreateFeatureclass_management(
        out_path=folder,
        out_name=ShapefileName,
        geometry_type="POLYGON",
        template="",
        has_m="DISABLED",
        has_z="DISABLED",
        spatial_reference="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision",)
    print("Master Shapefile Created")

def polygonTransform(FeatureClass):
    # set polygons which will be used to dissolve and create multipart
    # polygons in a single shapefile
    #
    dissolved = FeatureClass + "_dissolved"
    singlepart = FeatureClass + "_finished"

    # add field "merge"
    #
    arcpy.AddField_management(
        in_table=FeatureClass,
        field_name="MERGE",
        field_type="TEXT",
        field_precision="",
        field_scale="",
        field_length="5",
        field_alias="",
        field_is_nullable="NULLABLE",
        field_is_required="NON_REQUIRED",
        field_domain="")

    print "Field Added"

    # calculate the merge field to value 1, so that every polygon is
    # a value of 1
    arcpy.CalculateField_management(
        in_table=FeatureClass,
        field="MERGE",
        expression="1",
        expression_type="PYTHON",
        code_block="")
    print "Field Calculated"

    # dissolve based on the value 1 in 'merge' field
    #
    arcpy.Dissolve_management(
        in_features=FeatureClass,
        out_feature_class=dissolved,
        dissolve_field="MERGE",
        statistics_fields="",
        multi_part="MULTI_PART",
        unsplit_lines="DISSOLVE_LINES")

    print "Features Dissolved"

    # similar to the explode tool, take all of the multipart polygons
    # and create single part polygons that are separate when not
    # attached to another polygon
    #
    arcpy.MultipartToSinglepart_management(
        in_features=dissolved,
        out_feature_class=singlepart)
    print "Multi part to single part explosion"

    # Append the result into the shapefile that has all appended
    # polygons
    #
    arcpy.Append_management(
        inputs=singlepart,
        target=ShapefileAll,
        schema_type="NO_TEST",
        field_mapping="",
        subtype="")

def pointTransform(FeatureClass):
    # set polygons which will be used to dissolve and create multipart
    # polygons in a single shapefile
    #
    buffer = FeatureClass + "_buffer"
    dissolved = FeatureClass + "_dissolved"
    singlepart = FeatureClass + "_finished"

    # run buffer on the feature class to create a polygon feature class
    #
    arcpy.Buffer_analysis(
        in_features=FeatureClass,
        out_feature_class=buffer,
        buffer_distance_or_field="100 Meters",
        line_side="FULL",
        line_end_type="ROUND",
        dissolve_option="NONE",
        dissolve_field="",
        method="PLANAR")
    print "Buffer created for points - " + buffer

    # add field "merge"
    #
    arcpy.AddField_management(
        in_table=buffer,
        field_name="MERGE",
        field_type="TEXT",
        field_precision="",
        field_scale="",
        field_length="5",
        field_alias="",
        field_is_nullable="NULLABLE",
        field_is_required="NON_REQUIRED",
        field_domain="")
    print "Field Added"

    # calculate the merge field to value 1, so that every polygon is
    # a value of 1
    arcpy.CalculateField_management(
        in_table=buffer,
        field="MERGE",
        expression="1",
        expression_type="PYTHON",
        code_block="")
    print "Field Calculated"

    # dissolve based on the value 1 in 'merge' field
    #
    arcpy.Dissolve_management(
        in_features=buffer,
        out_feature_class=dissolved,
        dissolve_field="MERGE",
        statistics_fields="",
        multi_part="MULTI_PART",
        unsplit_lines="DISSOLVE_LINES")

    print "Features Dissolved"

    # similar to the explode tool, take all of the multipart polygons
    # and create single part polygons that are separate when not
    # attached to another polygon
    #
    arcpy.MultipartToSinglepart_management(
        in_features=dissolved,
        out_feature_class=singlepart)

    print "Multi part to single part explosion"

    # Append the result into the shapefile that has all appended
    # polygons
    #
    arcpy.Append_management(
        inputs=singlepart,
        target=ShapefileAll,
        schema_type="NO_TEST",
        field_mapping="",
        subtype="")

def lineTransform(FeatureClass):
    # create a name for the buffer and singlepart polygons to be created
    #
    buffer = FeatureClass + "_buffer"
    dissolved = FeatureClass + "_dissolved"
    singlepart = FeatureClass + "_finished"

    # run buffer on the feature class to create a polygon feature class
    #
    arcpy.Buffer_analysis(
        in_features=FeatureClass,
        out_feature_class=buffer,
        buffer_distance_or_field="100 Meters",
        line_side="FULL",
        line_end_type="ROUND",
        dissolve_option="NONE",
        dissolve_field="",
        method="PLANAR")

    print "Buffer created for Lines - " + buffer

    # add a field called "merge"
    #
    arcpy.AddField_management(
        in_table=buffer,
        field_name="MERGE",
        field_type="TEXT",
        field_precision="",
        field_scale="",
        field_length="5",
        field_alias="",
        field_is_nullable="NULLABLE",
        field_is_required="NON_REQUIRED",
        field_domain="")

    # calculate the merge field to value 1
    #
    arcpy.CalculateField_management(
        in_table=buffer,
        field="MERGE",
        expression="1",
        expression_type="PYTHON",
        code_block="")

    print "Field Calculated"

    # dissolve the polygons based on the merge value of 1 creating one multipart
    # polygon
    #
    arcpy.Dissolve_management(
        in_features=buffer,
        out_feature_class=dissolved,
        dissolve_field="MERGE",
        statistics_fields="",
        multi_part="MULTI_PART",
        unsplit_lines="DISSOLVE_LINES")

    print "Features Dissolved"

    # similar to the explode tool, take the multipart polygon that was
    # created and make it into singlepart seperate polygons
    #
    arcpy.MultipartToSinglepart_management(
        in_features=dissolved,
        out_feature_class=singlepart)

    print "Multi part to single part explosion"

    # append the new polyons into the shapefile which contains all
    # polygons
    #
    arcpy.Append_management(
        inputs=singlepart,
        target=ShapefileAll,
        schema_type="NO_TEST",
        field_mapping="",
        subtype="")

if __name__ == '__main__':

    Records_Clean_Table = r'C:\TEMP\Records_Clean.dbf'
    Fields = ['FILE_ID', 'SCORE', 'URL_FINAL']

    with arcpy.da.SearchCursor(Records_Clean_Table, Fields) as cursor:
        for row in cursor:
            if row[1] == 4:
                FILE_ID = unicode(row[0])
                SCORE = unicode(row[1])
                URL = unicode(row[2])
                print ("FILE_ID = " + unicode(row[0]))
                print ("SCORE = " + unicode(row[1]))
                print ("URL = " + unicode(row[2]))
                try:
                    # Need to make the folder come from the ID
                    folder = "C:\\Temp\\" + str(FILE_ID)
                    print("folder = " + folder)
                    path = r"C:\TEMP"
                    print("path = " + path)
                    # URL must come from the master clean table
                    Extract_URL = URL
                    print("Extract_URL = " + Extract_URL)
                    save_path = "C:\TEMP\download.zip"
                    # workspace must come from the folder name in the zip file (if that works)
                    workspace = "C:\\TEMP\\" + str(FILE_ID)
                    # Need a generic name to be used with all Shapefile datasets
                    ShapefileName = "Master_Merged_Shapefile.shp"
                    print("ShapefileName = " + ShapefileName)
                    # Take these from new restructured names
                    ShapefileAll = folder + "\\" + ShapefileName
                    print("ShapefileAll = " + ShapefileAll)
                    # Need a new generic name for geodatabase
                    Geodatabase_name = FILE_ID
                    print("Geodatabase_name = " + Geodatabase_name)
                    Geodatabase = workspace + "\\" + Geodatabase_name  + ".gdb"
                    print("Geodatabase = " + Geodatabase)
                    Geodatabase_basename = workspace + "\\" + Geodatabase_name

                    download_url(Extract_URL, save_path)
                    print("download complete")

                    extract_zipfile(save_path, folder)
                    print("extracted zipfile")

                    create_shapefile(folder, ShapefileName)
                    print("shapefile created")

                    arcpy.CreateFileGDB_management(
                        out_folder_path=workspace,
                        out_name=Geodatabase_name,
                        out_version="CURRENT")
                    print("GDB created")

                    print(path + " = PATH")
                    List_SHP = []
                    for (root,dirs,files) in os.walk(path, topdown=True):
                        print (root)
                        #print (dirs)
                        #print (files)
                        files = os.listdir(root)
                        files = [f for f in files if f.lower().endswith('.shp')]
                        if len(files)==0:
                            print("there are no files ending with .shp in your folder")
                        else:
                            print('There are {} shapefiles in your folder'.format(len(files)))
                        for f in files:
                            print root + "\\" + f
                            List_SHP.append(root + "\\" + f)
                        print ('--------------------------------')
                    print List_SHP
                    print ('There are {} shapefiles in your list'.format(len(List_SHP)))

                    ShapefileAllName = os.path.basename(ShapefileAll)
                    print("Name = " + ShapefileAllName)
                    BaseShapefileAllName = os.path.splitext(ShapefileAllName)[0]
                    print("Shapefile All base name = " + BaseShapefileAllName)
                    # create dissolve and singlepart shapefiles to complete the proceses on the
                    # merged shapefile with everything in it
                    #
                    ShapefileAll_Dissolve = folder + "\\" + BaseShapefileAllName + "_dissolve.shp"
                    ShapefileAll_SinglePart = folder + "\\" + BaseShapefileAllName + "_singlepart.shp"

                    arcpy.env.workspace = workspace

                    # A list of shapefiles (There is a better way to do this
                    #

                    # Shapefiles = arcpy.ListFeatureClasses()
                    # print("Shapefile list = " + str(Shapefiles))

                    # Create feature classes in the geodatabase to run tools on
                    # for SHP in Shapefiles:
                    for SHP in List_SHP:
                        # set up workspace, and shapefile name
                        #
                        print("SHP = " + SHP)
                        #Shapefile = workspace + "\\" + SHP
                        Shapefile = SHP
                        print "Shapefile: " + Shapefile
                        Name = os.path.basename(Shapefile)
                        print "Name = " + Name
                        BaseName = os.path.splitext(Name)[0]
                        print "BaseName = " + BaseName
                        arcpy.FeatureClassToFeatureClass_conversion(in_features=SHP, out_path=Geodatabase, out_name=BaseName, where_clause="", field_mapping="", config_keyword="")

                    fcs = listFcsInGDB(Geodatabase)

                    # Cycle through all feature classes in the geodatabase
                    #
                    print "Cycle through feature classes in geodatabase"
                    for fc in fcs:
                        # set feature class location and name
                        #
                        FeatureClass = Geodatabase + "\\" + fc
                        print "Feature class: " + FeatureClass

                        # Describe a feature class
                        #
                        desc = arcpy.Describe(FeatureClass)

                        # Get the shape type (Polygon, Polyline) of the feature class
                        #
                        type = desc.shapeType

                        print str(type)
                        # If the type is polygon run through these instructions
                        #
                        if type == "Polygon":
                            polygonTransform(FeatureClass)

                        # run these instructions if type is point
                        #
                        elif type == "Point":
                            pointTransform(FeatureClass)

                        # run these instructions if type is point
                        elif type == "Polyline":
                            lineTransform(FeatureClass)

                    # now work on the master shapefile
                    # add a field called "merge"
                    #
                    arcpy.AddField_management(
                        in_table=ShapefileAll,
                        field_name="MERGE",
                        field_type="TEXT",
                        field_precision="",
                        field_scale="",
                        field_length="5",
                        field_alias="",
                        field_is_nullable="NULLABLE",
                        field_is_required="NON_REQUIRED",
                        field_domain="")
                    print "Field Added"

                    # calculate the merge field to value 1
                    #
                    arcpy.CalculateField_management(
                        in_table=ShapefileAll,
                        field="MERGE",
                        expression="1",
                        expression_type="PYTHON",
                        code_block="")
                    print "Field Calculated"

                    # dissolve the polygons based on the merge value of 1 creating one multipart
                    # polygon
                    #
                    dissolve = "C:/TEMP/Map_Selection_Dissolve.shp"
                    arcpy.Dissolve_management(
                        in_features=ShapefileAll,
                        out_feature_class=dissolve,
                        dissolve_field="MERGE",
                        statistics_fields="",
                        multi_part="MULTI_PART",
                        unsplit_lines="DISSOLVE_LINES")

                    print "Features Dissolved"

                    # take the dissolved polygon and explode the single polygon into singlepart
                    # polygons
                    #
                    singlepart = "C:/TEMP/MAP_Selection_Finished.shp"
                    arcpy.MultipartToSinglepart_management(
                        in_features=dissolve,
                        out_feature_class=singlepart)

                    print "Multi part to single part explosion"

                    # Add a field to count vertices "vertices"
                    #
                    arcpy.AddField_management(
                        in_table=singlepart,
                        field_name="VERTICES",
                        field_type="FLOAT",
                        field_precision="255",
                        field_scale="0",
                        field_length="",
                        field_alias="",
                        field_is_nullable="NULLABLE",
                        field_is_required="NON_REQUIRED",
                        field_domain="")

                    print "Added field VERTICES"

                    # Calculate the vertices field with a count of vertices in that polygon
                    #
                    arcpy.CalculateField_management(
                        singlepart,
                        "VERTICES",
                        "!Shape!.pointCount-!Shape!.partCount",
                        "PYTHON")

                    print "Calculate the amount of vertices in VERTICES field"

                    # print the count of all polygons found within the master shapefile
                    #
                    PolygonCounter = 0
                    with arcpy.da.SearchCursor(singlepart,"MERGE") as cursor:
                        for row in cursor:
                            PolygonCounter = PolygonCounter + 1
                    print "There are " + str(PolygonCounter) + " polygons"
                    del row, cursor, PolygonCounter

                    # create an ESRI GeoJSON for the master shapefile to be used to load into
                    # GeoCore
                    #
                    '''
                    arcpy.FeaturesToJSON_conversion(
                        in_features=singlepart,
                        out_json_file="C:/TEMP/IPN_FeaturesToJSON.json",
                        format_json="FORMATTED",
                        include_z_values="NO_Z_VALUES",
                        include_m_values="NO_M_VALUES",
                        geoJSON="GEOJSON")
                    '''
                    arcpy.FeaturesToJSON_conversion(
                        in_features=singlepart,
                        out_json_file="C:/TEMP/" + str(FILE_ID) + ".json",
                        format_json="NOT_FORMATTED",
                        include_z_values="NO_Z_VALUES",
                        include_m_values="NO_M_VALUES",
                        geoJSON="NO_GEOJSON")

                    print "ESRI JSON created"

                except:
                    print "---------------------"
                    print "Error in longest loop"
                    print "---------------------"
                    pass

                try:
                    arcpy.Delete_management(folder)
                    print "Delete folder worked"
                except:
                    print "Delete Folder passed error, may not exist"
                    pass

                try:
                    arcpy.Delete_management(dissolve)
                    print "Delete dissolve worked"
                except:
                    print "Delete dissolve passed error, may not exist"
                    pass

                try:
                    arcpy.Delete_management(singlepart)
                    print "Delete singlepart worked"
                except:
                    print "Delete singlepart passed error, may not exist"
                    pass

                try:
                    arcpy.Delete_management(save_path)
                    print "Delete save_path worked"
                except:
                    print "Delete of save_path passed error, may not exist"
                    pass
