```
import pencilcase
```


# pencil

Drop-in debugger that allows you to write code while you debug. ✏️

Pencil it in! Write code by debugging your code. Lines of code are
automatically inserted into your file. Clean them up later and voilà!

```
pencilcase.pencil()
```

# timer

Super simple drop-in profiler. ⏱

Context manager that counts how much time is spent across all executions
of the contained code block, storing it in seconds to the specified global
variable. Prints out the value of that variable each time it is run.

```
with pencilcase.timer('weaving_baskets'):
    weave_baskets()
```

Alternatively, apply as a decorator to a function to count time spent in
that function.


```
@pencilcase.timer('weaving_baskets')
def weave_baskets():
    ...
```

# eraser
This is a totally unnecessary feature, but who has a pencil case without an eraser??

```
pencilcase.eraser()
```

# microfilm

Pretty-print the given dict as JSON. 🎞

```
blob = ...
pencilcase.microfilm(blob)
```

# butterfly_net

Context manager that catches all exceptions raised within, doing nothing but
printing their lovely exception traces and then letting them be free. 🦋

```
with pencilcase.butterfly_net():
    ...
```