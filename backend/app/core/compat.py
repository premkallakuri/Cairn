"""Python version compatibility shims.

Provides ``UTC`` for Python <3.11 environments where
``datetime.UTC`` is not available.
"""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from datetime import UTC
else:
    from datetime import timezone

    UTC = timezone.utc

__all__ = ["UTC"]
