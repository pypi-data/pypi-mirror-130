from typing import Sequence, Optional, Callable, Any


def sftp_upload(
    files: Sequence[str],
    host: str,
    username: str,
    destination_dir: str,
    envelope_dir: Optional[str] = None,
    pkey: Optional[str] = None,
    pkey_password: Optional[str] = None,
    progress: Optional[Callable[[float], Any]] = None,
    buf_size: Optional[int] = None,
    two_factor_callback: Optional[Callable[[], str]] = None,
) -> None:
    ...
