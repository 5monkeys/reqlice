import asyncio

import aiohttp
import tqdm

PACKAGE_URL = 'https://pypi.python.org/pypi/{package_name}/json'


class PackageFetchTask(asyncio.Task):
    """
    Fetches package info from pypi
    """

    def __init__(self, session, package_name, *, loop=None):
        self.session = session
        self.package_name = package_name
        self.url = PACKAGE_URL.format(package_name=package_name)

        super().__init__(self.fetch_package_info(), loop=loop)

    async def fetch_package_info(self):
        """ Fetch package info """
        async with self.session.get(self.url) as response:
            if response.status == 200:
                return await response.json()

        return None


async def fetch_packages(packages, loop=None):
    """ Fetch many packages from pypi

    :param packages: ['package name', ..]
    :param loop: Asyncio event loop
    :return list of PackageFetchTasks, which are done when returned
    """
    # Limit the maximum number of active requests
    connector = aiohttp.TCPConnector(limit=5)

    with aiohttp.ClientSession(loop=loop, connector=connector) as session:
        tasks = [
            PackageFetchTask(session, package_name, loop=loop)
            for package_name in packages
        ]

        # PROGRESS BAR, SUCH IMPORTANCE
        for future in tqdm.tqdm(asyncio.as_completed(tasks, loop=loop),
                                total=len(tasks)):
            await future

        return tasks
