# -*- coding: utf-8 -*-
#
#   SHM: Shared Memory
#
#                                Written in 2021 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2021 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

from abc import ABC, abstractmethod
from typing import Generic, Union

from .buffer import M
from .buffer import int_from_buffer, int_to_buffer
from .buffer import CycledBuffer


class CycledCache(CycledBuffer, Generic[M], ABC):
    """
        Cycled Data Cache
        ~~~~~~~~~~~~~~~~~

        Header:
            magic code             - 14 bytes
            offset of read offset  - 1 byte  # the highest bit is for alternate
            offset of write offset - 1 byte  # the highest bit is for alternate
            read offset            - 2/4/8 bytes
            alternate read offset  - 2/4/8 bytes
            write offset           - 2/4/8 bytes
            alternate write offset - 2/4/8 bytes
        Body:
            data item(s)           - data size (4 bytes) + data (variable length)
    """

    def __init__(self, shm: M, head_length: int = 4):
        super().__init__(shm=shm)
        self.__head_length = head_length

    @abstractmethod
    def detach(self):
        """ Detaches the shared memory """
        raise NotImplemented

    @abstractmethod
    def remove(self):
        """ Removes (deletes) the shared memory from the system """
        raise NotImplemented

    @property
    def buffer(self) -> bytes:
        """ Gets the whole buffer """
        raise NotImplemented

    def _buffer_to_string(self) -> str:
        buffer = self.buffer
        size = len(buffer)
        if size < 128:
            return str(buffer)
        else:
            return str(buffer[:125]) + '...'

    def __str__(self) -> str:
        mod = self.__module__
        cname = self.__class__.__name__
        buffer = self._buffer_to_string()
        return '<%s size=%d capacity=%d available=%d>\n%s\n</%s module="%s">'\
               % (cname, self.size, self.capacity, self.available, buffer, cname, mod)

    def __repr__(self) -> str:
        mod = self.__module__
        cname = self.__class__.__name__
        buffer = self._buffer_to_string()
        return '<%s size=%d capacity=%d available=%d>\n%s\n</%s module="%s">'\
               % (cname, self.size, self.capacity, self.available, buffer, cname, mod)

    # Override
    def _try_read(self, length: int) -> (Union[bytes, bytearray, None], int):
        try:
            return super()._try_read(length=length)
        except AssertionError as error:
            self._check_error(error=error)
            raise error

    def shift(self) -> Union[bytes, bytearray, None]:
        """ shift one data, measured with size (as leading 4 bytes) """
        # get data head as size
        head_size = self.__head_length
        head, _ = self._try_read(length=head_size)
        if head is None:
            return None
        body_size = int_from_buffer(buffer=head)
        item_size = head_size + body_size
        available = self.available
        if available < item_size:
            # data error
            self.read(length=available)  # clear buffer
            raise BufferError('buffer error: %d < %d + %d' % (available, head_size, body_size))
        # get data body with size
        item = self.read(length=item_size)
        if item is None:
            raise BufferError('failed to read item: %d' % item_size)
        return item[head_size:]

    def append(self, data: Union[bytes, bytearray]) -> bool:
        """ append data with size (as leading 4 bytes) into buffer """
        head_size = self.__head_length
        body_size = len(data)
        item_size = head_size + body_size
        if self.spaces < item_size:
            # not enough spaces
            return False
        head = int_to_buffer(value=body_size, length=head_size)
        if isinstance(data, bytearray):
            item = bytearray(head) + data
        else:
            item = bytearray(head + data)
        return self.write(data=item)
