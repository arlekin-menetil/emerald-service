from rest_framework.throttling import AnonRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    """
    Ограничивает количество попыток получения JWT
    с одного IP-адреса.
    """

    scope = "login"
    rate = "5/10m"

    def parse_rate(self, rate):
        if rate is None:
            return None, None

        num_requests, period = rate.split("/", 1)
        num_requests = int(num_requests)

        if len(period) == 1:
            duration = {
                "s": 1,
                "m": 60,
                "h": 3600,
                "d": 86400,
            }[period]

            return num_requests, duration

        unit = period[-1]
        amount = int(period[:-1])

        duration_multipliers = {
            "s": 1,
            "m": 60,
            "h": 3600,
            "d": 86400,
        }

        if unit not in duration_multipliers:
            raise ValueError(f"Неподдерживаемая единица времени: {unit}")

        duration = amount * duration_multipliers[unit]

        return num_requests, duration
