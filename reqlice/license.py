import re
from collections import namedtuple

OSI_APPROVED_LICENSES = """
Academic Free License 3.0
AFL-3.0
Affero General Public License
Adaptive Public License
APL-1.0
Apache License 2.0
Apache-2.0
http://www.apache.org/licenses/LICENSE-2.0
Apple Public Source License
APSL-2.0
Artistic license 2.0
Artistic-2.0
Attribution Assurance Licenses
AAL
BSD
3-clause BSD
2-clause BSD
Boost Software License
BSL-1.0
CeCILL License 2.1
CECILL-2.1
Computer Associates Trusted Open Source License 1.1
CATOSL-1.1
Common Development and Distribution License 1.0
CDDL-1.0
Common Public Attribution License 1.0
CPAL-1.0
CUA Office Public License Version 1.0
CUA-OPL-1.0
EU DataGrid Software License
EUDatagrid
Eclipse Public License 1.0
EPL-1.0
eCos License version 2.0
Educational Community License, Version 2.0
ECL-2.0
Eiffel Forum License V2.0
EFL-2.0
Entessa
European Union Public License, Version 1.1
EUPL-1.1
Frameworx License
Frameworx-1.0
Free Public License 1.0.0
GNU Affero General Public License v3
AGPL 3.0
GNU General Public License version 2.0
GPL 2.0
GNU General Public License version 3.0
GPL 3.0
GNU Library or "Lesser" General Public License version 2.1
LGPL 2.1
GNU Library or "Lesser" General Public License version 3.0
LGPL 3.0
Historical Permission Notice and Disclaimer
HPND
IBM Public License 1.0
IPL-1.0
IPA Font License
IPA
ISC License
ISC
LaTeX Project Public License 1.3c
LPPL-1.3c
Lucent Public License Version 1.02
LPL-1.02
MirOS Licence
MirOS
Microsoft Public License
MS-PL
Microsoft Reciprocal License
MS-RL
MIT license
MIT
Motosoto License
Motosoto
Mozilla Public License 2.0
MPL-2.0
Multics License
Multics
NASA Open Source Agreement 1.3
NASA-1.3
NTP License
NTP
Naumen Public License
Naumen
Nethack General Public License
NGPL
Nokia Open Source License
Nokia
Non-Profit Open Software License 3.0
NPOSL-3.0
OCLC Research Public License 2.0
OCLC-2.0
Open Group Test Suite License
OGTSL
Open Software License 3.0
OSL-3.0
OSET Public License version 2.1
PHP License 3.0
PHP-3.0
The PostgreSQL License
PIL Software License
Standard PIL License
PostgreSQL
Python License
Python-2.0
CNRI Python license
CNRI-Python
Q Public License
QPL-1.0
RealNetworks Public Source License V1.0
RPSL-1.0
Reciprocal Public License 1.5
RPL-1.5
Ricoh Source Code Public License
RSCPL
SIL Open Font License 1.1
OFL-1.1
Simple Public License 2.0
SimPL-2.0
Sleepycat License
Sleepycat
Sun Public License 1.0
SPL-1.0
Sybase Open Watcom Public License 1.0
Watcom-1.0
University of Illinois/NCSA Open Source License
NCSA
Universal Permissive License
UPL
Vovida Software License v. 1.0
VSL-1.0
W3C License
W3C
wxWindows Library License
WXwindows
X.Net License
Xnet
Zope Public License 2.0
ZPL-2.0
zlib/libpng license
Zlib
"""

pattern = r'|'.join(li for li in OSI_APPROVED_LICENSES.split('\n') if li)
osi_approved_re = re.compile(pattern)


class License(namedtuple('License', ['name', 'osi_approved'])):

    def __str__(self):
        name = self.name
        if self.osi_approved:
            name = 'OSI-Approved: {}'.format(name)
        else:
            name = 'Non-OSI-Approved: {}'.format(name)
        return name


def parse_license(info):
    """ Parse license from info dict retrieved from pypi

    Try to get the license from the classifiers first
    since many projects likes to dump the whole license into info['license']
    """
    classifiers = info['classifiers']
    license_classfiers = [
        c for c in classifiers
        if c.startswith('License')
    ]
    licenses = [c.split('::')[-1].strip() for c in license_classfiers]
    license_str = ', '.join(licenses)

    other_license = (info.get('license') or '').split('\n')[0]
    if other_license:
        if not license_str or license_str == 'OSI Approved':
            license_str = other_license
        elif other_license != 'UNKNOWN' and other_license not in license_str:
            license_str = '{}, {}'.format(license_str, other_license)

    if license_str:
        osi_approved = any('OSI Approved' in classifier
                           for classifier in license_classfiers)
        if not osi_approved:
            osi_approved = bool(osi_approved_re.match(license_str))
        return License(name=license_str, osi_approved=osi_approved)

    return None
