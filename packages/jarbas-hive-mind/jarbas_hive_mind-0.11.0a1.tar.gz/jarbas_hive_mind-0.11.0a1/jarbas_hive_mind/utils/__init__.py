import logging
from jarbas_hive_mind.utils.cert import create_self_signed_cert
import json
from jarbas_hive_mind.settings import LOG_BLACKLIST, DATA_PATH
from jarbas_hive_mind.exceptions import DecryptionKeyError, EncryptionKeyError
from ovos_utils.log import LOG
from ovos_utils.security import encrypt, decrypt
from binascii import hexlify, unhexlify

# TODO ovos_utils for all of these
# this used to be a method here, keep here for now in case something is
# importing it, TODO deprecate
from ovos_utils import get_ip


def validate_param(value, name):
    if not value:
        raise ValueError("Missing or empty %s in conf " % name)


def create_echo_function(name, whitelist=None):
    """ Standard logging mechanism for Mycroft processes.

    This handles the setup of the basic logging for all Mycroft
    messagebus-based processes.

    Args:
        name (str): Reference name of the process
        whitelist (list, optional): List of "type" strings.  If defined, only
                                    messages in this list will be logged.

    Returns:
        func: The echo function
    """
    blacklist = LOG_BLACKLIST

    def echo(message):
        global _log_all_bus_messages
        try:
            msg = json.loads(message)

            if whitelist and msg.get("type") not in whitelist:
                return

            if blacklist and msg.get("type") in blacklist:
                return

            if msg.get("type") == "mycroft.debug.log":
                # Respond to requests to adjust the logger settings
                lvl = msg["data"].get("level", "").upper()
                if lvl in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
                    LOG.level = lvl
                    LOG(name).info("Changing log level to: {}".format(lvl))
                    try:
                        logging.getLogger('urllib3').setLevel(lvl)
                    except Exception:
                        pass  # We don't really care about if this fails...

                # Allow enable/disable of messagebus traffic
                log_bus = msg["data"].get("bus", None)
                if log_bus is not None:
                    LOG(name).info("Bus logging: " + str(log_bus))
                    _log_all_bus_messages = log_bus
            elif msg.get("type") == "registration":
                # do not log tokens from registration messages
                msg["data"]["token"] = None
                message = json.dumps(msg)
        except Exception:
            pass

        if _log_all_bus_messages:
            # Listen for messages and echo them for logging
            LOG(name).debug(message)

    return echo


def serialize_message(message):
    # convert a Message object into raw data that can be sent over
    # websocket
    if hasattr(message, 'serialize'):
        return message.serialize()
    elif isinstance(message, dict):
        message = {k: v if not hasattr(v, 'serialize') else serialize_message(v)
                   for k, v in message.items()}
        return json.dumps(message)
    else:
        return json.dumps(message.__dict__)


def encrypt_as_json(key, data, nonce=None):
    if isinstance(data, dict):
        data = json.dumps(data)
    if len(key) > 16:
        key = key[0:16]
    try:
        ciphertext, tag, nonce = encrypt(key, data, nonce=nonce)
    except:
        raise EncryptionKeyError
    return json.dumps({"ciphertext": hexlify(ciphertext).decode('utf-8'),
            "tag": hexlify(tag).decode('utf-8'),
            "nonce": hexlify(nonce).decode('utf-8')})


def decrypt_from_json(key, data):
    if isinstance(data, str):
        data = json.loads(data)
    if len(key) > 16:
        key = key[0:16]
    ciphertext = unhexlify(data["ciphertext"])
    if data.get("tag") is None:  # web crypto
        ciphertext, tag = ciphertext[:-16], ciphertext[-16:]
    else:
        tag = unhexlify(data["tag"])
    nonce = unhexlify(data["nonce"])
    try:
        return decrypt(key, ciphertext, tag, nonce)
    except ValueError:
        raise DecryptionKeyError


def wscode2error(error_code):
    # Source: https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent#Status_codes
    codes = {
        1000: 'Normal Closure',
        1001: 'Going Away',
        1002: 'Protocol Error',
        1003: 'Unsupported Data',
        1004: '(For future)',
        1005: 'No Status Received',
        1006: 'Abnormal Closure',
        1007: 'Invalid frame payload data',
        1008: 'Policy Violation',
        1009: 'Message too big',
        1010: 'Missing Extension',
        1011: 'Internal Error',
        1012: 'Service Restart',
        1013: 'Try Again Later',
        1014: 'Bad Gateway',
        1015: 'TLS Handshake'
    }
    error_code = int(error_code)
    if error_code in codes:
        return codes[error_code]
    elif error_code <= 999:
        return '(Unused)'
    elif error_code <= 1999:
        return '(For WebSocket standard)'
    elif error_code <= 2999:
        return '(For WebSocket extensions)'
    elif error_code <= 3999:
        return '(For libraries and frameworks)'
    elif error_code <= 4999:
        return '(For applications)'
    return '(Unknown)'
