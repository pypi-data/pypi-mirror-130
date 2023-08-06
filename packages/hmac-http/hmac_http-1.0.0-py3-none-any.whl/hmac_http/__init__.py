from hmac import digest
from base64 import b64encode
from hashlib import sha256


class BadSignature(Exception):
    pass


class MissingData(Exception):
    pass


class UnknownHashAlgorithm(Exception):
    pass


_known_hash_algorithms = {"hmac-sha256": sha256}


def _generate_headers(headers):
    new_headers = {}

    for header in headers:
        header_data = headers[header]
        header = header.lower()
        new_headers[header] = header_data

    return new_headers


def verify(request, secret):
    headers = request.headers
    headers = _generate_headers(headers)

    if type(secret) == str:
        secret = secret.encode()

    # Get needed data.
    signature = headers["signature"]
    signature_items = {}

    for item in signature.split(","):
        item_split = item.split("=")
        key = item_split[0]
        value = "=".join(item_split[1:]).strip('"')
        signature_items[key] = value

    for key in ["keyId", "signature"]:
        if key not in signature_items:
            raise MissingData(f"Couldn't find key '{key}'.")

    if "headers" not in signature_items:
        signature_headers = ["date"]
    else:
        signature_headers = signature_items["headers"].split(" ")

    # Verify that the specified hash algorithm is known.
    algorithm = signature_items["algorithm"]
    hash_algorithm = _known_hash_algorithms.get(algorithm)

    if hash_algorithm is None:
        raise UnknownHashAlgorithm(f"Unknown hash algorithm '{algorithm}'.")

    # Generate the signature string.
    verification_string = ""

    for header in signature_headers:
        header_data = headers.get(header)

        if header_data is None:
            raise MissingData(f"Couldn't find header '{header}'.")

        verification_string += f"{header}: {header_data}\n"

    verification_string = verification_string.rstrip("\n")

    # Verify the generated signature string.
    hmac_digest = digest(secret, verification_string.encode(), hash_algorithm)
    hmac_digest_base64 = b64encode(hmac_digest).decode()
    recorded_digest_base64 = signature_items["signature"]

    if hmac_digest_base64 != recorded_digest_base64:
        raise BadSignature(
            f"Generated signature '{hmac_digest_base64}' didn't match prerecorded signature '{recorded_digest_base64}' in request."
        )

    return True
