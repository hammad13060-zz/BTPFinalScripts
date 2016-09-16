import numpy
import TransformOBJ as OBJ
import utmConvertor as utm
from sys import argv

readingsFile = argv[1]
""" if matrix mode = f:
        matrix is forced to be [[a, b], [-b, a]]
else if matrix mode = nf:
    matrix is forced to be [[a, b], [c, d]] """
matrixMode = argv[2]

"""reading file"""
readingsFileObject = open("./resources/" + readingsFile)
readingLines = readingsFileObject.readlines()

coordinates = []

#generating a list of coordinates
for line in readingLines:
    value = line.split()
    if not value:
        continue
    coordinate = [float(component) for component in value]
    utmCoordinates = utm.UTM(coordinate[2], coordinate[3])
    coordinate[2] = utmCoordinates.x
    coordinate[3] = utmCoordinates.y
    coordinates.append(coordinate)

print coordinates

txlocal = coordinates[0][0]
tylocal = coordinates[0][1]

txworld = coordinates[0][2]
tyworld = coordinates[0][3]

#shifting everything to origin
coordinates = [
    [coordinate[0] - txlocal, coordinate[1] - tylocal, coordinate[2] - txworld, coordinate[3] - tyworld]
    for coordinate in coordinates
    ]

print coordinates


#forming linear equations
left = [] #left side of the equation
right = [] #right side of the equation



for coordinate in coordinates:
    if matrixMode == "f":
        left.append(
            [
                coordinate[0],
                coordinate[1]
            ]
        )

        left.append(
            [
                coordinate[1],
                -coordinate[0]
            ]
        )

        right.append(coordinate[2])
        right.append(coordinate[3])

    elif matrixMode == "nf":
        left.append(
            [
                coordinate[0],
                coordinate[1],
                0.0,
                0.0
            ]
        )

        left.append(
            [
                0.0,
                0.0,
                coordinate[0],
                coordinate[1]
            ]
        )

        right.append(coordinate[2])
        right.append(coordinate[3])

leastSquareSoln = numpy.linalg.lstsq(left, right)[0]

#forming matrix
if matrixMode == "f":
    U,s,V = numpy.linalg.svd([
            [leastSquareSoln[0], leastSquareSoln[1]],
            [-leastSquareSoln[1], leastSquareSoln[0]]
        ]
    )
    mat1 = [
        [leastSquareSoln[0], leastSquareSoln[1], 0.0, 0.0],
        [-leastSquareSoln[1], leastSquareSoln[0], 0.0, 0.0],
        [0.0, 0.0, s.tolist()[0], 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ]

    print "scaling: " + str(s.tolist())

elif matrixMode == "nf":
    U,s,V = numpy.linalg.svd([
            [leastSquareSoln[0], leastSquareSoln[1]],
            [leastSquareSoln[2], leastSquareSoln[3]]
        ]
    )

    mat1 = [
        [leastSquareSoln[0], leastSquareSoln[1], 0.0, 0.0],
        [leastSquareSoln[2], leastSquareSoln[3], 0.0, 0.0],
        [0.0, 0.0, s.tolist()[0], 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ]

    print "scaling: " + str(s.tolist())

print "mat1: " + str(mat1)

mat2 = [
    [1, 0, 0, txworld],
    [0, 1, 0, tyworld],
    [0, 0, 1, -85.0],
    [0, 0, 0, 1]
]

iiitdUTMOffsetX = 722250.000
iiitdUTMOffsetY = 3159632.000

mat3 = [
    [1, 0, 0, -iiitdUTMOffsetX],
    [0, 1, 0, -iiitdUTMOffsetY],
    [0, 0, 1.0, 0.0],
    [0, 0, 0, 1]
]

matrix = numpy.dot(mat3, numpy.dot(mat2, mat1))

OBJ.TransformOBJ(matrix, "./models/1-library-obj.obj", "./transformedModels/new-1-library-obj.obj")
