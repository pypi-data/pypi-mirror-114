from mlp_tracking import MlpTracker, PipeType, IssueModule
from .config import client_config
from .logger import log

log.info(
    "connect kafka "
    + client_config.kafka_host
)
predict_tracker = MlpTracker(
    pipe_type=PipeType.FAQ_PREDIC_PIPE.value,
    issue_module=IssueModule.BM.value,
    kafka_servers=client_config.kafka_host,
    kafka_username=client_config.kafka_username,
    kafka_password=client_config.kafka_password,
)

train_tracker = MlpTracker(
    pipe_type=PipeType.FAQ_TRAIN_PIPE.value,
    issue_module=IssueModule.BM.value,
    kafka_servers=client_config.kafka_host,
    kafka_username=client_config.kafka_username,
    kafka_password=client_config.kafka_password,
)
