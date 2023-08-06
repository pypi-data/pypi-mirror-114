# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sloth_ci_ext_notifications']
install_requires = \
['sloth-ci>=2.2,<3.0']

setup_kwargs = {
    'name': 'sloth-ci-ext-notifications',
    'version': '1.0.8',
    'description': 'Email notifications for Sloth CI builds',
    'long_description': '# Email Notifications for Sloth CI Builds\n\nSend email notifications when builds complete or fail.\n\nExecuting actions of an app is called *build*. A build is considered *completed* if all its actions were completed. If some actions were completed and some failed, it\'s a *partially completed*; if all actions fail, the build *failed*.\n\nThis extension sends you emails via SMTP when your builds complete (fully or partially) or fail; just pick the desired notification level, list the recipient emails, and enter your SMTP credentials. Optionally, you can set the subject for each notification level.\n\n\n## Installation\n\n    $ pip install sloth-ci-ext-notifications\n\n\n## Usage\n\n    extensions:\n        notifications:\n            # Use the module sloth_ci_ext_notifications.\n            module: notifications\n\n            # Emails to send the notifications to.\n            emails:\n                - foo@bar.com\n                - admin@example.com\n\n            # Log level (number or valid Python logging level name).\n            # ERROR includes only build fails, WARNING adds partial completions,\n            # INFO adds completion, and DEBUG adds trigger notifications.\n            # Default is WARNING.\n            level: INFO\n\n            # The "from" address in the emails. Default is "build@sloth.ci."\n            from: notify@example.com\n\n            # The email subject on build trigger. You can use the {listen_point} placeholder.\n            # Default is "{listen_point}: Build Triggered."\n            subject_triggered: \'Triggered build on {listen_point}!\'\n\n            # The email subject on build completion.You can use the {listen_point} placeholder.\n            # Default is "{listen_point}: Build Completed."\n            subject_completed: \'Hooray! {listen_point} works!\'\n\n            # The email subject on build partial completion. You can use the {listen_point} placeholder.\n            # Default is "{listen_point}: Build Partially Completed."\n            subject_partially_completed: \'Better than nothing on {listen_point}\'\n\n            # The email subject on build fail. You can use the {listen_point} placeholder.\n            # Default is "{listen_point}: Build Failed."\n            subject_failed: \'Fail on {listen_point}\'\n\n            # SMTP settings.\n            # SMTP mail host and (if not default) port.\n            # Mandatory parameter.\n            mailhost: \'smtp-mail.outlook.com:25\'\n\n            # SMTP login.\n            login: foo@bar.baz\n\n            # SMTP password.\n            password: bar\n\n            # If the SMTP server requires TLS, set this to true. Default is false.\n            # If necessary, you can provide a keyfile name or a keyfile and a certificate file names.\n            # This param is used only if the login and password params are supplied.\n            secure: true\n            # secure:\n            #    -   keyfile\n            #    -   cerfile\n\n',
    'author': 'Constantine Molchanov',
    'author_email': 'moigagoo@live.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
