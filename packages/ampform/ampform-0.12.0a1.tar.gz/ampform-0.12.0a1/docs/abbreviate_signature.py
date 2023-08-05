# cspell:ignore docutils
# pylint: disable=import-error
# pyright: reportMissingImports=false
"""Abbreviated the annotations generated by sphinx-autodoc.

It's not necessary to generate the full path of type hints, because they are
rendered as clickable links.

See also https://github.com/sphinx-doc/sphinx/issues/5868.
"""

import sphinx.domains.python
from docutils import nodes
from sphinx import addnodes
from sphinx.environment import BuildEnvironment


def replace_link(text: str) -> str:
    replacements = {
        "SupportsIndex": "typing.SupportsIndex",
        "a set-like object providing a view on D's items": "typing.ItemsView",
        "a set-like object providing a view on D's keys": "typing.KeysView",
        "an object providing a view on D's values": "typing.ValuesView",
        "typing_extensions.Protocol": "typing.Protocol",
        # OrderedDict typing from collections,
        # see https://readthedocs.org/projects/ampform/builds/14828756
        "sp.Expr": "sympy.core.expr.Expr",
        "sp.Symbol": "sympy.core.symbol.Symbol",
    }
    for old, new in replacements.items():
        if text == old:
            return new
    return text


def new_type_to_xref(
    text: str, env: BuildEnvironment = None
) -> addnodes.pending_xref:
    """Convert a type string to a cross reference node."""
    if text == "None":
        reftype = "obj"
    else:
        reftype = "class"

    if env:
        kwargs = {
            "py:module": env.ref_context.get("py:module"),
            "py:class": env.ref_context.get("py:class"),
        }
    else:
        kwargs = {}

    text = replace_link(text)
    short_text = text.split(".")[-1]

    return addnodes.pending_xref(
        "",
        nodes.Text(short_text),
        refdomain="py",
        reftype=reftype,
        reftarget=text,
        **kwargs,
    )


def abbreviate_signature() -> None:
    sphinx.domains.python.type_to_xref = new_type_to_xref
