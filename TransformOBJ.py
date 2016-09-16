import numpy as np
from sys import argv

class TransformOBJ:
    def __init__(self, transformationMatrix, objectFile, resultFileName):

        normalTransformationMatrix = np.linalg.inv(transformationMatrix).transpose()

        inputFileObject = open(objectFile, "r")
        objLines = inputFileObject.readlines()

        newFileStr = ""

        #print objLines

        for line in objLines:
            values = line.split()

            if not values:
                newFileStr += "\n"
                continue

            #print line

            if values[0] == "v":
                vertex = [
                    [float(values[1])],
                    [float(values[3])],
                    [float(values[2])],
                    [1.0]
                ]

                transformedVertex = np.dot(transformationMatrix, vertex)

                vertexLine = "v " + str(transformedVertex[0][0]) + \
                             " " + str(transformedVertex[1][0]) + \
                             " " + str(transformedVertex[2][0]) + "\n"


                """vertexLine = "v " + str(transformedVertex[0][0]) + \
                             " " + str(0.0) + \
                             " " + str(transformedVertex[1][0]) + "\n"
                             """
                #print vertexLine
                newFileStr += vertexLine

            elif values[0] == "vn":
                vertex = [
                    [float(values[1])],
                    [float(values[3])],
                    [float(values[2])],
                    [1.0]
                ]

                transformedVertex = np.dot(normalTransformationMatrix, vertex)

                vertexLine = "vn " + str(transformedVertex[0][0]) + \
                             " " + str(transformedVertex[1][0]) + \
                             " " + str(transformedVertex[2][0]) + "\n"

                """vertexLine = "vn " + str(transformedVertex[0][0]) + \
                             " " + str(0.0) + \
                             " " + str(transformedVertex[1][0]) + "\n"
                             """
                newFileStr += vertexLine
            else:
                newFileStr += line

        outputFileObject = open(resultFileName, "w")

        outputFileObject.writelines(newFileStr)

        inputFileObject.close()
        outputFileObject.close()

iiitdUTMOffsetX = 722250.000
iiitdUTMOffsetY = 3159632.000

mat3 = [
    [1, 0, 0, iiitdUTMOffsetX],
    [0, 1, 0, iiitdUTMOffsetY],
    [0, 0, 1.0, 0.0],
    [0, 0, 0, 1]
]

#TransformOBJ(mat3, "./models/iiitd_2_simplified_3d_mesh.obj", "./transformedModels/new-iiitd_2_simplified_3d_mesh.obj")
