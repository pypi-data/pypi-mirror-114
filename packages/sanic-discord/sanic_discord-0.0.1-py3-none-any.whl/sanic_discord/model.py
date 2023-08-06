


class user(object):
  def __init__(api):
    self.api=api
    
  @property
  def id(self):
    return self.api["id"]
  
  @property
  def name(self):
    return self.api["username"]
  
  @property
  def avatar(self):
    return self.api["avatar"]