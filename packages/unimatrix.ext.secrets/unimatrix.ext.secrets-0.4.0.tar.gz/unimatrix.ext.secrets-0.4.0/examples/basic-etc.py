# pylint: skip-file
import asyncio
import os

import ioc
import unimatrix.runtime
import unimatrix.ext.secrets as secrets


if __name__ == '__main__':
    unimatrix.runtime.on.sync('boot')

    secrets.load()

    print(secrets.get_sync('EXAMPLE_SECRET_AZURE'))
    print(secrets.get_sync('EXAMPLE_SECRET_GOOGLE'))
