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


class SearchResultsCalendar(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~pyrogram.raw.base.messages.SearchResultsCalendar`.

    Details:
        - Layer: ``135``
        - ID: ``0x147ee23c``

    Parameters:
        count: ``int`` ``32-bit``
        min_date: ``int`` ``32-bit``
        min_msg_id: ``int`` ``32-bit``
        periods: List of :obj:`SearchResultsCalendarPeriod <pyrogram.raw.base.SearchResultsCalendarPeriod>`
        messages: List of :obj:`Message <pyrogram.raw.base.Message>`
        chats: List of :obj:`Chat <pyrogram.raw.base.Chat>`
        users: List of :obj:`User <pyrogram.raw.base.User>`
        inexact (optional): ``bool``
        offset_id_offset (optional): ``int`` ``32-bit``

    See Also:
        This object can be returned by 1 method:

        .. hlist::
            :columns: 2

            - :obj:`messages.GetSearchResultsCalendar <pyrogram.raw.functions.messages.GetSearchResultsCalendar>`
    """

    __slots__: List[str] = ["count", "min_date", "min_msg_id", "periods", "messages", "chats", "users", "inexact", "offset_id_offset"]

    ID = 0x147ee23c
    QUALNAME = "types.messages.SearchResultsCalendar"

    def __init__(self, *, count: int, min_date: int, min_msg_id: int, periods: List["raw.base.SearchResultsCalendarPeriod"], messages: List["raw.base.Message"], chats: List["raw.base.Chat"], users: List["raw.base.User"], inexact: Union[None, bool] = None, offset_id_offset: Union[None, int] = None) -> None:
        self.count = count  # int
        self.min_date = min_date  # int
        self.min_msg_id = min_msg_id  # int
        self.periods = periods  # Vector<SearchResultsCalendarPeriod>
        self.messages = messages  # Vector<Message>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.inexact = inexact  # flags.0?true
        self.offset_id_offset = offset_id_offset  # flags.1?int

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "SearchResultsCalendar":
        flags = Int.read(data)
        
        inexact = True if flags & (1 << 0) else False
        count = Int.read(data)
        
        min_date = Int.read(data)
        
        min_msg_id = Int.read(data)
        
        offset_id_offset = Int.read(data) if flags & (1 << 1) else None
        periods = TLObject.read(data)
        
        messages = TLObject.read(data)
        
        chats = TLObject.read(data)
        
        users = TLObject.read(data)
        
        return SearchResultsCalendar(count=count, min_date=min_date, min_msg_id=min_msg_id, periods=periods, messages=messages, chats=chats, users=users, inexact=inexact, offset_id_offset=offset_id_offset)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.inexact else 0
        flags |= (1 << 1) if self.offset_id_offset is not None else 0
        data.write(Int(flags))
        
        data.write(Int(self.count))
        
        data.write(Int(self.min_date))
        
        data.write(Int(self.min_msg_id))
        
        if self.offset_id_offset is not None:
            data.write(Int(self.offset_id_offset))
        
        data.write(Vector(self.periods))
        
        data.write(Vector(self.messages))
        
        data.write(Vector(self.chats))
        
        data.write(Vector(self.users))
        
        return data.getvalue()
