from pip.req import parse_requirements as pip_parse_requirements
from pip.req import InstallRequirement


def is_pypi_requirement(requirement):
    return requirement.req and not requirement.link


def parse_requirements(path_to_requirements):
    """ Parse requirements

    :param path_to_requirements: path/to/requirements.txt
    :return: ['package name', ..]
    """
    parsed_reqs = []
    for requirement in pip_parse_requirements(path_to_requirements,
                                              session=False):
        if not is_pypi_requirement(requirement):
            continue

        parsed_reqs.append(requirement.req.project_name)

    return parsed_reqs


def get_valid_pypi_requirement(line):
    try:
        requirement = InstallRequirement.from_line(line)
        if not is_pypi_requirement(requirement):
            raise ValueError
    except ValueError:
        return None

    return requirement
