import math

def lookInSphere(radius, anglePhi, angleTheta):
    #Spherical to Cartesian conversion.   
    #Degrees to radians conversion factor 0.0174532
    pointX = radius * math.sin(angleTheta*0.0174532) * math.sin(anglePhi*0.0174532)
    pointY = radius * math.cos(angleTheta*0.0174532)
    pointZ = radius * math.sin(angleTheta*0.0174532) * math.cos(anglePhi*0.0174532)
    #Reduce theta slightly to obtain another point on the same longitude line on the sphere.
    pointXtemp = radius * math.sin(angleTheta*0.0174532-0.01) * math.sin(anglePhi*0.0174532)
    pointYtemp = radius * math.cos(angleTheta*0.0174532-0.01)
    pointZtemp = radius * math.sin(angleTheta*0.0174532-0.01) * math.cos(anglePhi*0.0174532)
    #Connect these two points to obtain the camera's up vector.
    upVectorX = pointXtemp - pointX
    upVectorY = pointYtemp - pointY
    upVectorZ = pointZtemp - pointZ
    return (pointX, pointY, pointZ, upVectorX, upVectorY, upVectorZ)
    