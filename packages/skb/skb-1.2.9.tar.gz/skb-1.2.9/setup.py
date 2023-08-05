# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skb']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.3,<5.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['skb = skb.skb:main']}

setup_kwargs = {
    'name': 'skb',
    'version': '1.2.9',
    'description': 'Synth Kit builder for Synthstrom Deluge',
    'long_description': "# SKB - Synth Kit Builder for Synthstrom Deluge\n\nA Python utility for the Synthstrom Deluge, used for building KITS (drum kits) from existing SYNTH sounds.\n\n## Motivation\n\nReasoning: whilst you can manually create a KIT using the synthesis engine and you can build a KIT by loadinging one or more samples into a KIT LANE, it's not possible, as of Firmware 3.1.5, to load SYNTH files into KIT LANES. I wrote this utility to enable you to do just that.\n\n## Requirements\n\n- Latest Deluge firmware. At time of first release this is 3.1.5\n- The ability to mount your Deluge SD card in your computer and have read/write access\n- Python 3 plus Pip tools to install Paython packages\n- familiarity with Python command-line tools\n\n## Installation or Getting Started\n\nProvding you have Python 3 and the corresponding Pip installer tools it should be a case of just doing:\n\n```Text\npython3 -m pip install skb\n```\n\n## Usage\n\nskb --sd-root 'path' --input-file 'filemame' --ouput-file 'filename'\n\nExample:\n\n```Text\nskb --sd-root '/Volumes/DELUGE32/' --input-file 'kitfile.txt' --output-file skb.XML\n```\n\n**sd-root** = full path to root of your mounted SD card e.g. /Volumes/DELUGE/\n\n**input-file** = name of XML file which describes your KIT contents (see below)\n\n**output-file** = name of the generated KIT file, plain text, one synth filename per line\n\n## XML Kit File\n\nIn order to tell the tool which SYNTH patches you want in your KIT, you need to create a text file e.g.\n\n```Text\nKICK.XML\nSNARE.XML\nCLAP.XML\n```\n\nDo not include the full path e.g. /SYNTHS/KICK.XML - just specify the synth XML filename.\n\nThe script will create the KIT in reverse order meaning the first synth in your text file will be the lowest row etc.\n\nYou can specify the same SYNTH more than once and theoretically there should be no (reasonable) limit to how many lanes you can generate. For anyone wanting to build their own synth kits, this tool would be really handy as you could create, say, a kick drum synth patch that you're happy with and then load 16 copies of that into a KIT. Then you can tweak each one on the Deluge to give you a kit full of variation on the synthesis method.\n\nIt's probably worth pointing out that any editing or changes you make to the generated kit on the Deluge will not be reflected in the original SYNTH patches. That's probably a good thing though!\n\nNOTE:\n\nThe script assumes (correctly!) that you have a KITS and SYNTHS folder in the root of your Deluge SD card. It will look for the SYNTH patches in the SYNTHS folder and will output the KIT in the KITS folder.\n\n## Contributors\n\nContributions welcome!\n\n## License\n\nMIT\n",
    'author': 'neilbaldwin',
    'author_email': 'neil.baldwin@mac.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/neilbaldwin/skb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
