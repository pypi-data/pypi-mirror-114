:mod:`CryptoCore.Random` package
============================

.. function:: CryptoCore.Random.get_random_bytes(N)

    Return a random byte string of length *N*.

:mod:`CryptoCore.Random.random` module
----------------------------------

.. function:: CryptoCore.Random.random.getrandbits(N)

    Return a random integer, at most *N* bits long.

.. function:: CryptoCore.Random.random.randrange([start,] stop[, step])

    Return a random integer in the range *(start, stop, step)*.
    By default, *start* is 0 and *step* is 1.

.. function:: CryptoCore.Random.random.randint(a, b)

    Return a random integer in the range no smaller than *a*
    and no larger than *b*.

.. function:: CryptoCore.Random.random.choice(seq)

    Return a random element picked from the sequence *seq*.

.. function:: CryptoCore.Random.random.shuffle(seq)

    Randomly shuffle the sequence *seq* in-place.

.. function:: CryptoCore.Random.random.sample(population, k)

    Randomly chooses *k* distinct elements from the list *population*.
