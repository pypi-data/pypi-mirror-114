import aiohttp
from functools import wraps
from sanic.response import *
from .model import user

baseurl="https://discord.com/api/v8/"

class discordloginerror(Exception):
  def login_error(self):
    pass

class discord_oauth:
  def __init__(self, client_id, client_secret, redirect_uri):
    self.client_id=client_id
    self.client_secret=client_secret
    self.redirect_uri=redirect_uri
    
  def authorized():
    def decorator(f):
      @wraps(f)
      async def discord_oauth(request, *args, **kwargs):
        token=request.cookies["token"]
        headers={
          "Authorization": "Bearer {}".format(token)
        }
        async with aiohttp.ClientSession() as session:
          async with session.get(baseurl+"users/@me", headers=headers) as response:
            api=await response.json()
            if api["id"]:
              return True
            else:
              return False
            
  def login():
    def decorators(f):
      @wraps(f)
      async def discord_login(request, *args, **kwargs):
        code=request.args["code"][0]
        data = {
          'client_id': self.client_id,
          'client_secret': self.client_secret,
          'grant_type': 'authorization_code',
          'code': code,
          'redirect_uri': self.redirect_uri
        }
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
        async with aiohttp.ClientSession() as session:
          async with session.post(baseurl+"oauth2/token", data=data, headers=headers) as response:
            api=await response.json()
            if api["access_token"]:
              res=redirect(self.redirect_uri)
              res.cookies["token"]=api["access_token"]
              return res
            else:
              return False
      return discord_login
    return decorators

  async def get_user(self):
    headers={
      "Authorization": "Bearer {}".format(token)
    }
    async with aiohttp.ClientSession() as session:
      async with session.get(baseurl+"users/@me", headers=headers) as response:
        api=await response.json()
        return user(api)