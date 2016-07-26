from xpath.expression import Expression, ExpressionKind
from xpath.literal import Literal


class Renderer(object):
    """A rendering context for converting an XPath `Expression` into a valid string query."""

    _RENDER_METHOD_NAMES = {
        ExpressionKind.ATTR: "_attribute",
        ExpressionKind.CONTAINS: "_contains",
        ExpressionKind.DESCENDANT: "_descendant",
        ExpressionKind.EQUALITY: "_equality",
        ExpressionKind.IS: "_is",
        ExpressionKind.NORMALIZED_SPACE: "_normalized_space",
        ExpressionKind.ONE_OF: "_one_of",
        ExpressionKind.OR: "_or",
        ExpressionKind.STRING: "_string_function",
        ExpressionKind.THIS_NODE: "_this_node",
        ExpressionKind.UNION: "_union",
        ExpressionKind.WHERE: "_where",
    }

    def __init__(self, exact=False):
        """
        Args:
            exact (bool, optional): Whether the generated queries should perform exact or
                approximate locator matches. Defaults to False.
        """

        self.exact = exact

    def render(self, node):
        """
        Converts a given XPath `Expression` into a corresponding string query.

        Args:
            node (Expression): An XPath `Expression` to convert.

        Returns:
            str: A valid XPath query corresponding to the given `Expression`.
        """

        args = [self._convert_argument(arg) for arg in node.arguments]
        render_method_name = self._RENDER_METHOD_NAMES[node.kind]
        render_method = getattr(self, render_method_name)
        return render_method(*args)

    def _convert_argument(self, argument):
        if isinstance(argument, Expression):
            return self.render(argument)
        if isinstance(argument, list):
            return [self._convert_argument(element) for element in argument]
        if isinstance(argument, str):
            return self._string_literal(argument)
        if isinstance(argument, Literal):
            return argument.value

    def _attribute(self, node, attribute_name):
        return "{0}/@{1}".format(node, attribute_name)

    def _contains(self, expr, value):
        return "contains({0}, {1})".format(expr, value)

    def _descendant(self, node, element_name):
        return "{0}//{1}".format(node, element_name)

    def _equality(self, expr1, expr2):
        return "{0} = {1}".format(expr1, expr2)

    def _is(self, expr1, expr2):
        if self.exact:
            return self._equality(expr1, expr2)
        else:
            return self._contains(expr1, expr2)

    def _normalized_space(self, expr):
        return "normalize-space({0})".format(expr)

    def _one_of(self, expr, *values):
        return " or ".join(["{0} = {1}".format(expr, value) for value in values])

    def _or(self, *exprs):
        return "({0})".format(" or ".join(exprs))

    def _string_function(self, expr):
        return "string({0})".format(expr)

    def _string_literal(self, string):
        return "'{0}'".format(string)

    def _this_node(self):
        return "."

    def _union(self, *exprs):
        return " | ".join(exprs)

    def _where(self, expr, *predicate_exprs):
        predicates = ["[{0}]".format(predicate_expr) for predicate_expr in predicate_exprs]
        return "{0}{1}".format(expr, "".join(predicates))


def to_xpath(node, exact=False):
    """
    Converts a given XPath `Expression` into a corresponding string query.

    Args:
        node (Expression): An XPath `Expression` to convert.
        exact (bool, optional): Whether the generated query should perform exact or approximate
            locator matches. Defaults to False.

    Returns:
        str: A valid XPath query corresponding to the given `Expression`.
    """

    return Renderer(exact=exact).render(node)
