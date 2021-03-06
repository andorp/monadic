"""
http://code.activestate.com/recipes/578353-code-to-source-and-back/
"""

import ast
import inspect
import re
from types import CodeType as code, FunctionType as function
import inspect

from monadic.interop import map_list
from monadic.python_ver import PYTHON_VERSION, invalid_python_version

import __future__
PyCF_MASK = sum(v
                for k, v in vars(__future__).items()
                if k.startswith('CO_FUTURE'))


__all__ = ['monadic', 'monadic_comp']


class Error(Exception):
    pass


class Unsupported(Error):
    pass


class NoSource(Error):
    pass


def get_func_code(f):
    if PYTHON_VERSION is 2:
        return f.func_code
    elif PYTHON_VERSION is 3:
        return f.__code__
    else:
        value_expressions()


def set_func_code(f, code):
    if PYTHON_VERSION is 2:
        f.func_code = code
    elif PYTHON_VERSION is 3:
        f.__code__ = code
    else:
        value_expressions()


def uncompile(c):
    """ uncompile(codeobj)
        -> [source, filename, mode, flags, firstlineno, privateprefix] """
    if c.co_flags & inspect.CO_NESTED or c.co_freevars:
        raise Unsupported('nested functions not supported')
    if c.co_name == '<lambda>':
        raise Unsupported('lambda functions not supported')
    if c.co_filename == '<string>':
        raise Unsupported('code without source file not supported')

    filename = inspect.getfile(c)
    try:
        lines, firstlineno = inspect.getsourcelines(c)
    except IOError:
        raise NoSource('source code not available')
    source = ''.join(lines)

    # __X is mangled to _ClassName__X in methods. Find this prefix:
    privateprefix = None
    for name in c.co_names:
        m = re.match('^(_[A-Za-z][A-Za-z0-9_]*)__.*$', name)
        if m:
            privateprefix = m.group(1)
            break

    return [source, filename, 'exec', c.co_flags & PyCF_MASK,
            firstlineno, privateprefix]


def recompile(source, filename, mode,
              flags=0, firstlineno=1, privateprefix=None):
    """ recompile output of uncompile back to a code object.
        source may also be preparsed AST """
    if isinstance(source, ast.AST):
        a = source
    else:
        a = parse_snippet(source, filename, mode, flags, firstlineno)
    node = a.body[0]
    if not isinstance(node, ast.FunctionDef):
        raise Error('Expecting function AST node')

    c0 = compile(a, filename, mode, flags, True)

    # This code object defines the function.
    # Find the function's actual body code:
    for c in c0.co_consts:
        if not isinstance(c, code):
            continue
        if c.co_name == node.name and c.co_firstlineno == node.lineno:
            break
    else:
        raise Error('Function body code not found')

    # Re-mangle private names:
    if privateprefix is not None:

        def fixnames(names):
            isprivate = re.compile('^__.*(?<!__)$').match
            return tuple(privateprefix + name if isprivate(name)
                         else name for name in names)

        c = code(c.co_argcount, c.co_nlocals, c.co_stacksize,
                 c.co_flags, c.co_code, c.co_consts,
                 fixnames(c.co_names), fixnames(c.co_varnames),
                 c.co_filename, c.co_name, c.co_firstlineno,
                 c.co_lnotab, c.co_freevars, c.co_cellvars)
    return c


def parse_snippet(source, filename, mode,
                  flags, firstlineno, privateprefix_ignored=None):
    """ Like ast.parse, but accepts indented
        code snippet with a line number offset. """
    args = filename, mode, flags | ast.PyCF_ONLY_AST, True
    prefix = '\n'
    try:
        a = compile(prefix + source, *args)
    except IndentationError:
        # Already indented? Wrap with dummy compound statement
        prefix = 'with 0:\n'
        a = compile(prefix + source, *args)
        # peel wrapper
        a.body = a.body[0].body
    ast.increment_lineno(a, firstlineno - 2)
    return a


def monadic_comp(monad):
    """ Decorator that creates helper functions within the function body
        and transforms all the list comprehension into a monadic expression """
    module_name = inspect.getmodule(monad).__name__
    monad_name = monad.__name__

    def wrapper(func):
        # uncompile function
        unc = uncompile(get_func_code(func))

        # convert to ast and apply visitor
        tree = parse_snippet(*unc)
        MonadicFunctionDef(module_name, monad_name).visit(tree)
        MonadicListComp().visit(tree)
        ast.fix_missing_locations(tree)
        unc[0] = tree

        # recompile and patch function's code
        set_func_code(func, recompile(*unc))
        return func

    return wrapper


def monadic(monad):
    """ Decorator that creates helper functions within the function body
        and transforms it into a monadic expression """
    module_name = inspect.getmodule(monad).__name__
    monad_name = monad.__name__

    def wrapper(func):
        # uncompile function
        unc = uncompile(get_func_code(func))

        # convert to ast and apply visitor
        tree = parse_snippet(*unc)
        MonadicStatement().visit(tree)
        MonadicFunctionDef(module_name, monad_name).visit(tree)
        ast.fix_missing_locations(tree)
        unc[0] = tree

        # recompile and patch function's code
        set_func_code(func, recompile(*unc))
        return func

    return wrapper


class MonadicListComp(ast.NodeTransformer):

    def visit_ListComp(self, node):
        generators = node.generators

        def create_bind(gs):
            l = len(gs)
            g = gs[0]
            iter_call = g.iter
            if l == 1:
                la = ast_lambda(g.target,
                                func_call(name('unit'), args=[node.elt]))
                return func_call(name('bind'), [iter_call, la])
            if l > 1:
                la = ast_lambda(g.target, create_bind(gs[1:]))
                return func_call(name('bind'), [iter_call, la])
            raise Exception('Empty generators for list comprehension')

        call = create_bind(generators)
        newnode = call
        ast.copy_location(newnode, node)
        ast.fix_missing_locations(newnode)
        return newnode


class MonadicFunctionDef(ast.NodeTransformer):
    """ Import and declare the necessary functions
        to create monad abstractions """

    def __init__(self, module_name, monad_name):
        self.module_name = module_name
        self.monad_name = monad_name

    def visit_FunctionDef(self, node):
        monad_any_t = func_call(name(self.monad_name), [])

        # from contract import any_t, kleisli_arrow
        import_contract = ast.ImportFrom(
            module="monadic.monad_def",
            names=map_list(alias, ["kleisli_arrow", "unit"]))
        ast.fix_missing_locations(import_contract)

        # from monad_module import monad_name
        import_monad = ast.ImportFrom(module=self.module_name,
                                      names=map_list(alias, [self.monad_name]))
        ast.fix_missing_locations(import_monad)

        # bind = kleisli_arrow(monad_name(any_t))
        bind = ast.Assign(
            [name_store('bind')],
            func_call(name('kleisli_arrow'), [monad_any_t])
        )
        ast.fix_missing_locations(bind)

        # unit = unit(monad_name(any_t))
        unit = ast.Assign(
            [name_store('unit')],
            func_call(name('unit'), [monad_any_t])
        )
        ast.fix_missing_locations(unit)

        # non_monadic = unit
        normal = ast.Assign(
            [name_store('normal')],
            name('unit')
        )
        ast.fix_missing_locations(normal)

        node.body = [import_contract, import_monad,
                     bind, unit, normal] + node.body
        return node


class MonadicStatement(ast.NodeTransformer):
    """ Transforms the function body into a monadic expression """

    def visit_FunctionDef(self, node):
        def create_bind(stmts):
            l = len(stmts)
            s = stmts[0]
            if l == 1:
                return final_call(s)
            if l > 1:
                call = get_call(s)
                la = ast_lambda(get_name(s), create_bind(stmts[1:]))
                return func_call(name('bind'), [call, la])
            raise Exception('Empty statement for list comprehension')
        call = create_bind(node.body)
        newnode = ast.Return(call)
        ast.copy_location(newnode, node)
        ast.fix_missing_locations(newnode)
        node.body = [newnode]
        return node


# Helpers for assign, expr, return ast handlers


def get_name(stmt):

    def get_assign_name(a):
        a.targets[0].cxt = ast.Load()
        return a.targets[0]

    def get_expr_name(e):
        return name('_')

    # Algebra is like inversion of control
    return aer_algebra(
        get_assign_name,
        get_expr_name,
        class_error('name'),
        stmt)


def define_value_expression():
    exprs = [ast.BoolOp,
             ast.BinOp,
             ast.UnaryOp,
             ast.Dict,
             ast.ListComp,
             ast.Num,
             ast.Str,
             ast.Subscript,
             ast.List,
             ast.Tuple]
    if PYTHON_VERSION is 2:
        return exprs
    elif PYTHON_VERSION is 3:
        return (exprs + [ast.DictComp, ast.SetComp])
    else:
        invalid_python_version()


value_expressions = define_value_expression()


def is_value_expr(expr):
    return expr.__class__ in value_expressions


def get_assign_call(a):
    vclass = a.value.__class__
    if vclass is ast.Call:
        return a.value
    elif is_value_expr(a.value):
        return ast.Call(func=name('unit'), args=[a.value], keywords=[])
    else:
        raise TypeError("No call object is found")


def get_expr_call(e):
    vclass = e.value.__class__
    if vclass is ast.Call:
        return e.value
    else:
        raise TypeError("No call object is found")


def get_call(stmt):
    return aer_algebra(
        get_assign_call,
        get_expr_call,
        class_error('call'),
        stmt)


def get_return_expr(stmt):
    def get_expr(r):
        return r.value
    return aer_algebra(
        class_error('return'),
        class_error('return'),
        get_expr,
        stmt)


def final_call(stmt):
    def return_call(s):
        return func_call(name('unit'), args=[get_return_expr(s)])
    return aer_algebra(
        get_assign_call,
        get_expr_call,
        return_call,
        stmt)


def class_error(e):
    def check(s):
        raise Exception("Non {expected} type {t}".format(
            expected=e, t=s.__class__))
    return check


def aer_algebra(a, e, r, stmt):
    sc = stmt.__class__
    if sc == ast.Assign:
        return a(stmt)
    elif sc == ast.Expr:
        return e(stmt)
    elif sc == ast.Return:
        return r(stmt)
    else:
        raise TypeError("Unexpected statement {type}".format(type=sc))


# AST Helpers


def name(n):
    return ast.Name(id=n, ctx=ast.Load())


def name_store(n):
    return ast.Name(id=n, ctx=ast.Store())


def func_call(name, args):
    return ast.Call(func=name, args=args, keywords=[])


def alias(name):
    return ast.alias(name=name)


def at(name, str_idx):
    return ast.Subscript(value=name, slice=ast.Index(str_idx), ctx=ast.Load())


def ast_lambda(name, body):
    if PYTHON_VERSION is 2:
        return ast.Lambda(args=ast.arguments(args=[name],
                          defaults=[]), body=body)
    elif PYTHON_VERSION is 3:
        return ast.Lambda(args=ast.arguments(args=[ast.arg(arg=name.id)],
                                             defaults=[],
                                             kwonlyargs=[],
                                             kw_defaults=[]),
                          body=body)
    else:
        invalid_python_version()
