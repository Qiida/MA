import numpy as np

from src.data.__tuple import ellipsoid


def deg2utm(WGS84_LONG, WGS84_LAT):
    ELL = np.transpose(np.array([WGS84_LONG, WGS84_LAT]))

    ID = np.zeros(shape=(len(WGS84_LONG), 2), dtype=np.uint8)
    L0 = np.zeros(len(WGS84_LONG), dtype=np.uint8)

    for i, [longitude, latitude] in enumerate(ELL):

        if latitude >= 84:
            # North Pole
            if longitude < 0 and latitude < 90:
                ID[i] = [0, 25]
                L0[i] = 0
            else:
                ID[i] = [0, 26]
                L0[i] = 0

        elif latitude < -80:
            # South Pole
            if longitude < 0 and latitude > -90:
                ID[i] = [0, 1]
                L0[i] = 0
            else:
                ID[i] = [0, 1]
                L0[i] = 0

        elif latitude >= 56 and latitude <= 64 & longitude >= 0 and longitude < 3:
            # V31
            ID[i] = [31, 22]
            L0[i] = 3

        elif latitude >= 56 and latitude <= 64 & longitude >= 3 and longitude < 12:
            # V32
            ID[i] = [32, 22]
            L0[i] = 9

        elif latitude >= 72 and latitude <= 84 & longitude >= 0 and longitude < 9:
            # X31
            ID[i] = [31, 24]
            L0[i] = 3

        elif latitude >= 72 and latitude <= 84 & longitude >= 9 and longitude < 21:
            # X33
            ID[i] = [33, 24]
            L0[i] = 15

        elif latitude >= 72 and latitude <= 84 & longitude >= 21 and longitude < 33:
            # X35
            ID[i] = [35, 24]
            L0[i] = 27

        elif latitude >= 72 and latitude <= 84 & longitude >= 33 and longitude < 42:
            # X37
            ID[i] = [37, 24]
            L0[i] = 39

        else:
            ID[i][0] = np.floor(longitude / 6) + 31
            if np.all(ELL[:, 1] >= 72):
                ID[i, 1] = 24
            else:
                ID[i][1] = np.floor(latitude / 8) + 13
                if ID[i][1] >= 9:
                    ID[i][1] = ID[i][1] + 1
                if ID[i][1] >= 15:
                    ID[i][1] = ID[i][1] + 1

            L0[i] = ID[i][0] * 6 - 183

    PROs = np.zeros(ELL.shape)
    rho = 180 / np.pi

    e2 = (ellipsoid.a ** 2 - ellipsoid.b ** 2) / ellipsoid.a ** 2
    es2 = (ellipsoid.a ** 2 - ellipsoid.b ** 2) / ellipsoid.b ** 2

    if np.any(ID[:, 0] > 0):
        # handle all points except the pole regions
        B = ELL[ID[:, 0] > 0, 1] / rho
        L = (ELL[ID[:, 0] > 0, 0] - L0[ID[:, 0] > 0]) / rho
        m0 = 0.9996

        V = np.sqrt(1 + es2 * np.cos(B) ** 2)
        eta = np.sqrt(es2 * np.cos(B) ** 2)

        Bf = np.arctan(np.tan(B) / np.cos(V * L) * (1 + eta ** 2 / 6. * (1 - 3 * np.sin(B) ** 2) * L ** 4))
        Vf = np.sqrt(1 + es2 * np.cos(Bf) ** 2)
        etaf = np.sqrt(es2 * np.cos(Bf) ** 2)
        n = (ellipsoid.a - ellipsoid.b) / (ellipsoid.a + ellipsoid.b)

        r1 = (1 + n ** 2 / 4 + n ** 4 / 64) * Bf
        r2 = 3 / 2 * n * (1 - n ** 2 / 8) * np.sin(2 * Bf)
        r3 = 15 / 16 * n ** 2 * (1 - n ** 2 / 4) * np.sin(4 * Bf)
        r4 = 35 / 48 * n ** 3 * np.sin(6 * Bf)
        r5 = 315 / 512 * n ** 4 * np.sin(8 * Bf)

        PROs[ID[:, 0] > 0, 1] = ellipsoid.a / (1 + n) * (r1 - r2 + r3 - r4 + r5) * m0
        PROs[B < 0, 1] = PROs[B < 0, 1] + 10e6

        ys = np.arcsinh(np.tan(L) * np.cos(Bf) / Vf * (1 + etaf ** 2 * L ** 2. * np.cos(Bf) ** 2. *
                                                       (etaf ** 2 / 6 + L ** 2 / 10)))

        y = m0 * ellipsoid.a ** 2 / ellipsoid.b * ys
        PROs[ID[:, 0] > 0, 0] = y + 5e5

    if np.any(ID[:, 0] == 0):
        # deal the poles - ups mapping
        m0 = 0.994
        woN = np.logical_and(ID[:, 0] == 0, ID[:, 1] > 24)
        woS = np.logical_and(ID[:, 1] == 0, ID[:, 2] < 3)

        B = ELL[woN, 1] / rho
        L = ELL[woN, 0] / rho

        C0 = 2 * ellipsoid.a / np.sqrt(1 - e2) * ((1 - np.sqrt(e2)) / (1 + np.sqrt(e2))) ** (np.sqrt(e2) / 2)
        tanz2 = ((1 + np.sqrt(e2) * np.sin(B)) / (1 - np.sqrt(e2) * np.sin(B))) ** (np.sqrt(e2) / 2) * np.tan(
            np.pi / 4 - B / 2)
        R = m0 * C0 * tanz2
        PROs[woN, 1] = 2e6 + R * np.sin(L)
        PROs[woN, 2] = 2e6 - R * np.cos(L)

        B = -ELL[woS, 1] / rho
        L = ELL[woS, 0] / rho

        C0 = 2 * ellipsoid.a / np.sqrt(1 - e2) * ((1 - np.sqrt(e2)) / (1 + np.sqrt(e2))) ** (np.sqrt(e2) / 2)
        tanz2 = ((1 + np.sqrt(e2) * np.sin(B)) / (1 - np.sqrt(e2) * np.sin(B))) ** (np.sqrt(e2) / 2) * np.tan(
            np.pi / 4 - B / 2)
        R = m0 * C0 * tanz2

        PROs[woS, 1] = 2e6 + R * np.sin(L)
        PROs[woS, 2] = 2e6 + R * np.cos(L)

    UTM_LONG = PROs[:, 0]
    UTM_LAT = PROs[:, 1]
    UTM_ZONE_No = ID[0, 0]
    UTM_ZONE_Char = ID[0, 1] + 64

    return UTM_LONG, UTM_LAT, UTM_ZONE_No, UTM_ZONE_Char
