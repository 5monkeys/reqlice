try:  # for pip >= 10
    from pip._internal.req import parse_requirements as pip_parse_requirements
    from pip._internal.req import InstallRequirement
    from pip._internal.req.constructors import install_req_from_line as _from_line

except ImportError:
    from pip.req import parse_requirements as pip_parse_requirements
    from pip.req import InstallRequirement

    _from_line = InstallRequirement.from_line


def is_pypi_requirement(requirement):
    return requirement.req and not requirement.link


def parse_requirements(path_to_requirements):
    """ Parse requirements

    :param path_to_requirements: path/to/requirements.txt
    :return: ['package name', ..]
    """
    parsed_reqs = []
    for requirement in pip_parse_requirements(path_to_requirements, session=False):
        if not is_pypi_requirement(requirement):
            continue

        try:
            _name = requirement.req.project_name
        except AttributeError:
            _name = requirement.req.name

        parsed_reqs.append(_name)

    return parsed_reqs


def get_valid_pypi_requirement(line):
    try:
        requirement = _from_line(line)
        if not is_pypi_requirement(requirement):
            raise ValueError
    except ValueError:
        return None

    return requirement
