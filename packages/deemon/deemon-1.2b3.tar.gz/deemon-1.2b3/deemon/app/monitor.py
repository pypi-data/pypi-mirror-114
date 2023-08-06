from sqlite3 import OperationalError
from deemon.app import Deemon, refresh
import logging
import deezer

logger = logging.getLogger(__name__)


class Monitor(Deemon):

    def __init__(self, skip_refresh=False):
        super().__init__()
        self.artist = None
        self.artist_id = None
        self.playlist_id = None
        self.dz = deezer.Deezer()
        self.skip_refresh = skip_refresh

    def get_artist_info(self):
        if self.artist_id:
            try:
                artist = self.dz.api.get_artist(self.artist_id)
                self.artist = artist["name"]
                return True
            except deezer.api.DataException:
                logger.error(f"Artist ID '{self.artist_id}' not found.")

        if self.artist:
            try:
                artist = self.dz.api.search_artist(self.artist, limit=1)["data"][0]
                self.artist = artist["name"]
                self.artist_id = artist["id"]
                return True
            except IndexError:
                logger.error(f"Artist '{self.artist}' not found")

    def start_monitoring(self):
        artist_info = self.get_artist_info()
        values = {'artist_name': self.artist}
        sql = "SELECT * FROM monitor WHERE artist_name = ':artist_name'"
        already_monitored = self.db.query(sql, values).fetchone()
        if already_monitored:
            logger.debug(f"Artist: {self.artist} is already monitored, skipping...")
            return
        if artist_info:
            sql = ("INSERT OR REPLACE INTO monitor (artist_id, artist_name, bitrate, record_type, alerts) "
                   "VALUES (:artist_id, :artist_name, :bitrate, :record_type, :alerts)")
            values = {
                'artist_id': self.artist_id,
                'artist_name': self.artist,
                'bitrate': self.config["bitrate"],
                'record_type': self.config["record_type"],
                'alerts': self.config["alerts"]
            }

            try:
                self.db.query(sql, values)
            except OperationalError as e:
                logger.error(e)

            logger.info(f"Now monitoring {self.artist}")

            self.db.commit()
            return self.artist_id
        else:
            return

    def stop_monitoring(self):
        self.get_artist_info()
        if self.artist_id:
            values = {'artist_id': self.artist_id}
            sql_releases = "DELETE FROM 'releases' WHERE artist_id = :artist_id"
            sql_monitor = "DELETE FROM 'monitor' WHERE artist_id = :artist_id"
        else:
            values = {'artist': self.artist}
            sql_releases = "DELETE FROM 'releases' WHERE artist_name = ':artist' COLLATE NOCASE"
            sql_monitor = "DELETE FROM 'monitor' WHERE artist_name = ':artist' COLLATE NOCASE"

        result = self.db.query(sql_monitor, values)
        if result.rowcount > 0:
            logger.info("No longer monitoring " + self.artist)
            logger.info("Cleaning up release table...")
            self.db.query(sql_releases, values)
        else:
            logger.error(f"Artist '{self.artist}' not found")

        self.db.commit()

    def start_monitoring_playlist(self):
        found_new_tracks = False
        try:
            playlist = self.dz.api.get_playlist(self.playlist_id)
            self.db.monitor_playlist(playlist)
        except deezer.api.DataException:
            logger.error("Playlist ID not found")
            return
