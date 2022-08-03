import toml
import os
import subprocess
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

BASED_DATA = {
    "outputs": {
        "http": [
            {
                "url": "",
                "data_format": "prometheusremotewrite",
                "headers": {
                    "Content-Type": "application/x-protobuf",
                    "Content-Encoding": "snappy",
                    "X-Prometheus-Remote-Write-Version": "0.1.0",
                    "Authorization": ""
                }
            }
        ]
    },
    "inputs": {
        "docker": [
            {
                "endpoint": "",
                "gather_services": False,
                "container_names": [],
                "source_tag": True,
                "container_name_include": [],
                "container_name_exclude": [],
                "timeout": "",
                "perdevice": True,
                "total": False,
                "docker_label_include": [],
                "docker_label_exclude": []
            }
        ]
    }
}

ENV_GLOBAL_TAGS = "GLOBAL_TAGS"


class MetricsFetcher:
    def __init__(self):
        self.configured_data = ''
        logger.info('Starting...')

    def set_params(self):
        config_data = BASED_DATA

        if "EXCLUDED_IMAGES" in os.environ:
            excluded_images = [ad.strip()
                               for ad in os.environ["EXCLUDED_IMAGES"].split(",")]

            if len(excluded_images) > 0:
                config_data['inputs']['docker'][0]['container_name_exclude'] = excluded_images

        config_data['outputs']['http'][0]['url'] = os.getenv(
            'LOGZIO_LISTENER', 'https://listener.logz.io:8053')

        config_data['outputs']['http'][0]['headers']["Authorization"] = "Bearer " + os.getenv(
            'METRICS_TOKEN', 'no-default')

        config_data['inputs']['docker'][0]['endpoint'] = os.getenv(
            'DOCKER_ENDPOINT', 'unix:///var/run/docker.sock')
        config_data['inputs']['docker'][0]['timeout'] = os.getenv(
            'TIMEOUT', '5s')

        if ENV_GLOBAL_TAGS in os.environ:
            logger.debug('Trying to add global tags to metrics')
            try:
                tags = [t.strip() for t in os.environ[ENV_GLOBAL_TAGS].split(',')]
                config_data['global_tags'] = {}
                tag_key_index = 0
                tag_value_index = 0
                for tagStr in tags:
                    tag = [ts.strip() for ts in tagStr.split('=')]
                    config_data['global_tags'][tag[tag_key_index]] = tag[tag_value_index]
                logger.info('Added global tags')
            except Exception as e:
                logger.warning(f'Could not add global tags. Ignoring. Received exception: {e}')

        with open('./telegraf.conf', 'w') as file:
            try:
                toml.dump(config_data, file)
            except Exception as e:
                logger.info(e)

    def run(self):
        try:
            subprocess.run(["telegraf", "--config", "./telegraf.conf"])

        except subprocess.CalledProcessError as e:
            logger.error(e)
        except KeyboardInterrupt as e:
            logger.info('Application is stopped')
        except Exception as e:
            logger.info(e)


if __name__ == '__main__':
    w = MetricsFetcher()
    w.set_params()
    w.run()
