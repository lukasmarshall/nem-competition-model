

##Network Graph Analysis
network-analysis.py contains the work I've done reading trnsmission line maps into graph data structures.
Name formats in the GEOjson file were 'X to Y' ie. "Liddell Power Station to Newcastle"
I was originally stripping the X and Y and using them as node keys.
Unfortunately, the order in which the label was written often did not correspond to the order of the points in the GEOJSON file ie. the first and last point in the multi-line-string representing the transmission line may have been in reverse order to the title. Thus there was no way to tell which coordinates corresponded to which node.

I then tried using the pure lat,long coordinates of the start and end of the transmission line as node keys - but the subtle differences in colocated transmission endpoints mean that no two origins and destinations were ever the same - ie no graphs with more than 2 nodes were ever found.

To fix this, I started by rounding the lats and longs to 3 decimal places, which by google maps appeared to be a reasonable approximate length/width range for colocated nodes. There were however a few glaring exceptions, with a number of features in the Hunter Valley and the Snowy Hyrdoelectric scheme not appearing geolocated and thus being disconnected, when they should have been connected. Some drawbacks of wholesale lat-long rounding is that the range of distance deviation changes geographically, and is more pronounced in longitude than latitude. 

The final strategy was to use an estimate of the distance of a node from any other already-registered node, and assume that the nodes are colocated if the distance was under a threshold. For this I used the Vincenty distance measure from the geopy library. A threshold of 150 meters appears adequate for linking all colocated nodes and seems a reasonable distance for a facility to be considered cohesive. This strategy works well but slows graph creation time significantly as it increases algorithmic complexity to O(n^2). 

Another option would be to use a pre-pass clustering method but this does not seem necessary given that a colocation distance of 150 meters is sufficient to link all cohesive nodes in the transmission network structure. 

##Generators on top of network graph model
I found a list of generators on national map.
File format was GML. I used instructions here https://gis.stackexchange.com/questions/28613/convert-gml-to-geojson to convert to geojson.