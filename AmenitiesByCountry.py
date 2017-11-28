#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jolynn
#
# Created:     12/11/2016
# Copyright:   (c) jolynn 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    import arcpy
    arcpy.env.overwriteOutput = True

#define major variables
    amenities = ['school', 'hospital', 'place_of_worship']
    country = 'El Salvador'
    sourceName = "Open Street Map"

#Set Workspace and define working files
    arcpy.env.workspace = "C:\\GIS\\Python\\L3"
    allCountries = "CentralAmerica.shp"
    allAmenities = "OSMpoints.shp"

# Loop over all amenities making shape file for each
    for item in amenities:
        # create query for target country
        countryQuery = '"NAME" = ' + "'" + country + "'"

        # Make feature layer of target country and all amenities
        try:
            arcpy.MakeFeatureLayer_management(allCountries, "countryLayer", countryQuery)
            arcpy.MakeFeatureLayer_management(allAmenities, "amenitiesLayer")
        except:
            arcpy.AddError("Unable to create feature layer")
            arcpy.AddMessage(arcpy.GetMessages())

        #use spatial and attribute query to make a feature layer of the target Amenity in target country
        try:
            #get all amenities in target country
            arcpy.SelectLayerByLocation_management("amenitiesLayer", "CONTAINED_BY", "countryLayer")
            #limit to just target amenities
            amenityQuery = '"amenity" = ' + "'" + item + "'"
            arcpy.SelectLayerByAttribute_management("amenitiesLayer", "SUBSET_SELECTION", amenityQuery)
        except:
            arcpy.AddError("Unable to create target feature layers")
            arcpy.AddMessage(arcpy.GetMessages())

        #create shape file and add SOURCE field
        try:
            shpName = item + ".shp"
            arcpy.CopyFeatures_management("amenitiesLayer", shpName)
            arcpy.AddField_management(shpName, "SOURCE", "TEXT", field_length=25)
            #populate the source field
            with arcpy.da.UpdateCursor(shpName, ("SOURCE")) as cursor:
                for row in cursor:
                    row[0] = sourceName
                    cursor.updateRow(row)
        except:
            arcpy.AddError("Unable to create shape file %s" % shpName)
            arcpy.AddMessage(arcpy.GetMessages())

        #remove feature layers
        arcpy.Delete_management("amenitiesLayer")
        arcpy.Delete_management("countryLayer")

if __name__ == '__main__':
    main()
