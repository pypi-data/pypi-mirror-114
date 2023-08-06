# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deutschland']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.7.1,<2.0.0',
 'mapbox-vector-tile>=1.2.1,<2.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'deutschland',
    'version': '0.1.4',
    'description': '',
    'long_description': '# Deutschland\nA python package that gives you easy access to the most valuable datasets of Germany.\n\n## Installation\n```bash\npip install deutschland\n```\n\n## Geographic data\nFetch information about streets, house numbers, building outlines, …\n\n```python\nfrom deutschland import Geo\ngeo = Geo()\n# top_right and bottom_left coordinates\ndata = geo.fetch([52.50876180448243, 13.359631043007212], \n                 [52.530116236589244, 13.426532801586827])\nprint(data.keys())\n# dict_keys([\'Adresse\', \'Barrierenlinie\', \'Bauwerksflaeche\', \'Bauwerkslinie\', \'Bauwerkspunkt\', \'Besondere_Flaeche\', \'Besondere_Linie\', \'Besonderer_Punkt\', \'Gebaeudeflaeche\', \'Gebaeudepunkt\', \'Gewaesserflaeche\', \'Gewaesserlinie\', \'Grenze_Linie\', \'Historischer_Punkt\', \'Siedlungsflaeche\', \'Vegetationslinie\', \'Verkehrsflaeche\', \'Verkehrslinie\', \'Verkehrspunkt\', \'Hintergrund\'])\n\nprint(data["Adresse"][0])\n# {\'geometry\': {\'type\': \'Point\', \'coordinates\': (13.422642946243286, 52.51500157651358)}, \'properties\': {\'postleitzahl\': \'10179\', \'ort\': \'Berlin\', \'ortsteil\': \'Mitte\', \'strasse\': \'Holzmarktstraße\', \'hausnummer\': \'55\'}, \'id\': 0, \'type\': \'Feature\'}\n```\n',
    'author': 'Lilith Wittmann',
    'author_email': 'mail@lilithwittmann.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
