class Antenna:
    def __init__(self, latitude=0.0, longitude=0.0, altitude=0.0):
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude
        

    # Getter for Latitude
    @property
    def latitude(self):
        return self._latitude

    # Setter for Latitude
    @latitude.setter
    def latitude(self, value):
        self._latitude = value

    # Getter for Longitude
    @property
    def longitude(self):
        return self._longitude

    # Setter for Longitude
    @longitude.setter
    def longitude(self, value):
        self._longitude = value
        
    # Getter for Altitude
    @property
    def altitude(self):
        return self._altitude

    # Setter for Altitude
    @altitude.setter
    def altitude(self, value):
        self._altitude = value
