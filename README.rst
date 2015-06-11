
================================================================================
TestCase2
================================================================================

Nose disallows subclasses of ``unittest.TestCase`` from using any of Nose's
advanced features (e.g. test generators) in order to guarantee that legacy
behavior is preserved.

However, many of Nose's advanced features do not conflict with the behavior of
``unittest.TestCase`` so it would be nice to use them in anyway. To fix this,
this project implements a ``TestCase`` type that functions identically to
``unittest.TestCase`` without including it in its MRO.
