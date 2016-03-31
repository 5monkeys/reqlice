#!/usr/bin/env python3
import asyncio
import os
import re
import sys

import aiohttp
import tqdm
from reqlice.license import parse_license
from reqlice.requirement import get_valid_pypi_requirement, parse_requirements

PACKAGE_URL = 'https://pypi.python.org/pypi/{package_name}/json'
loop = asyncio.get_event_loop()
comment_start_tag = '# [license] '
comment_start_re = re.compile(re.escape(comment_start_tag) + '.+')


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


async def fetch_packages(deps):
    """ Fetch many packages from pypi

    :param deps: ['package name', ..]
    :return list of PackageFetchTasks, which are done when returned
    """
    # Limit the maximum number of active requests
    connector = aiohttp.TCPConnector(limit=5)

    with aiohttp.ClientSession(loop=loop, connector=connector) as session:
        tasks = [
            PackageFetchTask(session, package_name, loop=loop)
            for package_name in deps
        ]

        # PROGRESS BAR, SUCH IMPORTANCE
        for future in tqdm.tqdm(asyncio.as_completed(tasks, loop=loop),
                                total=len(tasks)):
            await future

        return tasks


class Reqlice:

    def __init__(self, target, out=sys.stdout, err=sys.stderr):
        assert os.path.isfile(target), \
            'Could not find {!r} on filesystem'.format(target)
        self.target = target
        self.out = out
        self.err = err

    def write(self, *what):
        print(*what, file=self.out)

    def error(self, *what):
        print(*what, file=self.err)

    def output_requirements(self, package_license_dict):
        """ Output requirements to self.out

        :param package_license_dict: dict of {'package name': {License}}
        """
        with open(self.target) as f:
            content = f.read()

        lines = [comment_start_re.sub('', line).strip()
                 for line in content.split('\n')]
        comment_startpoint = max(len(line) for line in lines) + 2

        for line in lines:
            requirement = get_valid_pypi_requirement(line)
            if requirement is None:
                self.write(line)
                continue

            package_name = requirement.req.project_name
            license = package_license_dict.get(package_name)
            if license is None:
                self.write(line)
                continue

            padding = ' ' * (comment_startpoint - len(line))

            output = '{line}{padding}{comment_start}{license}'.format(
                line=line,
                padding=padding,
                comment_start=comment_start_tag,
                license=license
            )
            self.write(output)

    def fetch_licenses(self, packages):
        package_license_dict = {}
        licence_fetch_tasks = loop.run_until_complete(
            fetch_packages(packages)
        )

        for task in licence_fetch_tasks:
            package_name = task.package_name
            json_data = task.result()

            if json_data is None:
                self.error('Could not fetch info for package:', package_name)
                continue

            info = json_data['info']
            license = parse_license(info)

            if license:
                package_license_dict[package_name] = license

        return package_license_dict

    def run(self):
        # Parse packages
        packages = parse_requirements(self.target)
        # Retrieve info from pypi
        package_license_dict = self.fetch_licenses(packages)
        # Print to the screen
        self.output_requirements(package_license_dict)


def cli():
    if len(sys.argv) != 2:
        print('Usage: reqlice path/to/requirements.txt')
        sys.exit(1)

    path_to_requirements = sys.argv[1]
    Reqlice(path_to_requirements).run()

if __name__ == '__main__':
    cli()