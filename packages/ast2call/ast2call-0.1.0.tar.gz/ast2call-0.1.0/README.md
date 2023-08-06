# ast2call

Mostly exists as a helper for other projects I'm working on.

Input: python source

Output: python source, that would be the equivalent of calling `ast.parse` on
the input

E.g. 

```
print('hello world!')
```

--> 

```
ast.Module(body=[ast.Expr(value=ast.Call(func=ast.Name(id='print', ctx=ast.Load(), lineno=None), args=[ast.Constant(value='hello world!', kind=None, lineno=None)], keywords=[], lineno=None), lineno=None)], type_ignores=[])
```

Usage:

```shell
$ ast2call hello_world.py
ast.Module(body=[ast.Expr(value=ast.Call(func=ast.Name(id='print', ctx=ast.Load(), lineno=None), args=[ast.Constant(value='hello world!', kind=None, lineno=None)], keywords=[], lineno=None), lineno=None)], type_ignores=[])
```

```python
>>> import ast2call
>>> import ast
>>> ast2call.ast2call(ast.parse('print("hello world!")'))
<ast.Call object at 0x7fc98a773250>
>>> ast2call.astprint('print("hello world!")')
"ast.Module(body=[ast.Expr(value=ast.Call(func=ast.Name(id='print', ctx=ast.Load(), lineno=None), args=[ast.Constant(value='hello world!', kind=None, lineno=None)], keywords=[], lineno=None), lineno=None)], type_ignores=[])"
```


