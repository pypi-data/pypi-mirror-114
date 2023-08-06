# pylint: skip-file
import asyncio
import os

import ioc
import unimatrix.runtime
import unimatrix.ext.secrets as secrets


if __name__ == '__main__':
    unimatrix.runtime.on.sync('boot')

    secrets.add({
        'provider': 'google',
        'name': 'EXAMPLE_SECRET',
        'alias': 'EXAMPLE_SECRET_GOOGLE',
        'encoding': 'utf-8',
        'opts': {
            'project': 'unimatrixdev',
        }
    })
    secrets.add({
        'provider': 'azure',
        'name': 'example-secret',
        'alias': 'EXAMPLE_SECRET_AZURE',
        'opts': {
            'vault': 'unimatrixdev',
        }
    })

    print(secrets.get_sync('EXAMPLE_SECRET_AZURE'))
    print(secrets.get_sync('EXAMPLE_SECRET_GOOGLE'))
