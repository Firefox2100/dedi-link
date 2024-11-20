class DDLConfig:
    def __init__(self,
                 name: str,
                 description: str,
                 url: str,
                 allow_non_client_authenticated: bool,
                 auto_user_registration: bool,
                 anonymous_access: bool,
                 default_ttl: int,
                 optimal_record_percentage: float,
                 time_score_weight: float,
                 ema_factor: float,
                 ):
        self.name = name
        self.description = description
        self.url = url
        self.allow_non_client_authenticated = allow_non_client_authenticated
        self.auto_user_registration = auto_user_registration
        self.anonymous_access = anonymous_access
        self.default_ttl = default_ttl
        self.optimal_record_percentage = optimal_record_percentage
        self.time_score_weight = time_score_weight
        self.ema_factor = ema_factor
