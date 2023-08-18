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
