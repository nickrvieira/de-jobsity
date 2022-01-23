from base64 import b64decode


def decode_b64(str_val):
    """This is not meant to be "safe" -  but rather parse the URI
    Ideally, any secret should be sent as an ID for a vault conn or a k8s secret.

    :param str_val: Base64 encoded string
    :type str_val: str
    :return: B64 decoded string (utf-8)
    :rtype: str
    """
    return b64decode(str_val).decode("utf-8")
