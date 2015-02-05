# This library follows (at least some basic) design by contract philosophies.
# Here is where we put things that help fulfill this need. Optimally this
# will eventually be its own package.

# TODO[TJ]: This can, and should, be sliced off into its own library
def must_be(what, name, types):
    if isinstance(what, types):
        return True
    if isinstance(types, tuple):
        type_list = ", ".join([t.__name__ for t in types])
    else:
        type_list = types.__name__
    raise ValueError(
        "{what} must be of types ({list}), is of type {type}".format(
            what=name,
            list=type_list,
            type=type(what)))
