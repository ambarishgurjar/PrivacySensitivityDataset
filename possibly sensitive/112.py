
available = True
try:
    import gps
    import serialGPS
    from gmapcatcher.gps import misc
except:
    available = False
import mapConst
import widgets.mapPixbuf as mapPixbuf
from threading import Event, Thread
import time
from datetime import datetime, timedelta


if time.localtime().tm_isdst:
    offset = timedelta(seconds=time.altzone)
else:
    offset = timedelta(seconds=time.timezone)


class GPS:
    def __init__(self, gps_callback, conf):
        global available

        self.conf = conf
        self.mode = conf.gps_mode
        self.type = conf.gps_type
        self.location = None
        self.gps_callback = gps_callback
        self.pixbuf = self.get_marker_pixbuf()
        self.update_rate = float(conf.gps_update_rate)
        self.serial_port = conf.gps_serial_port
        self.baudrate = conf.gps_serial_baudrate
        self.gps_updater = None
        self.gpsfix = None
        if self.mode != mapConst.GPS_DISABLED:
            self.startGPS()

    def startGPS(self):
        global available
        available = True
        if self.type == mapConst.TYPE_GPSD:
            try:

                self.gps_session = gps.gps()
                self.gps_session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
                self.gps_updater = GPSUpdater(self.type, self.update_rate, self.update, gps_session=self.gps_session)
                if self.mode != mapConst.GPS_DISABLED:
                    self.gps_updater.start()
            except:

                available = False
        elif self.type == mapConst.TYPE_SERIAL:
            print 'serial started'
            try:
                self.gps_updater = GPSUpdater(self.type, self.update_rate, self.update, serial_port=self.serial_port, baudrate=self.baudrate)
                if self.mode != mapConst.GPS_DISABLED:
                    self.gps_updater.start()
            except:
                available = False
        else:
            available = False

    def stop_all(self):
        try:
            self.gps_updater.cancel()
        except:
            pass


    def set_mode(self, mode):