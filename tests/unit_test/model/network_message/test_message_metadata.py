import time
from uuid import uuid4, UUID
from pydantic import ValidationError
import pytest

from dedi_link.model.network_message.message_metadata import MessageMetadata


class TestMessageMetadata:
    def test_init(self):
        network_id = uuid4()
        node_id = uuid4()
        message_id = uuid4()
        current_time = time.time()

        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
            messageId=message_id,
            timestamp=current_time,
        )

        assert metadata.network_id == network_id
        assert metadata.node_id == node_id
        assert metadata.message_id == message_id
        assert metadata.timestamp == current_time

        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
        )

        assert metadata.network_id == network_id
        assert metadata.node_id == node_id
        assert isinstance(metadata.message_id, UUID)
        assert isinstance(metadata.timestamp, float)
        assert metadata.timestamp >= current_time

    def test_model_validate(self):
        network_id = uuid4()
        node_id = uuid4()
        message_id = uuid4()
        current_time = time.time()

        metadata_dict = {
            'networkId': str(network_id),
            'nodeId': str(node_id),
            'messageId': str(message_id),
            'timestamp': current_time,
        }

        metadata = MessageMetadata.model_validate(metadata_dict)

        assert metadata.network_id == network_id
        assert metadata.node_id == node_id
        assert metadata.message_id == message_id
        assert metadata.timestamp == current_time

    def test_model_validate_invalid_uuid(self):
        metadata_dict = {
            'networkId': 'invalid-uuid',
            'nodeId': str(uuid4()),
        }

        with pytest.raises(ValidationError):
            MessageMetadata.model_validate(metadata_dict)

    def test_model_validate_missing_fields(self):
        metadata_dict = {
            'networkId': str(uuid4()),
        }

        with pytest.raises(ValidationError):
            MessageMetadata.model_validate(metadata_dict)

    def test_model_dump(self):
        network_id = uuid4()
        node_id = uuid4()
        message_id = uuid4()
        current_time = time.time()

        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
            messageId=message_id,
            timestamp=current_time,
        )

        metadata_dict = metadata.model_dump(by_alias=True)

        assert metadata_dict['networkId'] == str(network_id)
        assert metadata_dict['nodeId'] == str(node_id)
        assert metadata_dict['messageId'] == str(message_id)
        assert metadata_dict['timestamp'] == current_time

    def test_model_dump_json(self):
        network_id = uuid4()
        node_id = uuid4()
        message_id = uuid4()
        current_time = time.time()

        metadata = MessageMetadata(
            networkId=network_id,
            nodeId=node_id,
            messageId=message_id,
            timestamp=current_time,
        )

        metadata_json = metadata.model_dump_json(by_alias=True)

        expected_json = (
            f'{{"networkId":"{network_id}","nodeId":"{node_id}",'
            f'"messageId":"{message_id}","timestamp":{current_time}}}'
        )

        assert metadata_json == expected_json
