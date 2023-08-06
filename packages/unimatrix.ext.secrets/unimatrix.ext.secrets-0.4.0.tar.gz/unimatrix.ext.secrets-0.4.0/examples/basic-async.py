# pylint: skip-file
import asyncio
import os

import ioc
import unimatrix.runtime
import unimatrix.ext.secrets as secrets


async def main():
    await unimatrix.runtime.on('boot')
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

    print(await secrets.get('EXAMPLE_SECRET_AZURE'))
    print(await secrets.get('EXAMPLE_SECRET_AZURE'))
    print(await secrets.get('EXAMPLE_SECRET_GOOGLE'))
    print(await secrets.get('EXAMPLE_SECRET_GOOGLE'))


if __name__ == '__main__':
    asyncio.run(main())
