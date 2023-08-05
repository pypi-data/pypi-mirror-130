# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['robusta',
 'robusta.api',
 'robusta.cli',
 'robusta.core',
 'robusta.core.discovery',
 'robusta.core.model',
 'robusta.core.persistency',
 'robusta.core.playbooks',
 'robusta.core.playbooks.internal',
 'robusta.core.reporting',
 'robusta.core.schedule',
 'robusta.core.sinks',
 'robusta.core.sinks.datadog',
 'robusta.core.sinks.kafka',
 'robusta.core.sinks.robusta',
 'robusta.core.sinks.robusta.dal',
 'robusta.core.sinks.slack',
 'robusta.integrations',
 'robusta.integrations.argocd',
 'robusta.integrations.git',
 'robusta.integrations.kubernetes',
 'robusta.integrations.kubernetes.autogenerated',
 'robusta.integrations.kubernetes.autogenerated.v1',
 'robusta.integrations.kubernetes.autogenerated.v2beta1',
 'robusta.integrations.kubernetes.autogenerated.v2beta2',
 'robusta.integrations.prometheus',
 'robusta.integrations.resource_analysis',
 'robusta.integrations.scheduled',
 'robusta.integrations.slack',
 'robusta.model',
 'robusta.runner',
 'robusta.utils']

package_data = \
{'': ['*']}

install_requires = \
['click-spinner>=0.1.10,<0.2.0',
 'colorlog>=5.0.1,<6.0.0',
 'dpath>=2.0.5,<3.0.0',
 'hikaru>=0.5.1-beta.0,<0.6.0',
 'kubernetes>=12.0.1,<13.0.0',
 'prometheus-client>=0.12.0,<0.13.0',
 'pydantic>=1.8.1,<2.0.0',
 'pymsteams>=0.1.16,<0.2.0',
 'sphinx-autobuild>=2021.3.14,<2022.0.0',
 'typer>=0.3.2,<0.4.0']

extras_require = \
{'all': ['Flask>=1.1.2,<2.0.0',
         'grafana-api>=1.0.3,<2.0.0',
         'manhole>=1.8.0,<2.0.0',
         'watchdog>=2.1.0,<3.0.0',
         'dulwich>=0.20.23,<0.21.0',
         'better-exceptions>=0.3.3,<0.4.0',
         'CairoSVG>=2.5.2,<3.0.0',
         'tabulate>=0.8.9,<0.9.0',
         'kafka-python>=2.0.2,<3.0.0',
         'prometheus-api-client>=0.4.2,<0.5.0',
         'slack-sdk>=3.7.0,<4.0.0',
         'supabase-py>=0.0.2,<0.0.3',
         'datadog-api-client>=1.2.0,<2.0.0']}

entry_points = \
{'console_scripts': ['robusta = robusta.cli.main:app']}

setup_kwargs = {
    'name': 'robusta-cli',
    'version': '0.8.5',
    'description': '',
    'long_description': None,
    'author': 'Natan Yellin',
    'author_email': 'aantn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
