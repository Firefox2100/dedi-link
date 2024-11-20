from dedi_link.model import DDLConfig


class TestDDLConfig:
    def test_init(self):
        config = DDLConfig(
            name='Test instance',
            description='This is a test instance',
            url='https://test-node.example.com',
            allow_non_client_authenticated=True,
            auto_user_registration=True,
            anonymous_access=True,
            default_ttl=5,
            optimal_record_percentage=0.5,
            time_score_weight=0.5,
            ema_factor=0.5,
        )

        assert config.name == 'Test instance'
        assert config.description == 'This is a test instance'
        assert config.url == 'https://test-node.example.com'
        assert config.allow_non_client_authenticated == True
        assert config.auto_user_registration == True
        assert config.anonymous_access == True
        assert config.default_ttl == 5
        assert config.optimal_record_percentage == 0.5
        assert config.time_score_weight == 0.5
        assert config.ema_factor == 0.5
