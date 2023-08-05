from .capi import HS, HsApi, HsExprExt, HsMode, HsFlag, HsPlatformInfo, ManagedPtr, hs_database, hs_scratch, HyperscanError
from typing import Optional, Sequence, ByteString, TypeVar, Callable, List, Generator
import contextlib


class ScratchPool:
    def __init__(self, hs: HsApi = HS):
        self._hs = hs
        self._pool: List[ManagedPtr[hs_scratch]] = []

    def _take_or_create_scratch(self, db: ManagedPtr[hs_database]) -> ManagedPtr[hs_scratch]:
        try:
            s = self._pool.pop()
        except IndexError:
            s = None
        s = self._hs.alloc_scratch(db, s)
        return s

    def _return_scratch(self, scratch: ManagedPtr[hs_scratch]) -> None:
        self._pool.append(scratch)

    @contextlib.contextmanager
    def scratch(self, db: ManagedPtr[hs_database]) -> Generator[ManagedPtr[hs_scratch], None, None]:
        s = self._take_or_create_scratch(db)
        try:
            yield s
        finally:
            self._return_scratch(s)


T = TypeVar('T')
class Database:
    def __init__(
            self,
            expressions: Sequence[ByteString],
            ids: Optional[Sequence[int]] = None,
            flags: Optional[Sequence[HsFlag]] = None,
            ext: Optional[Sequence[HsExprExt]] = None,
            mode: HsMode = HsMode.BLOCK,
            hs: HsApi = HS,
    ) -> None:
        self._hs = hs
        self._sp = ScratchPool(hs)

        if ids is None:
            ids = [0] * len(expressions)
        if flags is None:
            flags = [HsFlag(0)] * len(expressions)
        if ext is None:
            ext = [None] * len(expressions)
        self._db = self._hs.compile_ext_multi(
            expressions=expressions,
            ids=ids,
            flags=flags,
            exts=ext,
            mode=mode,
            platform=HsPlatformInfo(),
        )

    @property
    def version(self) -> str:
        return self._hs.version

    @property
    def info(self) -> str:
        return self._hs.database_info(self._db)

    @classmethod
    def load(cls: T, data: ByteString, hs: HsApi = HS) -> T:
        self = object.__new__(cls)
        self._hs = hs
        self._db = hs.deserialize_database(data)
        return self

    def dump(self) -> ByteString:
        return self._hs.serialize_database(self._db)

    def scan(
            self,
            data: ByteString,
            match_event_handler: Optional[Callable[[int, int, int, int], Optional[bool]]],
    ) -> None:
        if match_event_handler is not None:
            def wrap_event_handler(id_, from_, to_, flags_, ignore_context, v=None):
                try:
                    v = match_event_handler(id_, from_, to_, flags_)
                finally:
                    return 1 if v else 0
        else:
            wrap_event_handler = None
        with self._sp.scratch(self._db) as scratch:
            self._hs.scan(self._db, scratch, data, wrap_event_handler)
