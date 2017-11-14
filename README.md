# ParseIt

A simple parsing tool in 200 lines of python

Give it a grammar and tokens, and it'll give you back an ast.

## Inputs

Use the `parse()` function to parse text. The `tokens` parameter is a dictionary of token names to compiled regular expressions.
Prefixing a token with `%` will ignore it. Token names must be uppercase

The `rules` parameter is a dictionary of names to lists of rules, and the `start` parameter is what node to start parsing first.

### Rules

A rule is a list of rulesegments. A rulesegment can be a string, which means parse that TOKEN/rule_name.
A list rule segement is a group, the last item in it can be one of the following:

- `?`: this group is optional
- `+`: match at least one of this group, and possibly more
- `*`: match any number of this group, including zero

An example rule looks like this:
```python
[["NUM", "?"], ["var", "*"]]
``` 

The rule dictionary is a dictionary of rule_names to lists of these rules, each one being a possibility, like this:
```python
{
    "multi_poly": [
        ["LPAREN", "polynomial", "RPAREN", "LPAREN", "polynomial", "RPAREN"],
        ["NUM", "LPAREN", "polynomial", "RPAREN"],
        ["polynomial"]
    ]
}
```

## Output

The tree format of ParseIt is very simple: for rule instances (nodes) you have a tuple with the first value being the node name, and the second being its children.

Tokens are represented as a tuple of: the token name, the token content, and its position in the stream

## `treeify`

There is also a module called treeify in the package that (if pydot is installed) allows you to create a graphical representation of
the generated trees.

## Example

`example.py` has an example grammar and code to convert the generated tree into a pydot