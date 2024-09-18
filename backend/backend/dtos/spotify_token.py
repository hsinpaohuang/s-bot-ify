from datetime import datetime, timedelta
from time import mktime
from pydantic import BaseModel

class SpotifyToken(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str

    @property
    def expires_at(self):
        expire_time = datetime.now() + timedelta(seconds=self.expires_in)
        return int(mktime(expire_time.timetuple()))
