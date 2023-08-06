# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deutschland', 'deutschland.bundesanzeiger']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.1,<9.0.0',
 'Shapely>=1.7.1,<2.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'boto3>=1.18.9,<2.0.0',
 'dateparser>=1.0.0,<2.0.0',
 'gql>=2.0.0,<3.0.0',
 'mapbox-vector-tile>=1.2.1,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0',
 'slugify>=0.0.1,<0.0.2',
 'tensorflow>=2.5.0,<3.0.0',
 'webdriver-manager>=3.4.2,<4.0.0']

setup_kwargs = {
    'name': 'deutschland',
    'version': '0.1.5',
    'description': '',
    'long_description': '# Deutschland\nA python package that gives you easy access to the most valuable datasets of Germany.\n\n## Installation\n```bash\npip install deutschland\n```\n\n## Geographic data\nFetch information about streets, house numbers, building outlines, …\n\n```python\nfrom deutschland import Geo\ngeo = Geo()\n# top_right and bottom_left coordinates\ndata = geo.fetch([52.50876180448243, 13.359631043007212], \n                 [52.530116236589244, 13.426532801586827])\nprint(data.keys())\n# dict_keys([\'Adresse\', \'Barrierenlinie\', \'Bauwerksflaeche\', \'Bauwerkslinie\', \'Bauwerkspunkt\', \'Besondere_Flaeche\', \'Besondere_Linie\', \'Besonderer_Punkt\', \'Gebaeudeflaeche\', \'Gebaeudepunkt\', \'Gewaesserflaeche\', \'Gewaesserlinie\', \'Grenze_Linie\', \'Historischer_Punkt\', \'Siedlungsflaeche\', \'Vegetationslinie\', \'Verkehrsflaeche\', \'Verkehrslinie\', \'Verkehrspunkt\', \'Hintergrund\'])\n\nprint(data["Adresse"][0])\n# {\'geometry\': {\'type\': \'Point\', \'coordinates\': (13.422642946243286, 52.51500157651358)}, \'properties\': {\'postleitzahl\': \'10179\', \'ort\': \'Berlin\', \'ortsteil\': \'Mitte\', \'strasse\': \'Holzmarktstraße\', \'hausnummer\': \'55\'}, \'id\': 0, \'type\': \'Feature\'}\n```\n\n\n\n\n## Company Data\n\n### Handelsregister\nGet financial reports for all german companies that are reporting to Handelsregister.\n\n*Big thanks to Nico Duldhardt and Friedrich Schöne, who [supported this implementation with their machine learning model](https://av.tib.eu/media/52366).*\n\n```python\nfrom deutschland import Bundesanzeiger\nba = Bundesanzeiger()\n# search term\ndata = ba.get_reports("Deutsche Bahn AG")\n# returns a dictionary with all reports found as fulltext reports\nprint(data.keys())\n# dict_keys([\'Jahresabschluss zum Geschäftsjahr vom 01.01.2020 bis zum 31.12.2020\', \'Konzernabschluss zum Geschäftsjahr vom 01.01.2020 bis zum 31.12.2020\\nErgänzung der Veröffentlichung vom 04.06.2021\',\n```\n',
    'author': 'Lilith Wittmann',
    'author_email': 'mail@lilithwittmann.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bundesAPI/deutschland',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
