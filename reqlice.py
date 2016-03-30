#!/usr/bin/env python3
import asyncio
import sys
from pip.req import parse_requirements as pip_parse_requirements

import aiohttp

PACKAGE_URL = 'https://pypi.python.org/pypi/{package_name}/{version}/json'
loop = asyncio.get_event_loop()


def _package_name(name):
    return name.replace('-', '_').lower()


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


def parse_requirements(path_to_requirements):
    """ Parse requirements

    :param path_to_requirements: path/to/requirements.txt
    :return: [('package name', 'version'), ..]
    """
    parsed_reqs = []  # (name, version)
    for requirement in pip_parse_requirements(path_to_requirements, session=False):
        specs = requirement.req.specs
        if len(specs) < 1:
            continue

        if len(specs[0]) == 2:
            # specs should be a tuple of '==' and 'version'
            parsed_reqs.append((requirement.req.project_name, specs[0][1]))

    return parsed_reqs


def output_requirements(requirements, package_license_dict, file=sys.stdout):
    with open(requirements) as f:
        content = f.read()

    lines = content.split('\n')
    comment_startpoint = max(len(line) for line in lines) + 2

    for line in lines:
        line = line.strip()
        line_length = len(line)
        padding = ' ' * (comment_startpoint - line_length)

        req = line.split('==')
        if len(req) != 2:
            print(line, file=file)
            continue

        package_name, version = req
        license = package_license_dict.get(_package_name(package_name))
        if license is None:
            print(line, file=file)
            continue

        line = line.rstrip()

        output = '{line}{padding}# {license}'.format(
            line=line, padding=padding, license=license
        )
        print(output, file=file)


async def fetch_package_info(session, package_name, version):
    """ Fetch package info """
    url = PACKAGE_URL.format(package_name=package_name, version=version)
    async with session.get(url) as response:
        if response.status == 200:
            json_data = await response.json()
        else:
            json_data = None
        return package_name, json_data


async def fetch_licenses(deps):
    """ Fetch many licenses

    :param deps: [('package name', 'version'), ..]
    :return dict like {'package_name': 'license'}
    """
    connector = aiohttp.TCPConnector(limit=5)

    with aiohttp.ClientSession(loop=loop, connector=connector) as session:
        coros = [
            fetch_package_info(session, package_name, version)
            for package_name, version in deps
        ]

        done, _ = await asyncio.wait(coros)

        package_license_dict = {}
        for future in done:
            package_name, json_data = future.result()
            if json_data is None:
                print('Could not fetch info for package:', package_name, file=sys.stderr)
                continue

            info = json_data['info']
            license_str = parse_license(info)

            if license_str:
                package_license_dict[_package_name(info['name'])] = license_str

        return package_license_dict


def main():
    if len(sys.argv) != 2:
        print('Usage: reqlice path/to/requirements.txt')
        sys.exit(1)

    path_to_requirements = sys.argv[1]
    # Parse requirements into a list of tuples, [('package name', 'version'), ..]
    parsed_requirements = parse_requirements(path_to_requirements)
    # Retrieve info from pypi
    package_license_dict = loop.run_until_complete(fetch_licenses(parsed_requirements))
    # Print to the screen
    output_requirements(path_to_requirements, package_license_dict)


if __name__ == '__main__':
    main()
