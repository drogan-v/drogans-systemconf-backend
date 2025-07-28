import hashlib
import hmac
from urllib.parse import parse_qs


def init_data_is_valid(init_data: str, bot_token: str) -> bool:
    parsed_data = parse_qs(init_data, keep_blank_values=True)
    if "hash" not in parsed_data:
        return False

    received_hash = parsed_data["hash"][0]
    del parsed_data["hash"]
    sorted_keys = sorted(parsed_data.keys())
    data_check_string = "\n".join(
        ["=".join([key, parsed_data[key][0]]) for key in sorted_keys]
    )
    secret_key = hmac.new(
        key=b"WebAppData", msg=bot_token.encode(), digestmod=hashlib.sha256
    ).digest()
    computed_hash = hmac.new(
        secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed_hash, received_hash)
