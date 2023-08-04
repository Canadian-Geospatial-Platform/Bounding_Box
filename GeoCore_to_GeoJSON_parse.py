import geojson
import json
import arcpy
import urllib2
from contextlib import closing

def main():
    pass

def download_url(url, save_path):
    with closing(urllib2.urlopen(url)) as dl_file:
        with open(save_path, 'wb') as out_file:
            out_file.write(dl_file.read())

if __name__ == '__main__':

    # Variables:
    #
    folder = "C:/TEMP"
    filename = "catalogue_scrape.dbf"
    catalogue_scrape = folder + "//" + filename
    geojson_url = 'https://geocore.metadata.geo.ca/0005301b-624e-4000-8dad-a1a1ac6b46c2.geojson'
    save_path = r"C:/TEMP/0005301b-624e-4000-8dad-a1a1ac6b46c2.geojson"
    file_id = "0005301b-624e-4000-8dad-a1a1ac6b46c2.geojson"

    # now download the geojson file and save it to the TEMP directory
    #
    download_url(geojson_url, save_path)

    #with open(r"C:\Users\seagles\Desktop\Bounding Boxes\00ccde98-1bbd-45bb-acf4-3f8b0e8aef1d.geojson") as f:
    #with open(r"c:\Users\seagles\Desktop\Bounding Boxes\0a2dfadd-57eb-4d64-a56d-ff53c431aaaa.geojson") as f:
    with open(save_path) as f:
        gj = geojson.load(f)
    '''features = gj['features'][0]
    print features'''
    '''options = gj['features'][0]['properties']['options'][0]
    print options'''
    item_dict = gj
    options_count = len(item_dict['features'][0]['properties']['options'])
    print str(options_count) + " = options count"
    url_count = options_count
    print "URL count for all options = " + str(url_count)
    protocol_count = options_count
    print "PROTOCOL count for all options = " + str(protocol_count)
    name_count = len(item_dict['features'][0]['properties']['options'][0]['name'])
    name_count = name_count * options_count
    print "NAME count for all options = " + str(name_count)
    description_count = len(item_dict['features'][0]['properties']['options'][0]['description'])
    description_count = description_count * options_count
    print "DESCRIPTION count for all options = " + str(description_count)


    print "Downloaded geoJSON GeoCore file"
    print "URL = " + str(geojson_url)
    print "save_path = " + str(save_path)



    """
    We now have every attribute counted from the original GeoJSON.
    We are going to create an attribute table to hold all of this data.
    We are going to use the name_count attribute as a number to define how many
    rows we are going to add to the attribute table.
    For this example the number of rows to add is """
    print "Number of lines to be added " + str(name_count)
    """the name_count attribute"""

    #  Create attribute table
    #
    arcpy.CreateTable_management(folder, "catalogue_scrape.dbf")
    print("Table Created")

    # add fields that are needed to the attribute table
    #
    arcpy.AddField_management(catalogue_scrape, "FILENAME", "TEXT", field_length=100)
    print "FILENAME field added to catalogue_scrape.dbf"
    arcpy.AddField_management(catalogue_scrape, "FILEID", "TEXT", field_length=100)
    print "FILEID field added to catalogue_scrape.dbf"
    arcpy.AddField_management(catalogue_scrape, "URL", "TEXT", field_length=256)
    print "URL field added to catalogue_scrape.dbf"
    arcpy.AddField_management(catalogue_scrape, "PROTOCOL", "TEXT", field_length=100)
    print "PROTOCOL field added to catalogue_scrape.dbf"
    arcpy.AddField_management(catalogue_scrape, "NAME", "TEXT", field_length=256)
    print "NAME field added to catalogue_scrape.dbf"
    arcpy.AddField_management(catalogue_scrape, "NAME-EN", "TEXT", field_length=256)
    print "NAME-EN field added to catalogue_scrape.dbf"
    arcpy.AddField_management(catalogue_scrape, "NAME-FR", "TEXT", field_length=256)
    print "NAME-FR field added to catalogue_scrape.dbf"
    arcpy.AddField_management(catalogue_scrape, "DESC", "TEXT", field_length=256)
    print "DESC field added to catalogue_scrape.dbf"
    arcpy.AddField_management(catalogue_scrape, "DESC-EN", "TEXT", field_length=256)
    print "DESC-EN field added to catalogue_scrape.dbf"
    arcpy.AddField_management(catalogue_scrape, "DESC-FR", "TEXT", field_length=256)
    print "DESC-EN field added to catalogue_scrape.dbf"
    arcpy.AddField_management(catalogue_scrape, "ROWID", "TEXT", field_length=10)
    print "ROWIDS field added to catalogue_scrape.dbf"

    # delete the automatically added Field1 attribute field
    #
    arcpy.DeleteField_management(catalogue_scrape, "Field1")

    # Create insert cursor for table
    #
    rows = arcpy.InsertCursor("c:\TEMP\catalogue_scrape.dbf")

    # Create new rows based off of how many names
    # exist in the options attributes.
    #
    for x in range(0, name_count):
        row = rows.newRow()
        rows.insertRow(row)
        #row.setValue("distance", 100)
        #row.setValue()


    # Delete cursor and row objects to remove locks on the data
    #
    del row
    del rows

    rows = arcpy.UpdateCursor("c:\TEMP\catalogue_scrape.dbf")


    for row in rows:
        row.setValue("FILENAME", save_path)
        row.setValue("FILEID", file_id)
        rows.updateRow(row)

    del row
    del rows

    feature = 0
    while feature < options_count:

        rows = arcpy.UpdateCursor("c:\TEMP\catalogue_scrape.dbf")
        row_number = 0
        print str(row_number) + " = row number in catalo"
        print str(options_count) + " = options count"
        print str(feature) + " = feature counter"
        print "inside loop1"

        for row in rows:
            print "inside loop2"
            #url = gj['features'][0]['properties']['options'][int(feature)]['url']
            #print str(feature) + " = feature"
            print str(row_number) + " = row number"
            if feature == row_number and feature < options_count:

                print "inside if statement"
                print feature
                url = gj['features'][0]['properties']['options'][int(feature)]['url']
                protocol = gj['features'][0]['properties']['options'][int(feature)]['protocol']
                name_en = gj['features'][0]['properties']['options'][int(feature)]['name']['en']
                name_fr = gj['features'][0]['properties']['options'][int(feature)]['name']['fr']
                name = name_en + name_fr
                description_en = gj['features'][0]['properties']['options'][int(feature)]['description']['en']
                description_fr = gj['features'][0]['properties']['options'][int(feature)]['description']['fr']
                description = description_en + description_fr
                row.setValue("NAME", name)
                row.setValue("NAME_EN", name_en)
                row.setValue("NAME_FR", name_fr)
                row.setValue("DESC_", description)
                row.setValue("DESC_EN", description_en)
                row.setValue("DESC_FR", description_fr)
                row.setValue("PROTOCOL", protocol)
                row.setValue("URL", url)
                row.setValue("ROWID_", feature)
                rows.updateRow(row)
                print "url = " + str(url)
            feature = feature + 1
            row_number = row_number + 1

            '''elif feature == row_number and feature >= name_count:
                url_adjust ='''


            print str(row_number) + " = row number"
            print str(feature) + " = feature number"

        #print "Option count = " + str(options_count)
        #print "Feature = " + str(feature)
        #options = gj['features'][0]['properties']['options'][int(feature)]

        print "url count = " + str(url_count)
        #print options

    del row
    del rows

    feature2 = 0
    feature = options_count
    print "Feature 2 = " + str(feature2)
    print "Feature = " + str(feature)
    print "Options count = " + str(options_count)

    while feature >= options_count and feature < name_count:

        row_number = 0

        rows = arcpy.UpdateCursor("c:\TEMP\catalogue_scrape.dbf")
        print "row number Loop 1 = " + str(row_number)

        for row in rows:
            print "row number Loop 2 =  " + str(row_number)

            if feature == row_number and feature2 < options_count:
                print "Feature2 in if statement = " + str(feature2)
                url = gj['features'][0]['properties']['options'][int(feature2)]['url']
                row.setValue("URL", url)
                rows.updateRow(row)
                print "url = " + str(url)
                print str(row_number) + " = row number"
                print str(feature) + " = feature number"
                print str(options_count) + " = options count"
                print str(feature2) + " = feature2 number"
                feature2 = feature2 + 1
                feature = feature + 1
            row_number = row_number + 1

    del row
    del rows

    print str(feature) + " = features for second round calculations"
    print str(row_number) + " = row number to start with for new calculations"
    print str(options_count) + " = options counter for calculating starter row value"
    print str(name_count) + " = maximum number for row calculations"

    print "When this is complete attributes should be added to another table using the append function"

    print "For the options attributes to be used to populate the attribute table, the statistics are below."
    print "There are " + str(options_count) + " options"
    print "There are " + str(url_count) + " urls, one for each feature under options"
    print "There are " + str(protocol_count) + " protocols, one for each feature under options"
    print "There are " + str(name_count) + " names, one english and one french for each feature under options"
    print "There are " + str(description_count) + " descriptions, one english and one french for each feature under options"
    print "This means that there are " + str(name_count) + " lines to be added to the attribute table, and four lines to fill based on attributes on the line before them"


