MiniDelegate
--------
Simple python module to add a delegate decorator type

    >>> @delegate
    >>> def foo():
    >>>   print("Foo")
    >>> 
    >>> def bar():
    >>>   print("Bar")
    >>> 
    >>> foo.bind(bar)
