"""
CARPI GPS REPORTER DAEMON
(C) 2021, Raphael "rGunti" Guntersweilerr
Licensed under MIT
"""

import gpsdaemon.keys as gpskeys

INPUT_DATA = {
    'latitude': gpskeys.KEY_LATITUDE,
    'longitude': gpskeys.KEY_LONGITUDE,
    'altitude': gpskeys.KEY_ALTITUDE,
    'epx': gpskeys.KEY_EPX,
    'epy': gpskeys.KEY_EPY,
    'speed': gpskeys.KEY_SPEED,
    'heading': gpskeys.KEY_TRACK,
    'timestamp': gpskeys.KEY_TIMESTAMP,
    'systimestamp': gpskeys.KEY_SYS_TIMESTAMP
}
