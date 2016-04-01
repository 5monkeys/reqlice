import os
from io import StringIO

from reqlice import Reqlice
from reqlice.license import parse_license
from .data import CLASSIFIERS, SMALL_FILE_DONE, PACKAGE_LICENSE_DICT

test_file = os.path.join(os.path.dirname(__file__), 'small.txt')


def test_output():
    out = StringIO()
    err = StringIO()
    req = Reqlice(test_file, out=out, err=err)
    req.output_requirements(PACKAGE_LICENSE_DICT)
    result = out.getvalue()

    print()
    print(result)
    assert result == SMALL_FILE_DONE
    assert not err.getvalue()


def test_strip_previous_output():
    test_file = os.path.join(os.path.dirname(__file__), 'small.txt')
    out = StringIO()
    err = StringIO()
    req = Reqlice(test_file, out=out, err=err)
    req.output_requirements(PACKAGE_LICENSE_DICT)
    result = out.getvalue()

    req = Reqlice(result, out=out, err=err)
    req.output_requirements(PACKAGE_LICENSE_DICT)

    print()
    print(result)
    assert result == SMALL_FILE_DONE
    assert not err.getvalue()


def test_parse_license():
    license = parse_license({'classifiers': CLASSIFIERS, 'license': 'BSD'})

    assert license is not None
    assert license.name == 'BSD License'
