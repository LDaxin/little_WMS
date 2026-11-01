"""Open Location Code (Plus Code) encoding and decoding.

Minimal implementation of the Open Location Code algorithm
(https://github.com/google/open-location-code). Only full codes are supported
(no short codes / reference locations).
"""

ALPHABET = "23456789CFGHJMPQRVWX"
SEPARATOR = "+"
PADDING = "0"
LATITUDE_MAX = 90
LONGITUDE_MAX = 180
PAIR_CODE_LENGTH = 10
PAIR_RESOLUTIONS = [20.0, 1.0, 0.05, 0.0025, 0.000125]


def encode(latitude, longitude, code_length=PAIR_CODE_LENGTH):
    """Return the full Plus Code for a coordinate."""
    if not -LATITUDE_MAX <= latitude <= LATITUDE_MAX:
        raise ValueError("Latitude must be between -90 and 90")
    if not -LONGITUDE_MAX <= longitude <= LONGITUDE_MAX:
        raise ValueError("Longitude must be between -180 and 180")
    if code_length < 2 or code_length % 2 != 0:
        raise ValueError("Code length must be even and at least 2")

    # Clamp to the valid range (the poles / antimeridian are edge cases).
    latitude = min(max(latitude, -LATITUDE_MAX), LATITUDE_MAX - 1e-9)
    longitude = min(max(longitude, -LONGITUDE_MAX), LONGITUDE_MAX - 1e-9)

    lat = latitude + LATITUDE_MAX
    lng = longitude + LONGITUDE_MAX

    code = []
    for i in range(code_length // 2):
        resolution = PAIR_RESOLUTIONS[i]
        lat_digit = int(lat / resolution)
        lng_digit = int(lng / resolution)
        code.append(ALPHABET[lat_digit])
        code.append(ALPHABET[lng_digit])
        lat -= lat_digit * resolution
        lng -= lng_digit * resolution

    code.insert(8, SEPARATOR)
    return "".join(code)


def decode(code):
    """Return (latitude, longitude) for a full Plus Code (cell centre)."""
    code = code.strip().upper().replace(" ", "")
    if SEPARATOR in code:
        code = code.replace(SEPARATOR, "")
    if len(code) < 2:
        raise ValueError("Plus Code is too short")
    if len(code) % 2 != 0:
        code += PADDING

    lat = -LATITUDE_MAX
    lng = -LONGITUDE_MAX
    resolution = PAIR_RESOLUTIONS[0]
    for i in range(0, len(code), 2):
        pair_index = i // 2
        if pair_index >= len(PAIR_RESOLUTIONS):
            break
        resolution = PAIR_RESOLUTIONS[pair_index]
        lat += ALPHABET.index(code[i]) * resolution
        lng += ALPHABET.index(code[i + 1]) * resolution

    # Return the centre of the decoded cell.
    return lat + resolution / 2, lng + resolution / 2
