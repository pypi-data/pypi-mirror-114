from transformer.result import ResultProducerConfig
from transformer.library import logger, aws_service
from transformer.library.kafka_service import send_messages

log = logger.set_logger(__name__)


class AbstractResult:
    arguments: dict

    def __init__(self, config: ResultProducerConfig):
        self.arguments = config.arguments

    def run(self, data: dict): pass


class S3Result(AbstractResult):
    def __init__(self, config: ResultProducerConfig):
        super().__init__(config)

    def run(self, data: dict):
        aws_service.upload_s3_with_bytes(
            bucket=self.arguments['bucket'],
            s3_key=self.arguments['key'],
            bytes=data
        )


class MSKScramResult(AbstractResult):
    def __init__(self, config: ResultProducerConfig):
        super().__init__(config)

    def run(self, data: list):
        send_messages(
            data=data,
            cluster_name=self.arguments['clusterName'],
            topic=self.arguments['topic'],
            secret_name=self.arguments['secretName'],
            batch_size=self.arguments['batchSize']
        )


class ConsoleResult(AbstractResult):
    def __init__(self, config: ResultProducerConfig):
        super().__init__(config)

    def run(self, data):
        print("--- Printing Data in Console ---")
        if isinstance(data, list):
            for d in data:
                print(d)
        else:
            print(data)
        print("--- Print Completed ---")