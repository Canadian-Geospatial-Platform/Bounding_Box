#-------------------------------------------------------------------------------
# Name:       MASTER SCRIPT Python 2.7
# Purpose:
#
# https://stackoverflow.com/questions/73306198/how-to-delete-a-particular-column-in-csv-file-without-pandas-library
# https://www.w3schools.com/python/pandas/pandas_cleaning_empty_cells.asp
#
#-------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Description:
    # Author: Sean Eagles
    # takes an input CSV and runs through a geodatabase and back out to clean
    # the table properly, simplify the output fields and make it work with
    # Joins and relates.
# ---------------------------------------------------------------------------
import dbf
import arcpy
import csv
import pandas as pd
import urllib2
from contextlib import closing
import geojson
import arcpy

def main():
    pass

def download_url(url, save_path):
    with closing(urllib2.urlopen(url)) as dl_file:
        with open(save_path, 'wb') as out_file:
            out_file.write(dl_file.read())

# Parameters/Variables
#
csv_path = (r"C:\temp\records.csv")
OutFolderPath = "C:/TEMP/"
OutName = "Records.gdb"
InputCSV = OutFolderPath + "records_remove_empty.csv"
GeoDataBase = OutFolderPath + OutName
GDBTableName = "records_cleaned_of_columns"
GDBOutputTableName = "records_column_and_rows_clean"
GDBInputTableName = "records_column_and_rows_clean"
GDBTablePathAndName = GeoDataBase + "/" + GDBTableName
GDBTableOutputPathAndName = GeoDataBase + "/" + GDBOutputTableName
GDBTableInputPathAndName = GeoDataBase + "/" + GDBInputTableName
ExcelOutputTable = OutFolderPath + "records.xls"
DBFName = "records_clean.dbf"
data = "C:/TEMP/records.csv"
data_out = "C:/TEMP/records_remove_empty.csv"

print "GeoDataBase path = " + GeoDataBase
print "Input CSV = " + InputCSV
print "GDB Name = " + OutName
print "Output Folder Path = " + OutFolderPath
print "Geodatabase Table Name (Cleaned columns) = " + GDBTableName
print "Geodatabase table path and name (Cleaned Columns) = " + GDBTablePathAndName
print "Geodatabase table output path and name (cleaned columns and rows) = " + GDBTableOutputPathAndName
print "Geodatabase table input path and name = " + GDBTableInputPathAndName
print "Excel output table (xls) = " + ExcelOutputTable
print csv_path + " = csv_path"
print "Data table input = " + data
print "Data table output = " + data_out

if __name__ == '__main__':

    with open(csv_path) as instream:
        # Setup the input
        reader = csv.DictReader(instream)
        rows = list(reader)

        # Setup the output fields
        output_fields = reader.fieldnames
        output_fields.remove("features_type")
        output_fields.remove("features_geometry_type")
        output_fields.remove("features_geometry_coordinates")
        output_fields.remove("features_properties_title_en")
        output_fields.remove("features_properties_title_fr")
        output_fields.remove("features_properties_description_en")
        output_fields.remove("features_properties_description_fr")
        output_fields.remove("features_properties_keywords_en")
        output_fields.remove("features_properties_keywords_fr")
        output_fields.remove("features_properties_topicCategory")
        output_fields.remove("features_properties_parentIdentifier")
        output_fields.remove("features_properties_date_published_text")
        output_fields.remove("features_properties_date_published_date")
        output_fields.remove("features_properties_date_created_text")
        output_fields.remove("features_properties_date_created_date")
        output_fields.remove("features_properties_date_revision_text")
        output_fields.remove("features_properties_date_revision_date")
        output_fields.remove("features_properties_date_notavailable_text")
        output_fields.remove("features_properties_date_notavailable_date")
        output_fields.remove("features_properties_date_inforce_text")
        output_fields.remove("features_properties_date_inforce_date")
        output_fields.remove("features_properties_date_adopted_text")
        output_fields.remove("features_properties_date_adopted_date")
        output_fields.remove("features_properties_date_deprecated_text")
        output_fields.remove("features_properties_date_deprecated_date")
        output_fields.remove("features_properties_date_superceded_text")
        output_fields.remove("features_properties_date_superceded_date")
        output_fields.remove("features_properties_spatialRepresentation")
        output_fields.remove("features_properties_type")
        output_fields.remove("features_properties_geometry")
        output_fields.remove("features_properties_temporalExtent_begin")
        output_fields.remove("features_properties_temporalExtent_end")
        output_fields.remove("features_properties_refSys")
        output_fields.remove("features_properties_refSys_version")
        output_fields.remove("features_properties_status")
        output_fields.remove("features_properties_maintenance")
        output_fields.remove("features_properties_metadataStandard_en")
        output_fields.remove("features_properties_metadataStandard_fr")
        output_fields.remove("features_properties_metadataStandardVersion")
        output_fields.remove("features_properties_otherConstraints_en")
        output_fields.remove("features_properties_otherConstraints_fr")
        output_fields.remove("features_properties_graphicOverview")
        output_fields.remove("features_properties_distributionFormat_name")
        output_fields.remove("features_properties_distributionFormat_format")
        output_fields.remove("features_properties_useLimits_en")
        output_fields.remove("features_properties_useLimits_fr")
        output_fields.remove("features_properties_accessConstraints")
        output_fields.remove("features_properties_dateStamp")
        output_fields.remove("features_properties_dataSetURI")
        output_fields.remove("features_properties_locale_language")
        output_fields.remove("features_properties_locale_country")
        output_fields.remove("features_properties_locale_encoding")
        output_fields.remove("features_properties_language")
        output_fields.remove("features_properties_characterSet")
        output_fields.remove("features_properties_environmentDescription")
        output_fields.remove("features_properties_supplementalInformation_en")
        output_fields.remove("features_properties_supplementalInformation_fr")
        output_fields.remove("features_properties_contact")
        output_fields.remove("features_properties_credits")
        output_fields.remove("features_properties_cited")
        output_fields.remove("features_properties_distributor")
        output_fields.remove("features_properties_options")
        output_fields.remove("features_properties_temporalExtent_end_@indeterminatePosition")
        output_fields.remove("features_properties_temporalExtent_end_#text")
        output_fields.remove("features_properties_plugins")
        output_fields.remove("features_properties_sourceSystemName")
        output_fields.remove("features_popularity")
        output_fields.remove("features_similarity")

    with open(csv_path, "w") as outstream:
        # Setup the output
        writer = csv.DictWriter(
            outstream,
            fieldnames=output_fields,
            extrasaction="ignore",  # Ignore extra dictionary keys/values
        )

        # Write to the output
        writer.writeheader()
        writer.writerows(rows)

    df = pd.read_csv(data)

    new_df = df.dropna()

    print(new_df.to_string())

    new_df.to_csv(data_out)

    # Create a file GDB for ease of use.
    #
    arcpy.CreateFileGDB_management(OutFolderPath, OutName, out_version="CURRENT")
    print "Created a file GDB for ease of use"

    # Convert to GDB table for ease of use
    #
    arcpy.TableToTable_conversion(InputCSV,GeoDataBase, GDBTableName, where_clause="", field_mapping='Field1 "Field1" true true false 4 Long 0 0 ,First,#,C:\TEMP\records_remove_empty.csv,Field1,-1,-1;features_properties_id "features_properties_id" true true false 8000 Text 0 0 ,First,#,C:\TEMP\records_remove_empty.csv,features_properties_id,-1,-1', config_keyword="")
    print "Converted to GDB table for ease of use"

    # Create a clean table with all of the elements that you don't need queried out
    #
    arcpy.TableSelect_analysis(GDBTablePathAndName, GDBTableOutputPathAndName, where_clause="features_properties_id NOT LIKE 'ccmeo%' AND features_properties_id NOT LIKE 'CGDI%' AND features_properties_id NOT LIKE 'eodms%' AND features_properties_id IS NOT NULL")
    print " Cleaned table of all rows that are not to be used in this process"

    # add field to table, old field is too long at 8000 characters
    #
    arcpy.AddField_management(GDBTableInputPathAndName, field_name="Feature_ID", field_type="TEXT", field_precision="", field_scale="", field_length="256", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
    print "Add a field to be a better length as opposed to 8000 characters, 256 characters now."

    # Calculate field to hold all values from original ID field from csv table
    #
    arcpy.CalculateField_management(GDBTableInputPathAndName, field="Feature_ID", expression="!features_properties_id!", expression_type="PYTHON_9.3", code_block="")
    print "Move field values over to Feature_ID from original field"

    # Delete extraineous fields
    #
    arcpy.DeleteField_management(GDBTableInputPathAndName, drop_field="Field1;features_properties_id;Unnamed__0")
    print "Delete extraneous fields"

    # Convert cleaned table to Excel file
    #
    arcpy.TableToExcel_conversion(GDBTableInputPathAndName, ExcelOutputTable, Use_field_alias_as_column_header="NAME", Use_domain_and_subtype_description="CODE")
    print "Excel table output created"

    # GDB table to DBF for interoperability
    #
    arcpy.TableToTable_conversion(GDBTableInputPathAndName, OutFolderPath, DBFName, where_clause="", field_mapping='Feature_ID "Feature_ID" true true false 256 Text 0 0 ,First,#,C:\TEMP\Records.gdb\records_column_and_rows_clean,Feature_ID,-1,-1', config_keyword="")
    print "DBF table exported for interoperability"

    # Variables:
    #
    # to do: change hardcoded to variables
    FOLDER = "C:/TEMP"
    FILENAME = "catalogue_scrape.dbf"
    CATALOGUE_SCRAPE = FOLDER + "//" + FILENAME
    #filename_geocore = "34c0dbf2-9595-84f3-679c-7d2d7c90ecfe.geojson"  #worked
    #filename_geocore = "000183ed-8864-42f0-ae43-c4313a860720.geojson"  #worked
    #filename_geocore = "cebc283f-bae1-4eae-a91f-a26480cd4e4a.geojson"  #worked
    #filename_geocore = "2606b1b4-c895-4d23-b466-ad3d64b6381e.geojson"  #worked
    #filename_geocore = "08166334-889d-4c3a-9b25-b1b85ba48f2c.geojson"  #worked
    #filename_geocore = "05002515-f6cc-4516-b225-38d510eaaf9c.geojson"  #worked
    #filename_geocore = "090494a6-8aaf-4c26-b7b3-cf52400bf619.geojson"  #worked
    #filename_geocore = "054cf636-6637-2508-9aef-0f9139734f4a.geojson"   #worked, 42 records long
    #filename_geocore = "02d6f853-b0fe-4aa4-bc73-dff0db45d8ae.geojson"
    #filename_geocore = "d2af02fe-9e12-413d-8959-06be963bde52.geojson"
    FILENAME_GEOCORE = "9e1507cd-f25c-4c64-995b-6563bf9d65bd.geojson"
    FILEID = str("9e1507cd-f25c-4c64-995b-6563bf9d65bd")
    GEOJSON_URL = 'https://geocore.metadata.geo.ca/' + str(FILENAME_GEOCORE)
    SAVE_PATH = "C:/TEMP/{}".format(FILENAME_GEOCORE)
    FILE_ID = str(FILENAME_GEOCORE)
    #cgp_encoding = ""

    # now download the geojson file and save it to the TEMP directory
    #
    download_url(GEOJSON_URL, SAVE_PATH)

    with open(SAVE_PATH) as f:
        GEOJSON = geojson.load(f)
    ITEM_DICTIONARY = GEOJSON
    OPTIONS_COUNT = len(ITEM_DICTIONARY['features'][0]['properties']['options'])
    print str(OPTIONS_COUNT) + " = options count"
    URL_COUNT = OPTIONS_COUNT
    print "URL count for all options = " + str(URL_COUNT)
    PROTOCOL_COUNT = OPTIONS_COUNT
    print "PROTOCOL count for all options = " + str(PROTOCOL_COUNT)
    NAME_COUNT = OPTIONS_COUNT
    print "NAME count for all options = " + str(NAME_COUNT)
    DESCRIPTION_COUNT = len(ITEM_DICTIONARY['features'][0]['properties']['options'][0]['description'])
    DESCRIPTION_COUNT = DESCRIPTION_COUNT * OPTIONS_COUNT
    print "DESCRIPTION count for all options = " + str(DESCRIPTION_COUNT)


    print "Downloaded geoJSON GeoCore file"
    print "URL = " + str(GEOJSON_URL)
    print "save_path = " + str(SAVE_PATH)

    #We now have every attribute counted from the original GeoJSON.
    #We are going to create an attribute table to hold all of this data.
    #We are going to use the name_count attribute as a number to define how many
    #rows we are going to add to the attribute table.
    #For this example the number of rows to add is

    print "Number of lines to be added " + unicode(NAME_COUNT)
    #the name_count attribute"""

    # Set DBF encoding from ASCII to UTF-8, also created new DBF table
    #
    dbf.Table(r'C:\TEMP\catalogue_scrape.dbf', 'FILENAME C(100); FILEID C(254); URL C(254); PROTOCOL C(100); NAME C(254); NAME_EN C(254); NAME_FR C(254); DESC_ C(254); DESC_EN C(254); DESC_FR C(254); ROWID_ C(10)', codepage=0xf0)
    print "Table created, catalogue_scrape.dbf"

    # Create insert cursor for table
    #
    ROWS = arcpy.InsertCursor(r"C:\TEMP\catalogue_scrape.dbf")

    # Create new rows based off of how many names
    # exist in the options attributes.
    #
    for x in range(0, NAME_COUNT):
        row = ROWS.newRow()
        ROWS.insertRow(row)

    # Delete cursor and row objects to remove locks on the data
    #
    del row
    del ROWS

    ROWS = arcpy.UpdateCursor(r"C:\TEMP\catalogue_scrape.dbf")


    for row in ROWS:
        row.setValue("FILENAME", SAVE_PATH)
        row.setValue("FILEID", str(FILEID))
        ROWS.updateRow(row)

    del row
    del ROWS

    FEATURE = 0
    while FEATURE < OPTIONS_COUNT:

        ROWS = arcpy.UpdateCursor(r"C:\TEMP\catalogue_scrape.dbf")
        ROW_NUMBER = 0
        print str(ROW_NUMBER) + " = row number in catalo"
        print str(OPTIONS_COUNT) + " = options count"
        print str(FEATURE) + " = feature counter"
        print "inside loop1"

        for row in ROWS:
            print "inside loop2"
            #url = gj['features'][0]['properties']['options'][int(feature)]['url']
            #print str(feature) + " = feature"
            print str(ROW_NUMBER) + " = row number"
            if FEATURE == ROW_NUMBER and FEATURE < OPTIONS_COUNT:

                print "inside if statement"
                print FEATURE
                url = GEOJSON['features'][0]['properties']['options'][int(FEATURE)]['url']
                protocol = GEOJSON['features'][0]['properties']['options'][int(FEATURE)]['protocol']
                name_en = GEOJSON['features'][0]['properties']['options'][int(FEATURE)]['name']['en']
                name_fr = GEOJSON['features'][0]['properties']['options'][int(FEATURE)]['name']['fr']
                name = unicode(GEOJSON['features'][0]['properties']['options'][int(FEATURE)]['name']['en']) + unicode(GEOJSON['features'][0]['properties']['options'][int(FEATURE)]['name']['fr'])
                print name + " = name"
                description_en = GEOJSON['features'][0]['properties']['options'][int(FEATURE)]['description']['en']
                description_fr = GEOJSON['features'][0]['properties']['options'][int(FEATURE)]['description']['fr']
                description = unicode(description_en) + unicode(description_fr)
                print description + " = description"
                row.setValue("NAME", name)
                row.setValue("NAME_EN", name_en)
                row.setValue("NAME_FR", name_fr)
                row.setValue("DESC_", description)
                row.setValue("DESC_EN", description_en)
                row.setValue("DESC_FR", description_fr)
                row.setValue("PROTOCOL", protocol)
                row.setValue("URL", url)
                row.setValue("ROWID_", FEATURE)
                ROWS.updateRow(row)
                print "url = " + str(url)
            FEATURE = FEATURE + 1
            ROW_NUMBER = ROW_NUMBER + 1

            print str(ROW_NUMBER) + " = row number"
            print str(FEATURE) + " = feature number"

        #print "Option count = " + str(options_count)
        #print "Feature = " + str(feature)
        #options = GEOJSON['features'][0]['properties']['options'][int(feature)]

        print "url count = " + str(URL_COUNT)
        #print options

    del row
    del ROWS

    # Clean up all files that are not needed and should be deleted after this
    # process is done
    arcpy.Delete_management(in_data="C:/TEMP/Records.gdb", data_type="Workspace")
    arcpy.Delete_management(in_data="C:/TEMP/Records.gdb", data_type="Folder")
    arcpy.Delete_management(in_data="C:/TEMP/records.csv", data_type="TextFile")
    arcpy.Delete_management(in_data="C:/TEMP/records.xls", data_type="File")
    arcpy.Delete_management(in_data="C:/TEMP/records_remove_empty.csv", data_type="TextFile")

