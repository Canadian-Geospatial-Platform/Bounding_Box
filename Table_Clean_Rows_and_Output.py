# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# TableSelect_ModelOutput.py
# Created on: 2023-11-07 11:56:53.00000
#   (generated by ArcGIS/ModelBuilder)
# Description:
# ---------------------------------------------------------------------------
import arcpy

# Parameters/Variables
#
OutFolderPath = "C:/TEMP/"
OutName = "Records.gdb"
InputCSV = OutFolderPath + "records.csv"
GeoDataBase = OutFolderPath + OutName
GDBTableName = "records_cleaned_of_columns"
GDBOutputTableName = "records_column_and_rows_clean"
GDBInputTableName = "records_column_and_rows_clean"
GDBTablePathAndName = GeoDataBase + "/" + GDBTableName
GDBTableOutputPathAndName = GeoDataBase + "/" + GDBOutputTableName
GDBTableInputPathAndName = GeoDataBase + "/" + GDBInputTableName
ExcelOutputTable = OutFolderPath + "records.xls"
DBFName = "records_clean.dbf"

print "GeoDataBase path = " + GeoDataBase
print "Input CSV = " + InputCSV
print "GDB Name = " + OutName
print "Output Folder Path = " + OutFolderPath
print "Geodatabase Table Name (Cleaned columns) = " + GDBTableName
print "Geodatabase table path and name (Cleaned Columns) = " + GDBTablePathAndName
print "Geodatabase table output path and name (cleaned columns and rows) = " + GDBTableOutputPathAndName
print "Geodatabase table input path and name = " + GDBTableInputPathAndName
print "Excel output table (xls) = " + ExcelOutputTable

# Create a file GDB for ease of use.
#
arcpy.CreateFileGDB_management(OutFolderPath, OutName, out_version="CURRENT")
print "Created a file GDB for ease of use"

# Convert to GDB table for ease of use
#
arcpy.TableToTable_conversion(InputCSV,GeoDataBase,GDBTableName, where_clause="", field_mapping='Field1 "Field1" true true false 4 Long 0 0 ,First,#,C:\TEMP\records.csv,Field1,-1,-1;features_properties_id_ "features_properties_id" true true false 8000 Text 0 0 ,First,#,C:\TEMP\records.csv,features_properties_id,-1,-1', config_keyword="")
print "Converted to GDB table for ease of use"

# Create a clean table with all of the elements that you don't need queried out
#
arcpy.TableSelect_analysis(GDBTablePathAndName, GDBTableOutputPathAndName, where_clause="features_properties_id_ NOT LIKE 'ccmeo%' AND features_properties_id_ NOT LIKE 'CGDI%' AND features_properties_id_ NOT LIKE 'eodms%' AND features_properties_id_ IS NOT NULL")
print " Cleaned table of all rows that are not to be used in this process"

# add field to table, old field is too long at 8000 characters
#
arcpy.AddField_management(GDBTableInputPathAndName, field_name="Feature_ID", field_type="TEXT", field_precision="", field_scale="", field_length="256", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
print "Add a field to be a better length as opposed to 8000 characters, 256 characters now.

# Calculate field to hold all values from original ID field from csv table
#
arcpy.CalculateField_management(GDBTableInputPathAndName, field="Feature_ID", expression="!features_properties_id_!", expression_type="PYTHON_9.3", code_block="")
print "Move field values over to Feature_ID from original field

# Delete extraineous fields
#
arcpy.DeleteField_management(GDBTableInputPathAndName, drop_field="Field1;features_properties_id_")
print "Delete extraneous fields"

# Convert cleaned table to Excel file
#
arcpy.TableToExcel_conversion(GDBTableInputPathAndName, ExcelOutputTable, Use_field_alias_as_column_header="NAME", Use_domain_and_subtype_description="CODE")
print "Excel table output created"

# GDB table to DBF for interoperability
#
arcpy.TableToTable_conversion(GDBTableInputPathAndName, OutFolderPath, DBFName, where_clause="", field_mapping='Feature_ID "Feature_ID" true true false 256 Text 0 0 ,First,#,C:\TEMP\Records.gdb\records_column_and_rows_clean,Feature_ID,-1,-1', config_keyword="")
print "DBF table exported for interoperability"