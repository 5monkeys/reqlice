#!/usr/bin/env python3
import asyncio
import os
import re
import sys

from reqlice.license import parse_license
from reqlice.package import fetch_packages
from reqlice.requirement import get_valid_pypi_requirement, parse_requirements

loop = asyncio.get_event_loop()
comment_start_tag = '# [license] '
comment_start_re = re.compile(re.escape(comment_start_tag) + '.+')


class Reqlice:

    def __init__(self, target, out=sys.stdout, err=sys.stderr):
        """
        :param target: 'path/to/requirements.txt'
        :param out: where to print
        :param err: where to print errors
        """
        self.target = target
        self.out = out
        self.err = err

    def write(self, *what):
        print(*what, file=self.out)

    def error(self, *what):
        print(*what, file=self.err)

    def read_target(self):
        if os.path.isfile(self.target):
            with open(self.target) as f:
                return f.read()

        # Assume string
        return self.target

    def output_requirements(self, package_license_dict):
        """ Output requirements to self.out

        :param package_license_dict: dict of {'package name': {License}}
        """
        content = self.read_target()
        lines = []

        # First pass, fetch requirement, strip line
        for line in content.splitlines():
            line = comment_start_re.sub('', line).strip()
            requirement = get_valid_pypi_requirement(line)
            if requirement is None:
                license = None
            else:
                package_name = requirement.req.project_name
                license = package_license_dict.get(package_name)

            lines.append((line, license))

        comment_startpoint = max(
            len(line) for line, license in lines if license
        ) + 2

        for line, license in lines:
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
            fetch_packages(packages, loop=loop)
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
