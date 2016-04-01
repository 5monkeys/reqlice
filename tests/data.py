from reqlice import comment_start_tag
from reqlice.license import License

PACKAGE_LICENSE_DICT = {'django-compressor': License(name='MIT License', osi_approved=True), 'asana': License(name='MIT License', osi_approved=True), 'pyquery': License(name='BSD', osi_approved=True), 'pylibmc': License(name='3-clause BSD <http://www.opensource.org/licenses/bsd-license.php>', osi_approved=True), 'elasticsearch': License(name='Apache Software License', osi_approved=True), 'django-bananas': License(name='UNKNOWN', osi_approved=False), 'Jinja2': License(name='BSD License', osi_approved=True), 'newrelic': License(name='Other/Proprietary License', osi_approved=False), 'Django': License(name='BSD License', osi_approved=True), 'scikit-learn': License(name='new BSD', osi_approved=True), 'jsonfield': License(name='MIT', osi_approved=True), 'logcolor': License(name='UNKNOWN', osi_approved=False), 'dropbox': License(name='Copyright (c) 2015 Dropbox Inc., http://www.dropbox.com/', osi_approved=False), 'requests-oauthlib': License(name='ISC', osi_approved=True)}  # noqa
SMALL_FILE_DONE = """
Django==1.8.10               {comment_start}OSI-Approved: BSD License
django-bananas==1.0.9b4      {comment_start}Non-OSI-Approved: UNKNOWN
django-compressor<2.0,>1.0   {comment_start}OSI-Approved: MIT License
elasticsearch==1.6.0         {comment_start}OSI-Approved: Apache Software License
Jinja2==2.8.0                {comment_start}OSI-Approved: BSD License
jsonfield==1.0.3  # Comment  {comment_start}OSI-Approved: MIT
logcolor==1.0.1              {comment_start}Non-OSI-Approved: UNKNOWN

# Anotha comment
pylibmc                      {comment_start}OSI-Approved: 3-clause BSD <http://www.opensource.org/licenses/bsd-license.php>
pyquery==1.2.9               {comment_start}OSI-Approved: BSD
requests-oauthlib==0.5.0     {comment_start}OSI-Approved: ISC
scikit-learn==0.16.1         {comment_start}OSI-Approved: new BSD
asana==0.5.0                 {comment_start}OSI-Approved: MIT License
dropbox                      {comment_start}Non-OSI-Approved: Copyright (c) 2015 Dropbox Inc., http://www.dropbox.com/
newrelic                     {comment_start}Non-OSI-Approved: Other/Proprietary License
git+https://github.com/mariocesar/sorl-thumbnail.git@master#egg=sorl_thumbnail
https://github.com/jezdez-archive/django-discover-runner/archive/0.4.zip
""".format(comment_start=comment_start_tag).lstrip()  # noqa

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Text Processing :: Markup :: HTML"
]
