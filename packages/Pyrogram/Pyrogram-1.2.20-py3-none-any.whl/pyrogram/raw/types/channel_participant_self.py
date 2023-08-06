#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Union, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class ChannelParticipantSelf(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~pyrogram.raw.base.ChannelParticipant`.

    Details:
        - Layer: ``135``
        - ID: ``0x35a8bfa7``

    Parameters:
        user_id: ``int`` ``64-bit``
        inviter_id: ``int`` ``64-bit``
        date: ``int`` ``32-bit``
        via_request (optional): ``bool``
    """

    __slots__: List[str] = ["user_id", "inviter_id", "date", "via_request"]

    ID = 0x35a8bfa7
    QUALNAME = "types.ChannelParticipantSelf"

    def __init__(self, *, user_id: int, inviter_id: int, date: int, via_request: Union[None, bool] = None) -> None:
        self.user_id = user_id  # long
        self.inviter_id = inviter_id  # long
        self.date = date  # int
        self.via_request = via_request  # flags.0?true

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "ChannelParticipantSelf":
        flags = Int.read(data)
        
        via_request = True if flags & (1 << 0) else False
        user_id = Long.read(data)
        
        inviter_id = Long.read(data)
        
        date = Int.read(data)
        
        return ChannelParticipantSelf(user_id=user_id, inviter_id=inviter_id, date=date, via_request=via_request)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.via_request else 0
        data.write(Int(flags))
        
        data.write(Long(self.user_id))
        
        data.write(Long(self.inviter_id))
        
        data.write(Int(self.date))
        
        return data.getvalue()
