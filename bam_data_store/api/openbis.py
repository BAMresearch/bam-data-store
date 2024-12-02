from decouple import config as environ
from pybis import Openbis


def openbis_login():
    o = Openbis(url=environ('OPENBIS_HOST'))
    # * In case of self-signed certificates
    # o = Openbis(url=environ("OPENBIS_HOST"), verify_certificates=False)

    username = environ('OPENBIS_USERNAME_ADMIN')
    password = environ('OPENBIS_PASSWORD_ADMIN')
    openbis_space = environ('OPENBIS_SPACE_ADMIN')  # VP.1_JPIZARRO or JPIZARRO_ADM

    o.login(username=username, password=password)
    return o, openbis_space
