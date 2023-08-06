# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_keycloack']

package_data = \
{'': ['*']}

install_requires = \
['python-jose>=3.3.0,<4.0.0']

setup_kwargs = {
    'name': 'fastapi-keycloack',
    'version': '0.2.1',
    'description': '',
    'long_description': '# FastAPI Keycloack\n\nKeycloack plugin for FastApi.\n\nYour aplication receives the claims decoded from the access token.\n\n# Usage\n\nRun keycloak on port 8080 and configure your keycloack server:\n\n```sh\ndocker run -p 8080:8080 -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin quay.io/keycloak/keycloak:15.0.2\n```\n\nInstall dependencies\n\n```sh\npip install fastapi fastapi-keycloack uvicorn\n```\n\nCreate the main.py module\n\n```python\nfrom fastapi import Depends, FastAPI, Security\n\nfrom fastapi_keycloack import JwtDecodeOptions, FastApiKeycloack, GrantType\n\napp = FastAPI()\n\ndecode_options = JwtDecodeOptions(verify_aud=False)\nallowed_grant_types = [\n    GrantType.IMPLICIT,\n    GrantType.PASSWORD,\n    GrantType.AUTHORIZATION_CODE,\n    GrantType.CLIENT_CREDENTIALS,\n]\n\nauth_scheme = FastApiKeycloack(\n    url="http://localhost:8080/auth/realms/master",\n    scheme_name="Keycloak",\n    jwt_decode_options=decode_options,\n    allowed_grant_types=allowed_grant_types,\n)\n\n\ndef get_current_user(claims: dict = Security(auth_scheme)):\n    return claims\n\n\n@app.get("/users/me")\ndef read_current_user(claims: dict = Depends(get_current_user)):\n    return claims\n\n```\n\nRun the application\n\n```sh\nuvicorn main:app\n```\n',
    'author': 'Elber Nava',
    'author_email': 'elbernava11@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/elbernv/fastapi-keycloack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
