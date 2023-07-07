"""
The module represents models for simplified mapping database records.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Staff:
    """
    An object representation of a record in the `members` database table.
    """
    tg_id: int
    member_alias: str
    role: str
    phone: Optional[str] = None
    file_id: Optional[str] = None
    created_at: Optional[datetime] = None
