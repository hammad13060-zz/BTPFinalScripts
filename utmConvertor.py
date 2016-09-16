import math as Math

class UTM:

    pi = 3.14159265358979
    sm_a = 6378137.0
    sm_b = 6356752.314
    sm_EccSquared = 6.69437999013e-03
    UTMScaleFactor = 0.9996

    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

        #computation
        self.zone = self.GetUTMZone(self.long) #utm zone
        xy = [0, 0]
        self.LatLonToUTMXY(self.DegToRad(self.lat), self.DegToRad(self.long), self.zone, xy)
        self.x = xy[0] #utm easting
        self.y = xy[1] #utm northing

    def DegToRad (self, deg):
        return (deg / 180.0 * UTM.pi)

    def RadToDeg (self, rad):
        return (rad / UTM.pi * 180.0)



    def ArcLengthOfMeridian(self, phi):
        n = (UTM.sm_a - UTM.sm_b) / (UTM.sm_a + UTM.sm_b);
        alpha = ((UTM.sm_a + UTM.sm_b) / 2.0)*(1.0 + (Math.pow(n, 2.0) / 4.0) + (Math.pow(n, 4.0) / 64.0))


        beta = (-3.0 * n / 2.0) + (9.0 * Math.pow(n, 3.0) / 16.0)+ (-3.0 * Math.pow(n, 5.0) / 32.0)

        gamma = (15.0 * Math.pow(n, 2.0) / 16.0)+ (-15.0 * Math.pow(n, 4.0) / 32.0)

        delta = (-35.0 * Math.pow(n, 3.0) / 48.0)+ (105.0 * Math.pow(n, 5.0) / 256.0)

        epsilon = (315.0 * Math.pow(n, 4.0) / 512.0)

        result = alpha *(phi + (beta * Math.sin(2.0 * phi)) + (gamma * Math.sin(4.0 * phi)) + (delta * Math.sin(6.0 * phi)) + (epsilon * Math.sin(8.0 * phi)));

        return result


    def UTMCentralMeridian(self, zone):
        cmeridian = self.DegToRad(-183.0 + (zone * 6.0))
        return cmeridian



    def MapLatLonToXY(self, phi, lambd , lambda0, xy):

        ep2 = (Math.pow(UTM.sm_a, 2.0) - Math.pow(UTM.sm_b, 2.0)) / Math.pow(UTM.sm_b, 2.0)

        nu2 = ep2 * Math.pow(Math.cos(phi), 2.0)

        N = Math.pow(UTM.sm_a, 2.0) / (UTM.sm_b * Math.sqrt(1 + nu2))

        t = Math.tan(phi)
        t2 = t * t
        tmp = (t2 * t2 * t2) - Math.pow(t, 6.0)


        l = lambd - lambda0

        l3coef = 1.0 - t2 + nu2;

        l4coef = 5.0 - t2 + 9 * nu2 + 4.0 * (nu2 * nu2);

        l5coef = 5.0 - 18.0 * t2 + (t2 * t2) + 14.0 * nu2 - 58.0 * t2 * nu2;

        l6coef = 61.0 - 58.0 * t2 + (t2 * t2) + 270.0 * nu2 - 330.0 * t2 * nu2;

        l7coef = 61.0 - 479.0 * t2 + 179.0 * (t2 * t2) - (t2 * t2 * t2);

        l8coef = 1385.0 - 3111.0 * t2 + 543.0 * (t2 * t2) - (t2 * t2 * t2);

        xy[0] = N * Math.cos (phi) * l + (N / 6.0 * Math.pow (Math.cos (phi), 3.0) * l3coef * Math.pow (l, 3.0)) + (N / 120.0 * Math.pow (Math.cos (phi), 5.0) * l5coef * Math.pow (l, 5.0)) + (N / 5040.0 * Math.pow (Math.cos (phi), 7.0) * l7coef * Math.pow (l, 7.0));


        xy[1] = self.ArcLengthOfMeridian (phi) + (t / 2.0 * N * Math.pow (Math.cos (phi), 2.0) * Math.pow (l, 2.0)) + (t / 24.0 * N * Math.pow (Math.cos (phi), 4.0) * l4coef * Math.pow (l, 4.0)) + (t / 720.0 * N * Math.pow (Math.cos (phi), 6.0) * l6coef * Math.pow (l, 6.0)) + (t / 40320.0 * N * Math.pow (Math.cos (phi), 8.0) * l8coef * Math.pow (l, 8.0));


    def GetUTMZone(self, long):
        zone = Math.floor((long + 180.0) / 6) + 1;
        return zone

    def LatLonToUTMXY (self, lat, lon, zone, xy):
        self.MapLatLonToXY (lat, lon, self.UTMCentralMeridian (zone), xy)
        xy[0] = xy[0] * UTM.UTMScaleFactor + 500000.0
        xy[1] = xy[1] * UTM.UTMScaleFactor
        if (xy[1] < 0.0):
            xy[1] = xy[1] + 10000000.0


utm = UTM(28.5440474,  77.2725022)

print str(utm.x) + " " + str(utm.y)

utm = UTM(28.54405798, 77.27259757)

print str(utm.x) + " " + str(utm.y)

utm = UTM(28.54403394, 77.27258923)

print str(utm.x) + " " + str(utm.y)