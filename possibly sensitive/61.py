def __init__(self,
               date_of_birth=False,
               home_city=False,
               min_date_of_birth=None):
    self.date_of_birth = date_of_birth
    self.home_city = home_city
    self.min_date_of_birth = min_date_of_birth

  def GetDateOfBirth(self):
    return self.date_of_birth

  def GetHomeCity(self):
    return self.home_city


@json_util.JSONDecorator({
    'google_place_id': json_util.JSONString(),
    'city': json_util.JSONString(),
    'state': json_util.JSONString(),
    'country': json_util.JSONString()})
class Place(data_util.AbstractObject):

  def __init__(self,
               google_place_id=None,
               city=None,
               state=None,
               country=None):
    self.google_place_id = google_place_id
    self.city = city
    self.state = state
    self.country = country

  def Update(self, value):
    place = Place.FromJSON(value)
    self.__dict__ = place.__dict__
  def Get(self):
    return self.ToJSON()

  def GetGooglePlaceId(self):
    return self.google_place_id

  def GetCity(self):
    return self.city

  def GetState(self):
    return self.state

  def GetCountry(self):
    return self.country