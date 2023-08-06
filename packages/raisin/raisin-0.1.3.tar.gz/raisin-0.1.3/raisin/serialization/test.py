#!/usr/bin/env python3

"""
** Allows for extensive testing around serialization. **
--------------------------------------------------------

There is a function capable of generating many types of objects.
For each of these objects they are serialized then deserialized.
"""

import itertools
import sys

import pytest

from raisin.serialization.constants import ALPHABET, BUFFER_SIZE
from raisin.serialization.iter_tools import (anticipate, concat_gen,
    deconcat_gen, relocate, resize, to_gen)
from raisin.serialization.core import size2tag, tag2size
from raisin.serialization import dumps, loads, serialize, deserialize
from raisin.encapsulation.packaging import Argument, Func, Result, Task


# OBJECTS GENERATION

def get_int():
    """
    ** Makes some various intergers. **
    """
    yield 0
    for i in [2 ** j for j in range(1, 16)]:
        yield 2 ** i - 1
        yield 2 ** i
        yield 2 ** i + 1
        yield -(2 ** i - 1)
        yield -(2 ** i)
        yield -(2 ** i + 1)

def get_float():
    """
    ** Makes some various floats. **
    """
    yield 0.0
    yield sys.float_info.max
    yield -sys.float_info.max
    yield sys.float_info.min
    yield -sys.float_info.min
    yield 1.0

def get_simple_objects():
    """
    ** Yield some vaious simple objects. **
    """
    yield None
    yield from get_int()
    yield from get_float()


# TESTS TOOLS

def test_tools():
    """
    ** Tests the tools. **
    """
    # anticipate
    assert list(anticipate([''])) == [(True, '')]
    assert list(anticipate(['', ''])) == [(False, ''), (True, '')]
    with pytest.raises(RuntimeError):
        list(anticipate([]))

    # concat
    for gen in ([], [b''], [b'', b''], [b'a'], [b'a', b'b'], [b'', b'b'], [b'a', b'']):
        assert list(deconcat_gen(gen=concat_gen(gen))) == gen
        assert list(deconcat_gen(pack=b''.join(concat_gen(gen)))) == gen

    # relocate
    iterator = iter([])
    iterator_bis = relocate(iterator)
    with pytest.raises(StopIteration):
        next(iterator_bis)
    with pytest.raises(StopIteration):
        next(iterator)
    for gen in (
            [b'a'],
            [b'a', b'b', b'c'],
            itertools.chain([b'a'], (b'b' * BUFFER_SIZE for _ in range(100)))):
        iterator = iter(gen)
        iterator_bis = relocate(iterator)
        with pytest.raises(StopIteration):
            next(iterator)
        assert next(iterator_bis) == b'a'

    # resize
    for nbr in [0, 1, 2, 10, 100, 1000]:
        for pack_len in [0, 1, 2, 10, 100, 1000]:
            for gen_len in [0, 1, 2, 4]:
                for gen_item_len in [0, 1, 100, 500]:
                    pack = bytes(pack_len)
                    gen = (bytes(gen_item_len) for _ in range(gen_len))
                    if nbr <= pack_len + gen_len*gen_item_len:
                        pack_, gen_ = resize(nbr, pack=pack, gen=gen)
                        assert len(pack_) == nbr
                        assert len(pack_ + b''.join(gen_)) == pack_len + gen_len*gen_item_len
                    else:
                        with pytest.raises(RuntimeError):
                            resize(nbr, pack=pack, gen=gen)

    # to_gen
    for size in [1, 2, 1000, BUFFER_SIZE]:
        for gen in (
                [],
                [b''],
                [b'a'],
                [b'a' * size],
                [b'a' * (size - 1)],
                [b'a' * (size + 1)],
                [b'', b''],
                [b'a' * ((2 ** l) % (2 * size)) for l in range(100)]):
            l_in = [len(e) for e in gen]
            l_out = [len(e) for e in to_gen(gen=gen, size=size)]
            assert sum(l_in) == sum(l_out)
            assert all(s == size for s in l_out[:-1])
            assert l_out[-1] <= size
            l_out = [len(e) for e in to_gen(pack=b''.join(gen), size=size)]
            assert sum(l_in) == sum(l_out)
            assert all(s == size for s in l_out[:-1])
            assert l_out[-1] <= size

    # size & tag
    with pytest.raises(StopIteration):
        tag2size(pack=b'')
    with pytest.raises(RuntimeError):
        tag2size(pack=b'\x01\x00\x00')
    for size in [0, 1, 2, 127, 128, 129, 123456789123456789]:
        pack = size2tag(size)
        assert tag2size(pack=pack)[0] == size



# TESTS SERIALIZATION

def test_dumps():
    """
    ** Tests dumps. **
    """
    for obj in get_simple_objects():
        for compresslevel in [0, 1]:
            ser = dumps(obj, compresslevel=compresslevel)
            assert all(c in ALPHABET for c in ser)
            assert loads(ser) == obj

def test_raisin_class():
    """
    ** Tests raisin class. **
    """
    arg = Argument(0)
    func = Func(lambda x : x**2)
    task = Task(hash(func), (hash(arg),))
    result = Result()

    assert deserialize(serialize(arg)) == arg
    assert deserialize(serialize(func)) == func
    assert deserialize(serialize(task)) == task
    assert deserialize(serialize(result)) == result
