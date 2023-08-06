# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytimeline']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0,<9.0',
 'loguru>=0.5.3,<0.6.0',
 'pendulum>=2.1,<3.0',
 'svgwrite>=1.4,<2.0']

setup_kwargs = {
    'name': 'pytimeline',
    'version': '0.2.0',
    'description': 'A library for creating and cleaning SVG timelines.',
    'long_description': '<h1 align="center">\n    <b>Pytimeline</b>\n</h1>\n\n`pytimeline` is a command line tool for the creating of SVG timelines from JSON.\n\n<p align="center">\n  <img alt="Simple example" src="examples/timeline.png">\n</p>\n\nNote: This is a rewrite of the old [timeline script](https://github.com/jasonreisman/Timeline) from Jason Reisman and full credits go to him for most of the work.\n\n## Install\n\nThe package is compatible with `Python 3.7+` and can be installed in your current environment with `pip`:\n```bash\npython -m pip install pytimeline\n```\n\n## Usage\n\nWhen the package is installed in your activated environment, it can be called through `python -m colorframe`.\nDetailed usage goes as follows:\n```bash\nUsage: python -m pytimeline [OPTIONS]\n\nOptions:\n  --inputfile PATH                Path to the input JSON file with the\n                                  timeline data.  [required]\n  --outputdir DIRECTORY           Path to the directory in which to write the\n                                  output SVG file. If not provided, will\n                                  pickthe directory of the input file.\n  --logging [trace|debug|info|warning|error|critical]\n                                  Sets the logging level.  [default: info]\n  --help                          Show this message and exit.\n```\n\nThe script will parse your input file and export the `SVG` document in the provided output folder or, if not provided, in the same directory as the input file.\n\nOne can otherwise import the high-level object from the package and use it directly:\n```python\nfrom pytimeline import Timeline\n\ntimeline = Timeline(inputfile="your_input.json")\ntimeline.build()\ntimeline.save("timeline.svg")\n```\n\n## Input Data Format\n\nThe input file is a `JSON` document that describes the start and end points of the timeline, tickmarks along the main axis, as well as callouts to specifc dates/times, and eras which highlight temporal periods.\n\nAll date fields can be described in several common date formats and may optionally also include a time of day (e.g. "3/14/15 9:26am").\nDatetime parsing is handled by the `pendulum` package, and one can find all the accepted date formats [in the relevant documentation](https://pendulum.eustace.io/docs/#parsing).\n\n### Required and Optional Fields\n\nThe required fields are `width`, `start`, and `end`. \nAll other fields are optional.  \n\n**Required:**\n* `width` describes the width, in pixels, of the output SVG document, and the height will be determined automatically.\n* `start` is the date/time of the leftmost date/time on the axis.\n* `end` is the date/time of the rightmost date/time on the axis.\n\n**Optional:**\n* `num_ticks` contols the number of tickmarks along the axis between the `start` and `end` date/times (inclusive).  If this field is not present, no tickmarks will be generated except for those at the `start` and `end` dates.\n* `tick_format` describes the string format of the tickmarks along the axis. See the [valid formats](https://pendulum.eustace.io/docs/#formatter) for the `pendulum` package.\n\n### Special Fields\n\n#### Callouts\n\nCallouts along the axis are described in the `callouts` list, in which each entry is also a list with two to three string values:\n* The first value is the `description` of the callout (e.g., "Pi Day"). It is required.\n* The second value is the `date/time` of the callout (e.g., "3/14/15 9:26am"). It is required.\n* The third value can specify a `color` for the callout, either as a hexcode or a valid SVG color alias. It is optional.\n\nCallout examples:\n```JSON\n["Ultimate Pi Day", "3/14/15 9:26am"]\n```\nOr, with a custom callout color:\n```JSON\n["Ultimate Pi Day", "3/14/15 9:26am", "#CD3F85"]\n```\n#### Eras\n\nEras are highlighted temporal periods and are described in the `eras` list.\nLike the `callouts` list, each entry in the eras list is itself a list with either three or four string values:\n* The first value is the `description` of the era (e.g., "Summer"). It is required.\n* The second value is the start `date/time` of the era (e.g., "6/21/15 12am"). It is required.\n* The third value is the end `date/time` of the era (e.g. "9/20/15 11:59pm"). It is required.\n* The fourth value can specify a `color` for the era, either as a hexcode or a valid SVG color alias. It is optional.\n\nEra examples:\n```JSON\n["Summer 2015", "6/21/15 12am", "9/20/15 11:59pm"]\n```\nOr, with a custom era color:\n```JSON\n["Summer 2015", "6/21/15 12am", "9/20/15 11:59pm", "Orange"]\n```\n\n## Simple Example\n\nThe `JSON` input for the example timeline at the top of this `README` is:\n```json\n{\n\t"width" : 750,\n\t"start" : "Oct 8 2015",\n\t"end" : "Oct 15 2015",\t\n\t"num_ticks" : 14,\n\t"tick_format" : "%b %d, %Y - %I:%M%p",\n\t"callouts" : [\n\t\t["ABC easy as 123", "Oct 14, 2015 3pm"],\t\t\n\t\t["Midnight Event A", "12am Oct 10, 2015", "#DD0000"],\n\t\t["Noon Event A", "12pm Oct 10, 2015"],\t\t\n\t\t["5pm Event A", "5pm Oct 10, 2015"],\t\t\t\t\n\t\t["Something amazing happening", "Oct 11, 2015"],\n\t\t["Awesome Event B", "Oct 12, 2015", "#DD0000"],\n\t\t["C", "Oct 13, 2015"],\n\t\t["Event E", "Oct 14, 2015"]\n\t],\n\t"eras" : [\n\t\t["Era 1", "12pm Oct 8, 2015", "3am Oct 12, 2015", "#CD3F85"],\n\t\t["Era 2", "8am Oct 12, 2015", "12am Oct 15, 2015", "#C0C0FF"]\n\t]\n}\n```',
    'author': 'Felix Soubelet',
    'author_email': 'felix.soubelet@cern.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fsoubelet/Timeline',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
