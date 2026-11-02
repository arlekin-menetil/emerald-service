from decimal import Decimal, InvalidOperation

from .translations import t


def normalize_coordinate(value):
    if value is None:
        return None

    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


def is_valid_location(latitude, longitude):
    latitude = normalize_coordinate(latitude)
    longitude = normalize_coordinate(longitude)

    if latitude is None or longitude is None:
        return False

    return (
        Decimal("-90") <= latitude <= Decimal("90")
        and Decimal("-180") <= longitude <= Decimal("180")
    )


def format_location_coordinates(latitude, longitude, client=None):
    latitude = normalize_coordinate(latitude)
    longitude = normalize_coordinate(longitude)

    if latitude is None or longitude is None:
        return t(client, "coordinates_not_specified")

    return f"{latitude:.6f}, {longitude:.6f}"


def get_google_maps_url(latitude, longitude):
    if not is_valid_location(latitude, longitude):
        return None

    latitude = normalize_coordinate(latitude)
    longitude = normalize_coordinate(longitude)

    return (
        f"https://www.google.com/maps/search/"
        f"?api=1&query={latitude},{longitude}"
    )


def get_yandex_maps_url(latitude, longitude):
    if not is_valid_location(latitude, longitude):
        return None

    latitude = normalize_coordinate(latitude)
    longitude = normalize_coordinate(longitude)

    return f"https://yandex.com/maps/?pt={longitude},{latitude}"