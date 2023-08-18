# Purpose: This script reads from an S3 bucket and creates a disctionary filled with
# the filenames.  These names will get used with the lookup table to iterate through 
# all of the metadata records and one by one convert them to geo.json files
# with more detail than the original 4 corners.
# Authors: Bo Lu and Sean Eagles
# Copyright: 2023

import json
import boto3

GEOJSON_BUCKET_NAME='webpresence-geocore-json-to-geojson-dev'

def lambda_handler(event, context):

    GEOJSON_BUCKET_NAME='webpresence-geocore-json-to-geojson-dev'
    
    s3_paginate_options = {'Bucket':GEOJSON_BUCKET_NAME}

    filenames = s3_filenames_paginated('ca-central-1', **s3_paginate_options)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": filenames,
            }
        ),
    }

def s3_filenames_paginated(region, **kwargs):
    """Paginates a S3 bucket to obtain file names. Pagination is needed as S3 returns 999 objects per request (hard limitation)
    :param region: region of the s3 bucket
    :param kwargs: Must have the bucket name. For other options see the list_objects_v2 paginator:
    :              https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2
    :return: a list of filenames within the bucket
    """
    client = boto3.client('s3', region_name=region)

    paginator = client.get_paginator('list_objects_v2')
    result = paginator.paginate(**kwargs)

    filename_list = []
    count = 0

    for page in result:
        if "Contents" in page:
            for key in page[ "Contents" ]:
                keyString = key[ "Key" ]
                count += 1
                filename_list.append(keyString)

    print("Bucket contains:", count, "files")

    return filename_list

if __name__ == '__main__':
    #main()

    region = 'ca-central-1'
    kwargs = {'Bucket':'webpresence-geocore-json-to-geojson-dev'}

    s3_bucket_filenames = s3_filenames_paginated(region, **kwargs)
    print(s3_bucket_filenames)