#!/usr/bin/env python3
import asyncio
import os
import sys

import aiohttp
import tqdm
from pip.req import parse_requirements as pip_parse_requirements
from pip.req import InstallRequirement
from pip.utils import cached_property

PACKAGE_URL = 'https://pypi.python.org/pypi/{package_name}/json'
loop = asyncio.get_event_loop()


def parse_license(info):
    """ Parse license from info dict retrieved from pypi

    Try to get the license from the classifiers first
    since many projects likes to dump the whole license into info['license']
    """
    classifiers = info['classifiers']
    licenses = [
        c.split('::')[-1].strip()
        for c in classifiers
        if c.startswith('License')
    ]
    license_str = ', '.join(licenses)

    if not license_str or license_str == 'OSI Approved':
        license_str = info.get('license', '').split('\n')[0]

    return license_str or None


def is_pypi_requirement(requirement):
    return requirement.req and not requirement.link


def parse_requirements(path_to_requirements):
    """ Parse requirements

    :param path_to_requirements: path/to/requirements.txt
    :return: ['package name', ..]
    """
    parsed_reqs = []  # (name, version)
    for requirement in pip_parse_requirements(path_to_requirements,
                                              session=False):
        if not is_pypi_requirement(requirement):
            continue

        parsed_reqs.append(requirement.req.project_name)

    return parsed_reqs


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

    @cached_property
    def requirements_dict(self):
        return parse_requirements(self.target)

    def output_requirements(self, package_license_dict):
        with open(self.target) as f:
            content = f.read()

        lines = content.split('\n')
        comment_startpoint = max(len(line) for line in lines) + 2

        for line in lines:
            line = line.strip()

            try:
                requirement = InstallRequirement.from_line(line)
                if not is_pypi_requirement(requirement):
                    raise ValueError
            except ValueError:
                self.write(line)
                continue

            package_name = requirement.req.project_name
            license = package_license_dict.get(package_name)
            if license is None:
                self.write(line)
                continue

            line_length = len(line)
            padding = ' ' * (comment_startpoint - line_length)

            output = '{line}{padding}# {license}'.format(
                line=line, padding=padding, license=license
            )
            self.write(output)

    def fetch_licenses(self):
        package_license_dict = {}
        licence_fetch_tasks = loop.run_until_complete(
            fetch_packages(self.requirements_dict)
        )

        for task in licence_fetch_tasks:
            package_name = task.package_name
            json_data = task.result()

            if json_data is None:
                self.error('Could not fetch info for package:', package_name)
                continue

            info = json_data['info']
            license_str = parse_license(info)

            if license_str:
                package_license_dict[package_name] = license_str

        return package_license_dict

    def run(self):
        # Retrieve info from pypi
        package_license_dict = self.fetch_licenses()
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
