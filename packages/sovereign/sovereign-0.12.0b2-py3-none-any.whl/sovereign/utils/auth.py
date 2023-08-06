from fastapi import Request
from fastapi.exceptions import HTTPException
from cryptography.fernet import InvalidToken
from sovereign.schemas import DiscoveryRequest


def validate_authentication_string(s: str, r: Request) -> bool:
    try:
        password = r.app.state.CIPHER_SUITE.decrypt(s)
    except Exception:
        r.app.state.STATS.increment("discovery.auth.failed")
        raise

    if password in r.app.state.CONFIG.passwords:
        r.app.state.STATS.increment("discovery.auth.success")
        return True
    r.app.state.STATS.increment("discovery.auth.failed")
    return False


def authenticate(r: Request, request: DiscoveryRequest) -> None:
    if not r.app.state.CONFIG.authentication.enabled:
        return
    if not r.app.state.CIPHER_SUITE.key_available:
        raise RuntimeError(
            "No Fernet key loaded, and auth is enabled. "
            "A fernet key must be provided via SOVEREIGN_ENCRYPTION_KEY. "
            "See https://vsyrakis.bitbucket.io/sovereign/docs/html/guides/encryption.html "
            "for more details"
        )
    try:
        encrypted_auth = request.node.metadata["auth"]
        with r.app.state.STATS.timed("discovery.auth.ms"):
            assert validate_authentication_string(encrypted_auth, r)
    except KeyError:
        raise HTTPException(
            status_code=401,
            detail=f"Discovery request from {request.node.id} is missing auth field",
        )
    except (InvalidToken, AssertionError):
        raise HTTPException(
            status_code=401, detail="The authentication provided was invalid"
        )
    except Exception as e:
        description = getattr(e, "detail", "Unknown")
        raise HTTPException(
            status_code=400,
            detail=f"The authentication provided was malformed [Reason: {description}]",
        )
