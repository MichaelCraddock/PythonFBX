﻿import FbxCommon
import fbx
import math
import sys
import webbrowser
import glob, os
from xml.etree import ElementTree as et
import Image

# global variables
filenames = []
filenum = 0
edges = []
depth = []
vertices = []
xPoints = []
yPoints = []
zPoints = []
centerX = 0
centerY = 0 
centerZ = 0
minX = 0 
minY = 0 
maxX = 0
maxY = 0
textureArray = fbx.FbxTextureArray()


#converter = fbx.FbxGeometryConverter(sdk_manager)

path = os.getcwd()
newpath=path+"\Fbx Files"
print(newpath)

os.chdir(newpath)
for file in glob.glob("*.fbx"):
    filenames.append(file)

print "number of files ", len(filenames)

filenum = len(filenames)
doc = et.Element('svg', width='480', height='480', version='1.1', xmlns='http://www.w3.org/2000/svg', viewBox = '0,0,0,0', preserveAspectRatio = 'xMidYMid meet', onload='init(evt)')
script = et.SubElement(doc,'script', type='text/ecmascript')
data = '![CDATA[\n'
doc.text=("\n")
#script.text =("\n")
def clamp(x): 
    return max(0, min(x, 255))

#def calculatedepth():
#    facesDepth = len(vertices)
#    for i in range(facesDepth):
#        currentDepth = 0
#        for j in range(len(vertices[i])):
#            currentDepth += zPoints[vertices[i][j]]
#        currentDepth /= len(vertices[i])
#        facesDepth[i] = currentDepth

#    for i in range(len(depth)):
#        smallest = -1
#        for j in range(facesDepth):
#            if facesDepth[j] != -99999 and (smallest ==-1 or facesDepth[smallest] > facesDepth[j]):
#                smallest = j
#        depth[i] = smallest
#        facesDepth[smallest] = -99999

#def rotateX(rads):
#    for i in range(len(xPoints)):
#        y = yPoints[i] - centerY
#        z = zPoints[i] - centerZ
#        d = math.sqrt(y*y + z*z)
#        theta = math.atan2(y,z) + rads
#        yPoints[i] = centerY + d + math.sin(theta)
#        zPoints[i] = centerZ + d + math.sin(theta)

#def rotateY(rads):
#    for i in range(len(xPoints)):
#        x = xPoints[i] - centerX
#        z = zPoints[i] - centerZ
#        d = math.sqrt(x*x + z*z)
#        theta = math.atan2(x,z) + rads
#        xPoints[i] = centerX + d + math.sin(theta)
#        zPoints[i] = centerZ + d + math.sin(theta)

#def rotateZ(rads):
#    for i in range(len(xPoints)):
#        y = yPoints[i] - centerY
#        x = zPoints[i] - centerX
#        d = math.sqrt(x*x + y*y)
#        theta = math.atan2(x,y) + rads
#        yPoints[i] = centerY + d + math.sin(theta)
#        xPoints[i] = centerX + d + math.sin(theta)


for file in range(len(filenames)):
    sdk_manager, scene = FbxCommon.InitializeSdkObjects()
    if not FbxCommon.LoadScene(sdk_manager, scene, filenames[file]):
        print str(filenames[file])
        print("Not found")

    rotation =  180
    rotation = rotation * 3.1415926 / 180

    node = scene.GetRootNode()
    for i in range(node.GetChildCount()):
        child = node.GetChild(i)
        attr_type = child.GetNodeAttribute().GetAttributeType()
        edges = []
        vertices = []
        if attr_type==FbxCommon.FbxNodeAttribute.eMesh:          
            mesh = child.GetNodeAttribute()
            triangulateMesh = mesh
            triangulateMesh.GetNode().GetMesh().RemoveBadPolygons()
            edgecount = triangulateMesh.GetNode().GetMesh().GetMeshEdgeCount()
            polygoncount = triangulateMesh.GetNode().GetMesh().GetPolygonCount()
            contents = "edges = ["
            for edge in range(edgecount):
                start, end = triangulateMesh.GetNode().GetMesh().GetMeshEdgeVertices(edge)
                contents += "[" + str(start) + "," + str(end) + "],"
            contents = contents[:-1] +"]\n"
            contents += "faces = ["
            for polygon in range(polygoncount):
                contents += "["
                for size in range(triangulateMesh.GetNode().GetMesh().GetPolygonSize(polygon)):
                    contents +=str(triangulateMesh.GetNode().GetMesh().GetPolygonVertex(polygon,size))+","
                contents = contents[:-1] +"],"
            contents = contents[:-1] + "]\n"

            contents += "depth =["
            depth = []
            for polygon in range(triangulateMesh.GetNode().GetMesh().GetPolygonCount()):
                contents += "0,"
            contents = contents[:-1] + "]\n"

            xPoints = "x_coords = ["
            yPoints = "y_coords = ["
            zPoints = "z_coords = ["
            smallestControlPointX = 0
            smallestControlPointY = 0
            smallestControlPointZ = 0
            largestControlPointX = 0
            largestControlPointY = 0
            largestControlPointZ = 0
            for point in range(triangulateMesh.GetNode().GetMesh().GetControlPointsCount()):
                if(smallestControlPointX > triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][0]):
                    smallestControlPointX = triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][0]
                    if(smallestControlPointY > triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][1]):
                        smallestControlPointY = triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][1]
                        if(smallestControlPointZ > triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][2]):
                            smallestControlPointZ = triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][2]

            for point in range(triangulateMesh.GetNode().GetMesh().GetControlPointsCount()):
                if(largestControlPointX < triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][0]):
                    largestControlPointX = triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][0]
                    if(largestControlPointY < triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][1]):
                        largestControlPointY = triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][1]
                        if(largestControlPointZ < triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][2]):
                            largestControlPointZ = triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][2]

            for point in range(triangulateMesh.GetNode().GetMesh().GetControlPointsCount()):
                xPoints += str(triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][0] - smallestControlPointX) + ","
                yPoints += str(triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][1] - smallestControlPointY) + ","
                zPoints += str(triangulateMesh.GetNode().GetMesh().GetControlPoints()[point][2] - smallestControlPointZ) + ","
                      
            xPoints = xPoints[:-1] +"];\n"
            yPoints = yPoints[:-1] +"];\n"
            zPoints = zPoints[:-1] +"];\n"
            contents += xPoints + yPoints + zPoints
            data += contents
            
            
            data += "\n\ncentre_x = "+str(-smallestControlPointX)+";\ncentre_y = "+str(-smallestControlPointY)+";\ncentre_z = "+str(-smallestControlPointZ)+";\n\n\n\n\tvar minX = -999;\n\tvar minY = -999;\n\tvar maxX = -999;\n\tvar maxY = -999;\n\n"
            data += "function init(evt)\n{\n\tif ( window.svgDocument == null )\n\t{\n\t\tsvgDocument = evt.target.ownerDocument;\n\t}\n\trotateAboutY("+str((135*3.14/180))+");\n\trotateAboutX("+str(-(135*3.14/180))+");\n\tcalculateDepth()\n\tdrawBox();\n\tsetViewBox();\nif(minX < 0 || minY < 0)\n{\n\tfixCoords();\n\tdrawBox();\n\tsetViewBox();\n}}"

            data += "\n\n\nfunction setViewBox()\n{\n\tminX = -999;\n\tminY = -999;\n\tmaxX = -999;\n\tmaxY = -999;\n\t\n\tfor(var i = 0; i < x_coords.length; i++)\n\t{\n\t\tif(minX == -999 || x_coords[i] < minX)\n\t\t\tminX = x_coords[i];\n\t\tif(minY == -999 || y_coords[i] < minY)\n\t\t\tminY = y_coords[i];\n\t\tif(maxX == -999 || x_coords[i] > maxX)\n\t\t\tmaxX = x_coords[i];\n\t\tif(maxY == -999 || y_coords[i] > maxY)\n\t\t\tmaxY = y_coords[i];\n\t}\n\tshape = document.getElementsByTagName('svg')[0];\n\tshape.setAttribute('viewBox', minX+'" + str(file*50) + " '+ minY+' '+ maxX+'" + str(file*50) + " '+maxY);\n}"
            data += "\n\n\nfunction fixCoords()\n{\n\tif(minX < 0)\n\t{\n\t\tcentre_x += -minX;\n\t\tfor(var i = 0; i < x_coords.length;i++)\n\t\t{\n\t\t\tx_coords[i] += -minX;\n\t\t}\n\t}\n\tif(minY < 0)\n\t{\n\t\tcentre_y += -minY;\n\t\tfor(var i = 0; i < y_coords.length;i++)\n\t\t{\n\t\t\ty_coords[i] += -minY;\n\t\t}\n\t}\n}"            
            data += "\n\n\nfunction calculateDepth()\n{\n\tvar facesDepth = Array(faces.length);\n\tfor(var i = 0; i < faces.length; i++)\n\t{\n\t\tvar currentDepth = 0;\n\t\tfor(var u = 0; u < faces[i].length; u ++)\n\t\t{\n\t\t\tcurrentDepth += z_coords[faces[i][u]];\n\t\t}\n\t\tcurrentDepth /= faces[i].length;\n\t\tfacesDepth[i] = currentDepth;\n\t}\n\tfor(var i = 0; i < depth.length; i++)\n\t{\n\t\tvar smallest = -1;\n\t\tfor(var u = 0; u < facesDepth.length; u++)\n\t\t{\n\t\t\tif(facesDepth[u] != -99999 && (smallest == -1 || facesDepth[smallest] > facesDepth[u]))\n\t\t\t\tsmallest = u;\n\t\t}\n\t\tdepth[i] = smallest;\n\t\tfacesDepth[smallest] = -99999;\n\t}\n}"
            data += "\n\n\nfunction drawBox()\n{\n\tfor(var i=0; i<depth.length; i++)\n\t{\n\t\tface = svgDocument.getElementById('face-'+i);\n\t\tvar d = 'm'+x_coords[faces[depth[i]][0]]+' '+y_coords[faces[depth[i]][0]];\n\t\tfor(var u = 1; u < faces[depth[i]].length; u++)\n\t\t{\n\t\t\td+= ' ' + 'L'+x_coords[faces[depth[i]][u]]+' '+y_coords[faces[depth[i]][u]];\n\t\t}\n\t\td+= ' Z';\n\t\tface.setAttributeNS(null, 'd', d);\n\t}\n}"
            

            data += "\n\n\nfunction rotateAboutX(radians)\n{\n\tfor(var i=0; i<x_coords.length; i++)\n\t{\n\t\ty = y_coords[i] - centre_y;\n\t\tz = z_coords[i] - centre_z;\n\t\td = Math.sqrt(y*y + z*z);\n\t\ttheta  = Math.atan2(y, z) + radians;\n\t\ty_coords[i] = centre_y + d * Math.sin(theta);\n\t\tz_coords[i] = centre_z + d * Math.cos(theta);\n\t}\n}"
            data += "\n\n\nfunction rotateAboutY(radians)\n{\n\tfor(var i=0; i<x_coords.length; i++)\n\t{\n\t\tx = x_coords[i] - centre_x;\n\t\tz = z_coords[i] - centre_z;\n\t\td = Math.sqrt(x*x + z*z);\n\t\ttheta  = Math.atan2(x, z) + radians;\n\t\tx_coords[i] = centre_x + d * Math.sin(theta);\n\t\tz_coords[i] = centre_z + d * Math.cos(theta);\n\t}\n}"
            data += "\n\n\nfunction rotateAboutZ(radians)\n{\n\tfor(var i=0; i<x_coords.length; i++)\n\t{\n\t\tx = x_coords[i] - centre_x;\n\t\ty = y_coords[i] - centre_y;\n\t\td = Math.sqrt(x*x + y*y);\n\t\ttheta  = Math.atan2(x, y) + radians;\n\t\tx_coords[i] = centre_x + d * Math.sin(theta);\n\t\ty_coords[i] = centre_y + d * Math.cos(theta);\n\t}\n}"

            data += "\n]]"
            cdata = et.SubElement(script, data)
            for polygon in range (triangulateMesh.GetNode().GetMesh().GetPolygonCount()):
                poly = FbxCommon.FbxPropertyDouble3(triangulateMesh.GetNode().GetMesh().FindProperty("Color")).Get()
                r = clamp(poly[0] * 255 - poly[0] * 0.4 * ((polygon+0.0) / child.GetMesh().GetPolygonCount()) * 255)
                g = clamp(poly[1] * 255 - poly[1] * 0.4 * ((polygon+0.0) / child.GetMesh().GetPolygonCount()) * 255)
                b = clamp(poly[2] * 255 - poly[2] * 0.4 * ((polygon+0.0) / child.GetMesh().GetPolygonCount()) * 255)
                svgPath = et.SubElement(doc, 'path', stroke = str('#%02x%02x%02x' % (r,g,b)), fill = str('#%02x%02x%02x' % (r,g,b)), id = "face-"+str(polygon), d = '')
                svgPath.text = "\n"

            scene.FillTextureArray(textureArray)
            for i in range(0, textureArray.GetCount()):
                texture = textureArray.GetAt(i)
                if texture.ClassId == fbx.FbxFileTexture.ClassId:
                    textureFilename = texture.GetFileName()
                    image = Image.open(textureFilename)
                    width, height = image.size
                    print("%sx%s = %s" % (width, height, textureFilename))

            os.chdir(path)
            f = open(str(filenames[file]) + '.svg', 'w')
            f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
            f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
            f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')
            f.write(et.tostring(doc))
            f.close()

            r = open(str(filenames[file]) + '.svg', 'r')
            filedata = r.read()
            r.close()

            newdata = filedata.replace("] />", "]>")

            f = open(str(filenames[file]) + '.svg', 'w')
            f.write(newdata)
            f.close()
    scene.UnloadContent()




f = open('index.html', 'w')
message = """<html>

<head><title> FBX Viewer </title></head>
<body><p>This is my FBX viewer!</p>"""
for file in range(filenum):
    message += """<object data="""
    message += str(filenames[file])
    message +=""".svg type="image/svg+xml"></object>"""
message +="""</body>

</html>"""

f.write(message)
f.close()