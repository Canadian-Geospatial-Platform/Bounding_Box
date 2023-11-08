#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# https://stackoverflow.com/questions/73306198/how-to-delete-a-particular-column-in-csv-file-without-pandas-library
#
#-------------------------------------------------------------------------------
import dbf
import arcpy

def main():
    pass

if __name__ == '__main__':

    csv_path = (r"C:\temp\records.csv")
    print csv_path + " = csv_path"

    import csv

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

