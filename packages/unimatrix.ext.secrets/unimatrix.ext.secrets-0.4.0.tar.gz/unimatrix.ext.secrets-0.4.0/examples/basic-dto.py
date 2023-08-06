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
        'name': 'EXAMPLE_DTO_JSON',
        'encoding': 'utf-8',
        'content_type': "application/json",
        'opts': {
            'project': 'unimatrixdev',
        }
    })

    print(await secrets.get('EXAMPLE_DTO_JSON'))


if __name__ == '__main__':
    asyncio.run(main())
