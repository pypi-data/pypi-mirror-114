from typing import Optional

import msmcauth


class Microsoft(object):
    @staticmethod
    async def login(email: str, password: str) -> Optional[str]:
        try:
            return msmcauth.login(email, password).access_token
        except ConnectionError:
            return None
        except msmcauth.errors.MsMcAuthException:
            return None
