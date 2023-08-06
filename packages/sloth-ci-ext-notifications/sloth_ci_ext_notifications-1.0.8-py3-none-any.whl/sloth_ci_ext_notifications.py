def extend_sloth(cls, extension):
    """Add an SMTP handler to the default logger when the app is created and remove it when the app stops."""

    from logging import WARNING
    from logging.handlers import SMTPHandler


    class Sloth(cls):
        def __init__(self, config):
            '''Add an SMTP handler to the app logger.'''

            super().__init__(config)

            build_email_config = extension['config']

            split_mail_host = build_email_config['mail_host'].split(':')

            if len(split_mail_host) == 2:
                mail_host = (split_mail_host[0], split_mail_host[1])

            else:
                mail_host = split_mail_host[0]

            from_addr = build_email_config.get('from', 'build@sloth.ci')

            to_addrs = build_email_config.get('emails', [])

            smtp_login = build_email_config.get('login')

            if smtp_login:
                credentials = (smtp_login, build_email_config['password'])

            else:
                credentials = None

            secure = build_email_config.get('secure')

            if secure == True:
                secure = ()

            elif secure:
                secure = tuple(secure)

            else:
                secure = None

            self._subjects = {
                'triggered': build_email_config.get('subject_triggered', '{listen_point}: Build Triggered'),
                'completed': build_email_config.get('subject_completed', '{listen_point}: Build Completed'),
                'partially_completed': build_email_config.get('subject_partially_completed', '{listen_point}: Build Partially Completed'),
                'failed': build_email_config.get('subject_failed', '{listen_point}: Build Failed')
            }

            smtp_handler = SMTPHandler(
                mailhost=mail_host,
                fromaddr=from_addr,
                toaddrs=to_addrs,
                subject='Sloth CI: Build Notification',
                credentials=credentials,
                secure=secure
            )

            smtp_handler.getSubject = self._get_email_subject

            smtp_handler.setLevel(build_email_config.get('level', WARNING))

            self.build_logger.addHandler(smtp_handler)

            self.log_handlers[extension['name']] = smtp_handler

        def stop(self):
            '''Remove the SMTP handler when the app stops.'''

            super().stop()
            self.build_logger.removeHandler(self.log_handlers.pop(extension['name']))

        def _get_email_subject(self, record):
            '''Get a subject based on record level and message.'''

            if record.levelname == 'DEBUG':
                return self._subjects['triggered'].format(listen_point=self.listen_point)

            elif record.levelname == 'INFO':
                return self._subjects['completed'].format(listen_point=self.listen_point)

            elif record.levelname == 'WARNING':
                return self._subjects['partially_completed'].format(listen_point=self.listen_point)

            elif record.levelname == 'ERROR':
                return self._subjects['failed'].format(listen_point=self.listen_point)


    return Sloth
