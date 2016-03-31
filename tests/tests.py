import os
from io import StringIO

from reqlice import Reqlice
from reqlice.license import License

test_file = os.path.join(os.path.dirname(__file__), 'small.txt')
PACKAGE_LICENSE_DICT = {'django-compressor': License(name='MIT License', osi_approved=True), 'asana': License(name='MIT License', osi_approved=True), 'pyquery': License(name='BSD', osi_approved=True), 'pylibmc': License(name='3-clause BSD <http://www.opensource.org/licenses/bsd-license.php>', osi_approved=True), 'elasticsearch': License(name='Apache Software License', osi_approved=True), 'django-bananas': License(name='UNKNOWN', osi_approved=False), 'Jinja2': License(name='BSD License', osi_approved=True), 'newrelic': License(name='Other/Proprietary License', osi_approved=False), 'Django': License(name='BSD License', osi_approved=True), 'scikit-learn': License(name='new BSD', osi_approved=True), 'jsonfield': License(name='MIT', osi_approved=True), 'logcolor': License(name='UNKNOWN', osi_approved=False), 'dropbox': License(name='Copyright (c) 2015 Dropbox Inc., http://www.dropbox.com/', osi_approved=False), 'requests-oauthlib': License(name='ISC', osi_approved=True)}  # noqa
SMALL_FILE_DONE = """
Django==1.8.10                                                                  # RQL - OSI-Approved: BSD License
django-bananas==1.0.9b4                                                         # RQL - UNKNOWN
django-compressor<2.0,>1.0                                                      # RQL - OSI-Approved: MIT License
elasticsearch==1.6.0                                                            # RQL - OSI-Approved: Apache Software License
Jinja2==2.8.0                                                                   # RQL - OSI-Approved: BSD License
jsonfield==1.0.3  # Comment                                                     # RQL - OSI-Approved: MIT
logcolor==1.0.1                                                                 # RQL - UNKNOWN
pylibmc                                                                         # RQL - OSI-Approved: 3-clause BSD <http://www.opensource.org/licenses/bsd-license.php>
pyquery==1.2.9                                                                  # RQL - OSI-Approved: BSD
requests-oauthlib==0.5.0                                                        # RQL - OSI-Approved: ISC
scikit-learn==0.16.1                                                            # RQL - OSI-Approved: new BSD
asana==0.5.0                                                                    # RQL - OSI-Approved: MIT License
dropbox                                                                         # RQL - Copyright (c) 2015 Dropbox Inc., http://www.dropbox.com/
newrelic                                                                        # RQL - Other/Proprietary License
git+https://github.com/mariocesar/sorl-thumbnail.git@master#egg=sorl_thumbnail
https://github.com/jezdez-archive/django-discover-runner/archive/0.4.zip
""".strip()  # noqa


def test_output():
    out = StringIO()
    err = StringIO()
    req = Reqlice(test_file, out=out, err=err)
    req.output_requirements(PACKAGE_LICENSE_DICT)
    result = out.getvalue()

    print()
    print(result)
    assert result.strip() == SMALL_FILE_DONE
    assert not err.getvalue()


def test_strip_previous_output():
    test_file = os.path.join(os.path.dirname(__file__), 'small-done.txt')
    out = StringIO()
    err = StringIO()
    req = Reqlice(test_file, out=out, err=err)
    req.output_requirements(PACKAGE_LICENSE_DICT)
    result = out.getvalue()

    print()
    print(result)
    assert result.strip() == SMALL_FILE_DONE
    assert not err.getvalue()
