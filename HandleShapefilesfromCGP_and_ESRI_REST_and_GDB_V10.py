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
import json
import arcpy
import sys
import os

# module to download zip files
def download_url(url, save_path):
    with closing(urllib2.urlopen(url)) as dl_file:
        with open(save_path, 'wb') as out_file:
            out_file.write(dl_file.read())

def extract_zipfile(save_path, folder):
    with zipfile.ZipFile(save_path, 'r') as zip_ref:
        zip_ref.extractall(folder)
    # print "Zip file folder extracted to: " + folder

# module for listing all feature classes within a given geodatabase
def listFcsInGDB(gdb):
    arcpy.env.workspace = gdb
    # print 'Processing ', arcpy.env.workspace

    fcs = []
    for fds in arcpy.ListDatasets('','feature') + ['']:
        for fc in arcpy.ListFeatureClasses('','',fds):
            #yield os.path.join(fds, fc)
            fcs.append(os.path.join(fds, fc))
    return fcs

def create_shapefile(folder, ShapefileName):
    # Create a shapefile to merge everything
    # print("Creating master Shapefile " + str(folder) + "\\" + str(ShapefileName))
    arcpy.env.workspace = folder
    arcpy.CreateFeatureclass_management(
        out_path=folder,
        out_name=ShapefileName,
        geometry_type="POLYGON",
        template="",
        has_m="DISABLED",
        has_z="DISABLED",
        spatial_reference="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision",)
    # print("Master Shapefile Created")

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

    # print "Field Added"

    # calculate the merge field to value 1, so that every polygon is
    # a value of 1
    arcpy.CalculateField_management(
        in_table=FeatureClass,
        field="MERGE",
        expression="1",
        expression_type="VB",
        code_block="")
    # print "Field Calculated"

    # dissolve based on the value 1 in 'merge' field
    #
    arcpy.Dissolve_management(
        in_features=FeatureClass,
        out_feature_class=dissolved,
        dissolve_field="MERGE",
        statistics_fields="",
        multi_part="MULTI_PART",
        unsplit_lines="DISSOLVE_LINES")

    # print "Features Dissolved"

    # similar to the explode tool, take all of the multipart polygons
    # and create single part polygons that are separate when not
    # attached to another polygon
    #
    arcpy.MultipartToSinglepart_management(
        in_features=dissolved,
        out_feature_class=singlepart)
    # print "Multi part to single part explosion"

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
    # print "Buffer created for points - " + buffer

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
    # print "Field Added"

    # calculate the merge field to value 1, so that every polygon is
    # a value of 1
    arcpy.CalculateField_management(
        in_table=buffer,
        field="MERGE",
        expression="1",
        expression_type="VB",
        code_block="")
    # print "Field Calculated"

    # dissolve based on the value 1 in 'merge' field
    #
    arcpy.Dissolve_management(
        in_features=buffer,
        out_feature_class=dissolved,
        dissolve_field="MERGE",
        statistics_fields="",
        multi_part="MULTI_PART",
        unsplit_lines="DISSOLVE_LINES")

    # print "Features Dissolved"

    # similar to the explode tool, take all of the multipart polygons
    # and create single part polygons that are separate when not
    # attached to another polygon
    #
    arcpy.MultipartToSinglepart_management(
        in_features=dissolved,
        out_feature_class=singlepart)

    # print "Multi part to single part explosion"

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

    # print "Buffer created for Lines - " + buffer

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
        expression_type="VB",
        code_block="")

    # print "Field Calculated"

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

    # print "Features Dissolved"

    # similar to the explode tool, take the multipart polygon that was
    # created and make it into singlepart seperate polygons
    #
    arcpy.MultipartToSinglepart_management(
        in_features=dissolved,
        out_feature_class=singlepart)

    # print "Multi part to single part explosion"

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
    #arcpy.AddField_management(
        #in_table=Records_Clean_Table,
        #field_name="FINAL",
        #field_type="TEXT",
        #field_precision="",
        #field_scale="",
        #field_length="25",
        #field_alias="",
        #field_is_nullable="NULLABLE",
        #field_is_required="NON_REQUIRED",
        #field_domain="")
    try:
        arcpy.AddField_management(
            in_table=Records_Clean_Table,
            field_name="FINAL",
            field_type="SHORT",
            field_precision="",
            field_scale="",
            field_length="",
            field_alias="",
            field_is_nullable="NULLABLE",
            field_is_required="NON_REQUIRED",
            field_domain="")
    except:
        print("Field named FINAL already exists in " + Records_Clean_Table)
        pass
    try:
        arcpy.AddField_management(
            in_table=Records_Clean_Table,
            field_name="NOTES",
            field_type="SHORT",
            field_precision="",
            field_scale="",
            field_length="",
            field_alias="",
            field_is_nullable="NULLABLE",
            field_is_required="NON_REQUIRED",
            field_domain="")
    except:
        print("Field named NOTES already exists in " + Records_Clean_Table)

    Fields = ['FILE_ID', 'SCORE', 'URL_FINAL', 'FINAL', 'NOTES']

    with arcpy.da.UpdateCursor(Records_Clean_Table, Fields) as cursor:
        for row in cursor:
            if row[1] == 5 and row[3] != 1:
                FILE_ID = unicode(row[0])
                SCORE = unicode(row[1])
                URL = unicode(row[2])
                FINAL = unicode(row[3])
                NOTES = unicode(row[4])
                print("FILE_ID = " + unicode(row[0]))
                print("SCORE = " + unicode(row[1]))
                print("URL = " + unicode(row[2]))
                print("FINAL = " + unicode(row[3]))
                print("NOTES = " + unicode(row[4]))
                # set the url that needs to be downloaded
                try:
                    #
                    #url = 'http://ftp.maps.canada.ca/pub/statcan_statcan/Census_Recensement/census_subdivisions_2016/census_subdivisions_2016_en.gdb.zip'
                    #url = 'https://ftp.maps.canada.ca/pub/nrcan_rncan/Aboriginal-languages_Langue-autochtone/indigenous_place_names_2019/indigenous_place_names.gdb.zip'
                    url = URL
                    # set the path to save the zip file (needs to be dynamic later)
                    #
                    save_path = "C:\\TEMP\\download.zip"
                    print(save_path + " = save path")

                    # download the url to the save path
                    #
                    download_url(url, save_path)
                    print("zip file downloaded to: " + save_path)

                    # set the geodatabase (this needs to be dynamic in future)
                    #
                    gdb = "C:\\TEMP\\" + FILE_ID + "\\geodatabase.gdb"
                    print("gdb = " + str(gdb))

                    # set folder for extraction
                    #
                    folder = "C:\\TEMP\\" + FILE_ID
                    # unzip the zipfile to the folder location
                    #
                    print(folder + " = folder")
                    with zipfile.ZipFile(save_path, 'r') as zip_ref:
                        zip_ref.extractall(folder)
                    print "Zip file folder extracted to: " + folder


                    # set the shapefile up for creation where all polygons will be appended
                    ## also create the polygon
                    #ShapefileName = "Master_Shapefile.shp"
                    #ShapefileAll = folder + "\\" + ShapefileName
                    #arcpy.CreateFeatureclass_management(out_path=folder, out_name=ShapefileName, geometry_type="POLYGON", template="", has_m="DISABLED", has_z="DISABLED", spatial_reference="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision", config_keyword="", spatial_grid_1="0", spatial_grid_2="0", spatial_grid_3="0")

                    #dir_list = os.listdir(folder)
                    #print("Files and directories in '", path, "' :")

                    #print the list
                    #print("dir list = " + dir_list)

                    Distance_For_Buffer = "100 Kilometers"

                    print(folder + " = folder") # folder exists within main script, built the same way.
                    List_dirs = []
                    for (root,dirs,files) in os.walk(folder, topdown=True):
                        print ("root = " + root)
                        print ("dirs = " + unicode(dirs))
                        #print ("files = " + files)
                        files = os.listdir(root)
                        files = [f for f in files if f.lower().endswith('.gdb')]
                        if len(dirs)==0:
                            print("there are no folders in your root")
                        else:
                            print('There are {} geodatabase(s) in your folder'.format(len(dirs)))
                        for f in files:
                            print root + "\\" + f
                            List_dirs.append(root + "\\" + f)
                        print ('--------------------------------')

                    print List_dirs
                    print('There are {} geodatbase(s) in your list'.format(len(List_dirs)))

                    # set the shapefile up for creation where all polygons will be appended
                    # also create the polygon
                    ShapefileName = "Master_Shapefile.shp"
                    ShapefileAll = folder + "\\" + ShapefileName
                    arcpy.CreateFeatureclass_management(out_path=folder, out_name=ShapefileName, geometry_type="POLYGON", template="", has_m="DISABLED", has_z="DISABLED", spatial_reference="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision", config_keyword="", spatial_grid_1="0", spatial_grid_2="0", spatial_grid_3="0")

                    print("Shapefile created to hold all finished polygons: " + ShapefileAll)

                    fcs = []

                    for dirs in List_dirs:
                        # list all feature classes within the geodatabase
                        #
                        print(dirs)
                        fcs = listFcsInGDB(dirs)
                        #fcs = arcpy.ListFeatureClasses(dirs)
                        for fc in fcs:
                            FeatureClass = dirs + "\\" + fc
                            print("FeatureClass = " + FeatureClass)

                            # Describe a feature class
                            #
                            desc = arcpy.Describe(FeatureClass)

                            # Get the shape type (Polygon, Polyline) of the feature class
                            #
                            type = desc.shapeType

                            print("Feature Class Type = " + str(type))

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
                    print("Field Added")

                    # calculate the merge field to value 1
                    #
                    arcpy.CalculateField_management(
                        in_table=ShapefileAll,
                        field="MERGE",
                        expression="1",
                        expression_type="VB",
                        code_block="")
                    print("Field Calculated")

                    # dissolve the polygons based on the merge value of 1 creating one multipart
                    # polygon
                    #
                    dissolve = "C:\\TEMP\\" + FILE_ID + "\\Map_Selection_Dissolve.shp"
                    print("dissolve = " + dissolve)

                    arcpy.Dissolve_management(
                        in_features=ShapefileAll,
                        out_feature_class=dissolve,
                        dissolve_field="MERGE",
                        statistics_fields="",
                        multi_part="MULTI_PART",
                        unsplit_lines="DISSOLVE_LINES")
                    print("Features Dissolved")

                    # take the dissolved polygon and explode the single polygon into singlepart
                    # polygons
                    #
                    singlepart = "C:\\TEMP\\" + FILE_ID + "\\Map_Selection_Finished.shp"
                    print("singlepart = " + singlepart)
                    arcpy.MultipartToSinglepart_management(
                        in_features=ShapefileAll,
                        out_feature_class=singlepart)
                    print("Multi part to single part explosion")

                    # Add a field to count vertices "vertices"
                    #
                    arcpy.AddField_management(
                        in_table=ShapefileAll,
                        field_name="VERTICES",
                        field_type="FLOAT",
                        field_precision="255",
                        field_scale="0",
                        field_length="",
                        field_alias="",
                        field_is_nullable="NULLABLE",
                        field_is_required="NON_REQUIRED",
                        field_domain="")
                    print("Added field VERTICES")

                    # Calculate the vertices field with a count of vertices in that polygon
                    #
                    arcpy.CalculateField_management(ShapefileAll, "VERTICES", "!Shape!.pointCount-!Shape!.partCount", "PYTHON")
                    print("Calculate the amount of vertices in VERTICES field")

                    # print the count of all polygons found within the master shapefile
                    #
                    PolygonCounter = 0
                    with arcpy.da.SearchCursor(ShapefileAll,"MERGE") as cursor2:
                        for rows in cursor2:
                            PolygonCounter = PolygonCounter + 1
                    print("There are " + str(PolygonCounter) + " polygons")
                    del rows, cursor2, PolygonCounter

                    # create an ESRI GeoJSON for the master shapefile to be used to load into
                    # GeoCore
                    #
                    Out_JSON = "C:\\TEMP\\" + FILE_ID + ".json"
                    print("output JSON = " + unicode(Out_JSON))
                    arcpy.FeaturesToJSON_conversion(
                        in_features=ShapefileAll,
                        out_json_file=Out_JSON,
                        format_json="FORMATTED",
                        include_z_values="NO_Z_VALUES",
                        include_m_values="NO_M_VALUES",
                        geoJSON="GEOJSON")

                    print("-----------------")
                    print("ESRI JSON created")
                    print("-----------------")
                    row[3] = 1
                    row[4] = 1
                    cursor.updateRow(row)


                except:
                    print("--------------------")
                    print("JSON CREATION FAILED")
                    print("--------------------")
                    row[3] = 1
                    row[4] = 2
                    cursor.updateRow(row)
                    pass

                try:
                    arcpy.Delete_management(gdb)
                    print("Deleted Geodatabase")
                except:
                    print("Failed to delete Geodatabase")
                    pass
                try:
                    arcpy.Delete_management(save_path)
                    print("Deleted zip file")
                except:
                    print("Failed to delete zip file")
                    pass
                try:
                    arcpy.Delete_management(dissolve)
                    print("Deleted dissolved polygon shapefile")
                except:
                    print("Failed to delete disolved polygon shapefile")
                    pass
                try:
                    arcpy.Delete_management(singlepart)
                    print("Deleted singlepart polygon shapefile")
                except:
                    print("Failed to delete singlepart polygon shapefile")
                    pass
                try:
                    arcpy.Delete_management(ShapefileAll)
                    print("Deleted master shapefile")
                except:
                    print("failed to delete singlepart polygon shapefile")
                try:
                    arcpy.Delete_management(folder)
                except:
                    print("failed to delete folder")

            elif row[1] == 4 and row[3] != 1:
                FILE_ID = unicode(row[0])
                SCORE = unicode(row[1])
                URL = unicode(row[2])
                FINAL = unicode(row[3])
                print("FILE_ID = " + unicode(row[0]))
                print("SCORE = " + unicode(row[1]))
                print("URL = " + unicode(row[2]))
                print("FINAL = " + unicode(row[3]))

                try:
                    # Need to make the folder come from the ID
                    folder = "C:\\Temp\\" + str(FILE_ID)
                    # print("folder = " + folder)
                    path = r"C:\TEMP"
                    # print("path = " + path)
                    # URL must come from the master clean table
                    Extract_URL = URL
                    # print("Extract_URL = " + Extract_URL)
                    save_path = "C:\TEMP\download.zip"
                    # workspace must come from the folder name in the zip file (if that works)
                    workspace = "C:\\TEMP\\" + str(FILE_ID)
                    # Need a generic name to be used with all Shapefile datasets
                    ShapefileName = "Master_Merged_Shapefile.shp"
                    # print("ShapefileName = " + ShapefileName)
                    # Take these from new restructured names
                    ShapefileAll = folder + "\\" + ShapefileName
                    # print("ShapefileAll = " + ShapefileAll)
                    # Need a new generic name for geodatabase
                    Geodatabase_name = FILE_ID
                    # print("Geodatabase_name = " + Geodatabase_name)
                    Geodatabase = workspace + "\\" + Geodatabase_name  + ".gdb"
                    # print("Geodatabase = " + Geodatabase)
                    Geodatabase_basename = workspace + "\\" + Geodatabase_name

                    download_url(Extract_URL, save_path)
                    # print("download complete.  This is where it fails if the")
                    # print("URL doesn't point directly to a zip file")

                    extract_zipfile(save_path, folder)
                    # print("extracted zipfile")

                    create_shapefile(folder, ShapefileName)
                    # print("shapefile created")

                    arcpy.CreateFileGDB_management(
                        out_folder_path=workspace,
                        out_name=Geodatabase_name,
                        out_version="CURRENT")
                    # print("GDB created")

                    # print(folder + " = folder")
                    List_SHP = []
                    for (root,dirs,files) in os.walk(folder, topdown=True):
                        #print (root)
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
                        #print ('--------------------------------')
                    # print List_SHP
                    # print ('There are {} shapefiles in your list'.format(len(List_SHP)))

                    ShapefileAllName = os.path.basename(ShapefileAll)
                    # print("Name = " + ShapefileAllName)
                    BaseShapefileAllName = os.path.splitext(ShapefileAllName)[0]
                    # print("Shapefile All base name = " + BaseShapefileAllName)
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
                        # print("SHP = " + SHP)
                        #Shapefile = workspace + "\\" + SHP
                        Shapefile = SHP
                        # print "Shapefile: " + Shapefile
                        Name = os.path.basename(Shapefile)
                        # print "Name = " + Name
                        BaseName = os.path.splitext(Name)[0]
                        # print "BaseName = " + BaseName
                        arcpy.FeatureClassToFeatureClass_conversion(in_features=SHP, out_path=Geodatabase, out_name=BaseName, where_clause="", field_mapping="", config_keyword="")

                    fcs = listFcsInGDB(Geodatabase)

                    # Cycle through all feature classes in the geodatabase
                    #
                    # print "Cycle through feature classes in geodatabase"
                    for fc in fcs:
                        # set feature class location and name
                        #
                        FeatureClass = Geodatabase + "\\" + fc
                        # print "Feature class: " + FeatureClass

                        # Describe a feature class
                        #
                        desc = arcpy.Describe(FeatureClass)

                        # Get the shape type (Polygon, Polyline) of the feature class
                        #
                        type = desc.shapeType

                        # print str(type)
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
                    # print "Field Added"

                    # calculate the merge field to value 1
                    #
                    arcpy.CalculateField_management(
                        in_table=ShapefileAll,
                        field="MERGE",
                        expression="1",
                        expression_type="PYTHON",
                        code_block="")
                    # print "Field Calculated"

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

                    # print "Features Dissolved"

                    # take the dissolved polygon and explode the single polygon into singlepart
                    # polygons
                    #
                    singlepart = "C:/TEMP/MAP_Selection_Finished.shp"
                    arcpy.MultipartToSinglepart_management(
                        in_features=dissolve,
                        out_feature_class=singlepart)

                    # print "Multi part to single part explosion"

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

                    # print "Added field VERTICES"

                    # Calculate the vertices field with a count of vertices in that polygon
                    #
                    arcpy.CalculateField_management(
                        singlepart,
                        "VERTICES",
                        "!Shape!.pointCount-!Shape!.partCount",
                        "PYTHON")

                    print "Calculated the amount of vertices in VERTICES field"

                    # print the count of all polygons found within the master shapefile
                    #

                    PolygonCounter = 0
                    with arcpy.da.SearchCursor(singlepart,"MERGE") as cursor4:
                        for row4 in cursor4:
                            PolygonCounter = PolygonCounter + 1
                    print "There are " + str(PolygonCounter) + " polygons"
                    del row4, cursor4, PolygonCounter

                    #polygon_count = arcpy.GetCount_management(singlepart)
                    #print("There are " + str(polygon_count) + " polygons in this GEOJSON")
                    #del polygon_count


                    # create an ESRI GeoJSON for the master shapefile to be used to load into
                    # GeoCore
                    #
                    arcpy.FeaturesToJSON_conversion(
                        in_features=singlepart,
                        out_json_file="C:/TEMP/" + str(FILE_ID) + ".json",
                        format_json="NOT_FORMATTED",
                        include_z_values="NO_Z_VALUES",
                        include_m_values="NO_M_VALUES",
                        geoJSON="GEOJSON")

                    print "---------------------"
                    print "ESRI JSON created for " + str(FILE_ID)
                    print "---------------------"
                    row[3] = 1
                    row[4] = 1
                    cursor.updateRow(row)

                except:
                    print "---------------------"
                    print "Error in longest loop for " + str(FILE_ID)
                    print "---------------------"
                    row[3] = 1
                    row[4] = 2
                    cursor.updateRow(row)
                    pass
            elif row[1] == 3 and row[3] != 1:
                FILE_ID = unicode(row[0])
                SCORE = unicode(row[1])
                URL = unicode(row[2])
                FINAL = unicode(row[3])
                print("FILE_ID = " + unicode(row[0]))
                print("SCORE = " + unicode(row[1]))
                print("URL = " + unicode(row[2]))
                print("FINAL = " + unicode(row[3]))
                try:
                    arcpy.env.overwriteOutput = True
                    #baseURL = "https://gisp.dfo-mpo.gc.ca/arcgis/rest/services/FGP/Herring_Sections_Shapefile/MapServer/0"
                    #baseURL = "https://webservices.maps.canada.ca/arcgis/rest/services/StatCan/census_division_2016_en/MapServer/0"
                    #baseURL = "https://proxyinternet.nrcan-rncan.gc.ca/arcgis/rest/services/CLSS-SATC/CLSS_Administrative_Boundaries/MapServer/1"
                    #baseURL = "https://agriculture.canada.ca/atlas/rest/services/servicesimage/anomalies_idvn_maximal_hebdomadaire_v2/ImageServer"
                    #baseURL = "https://maps-cartes.services.geo.ca/imagery_images/rest/services/NRCan/couverture_terrestre_du_canada_2000_2011/ImageServer"
                    baseURL = URL
                    #baseURL = "https://maps-cartes.services.geo.ca/server_serveur/rest/services/NRCan/dsra_cascadia_en/MapServer/3"
                    #baseURL = "https://agriculture.canada.ca/atlas/rest/services/servicesimage/inventaire_annuel_des_cultures_2018/ImageServer"
                    fields = "*"
                    outdata = "C:/TEMP/geodatabase.gdb/FeatureClass"
                    gdb = "C:/TEMP/geodatabase.gdb"
                    gdbName = "geodatabase"
                    folder = "C:/TEMP"
                    ShapefileName = "MasterShapefile.shp"
                    ShapefileAll = folder + "\\" + ShapefileName

                    arcpy.CreateFileGDB_management(
                    out_folder_path=folder,
                    out_name=gdbName,
                    out_version="CURRENT")

                    # Get record extract limit
                    urlstring = baseURL + "?f=json"
                    j = urllib2.urlopen(urlstring)
                    js = json.load(j)
                    maxrc = int(js["maxRecordCount"])
                    print "Record extract limit: %s" % maxrc

                    # Get object ids of features
                    where = "1=1"
                    urlstring = baseURL + "/query?where={}&returnIdsOnly=true&f=json".format(where)
                    j = urllib2.urlopen(urlstring)
                    js = json.load(j)
                    idfield = js["objectIdFieldName"]
                    idlist = js["objectIds"]
                    idlist.sort()
                    numrec = len(idlist)
                    print "Number of target records: %s" % numrec

                    # Gather features
                    print "Gathering records..."
                    fs = dict()
                    for i in range(0, numrec, maxrc):
                        torec = i + (maxrc - 1)
                        if torec > numrec:
                            torec = numrec - 1
                        fromid = idlist[i]
                        toid = idlist[torec]
                        where = "{} >= {} and {} <= {}".format(idfield, fromid, idfield, toid)
                        print "  {}".format(where)
                        urlstring = baseURL + "/query?where={}&returnGeometry=true&outFields={}&f=json".format(where,fields)
                        fs[i] = arcpy.FeatureSet()
                        fs[i].load(urlstring)

                    # Save features
                    print "Saving features..."
                    fslist = []
                    for key,value in fs.items():
                        fslist.append(value)

                    arcpy.Merge_management(fslist, outdata)
                    print "Done!"

                    arcpy.CreateFeatureclass_management(
                        out_path=folder,
                        out_name=ShapefileName,
                        geometry_type="POLYGON",
                        template="",
                        has_m="DISABLED",
                        has_z="DISABLED",
                        spatial_reference="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision",
                        config_keyword="",
                        spatial_grid_1="0",
                        spatial_grid_2="0",
                        spatial_grid_3="0")

                    arcpy.env.workspace = gdb

                    fcs = arcpy.ListFeatureClasses()

                    for fc in fcs:
                        # set feature class location and name
                        #
                        FeatureClass = gdb + "\\" + fc
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

                        # run these instructions if type is polyline
                        #
                        elif type == "Polyline":
                            lineTransform(FeatureClass)

                        del fcs
                        del fc
                        #Extract shapefile names to create paths and new shapefiles from them.
                    #
                    ShapefileAllName = os.path.basename(ShapefileAll)
                    BaseShapefileAllName = os.path.splitext(ShapefileAllName)[0]

                    dissolve = folder + "\\" + BaseShapefileAllName + "_dissolve.shp"
                    singlepart = folder + "\\" + BaseShapefileAllName + "_singlepart.shp"
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
                    arcpy.Dissolve_management(
                        in_features=ShapefileAll,
                        out_feature_class=singlepart,
                        dissolve_field="MERGE",
                        statistics_fields="",
                        multi_part="SINGLE_PART",
                        unsplit_lines="DISSOLVE_LINES")

                    print "Features Dissolved to Single Part"

                    # take the dissolved polygon and explode the single polygon into singlepart
                    # polygons
                    #
                    arcpy.MultipartToSinglepart_management(
                        in_features=ShapefileAll,
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

                    with arcpy.da.SearchCursor(singlepart,"MERGE") as cursor3:
                        for row3 in cursor3:
                            PolygonCounter = PolygonCounter + 1
                    print "There are " + str(PolygonCounter) + " polygons"

                    del row3, cursor3, PolygonCounter

                    # create an ESRI GeoJSON for the master shapefile to be used to load into
                    # GeoCore
                    #
                    arcpy.FeaturesToJSON_conversion(
                        in_features=singlepart,
                        out_json_file="C:/TEMP/" + str(FILE_ID) + ".json",
                        format_json="FORMATTED",
                        include_z_values="NO_Z_VALUES",
                        include_m_values="NO_M_VALUES",
                        geoJSON="GEOJSON")
                    print "---------------------------"
                    print "SUCCESS! ESRI JSON created"
                    print "---------------------------"
                    row[3] = 1
                    row[4] = 1
                    cursor.updateRow(row)

                except:
                    print "Failed"
                    print "------------------------"
                    print "ERROR in JSON creation"
                    print "------------------------"
                    row[3] = 1
                    row[4] = 2
                    cursor.updateRow(row)
                    pass

                try:
                    arcpy.Delete_management(gdb)
                    #print "Delete gdb worked"
                except:
                    #print "Delete gdb passed error, may not exist"
                    pass

                try:
                    arcpy.Delete_management(ShapefileAll)
                    #print "Delete ShapefileAll worked"
                except:
                    #print "Delete gdb passed error, may not exist"
                    pass

                try:
                    arcpy.Delete_management(dissolve)
                    #print "Delete dissolve worked"
                except:
                    #print "Delete dissolve passed error, may not exist"
                    pass

                try:
                    arcpy.Delete_management(singlepart)
                    #print "Delete singlepart worked"
                except:
                    #print "Delete singlepart passed error, may not exist"
                    pass

            try:
                arcpy.Delete_management(folder)
                #print "Delete folder worked"
            except:
                #print "Delete Folder passed error, may not exist"
                pass

            try:
                arcpy.Delete_management(dissolve)
                #print "Delete dissolve worked"
            except:
                #print "Delete dissolve passed error, may not exist"
                pass

            try:
                arcpy.Delete_management(singlepart)
                #print "Delete singlepart worked"
            except:
                #print "Delete singlepart passed error, may not exist"
                pass

            try:
                arcpy.Delete_management(save_path)
                #print "Delete save_path worked"
            except:
                #print "Delete of save_path passed error, may not exist"
                pass
