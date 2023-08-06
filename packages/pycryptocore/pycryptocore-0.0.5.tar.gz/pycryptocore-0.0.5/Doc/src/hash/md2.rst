MD2
===

MD2 is specified in RFC1319_ and it produces the 128 bit digest of a message.
For example::

    >>> from CryptoCore.Hash import MD2
    >>>
    >>> h = MD2.new()
    >>> h.update(b'Hello')
    >>> print h.hexdigest()

MD2 stand for Message Digest version 2, and it was invented by Rivest in 1989.

.. warning::
    This algorithm is not considered secure. Do not use it for new designs.

.. _RFC1319: http://tools.ietf.org/html/rfc1319

.. automodule:: CryptoCore.Hash.MD2
    :members:
