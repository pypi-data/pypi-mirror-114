# special-engine

A Hyperscan binding, written in pure Python with ctypes. It's meant to be a
drop-in replacement for [python-hyperscan][python-hyperscan], but with extra
flexibility: you can load multiple versions of Hyperscan at the same time, and
since the code is just Python, it can be packaged as is or vendored into other
projects, and it can be instantiated multiple times against different versions
of libhs.so.

It's probably not as fast as python-hyperscan; I use it for offline compilation,
so performance isn't much of a goal.

[python-hyperscan]: https://github.com/darvid/python-hyperscan/
