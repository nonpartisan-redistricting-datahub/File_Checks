# File_Checks

Code used to validate and check files before posting on the website

- ERJ_Checks
    - UNIQUE_ID and COUNTYFP columns exist, in the right position, and UNIQUE_ID unique
    - Stated district assignments match actual district assignments
    - Checks for any “None” values in the columns
    - Checks that all the different file types are included for .shp files
- Census_File_Checks
    - Has counts of different census geographies for all states / levels, can compare the length of a dataset against those, or copy and paste the dictionary to use elsewhere
- Standard_Checks
    - Code to be run on either a .csv or .shp, generates a .txt file with results
    - Prints out data related to:
        - None values in columns
        - File shape
        - Invalid geometries
        - Column names
        - Column name lengths
        - Summary of the file (using .describe() )
        - Max value for every column
        - Min value for every column
        - Numeric column sums
        - Whether columns contain duplicate values
