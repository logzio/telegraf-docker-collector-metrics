import os
import subprocess
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class MetricsFetcher:
    def __init__(self):
        self.configured_data = ''
        logger.info('Starting...')

    def save_file(self):
        with open('./telegraf.conf', 'w') as file:
            try:
                file.write(self.configured_data)
            except IOError as exc:
                logger.error(exc)

    def store_array_in_toml(self):
        excluded_images = [ad.strip()
                           for ad in os.environ["EXCLUDED_IMAGES"].split(",")]

        with open('./telegraf.conf') as file:
            try:
                paths_conf = self.configured_data.split("\n")
                paths_conf_done = []
                for path_conf in paths_conf:
                    values = path_conf.split(' = ')
                    if len(values) >= 2 and values[-1].find('EXCLUDED_IMAGES') != -1:
                        arr_excluded_images = []
                        if len(excluded_images) > 0:
                            for ex_image in excluded_images:
                                arr_excluded_images.append('"' +
                                                           ex_image + '"')
                            values[1] = '[' + \
                                ', '.join(arr_excluded_images) + ']'
                        else:
                            values[1] = '[]'
                        path_conf = ' = '.join(values)
                    paths_conf_done.append(path_conf)
                self.configured_data = '\n'.join(paths_conf_done)
            except IOError as exc:
                logger.error(exc)

        self.save_file()

    def default_params(self):
        with open('./telegraf.conf', ) as file:
            try:
                config_data = file.read()
                paths_conf = config_data.split("\n")
                paths_conf_done = []
                for path_conf in paths_conf:
                    values = path_conf.split(' = ')
                    if len(values) >= 2 and values[-1].find('DOCKER_ENDPOINT') != -1:
                        values[1] = '"' + os.getenv(
                            'DOCKER_ENDPOINT', 'unix:///var/run/docker.sock') + '"'
                        path_conf = ' = '.join(values)
                    elif len(values) >= 2 and values[-1].find('TIMEOUT') != -1:
                        values[1] = '"' + os.getenv(
                            'TIMEOUT', '5s') + '"'
                        path_conf = ' = '.join(values)
                    elif len(values) >= 2 and values[-1].find('LOGZIO_LISTENER') != -1:
                        values[1] = '"' + os.getenv(
                            'LOGZIO_LISTENER', 'https://listener.logz.io') + '"'
                        path_conf = ' = '.join(values)
                    elif len(values) >= 2 and values[-1].find('Bearer ${METRICS_TOKEN}') != -1:
                        values[1] = '"Bearer ' + os.getenv(
                            'METRICS_TOKEN', 'no-token') + '"'
                        path_conf = ' = '.join(values)
                    paths_conf_done.append(path_conf)
                self.configured_data = '\n'.join(paths_conf_done)
            except IOError as exc:
                logger.error(exc)

        self.save_file()

    def run(self):
        try:
            subprocess.run(["telegraf", "--config", "./telegraf.conf"])

        except subprocess.CalledProcessError as e:
            logger.error(e)
        except KeyboardInterrupt as e:
            logger.info('Application is stopped')


if __name__ == '__main__':
    w = MetricsFetcher()
    w.default_params()
    if 'EXCLUDED_IMAGES' in os.environ:
        w.store_array_in_toml()
    w.run()
