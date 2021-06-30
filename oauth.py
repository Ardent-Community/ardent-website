import requests
import os 

class OAuth2:
    DISCORD_LOGIN_URL = os.environ['DISCORD_LOGIN_URL']  # the login redirect url
    CLIENT_ID = os.environ['CLIENT_ID']
    CLIENT_SECRET = os.environ['CLIENT_SECRET']
    REDIRECT_URL = "https://discord.com/"
    SCOPE = "identify"  # all the scopes separeted by `%20`
    DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
    DISCORD_API_URL = "https://discord.com/api"

    @staticmethod
    def get_access_token(code):
        payload = {
            "client_id": OAuth2.CLIENT_ID,
            "client_secret": OAuth2.CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": OAuth2.REDIRECT_URL,
            # "scope": OAuth2.SCOPE
        }

        headers = {"Content-Type": 'application/x-www-form-urlencoded'}

        access_token = requests.post(url=OAuth2.DISCORD_TOKEN_URL, data=payload, headers=headers).json()
        print(access_token)
        return access_token.get("access_token")

    @staticmethod
    def get_user_json(access_token):
        url = f"{OAuth2.DISCORD_API_URL}/users/@me"
        headers = {"Authorization": f"Bearer {access_token}"}
 
        user_object = requests.get(url=url, headers=headers).json()
        return user_object

