import pytest
import requests
from unittest.mock import MagicMock, patch, PropertyMock

from dedi_link.etc.exceptions import NetworkRequestFailed
from dedi_link.model.network_interface import Session


@pytest.fixture
def mock_session():
    with patch('dedi_link.model.network_interface.session.requests.Session') as mock_session:
        yield mock_session


class TestSession:
    def test_init(self):
        session = Session()

        assert isinstance(session._session, requests.Session)

    def test_context_manager(self):
        with Session() as session:
            assert isinstance(session, Session)

            assert isinstance(session._session, requests.Session)

    def test_get(self,
                 mock_session,
                 ):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'key': 'value'}

        mock_session.return_value.get.return_value = mock_response
        session = Session()
        response = session.get('https://example.com')

        assert response == {'key': 'value'}

    def test_get_error_code(self,
                            mock_session,
                            ):
        mock_response = MagicMock()
        mock_response.status_code = 404

        mock_session.return_value.get.return_value = mock_response
        session = Session()

        with pytest.raises(NetworkRequestFailed):
            session.get('https://example.com')

    def test_post(self,
                  mock_session,
                  mock_auth_request_invite_1,
                  mock_auth_request_invite_dict_1,
                  mock_auth_response_1,
                  mock_auth_response_dict_1,
                  mock_network_message_header_1,
                  mock_network_message_header_dict_1,
                  ):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_auth_response_dict_1
        mock_response.headers = mock_network_message_header_dict_1

        mock_session.return_value.post.return_value = mock_response

        with patch(
                'dedi_link.model.network_message.network_message.SyncNetworkMessageInterface.generate_headers',
        ) as mock_generate_headers:
            mock_generate_headers.return_value.headers = mock_network_message_header_1

            session = Session()
            response = session.post(
                url='https://example.com',
                message=mock_auth_request_invite_1,
                access_token='access_token',
            )

            assert response[0] == mock_auth_response_1
            assert response[1] == mock_network_message_header_1

            assert mock_session.return_value.post.called_once_with(
                'https://example.com',
                json=mock_auth_request_invite_dict_1,
                headers=mock_network_message_header_dict_1,
            )

    def test_post_error_code(self,
                             mock_session,
                             mock_auth_request_invite_1,
                             mock_network_message_header_1,
                             ):
        mock_response = MagicMock()
        mock_response.status_code = 404

        mock_session.return_value.post.return_value = mock_response

        with patch(
                'dedi_link.model.network_message.network_message.SyncNetworkMessageInterface.generate_headers',
        ) as mock_generate_headers:
            mock_generate_headers.return_value.headers = mock_network_message_header_1

            session = Session()

            with pytest.raises(NetworkRequestFailed):
                session.post(
                    url='https://example.com',
                    message=mock_auth_request_invite_1,
                    access_token='access_token',
                )

    def test_post_non_json_response(self,
                                    mock_session,
                                    mock_auth_request_invite_1,
                                    mock_auth_response_1,
                                    mock_network_message_header_1,
                                    ):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers.get.return_value = 'text/plain'

        mock_session.return_value.post.return_value = mock_response

        with patch(
                'dedi_link.model.network_message.network_message.SyncNetworkMessageInterface.generate_headers',
        ) as mock_generate_headers:
            mock_generate_headers.return_value.headers = mock_network_message_header_1

            session = Session()

            response, response_header = session.post(
                url='https://example.com',
                message=mock_auth_request_invite_1,
                access_token='access_token',
            )

            assert response is None
            assert response_header is None
