def extend_sloth(cls, extension):
    '''Add a file handler to the default logger when the app is created and remove it when the app stops.'''

    from os.path import abspath, join, exists
    from os import makedirs

    import logging
    import logging.handlers


    class Sloth(cls):
        def __init__(self, config):
            '''Add a file handler to the app logger.'''

            super().__init__(config)

            log_config = extension['config']

            log_dir = log_config.get('path', '.')
            log_filename = log_config.get('filename', self.listen_point + '.log')

            if not exists(abspath(log_dir)):
                makedirs(abspath(log_dir))

            log_formatter = logging.Formatter(
                log_config.get('format') or '%(asctime)s | %(name)30s | %(levelname)10s | %(message)s'
            )

            if log_config.get('rotating'):
                file_handler = logging.handlers.RotatingFileHandler(
                    abspath(join(log_dir, log_filename)),
                    'a+',
                    maxBytes=log_config.get('max_bytes') or 0,
                    backupCount=log_config.get('backup_count') or 0
                )

            else:
                file_handler = logging.FileHandler(abspath(join(log_dir, log_filename)), 'a+')

            file_handler.setFormatter(log_formatter)

            file_handler.setLevel(log_config.get('level', logging.INFO))

            self.logger.addHandler(file_handler)

            self.log_handlers[extension['name']] = file_handler

        def stop(self):
            '''Remove the file handler when the app stops.'''

            super().stop()
            self.logger.removeHandler(self.log_handlers.pop(extension['name']))


    return Sloth

