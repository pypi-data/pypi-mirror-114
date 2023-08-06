# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.mau_reader']

package_data = \
{'': ['*'], 'pelican.plugins.mau_reader': ['test_data/*']}

install_requires = \
['mau>=1.4.0', 'pelican>=4.5']

extras_require = \
{'markdown': ['markdown>=3.2']}

setup_kwargs = {
    'name': 'pelican-mau-reader',
    'version': '1.0.1',
    'description': 'Pelican plugin that converts Mau-formatted content into HTML',
    'long_description': '# Mau Reader: A Plugin for Pelican\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/mau-reader/build)](https://github.com/pelican-plugins/mau-reader/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-mau-reader)](https://pypi.org/project/pelican-mau-reader/)\n![License](https://img.shields.io/pypi/l/pelican-mau-reader?color=blue)\n\nMau Reader is a Pelican plugin that converts the [Mau](https://github.com/Project-Mau/mau) format into HTML.\n\n## Requirements\n\nThis plugin requires:\n\n* Python 3.6+\n* Pelican 4.5+\n* Mau 1.3+\n\n## Installation\n\nThis plugin can be installed via the following command, which will also automatically install Mau itself:\n\n    python -m pip install pelican-mau-reader\n\n## Usage\n\nThe plugin automatically manages all Pelican content files ending with the extension: `.mau`\n\nMetadata shall be expressed as Mau variables under the `pelican` namespace. For example:\n\n```\n:pelican.title:Test Mau file with content\n:pelican.date:2021-02-17 13:00:00\n:pelican.modified:2021-02-17 14:00:00\n:pelican.category:test\n:pelican.tags:foo, bar, foobar\n:pelican.summary:I have a lot to test\n```\n\nThe value of a metadata field is a string, just as it is in the standard Markdown format. Please note that Mau variable values include all characters after the colon, spaces included.\n\nAll values in the `config` dictionary are available as variables, so you can specify global values that are valid for all documents.\n\n## Custom templates\n\nYou can override some or all Mau default HTML templates via the `custom_templates` configuration variable. For example, should you want to add a permanent link to all headers you can define:\n\n``` python\nMAU = {\n    "custom_templates": {\n        "header.html": (\n            \'<h{{ level }} id="{{ anchor }}">\'\n            "{{ value }}"\n            \'<a href="#{{ anchor }}" title="Permanent link">¶</a>\'\n            "</h{{ level }}>"\n        )\n    }\n}\n```\n\n… and if you want to limit that to only headers of level 1 and 2 you can use:\n\n``` python\nMAU = {\n    "custom_templates": {\n        "header.html": (\n            \'<h{{ level }} id="{{ anchor }}">\'\n            "{{ value }}"\n            \'{% if level <= 2 %}<a href="#{{ anchor }}" title="Permanent link">¶</a>{% endif %}\'\n            "</h{{ level }}>"\n        )\n    }\n}\n```\n\n## Table of contents and footnotes\n\nThe TOC (Table of Contents) and footnotes are specific to each content file and can be inserted as usual with the Mau commands `::toc:` and `::footnotes:`.\n\n## Custom header anchors\n\nMau provides a simple function to compute IDs for headers, based on the content. The current function is:\n\n``` python\ndef header_anchor(text, level):\n    # Everything lowercase\n    sanitised_text = text.lower()\n\n    # Get only letters, numbers, dashes, and spaces\n    sanitised_text = "".join(re.findall("[a-z0-9- ]+", sanitised_text))\n\n    # Remove multiple spaces\n    sanitised_text = "-".join(sanitised_text.split())\n\n    return sanitised_text\n```\n\nThis provides deterministic header IDs that should suit the majority of cases. Should you need something different, you can provide your own function specifying `mau.header_anchor_function` in the configuration:\n\n``` python\nMAU = {\n    "mau.header_anchor_function": lambda text, level: "XYZ",\n}\n```\n\nThe example above returns the ID `XYZ` for all headers (not recommended as it is not unique). The arguments `text` and `level` are respectively the text of the header itself and an integer representing the level of depth (e.g., `1` for `h1` headers, `2` for `h2` headers, and so on).\n\n## Contributing\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/pelican-plugins/mau-reader/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\n## License\n\nThis project is licensed under the MIT license.\n',
    'author': 'Leonardo Giordani',
    'author_email': 'giordani.leonardo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/mau-reader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
