# Bounding_Box
Getting scripts together to be able to translate bounding boxes from online GeoCore metadata into geoJSON files.
In this script the GeoJSON available online through the catalogue (GeoCore format) translates into a Look-
Up-Table to be used to guide the next scripts through translating the new table into GeoJSON with new spatial coordinates
representing the bounding boxes of the layers with better representation than 4 points.

# GeoJSON list of files in s3 bucket
1) Use your AWS credentials to log in to AWS.
2) Paginate by 1000 through chosen directory (s3 bucket) and extract filenames as a list
3) create a pythin list/dictionary to load filenames

# GeoCore Options to Look-Up-Table
1) GeoJSON / Geocore: Download first (or next) URL found in metadata (GeoCore).
2) DBF - LUT: Create a Look-Up-Table (LUT) with Options attributes as columns.
3) Transfer Attributes: Moving attributes from GeoCore metadata to LUT.
4) Complete - Transfer of metadata element complete, if yes and with no errors, repeat 1-3
5) Log Errors - Transfer not complete, aborted due to errors.  Log errors, then repeat 1-3 

# Export to CSV
1) open a S3 file returning the body of the file
2) List the amount of files/rows
3) Transform the Pandas Data Frame into a CSV file

# Parquet to Pandas Data Frame
1) Open a S3 parquet file from bucket and filename and return the aprquet as pandas dataframe
2) Output csv with changes, to be further cleaned

# CSV cleaner
1) clean all extraneous fields
2) leave in csv format
   
# Table Clean Rows and Output
1) Clean all rows that will not be used in this process and are extraneous
2) Output as excel file or DBF, DBF prefered for interoperability
3) Clean table to by exported to DynamoDB for next steps

# List all Shapefiles in directory and all subdirectories within
1) Set current working directory
2) Create a list for file names to be appended to
3) use os.walk to step through directories using topdown approach.
4) while stepping through directories get files to list all files that end with .shp (shapefiles)
5) append to list all shapefiles including path (so path + // + shp name)
6) Print the list
