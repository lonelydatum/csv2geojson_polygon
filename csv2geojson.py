import csv

# Read in raw data from csv
rawData = csv.reader(open('list.csv', 'rb'), dialect='excel')

# the template. where data from the csv will be formatted to geojson
# you will most likely have to modify the properities to match your csv file
template = \
    ''' \
    { "type":"Feature", "properties":{"city": "%s", "income": "%s"}, "geometry": {"type":"Polygon", "coordinates": %s } }%s
    '''

# the head of the geojson file
output = '''var statesData = {"type" : "FeatureCollection", "features" : [ 
'''


polygonTemplate = '[[%s]]'


polygon = ''

indexNow = 0
list = list(rawData)






def isPolygonBegin( indexNow ):
    boo = False
    indexBefore = indexNow - 1
    idBefore = ''
    idNow = list[indexNow][0]

    #set the BEFORE id if its not the first row
    if indexNow >= 1 :
        idBefore = list[indexBefore][0]
        if idBefore != idNow :
            boo = True
    elif indexNow == 0:
        boo = True
    return boo
    

def isPolygonEnd(indexNow):
    boo = False
    indexNext = indexNow + 1
    idNext = ''
    idNow = list[indexNow][0]

    #set the AFTER id if its not the last row
    if indexNext <= len(list)-2 :
        idNext = list[indexNext][0]
        if idNext != idNow:
            boo = True
    elif indexNow == len(list)-1:
        boo = True

    return boo



def polygonCreate(indexNow):
    indexBefore = indexNow-1
    indexNext = indexNow+1
    
    idBefore = ''
    idNext = ''
    idNow = list[indexNow][0]
    row = list[indexNow]
    return '[' + row[1] + ', ' + row[2] + ']'    


for row in list:
    
    #this is the first row of the polygon
    if isPolygonBegin(indexNow):        
        polygon = ''

        

    polygon += polygonCreate(indexNow)    
    
    #this is the last row of the polygon
    if isPolygonEnd(indexNow):
        polygonList = polygonTemplate % (polygon)
        comma = ''
        if indexNow<len(list)-1: 
            comma = ','
        output += template % (list[indexNow][0], list[indexNow][1], polygonList, comma)
    else:
        polygon += ','
    
    indexNow += 1
    
        
        
# the tail of the geojson file
output += \
    ''' \
    ]
}
    '''

# opens an geoJSON file to write the output to
outFileHandle = open("list.geojson", "w")
outFileHandle.write(output)
outFileHandle.close()
