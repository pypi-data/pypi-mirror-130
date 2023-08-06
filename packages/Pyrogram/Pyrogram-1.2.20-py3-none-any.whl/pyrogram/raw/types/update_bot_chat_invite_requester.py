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


class UpdateBotChatInviteRequester(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``135``
        - ID: ``0x11dfa986``

    Parameters:
        peer: :obj:`Peer <pyrogram.raw.base.Peer>`
        date: ``int`` ``32-bit``
        user_id: ``int`` ``64-bit``
        about: ``str``
        invite: :obj:`ExportedChatInvite <pyrogram.raw.base.ExportedChatInvite>`
        qts: ``int`` ``32-bit``
    """

    __slots__: List[str] = ["peer", "date", "user_id", "about", "invite", "qts"]

    ID = 0x11dfa986
    QUALNAME = "types.UpdateBotChatInviteRequester"

    def __init__(self, *, peer: "raw.base.Peer", date: int, user_id: int, about: str, invite: "raw.base.ExportedChatInvite", qts: int) -> None:
        self.peer = peer  # Peer
        self.date = date  # int
        self.user_id = user_id  # long
        self.about = about  # string
        self.invite = invite  # ExportedChatInvite
        self.qts = qts  # int

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "UpdateBotChatInviteRequester":
        # No flags
        
        peer = TLObject.read(data)
        
        date = Int.read(data)
        
        user_id = Long.read(data)
        
        about = String.read(data)
        
        invite = TLObject.read(data)
        
        qts = Int.read(data)
        
        return UpdateBotChatInviteRequester(peer=peer, date=date, user_id=user_id, about=about, invite=invite, qts=qts)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        # No flags
        
        data.write(self.peer.write())
        
        data.write(Int(self.date))
        
        data.write(Long(self.user_id))
        
        data.write(String(self.about))
        
        data.write(self.invite.write())
        
        data.write(Int(self.qts))
        
        return data.getvalue()
