PKCS#1 PSS (RSA)
================

A probabilistic digital signature scheme based on RSA.

It is more formally called ``RSASSA-PSS``
in `Section 8.1 of RFC8017`__.

The following example shows how the sender can use its own *private* key
(loaded from a file) to create the signature of a message::

    >>> from CryptoCore.Signature import pss
    >>> from CryptoCore.Hash import SHA256
    >>> from CryptoCore.PublicKey import RSA
    >>> from CryptoCore import Random
    >>>
    >>> message = 'To be signed'
    >>> key = RSA.import_key(open('privkey.der').read())
    >>> h = SHA256.new(message)
    >>> signature = pss.new(key).sign(h)

At the receiver side, the matching *public* RSA key is used to verify
authenticity of the incoming message::

    >>> key = RSA.import_key(open('pubkey.der').read())
    >>> h = SHA256.new(message)
    >>> verifier = pss.new(key)
    >>> try:
    >>>     verifier.verify(h, signature)
    >>>     print "The signature is authentic."
    >>> except (ValueError, TypeError):
    >>>     print "The signature is not authentic."

.. __: https://tools.ietf.org/html/rfc8017#section-8.1

.. automodule:: CryptoCore.Signature.pss
    :members:
