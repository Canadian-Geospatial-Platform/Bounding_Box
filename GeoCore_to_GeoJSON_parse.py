import urllib2
from contextlib import closing
import geojson
import dbf
import arcpy

def main():
    pass

def download_url(url, save_path):
    with closing(urllib2.urlopen(url)) as dl_file:
        with open(save_path, 'wb') as out_file:
            out_file.write(dl_file.read())

if __name__ == '__main__':

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
    dbf.Table(r'C:\TEMP\catalogue_scrape.dbf', 'FILENAME C(100); FILEID C(100); URL C(254); PROTOCOL C(100); NAME C(254); NAME_EN C(254); NAME_FR C(254); DESC_ C(254); DESC_EN C(254); DESC_FR C(254); ROWID_ C(10)', codepage=0xf0)
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
        row.setValue("FILEID", FILE_ID)
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

    print str(FEATURE) + " = features for second round calculations"
    print str(ROW_NUMBER) + " = row number to start with for new calculations"
    print str(OPTIONS_COUNT) + " = options counter for calculating starter row value"
    print str(NAME_COUNT) + " = maximum number for row calculations"

    print "When this is complete attributes should be added to another table using the append function"

    print "For the options attributes to be used to populate the attribute table, the statistics are below."
    print "There are " + str(OPTIONS_COUNT) + " options"
    print "There are " + str(URL_COUNT) + " urls, one for each feature under options"
    print "There are " + str(PROTOCOL_COUNT) + " protocols, one for each feature under options"
    print "There are " + str(NAME_COUNT) + " names, one english and one french for each feature under options"
    print "There are " + str(DESCRIPTION_COUNT) + " descriptions, one english and one french for each feature under options"
    print "This means that there are " + str(NAME_COUNT) + " lines to be added to the attribute table"

