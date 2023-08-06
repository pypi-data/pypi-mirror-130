from __future__ import annotations

import operator
from copy import copy
from enum import Enum
from itertools import product
from typing import Dict, List, Set, Tuple, Union, cast

import numpy as np
from attr import attrib, attrs
from bs4 import BeautifulSoup
from bs4.element import Tag

PRIME = 3
# When MATHML_SANITY is `True`, allows the use of the <rem/> function. When `False`, this function
# is emulated. To conform to the SBML specification, we have to set sanity to false.
# (Tell me how you _really_ feel...)
MATHML_SANITY = False

ExpressionOrInt = Union[int, "Expression"]
TruthTable = List[Tuple[Tuple[Tuple[str, int], ...], int]]


class Operation(Enum):
    PLUS = "PLUS"
    MINUS = "MINUS"
    TIMES = "TIMES"
    EXP = "EXP"
    MAX = "MAX"
    MIN = "MIN"
    CONT = "CONT"
    NOT = "NOT"


####################################################################################################


def h(x: int, fx: int):
    """helper function as in the PLoS article, doi:10.1371/journal.pcbi.1005352.t003 pg 16/24"""
    fx %= PRIME
    x %= PRIME
    if fx > x:
        return x + 1
    elif fx < x:
        return x - 1
    else:
        return x


####################################################################################################


def inner_mathml_constant(value: int) -> Tag:
    constant_tag = Tag(name="cn", is_xml=True, attrs={"type": "integer"})
    constant_tag.append(str(value))
    return constant_tag


def inner_mathml_variable(var_name: str) -> Tag:
    var_tag = Tag(name="ci", is_xml=True)
    var_tag.append(var_name)
    return var_tag


def function_inner_mathml(function_name: str, operands: List[Tag]) -> Tag:
    # Note: up to you to do any copying of the operands that is needed
    top_tag = Tag(name="apply", is_xml=True)
    top_tag.append(Tag(name=function_name, is_xml=True, can_be_empty_element=True))
    for operand in operands:
        top_tag.append(operand)
    return top_tag


def single_var_to_power_inner_mathml(var_name: str, power: int) -> Tag:
    """Handle var^power"""
    if power == 0:
        return inner_mathml_constant(1)
    elif power == 1:
        return inner_mathml_variable(var_name)
    else:
        return function_inner_mathml(
            "power", [inner_mathml_variable(var_name), inner_mathml_constant(power)]
        )


def wrap_with_modulus_inner_mathml(
    expression: Tag, base: int, sane: bool = False
) -> Tag:
    """
    Wrap some inner mathml with a modulus operation.

    SBML does not support the <rem/> ("remainder") tag, which is a pain. So we have a sanity flag,
    `sane`, turned off by default for compatibility, which turns the simpler expression on.

    Parameters
    ----------
    expression: Tag
        The expression to wrap.
    base: int
        The base for the modulus.
    sane: bool
        Set sane to False to conform to the SBML subset of MathML. True allows a broader range
        of functions. e.g. <rem/>, the remainder


    Returns
    -------
    Tag
        Wrapped tag
    """
    if sane:
        return function_inner_mathml("rem", [expression, inner_mathml_constant(base)])
    else:
        # a mod b = a - b * floor(a/b)
        return function_inner_mathml(
            "minus",
            [
                expression,
                function_inner_mathml(
                    "times",
                    [
                        inner_mathml_constant(base),
                        function_inner_mathml(
                            "floor",
                            [
                                function_inner_mathml(
                                    "divide",
                                    [copy(expression), inner_mathml_constant(base)],
                                )
                            ],
                        ),
                    ],
                ),
            ],
        )


####################################################################################################
# monomial and sparse polynomial classes. These are faster than the sympy versions due to
# their reduced scope.
####################################################################################################


class Expression(object):
    def __add__(self, other):
        return BinaryOperation("PLUS", self, other)

    __radd__ = __add__

    def __sub__(self, other):
        return BinaryOperation("MINUS", self, other)

    def __mul__(self, other):
        return BinaryOperation("TIMES", self, other)

    __rmul__ = __mul__

    def __neg__(self):
        return UnaryRelation("MINUS", self)

    def __pow__(self, power, modulo=None):
        return BinaryOperation("EXP", self, power)

    # def __divmod__(self, other):
    #    raise NotImplementedError("division, modulus not implemented")

    # def __truediv__(self, other):
    #    raise NotImplementedError("truediv not implemented")

    # def __floordiv__(self, other):
    #    raise NotImplementedError("floordiv not implemented")

    def eval(self, variable_dict) -> ExpressionOrInt:
        """
        Evaluates the expression.

        Parameters
        ----------
        variable_dict
            variable_dict is expected to be a dict containing str:Expression or
            Monomial:Expression pairs. The latter are constrained to be of single-variable type.

        Returns
        -------

        """
        raise NotImplementedError("eval() unimplemented in " + str(type(self)))

    def __int__(self) -> int:
        raise NotImplementedError("__int__() unimplemented in " + str(type(self)))

    def is_constant(self) -> bool:
        raise NotImplementedError("is_constant() unimplemented in " + str(type(self)))

    def as_c_expression(self):
        raise NotImplementedError(
            "as_c_expression() unimplemented in " + str(type(self))
        )

    def as_polynomial(self) -> Union[int, Expression]:
        raise NotImplementedError("as_polynomial() unimplemented in " + str(type(self)))

    # def as_sympy(self):
    #     """
    #     converts to sympy expression
    #
    #     Returns
    #     -------
    #     sympy expression
    #     """
    #     raise NotImplementedError("as_sympy() unimplemented in " + str(type(self)))

    def as_numpy_str(self, variables: Tuple[str]) -> str:
        """
        Returns numpy-based function of variables.

        Order corresponds to that given in the variables parameter

        Parameters
        ----------
        variables

        Returns
        -------
        lambda with len(variables) parameters
        """
        raise NotImplementedError("as_numpy_str() unimplemented in " + str(type(self)))

    def as_mathml(self) -> BeautifulSoup:
        """
        Finds a mathml-based representation of the expression.

        Returns
        -------
        BeautifulSoup
        """
        soup = BeautifulSoup(features="xml")
        mathml = soup.new_tag(
            "math", attrs={"xmlns": "http://www.w3.org/1998/Math/MathML"}
        )
        soup.append(mathml)
        mathml.append(
            wrap_with_modulus_inner_mathml(
                self._make_inner_mathml(), base=PRIME, sane=MATHML_SANITY
            )
        )

        return soup

    def as_sbml_qual_relation(self, level: int) -> BeautifulSoup:
        """
        Finds a mathml represenation of 'level=expression', suitable for inclusion in SBML-qual.

        Parameters
        ----------
        level: int

        Returns
        -------
        BeautifulSoup
        """

        apply_tag = Tag(name="apply", is_xml=True)
        apply_tag.append(Tag(name="eq", is_xml=True, can_be_empty_element=True))
        apply_tag.append(inner_mathml_constant(level))
        apply_tag.append(
            wrap_with_modulus_inner_mathml(
                self._make_inner_mathml(), base=PRIME, sane=MATHML_SANITY
            )
        )

        soup = BeautifulSoup(features="xml")
        mathml = soup.new_tag(
            "math", attrs={"xmlns": "http://www.w3.org/1998/Math/MathML"}
        )
        soup.append(mathml)
        mathml.append(apply_tag)

        return soup

    def _make_inner_mathml(self) -> Union[BeautifulSoup, Tag]:
        raise NotImplementedError("_inner_mathml() unimplemented in " + str(type(self)))

    def get_variable_set(self) -> Set[str]:
        """returns a set containing all variable which occur in this expression"""
        raise NotImplementedError("get_var_set() unimplemented in " + str(type(self)))

    def num_variables(self):
        """returns the number of variables which occur in this expression"""
        return len(self.get_variable_set())

    def rename_variables(self, name_dict: Dict[str, str]):
        """rename variables"""
        raise NotImplementedError(
            "rename_variables() unimplemented in " + str(type(self))
        )

    def continuous_function_version(self, control_variable):
        """
        Wrap this equation with the 'continuity controller' i.e. return CONT(control_variable,self)
        :param control_variable: variable or string
        :return: functional continuous version
        """
        if self.is_constant():
            return self

        if isinstance(control_variable, str):
            control_variable = Monomial.as_var(control_variable)

        return Function("CONT", [control_variable, self])

    ################################################################################################
    #
    # the following method converts a system of equations into one which is "continuous" in the
    # sense that application of the system does not change the per-coordinate values by more than 1.
    # This is accomplished by a type of curve fitting. Fortunately, the formula for this
    #
    # g(x) = sum_{c\in \F_3^n} h(c) prod_{j=0}^n (1-(x_j-c_j)**2)
    #
    # (as seen in the PLoS article, doi:10.1371/journal.pcbi.1005352.t003 pg 16/24) admits a
    # recursive formulation. That is, for a polynomial x_k = f_k(x_0,x_1,...,x_l) we can select one
    # of the variables, say x_0 and reduce the polynomial each of 3-ways x_0=0, x_0=1, and x_0=2.
    # This correspondingly divides the sum into those which have each of the 3 types of terms
    # (1-(x_0-c_0)**2) for c_0=0, c_0=1, and c_0=2
    #
    # fortunately, (1-(x_j-0)**2)+(1-(x_j-1)**2)+(1-(x_j-2)**2) = 1 so if the evaluations of f
    # become constant or even simply eliminate a variable, we need no longer consider that variable.
    #
    # recursion proceeds by eliminating variables in this manner, multiplying by the appropriate
    # fitting term (1-(x_j-c_j)**2) (c_j being the evaluated value of x_j) on the way up.
    #
    # this comment is not really the place for a full proof of this method, but the proof is easily
    # obtained from the above.
    #
    ################################################################################################

    def continuous_polynomial_version(self, control_variable):
        if self.is_constant():
            return self

        if isinstance(control_variable, str):
            control_variable = Monomial.as_var(control_variable)

        # as the control variable is special (due to use in the 'h' function),
        # we will need to go through the procedure for it separately, first
        accumulator = Mod3Poly.zero()
        for control_variable_value in range(3):
            evaluated_poly = self.eval({control_variable: control_variable_value})
            if is_integer(evaluated_poly) or evaluated_poly.is_constant():
                computed_value: int = int(evaluated_poly)
                continuous_value = h(control_variable_value, computed_value)
                accumulator += continuous_value * (
                    1 - (control_variable - control_variable_value) ** 2
                )
            else:
                accumulator += evaluated_poly.continuous_version_helper(
                    control_variable_value
                ) * (1 - (control_variable - control_variable_value) ** 2)
        return accumulator

    def continuous_version_helper(self, control_variable_value):
        # find some free variable
        free_variable = tuple(self.get_variable_set())[0]
        if isinstance(free_variable, str):
            free_variable = Monomial.as_var(free_variable)

        # iterate over the ways of setting that variable: 0, 1, 2
        accumulator = Mod3Poly.zero()
        for free_variable_value in range(3):
            evaluated_poly = self.eval({free_variable: free_variable_value})
            if is_integer(evaluated_poly) or evaluated_poly.is_constant():
                computed_value: int = int(evaluated_poly)
                continuous_value = h(control_variable_value, computed_value)
                accumulator += continuous_value * (
                    1 - (free_variable - free_variable_value) ** 2
                )
            else:
                accumulator += evaluated_poly.continuous_version_helper(
                    control_variable_value
                ) * (1 - (free_variable - free_variable_value) ** 2)
        return accumulator

    def as_truth_table(self) -> Tuple[TruthTable, List[int]]:
        """
        Output the function as a truth table.

        Returns
        -------
        TruthTable
            a list of (inputs,output) tuples, where the inputs are tuples of (var,val) tuples
        """
        free_variables: Tuple[str] = tuple(self.get_variable_set())
        truth_table: TruthTable = []
        counts = []
        for input_values in product(range(3), repeat=len(free_variables)):
            inputs: Tuple[Tuple[str, int], ...] = tuple(
                zip(free_variables, input_values)
            )
            output: int = (
                int(self.eval(variable_dict=dict(zip(free_variables, input_values))))
                % 3
            )
            while len(counts) <= output:
                counts.append(0)
            counts[output] += 1
            truth_table.append((inputs, output))
        return truth_table, counts


####################################################################################################


def rename_helper(expression: Union[Expression, int], name_dict: Dict[str, str]):
    if is_integer(expression):
        return expression
    else:
        return expression.rename_variables(name_dict=name_dict)


####################################################################################################
# actions on expressions, suitable for conversion to polynomial form. Not best for simulator.


def mod_3(n):
    return n % 3


def not3(n):
    value = 2 + 2 * n
    if is_integer(value) or value.is_constant():
        return mod_3(int(value))
    else:
        return value


def max3(a, b):
    value = a + b + 2 * a * b + (a ** 2) * b + a * (b ** 2) + (a ** 2) * (b ** 2)
    if is_integer(value) or value.is_constant():
        return mod_3(int(value))
    else:
        return value


def min3(a, b):
    value = a * b + 2 * (a ** 2) * b + 2 * a * (b ** 2) + 2 * (a ** 2) * (b ** 2)
    if is_integer(value) or value.is_constant():
        return mod_3(int(value))
    else:
        return value


def is_integer(x):
    return isinstance(x, int) or isinstance(x, np.integer)


####################################################################################################


class Function(Expression):
    def __init__(self, function_name: str, expression_list):
        self._function_name = function_name
        self._expression_list: List[ExpressionOrInt] = expression_list

    def rename_variables(self, name_dict: Dict[str, str]):
        renamed_parameters = [
            rename_helper(expr, name_dict) for expr in self._expression_list
        ]
        return Function(self._function_name, renamed_parameters)

    def eval(self, variable_dict) -> ExpressionOrInt:
        # evaluate function parameters
        evaluated_expressions = [
            expr if is_integer(expr) else expr.eval(variable_dict)
            for expr in self._expression_list
        ]
        # simplify constants to ints, if possible
        evaluated_expressions = [
            mod_3(int(expr)) if is_integer(expr) or expr.is_constant() else expr
            for expr in evaluated_expressions
        ]

        if self._function_name == "MAX":
            assert len(evaluated_expressions) == 2, "wrong number of arguments for MAX"
            expr_one, expr_two = evaluated_expressions
            # if it can be computed directly, do it. otherwise, return in function form
            if is_integer(expr_one) and is_integer(expr_two):
                expr_one = mod_3(expr_one)
                expr_two = mod_3(expr_two)
                return max(expr_one, expr_two)
            elif is_integer(expr_one) and expr_one == 2:
                return 2
            elif is_integer(expr_one) and expr_one == 0:
                return expr_two
            elif is_integer(expr_two) and expr_two == 2:
                return 2
            elif is_integer(expr_two) and expr_two == 0:
                return expr_one
            else:
                return Function("MAX", [expr_one, expr_two])
        elif self._function_name == "MIN":
            assert len(evaluated_expressions) == 2, "wrong number of arguments for MIN"
            expr_one, expr_two = evaluated_expressions
            # if it can be computed directly, do it. otherwise, return in function form
            if is_integer(expr_one) and is_integer(expr_two):
                expr_one = mod_3(expr_one)
                expr_two = mod_3(expr_two)
                return min(expr_one, expr_two)
            elif is_integer(expr_one) and expr_one == 2:
                return expr_two
            elif is_integer(expr_one) and expr_one == 0:
                return 0
            elif is_integer(expr_two) and expr_two == 2:
                return expr_one
            elif is_integer(expr_two) and expr_two == 0:
                return 0
            else:
                return Function("MIN", [expr_one, expr_two])
        elif self._function_name == "CONT":
            assert len(evaluated_expressions) == 2, "wrong number of arguments for CONT"
            ctrl_var, expr = evaluated_expressions
            if is_integer(ctrl_var):
                raise Exception("Unsupported; nonsense")
            return Function("CONT", [ctrl_var, expr])
        elif self._function_name == "NOT":
            assert len(evaluated_expressions) == 1, "wrong number of arguments for NOT"
            expr = evaluated_expressions[0]
            # if it can be computed directly, do it. otherwise, return in function form
            if is_integer(expr):
                return not3(int(expr))
            else:
                return Function("NOT", [expr])
        else:
            raise Exception("cannot evaluate unknown function " + self._function_name)

    def __int__(self) -> int:
        if not self.is_constant():
            raise ValueError("non constant expressions can't be cast to ints")

        return cast(int, self.eval({}))

    def is_constant(self) -> bool:
        return all(
            is_integer(expr) or expr.is_constant() for expr in self._expression_list
        )

    def __str__(self):
        return (
            self._function_name
            + "("
            + ",".join([str(exp) for exp in self._expression_list])
            + ")"
        )

    __repr__ = __str__

    def as_c_expression(self):
        c_exprs = [
            str(expr) if is_integer(expr) else expr.as_c_expression()
            for expr in self._expression_list
        ]

        if self._function_name == "MAX":
            func_name = "mod3max"
        elif self._function_name == "MIN":
            func_name = "mod3min"
        elif self._function_name == "CONT":
            func_name = "mod3continuity"
        elif self._function_name == "NOT":
            func_name = "mod3not"
        else:
            raise Exception("Unknown binary relation: " + self._function_name)

        return func_name + "(" + ",".join(c_exprs) + ")"

    def as_polynomial(self):
        expressions_as_polynomials = [
            mod_3(expr) if is_integer(expr) else expr.as_polynomial()
            for expr in self._expression_list
        ]

        if self._function_name == "MAX":
            assert (
                len(expressions_as_polynomials) == 2
            ), "wrong number of arguments for MAX"
            return max3(expressions_as_polynomials[0], expressions_as_polynomials[1])

        elif self._function_name == "MIN":
            assert (
                len(expressions_as_polynomials) == 2
            ), "wrong number of arguments for MIN"
            return min3(expressions_as_polynomials[0], expressions_as_polynomials[1])

        elif self._function_name == "CONT":
            assert (
                len(expressions_as_polynomials) == 2
            ), "wrong number of arguments for CONT"
            return expressions_as_polynomials[1].continuous_polynomial_version(
                expressions_as_polynomials[0]
            )

        elif self._function_name == "NOT":
            assert (
                len(expressions_as_polynomials) == 1
            ), "wrong number of arguments for NOT"
            return not3(expressions_as_polynomials[0])

        else:
            raise Exception(
                "cannot evaluate unknown function "
                + self._function_name
                + " as a polynomial"
            )

    # def as_sympy(self):
    #
    #     def cont_sympy(control, expr):
    #         return expr if is_integer(expr) \
    #             else expr.continuous_polynomial_version(control)
    #
    #     def not_sympy(expr):
    #         return 1 - expr
    #
    #     # tuples are param-count, function
    #     functions = {'MAX': (2, sympy.Max),
    #                  'MIN': (2, sympy.Min),
    #                  'CONT': (2, cont_sympy),
    #                  'NOT': (1, not_sympy)}
    #
    #     if self._function_name not in functions:
    #         raise Exception("cannot evaluate unknown function " + self._function_name +
    #                         " as a sympy expression")
    #
    #     if len(self._expression_list) != functions[self._function_name][0]:
    #         raise Exception(f"Wrong number of arguments for {self._function_name}")
    #
    #     function = functions[self._function_name][1]
    #
    #     sympy_expressions = [sympy.Mod(expr, 3) if is_integer(expr)
    #                          else sympy.Mod(expr.as_sympy(), 3)
    #                          for expr in self._expression_list]
    #     return function(*sympy_expressions)

    def as_numpy_str(self, variables) -> str:
        np_parameter_strings = [
            str(expr) if is_integer(expr) else expr.as_numpy_str(variables)
            for expr in self._expression_list
        ]

        continuous_str = "( {0}+np.sign(np.mod({1},3)-np.mod({0},3)) )"
        max_str = "np.maximum(np.mod({0},3),np.mod({1},3))"
        min_str = "np.minimum(np.mod({0},3),np.mod({1},3))"
        not_str = "(2-({0}))"

        # tuples are param-count, function
        function_strings = {
            "MAX": (2, max_str),
            "MIN": (2, min_str),
            "CONT": (2, continuous_str),
            "NOT": (1, not_str),
        }

        if self._function_name not in function_strings:
            raise Exception(
                "cannot evaluate unknown function "
                + self._function_name
                + " as a numpy function"
            )

        if len(self._expression_list) != function_strings[self._function_name][0]:
            raise Exception(f"Wrong number of arguments for {self._function_name}")

        function = function_strings[self._function_name][1]

        return function.format(*np_parameter_strings)

    def _make_inner_mathml(self) -> Tag:
        apply_tag = Tag(name="apply", is_xml=True)

        mathml_function_strings = {
            "MAX": Tag(name="max", is_xml=True, can_be_empty_element=True),
            "MIN": Tag(name="min", is_xml=True, can_be_empty_element=True),
        }

        if self._function_name in mathml_function_strings:
            apply_tag.append(mathml_function_strings[self._function_name])
            for expression in self._expression_list:
                apply_tag.append(
                    wrap_with_modulus_inner_mathml(
                        expression._make_inner_mathml(), base=PRIME, sane=MATHML_SANITY
                    )
                )
        elif self._function_name == "NOT":
            # rewrite as (prime-1)-expression
            apply_tag.append(Tag(name="minus", is_xml=True, can_be_empty_element=True))
            apply_tag.append(inner_mathml_constant(PRIME - 1))
            apply_tag.append(
                wrap_with_modulus_inner_mathml(
                    self._expression_list[0]._make_inner_mathml(),
                    base=PRIME,
                    sane=MATHML_SANITY,
                )
            )
        else:
            raise NotImplementedError(
                "_inner_mathml() unimplemented in " + str(type(self))
            )

        return apply_tag

    def get_variable_set(self) -> Set[str]:
        var_set = set()
        for expr in self._expression_list:
            if not is_integer(expr):
                var_set = var_set.union(expr.get_variable_set())
        return var_set


class BinaryOperation(Expression):
    def __init__(
        self,
        relation_name,
        left_expression: ExpressionOrInt,
        right_expression: ExpressionOrInt,
    ):
        self._relation_name = relation_name
        self._left_expression: ExpressionOrInt = left_expression
        self._right_expression: ExpressionOrInt = right_expression

    def rename_variables(self, name_dict: Dict[str, str]):
        renamed_left_expression = rename_helper(self._left_expression, name_dict)
        renamed_right_expression = rename_helper(self._right_expression, name_dict)
        return BinaryOperation(
            self._relation_name,
            left_expression=renamed_left_expression,
            right_expression=renamed_right_expression,
        )

    def is_constant(self) -> bool:
        return (
            is_integer(self._left_expression) or self._left_expression.is_constant()
        ) and (
            is_integer(self._right_expression) or self._right_expression.is_constant()
        )

    def eval(self, variable_dict) -> ExpressionOrInt:
        """
        Evaluate parameters, making them ints if possible.

        Parameters
        ----------
        variable_dict
            a dictionary of taking either single-term monomials or string (variable names) to ints

        Returns
        -------
        evaluated expression
        """

        def eval_or_reduce(expression: ExpressionOrInt, var_dict) -> ExpressionOrInt:
            if isinstance(expression, Expression):
                evaled_expr = expression.eval(var_dict)
                if isinstance(evaled_expr, Expression):
                    if evaled_expr.is_constant():
                        return int(evaled_expr) % 3
                    else:
                        return evaled_expr
                elif is_integer(evaled_expr):
                    return evaled_expr % 3
                else:
                    raise ValueError("unknown error")
            elif is_integer(expression):
                return int(expression) % 3
            else:
                raise ValueError("unknown error")

        evaled_left_expr = eval_or_reduce(self._left_expression, variable_dict)
        evaled_right_expr = eval_or_reduce(self._right_expression, variable_dict)

        operations = {
            "PLUS": operator.add,
            "MINUS": operator.sub,
            "TIMES": operator.mul,
            "EXP": operator.pow,
        }
        if self._relation_name in operations:
            return operations[self._relation_name](evaled_left_expr, evaled_right_expr)
        else:
            raise Exception(f"cannot evaluate unknown binary op: {self._relation_name}")

    def __int__(self) -> int:
        if not self.is_constant():
            raise ValueError("non constant expressions can't be cast to ints")

        return cast(int, self.eval({}))

    def __str__(self):
        short_relation_names = {"PLUS": "+", "MINUS": "-", "TIMES": "*", "EXP": "^"}
        if self._relation_name in short_relation_names:
            short_relation_name = short_relation_names[self._relation_name]
        else:
            short_relation_name = "?"

        left_side = str(self._left_expression)
        if isinstance(self._left_expression, BinaryOperation):
            left_side = "(" + left_side + ")"

        right_side = str(self._right_expression)
        if isinstance(self._right_expression, BinaryOperation):
            right_side = "(" + right_side + ")"

        return left_side + short_relation_name + right_side

    __repr__ = __str__

    def as_c_expression(self):
        if is_integer(self._left_expression):
            left_c_expr = str(self._left_expression)
        else:
            left_c_expr = self._left_expression.as_c_expression()

        if is_integer(self._right_expression):
            right_c_expr = str(self._right_expression)
        else:
            right_c_expr = self._right_expression.as_c_expression()

        if self._relation_name == "PLUS":
            return "(" + left_c_expr + ")+(" + right_c_expr + ")"

        elif self._relation_name == "MINUS":
            return "(" + left_c_expr + ")-(" + right_c_expr + ")"

        elif self._relation_name == "TIMES":
            return "(" + left_c_expr + ")*(" + right_c_expr + ")"

        elif self._relation_name == "EXP":
            return "mod3pow(" + left_c_expr + "," + right_c_expr + ")"

        else:
            raise Exception("Unknown binary relation: " + self._relation_name)

    def as_polynomial(self):
        if is_integer(self._left_expression):
            left_poly = self._left_expression
        else:
            left_poly = self._left_expression.as_polynomial()

        if is_integer(self._right_expression):
            right_poly = self._right_expression
        else:
            right_poly = self._right_expression.as_polynomial()

        if self._relation_name == "PLUS":
            return left_poly + right_poly

        elif self._relation_name == "MINUS":
            return left_poly - right_poly

        elif self._relation_name == "TIMES":
            return left_poly * right_poly

        elif self._relation_name == "EXP":
            # simplify the exponent = 0, 1 cases
            if is_integer(right_poly):
                if right_poly == 0:
                    return 1
                elif right_poly == 1:
                    return left_poly
                else:
                    return left_poly ** right_poly
            else:
                return left_poly ** right_poly
        else:
            raise Exception("Unknown binary relation: " + self._relation_name)

    # def as_sympy(self):
    #     """
    #     Convert to sympy expression
    #     Returns
    #     -------
    #     sympy expression
    #     """
    #
    #     def simple_pow(left_exp, right_exp):
    #         # simplify the exponent = 0, 1 cases
    #         if is_integer(right_exp):
    #             if right_exp == 0:
    #                 return 1
    #             elif right_exp == 1:
    #                 return left_exp
    #             else:
    #                 return left_exp ** right_exp
    #         else:
    #             return left_exp ** right_exp
    #
    #     relations = {'PLUS': operator.add,
    #                  'MINUS': operator.sub,
    #                  'TIMES': operator.mul,
    #                  'EXP': simple_pow}
    #
    #     if self.relation_name not in relations:
    #         raise Exception("Unknown binary relation: " + self.relation_name)
    #
    #     lhs = (self._left_expression if is_integer(self._left_expression)
    #            else self._left_expression.as_sympy())
    #     rhs = (self._right_expression if is_integer(self._right_expression)
    #            else self._right_expression.as_sympy())
    #
    #     return relations[self.relation_name](lhs, rhs)

    def as_numpy_str(self, variables) -> str:
        """
        Convert to numpy function
        Parameters
        ----------
        variables

        Returns
        -------
        str version of numpy function
        """

        relations = {
            "PLUS": "(({0})+({1}))",
            "MINUS": "(({0})-({1}))",
            "TIMES": "(({0})*({1}))",
            "EXP": "(({0})**({1}))",
        }

        if self._relation_name not in relations:
            raise Exception("Unknown binary relation: " + self._relation_name)

        lhs = (
            str(self._left_expression)
            if is_integer(self._left_expression)
            else self._left_expression.as_numpy_str(variables)
        )
        rhs = (
            str(self._right_expression)
            if is_integer(self._right_expression)
            else self._right_expression.as_numpy_str(variables)
        )

        return relations[self._relation_name].format(lhs, rhs)

    def _make_inner_mathml(self) -> Tag:
        apply_tag = Tag(name="apply", is_xml=True)

        mathml_relations = {
            "PLUS": Tag(name="plus", is_xml=True, can_be_empty_element=True),
            "MINUS": Tag(name="minus", is_xml=True, can_be_empty_element=True),
            "TIMES": Tag(name="times", is_xml=True, can_be_empty_element=True),
            "EXP": Tag(name="power", is_xml=True, can_be_empty_element=True),
        }

        if self._relation_name in mathml_relations:
            apply_tag.append(mathml_relations[self._relation_name])

            if (
                isinstance(self._left_expression, Expression)
                and not self._left_expression.is_constant()
            ):
                apply_tag.append(self._left_expression._make_inner_mathml())
            else:
                apply_tag.append(inner_mathml_constant(int(self._left_expression)))

            if (
                isinstance(self._right_expression, Expression)
                and not self._right_expression.is_constant()
            ):
                apply_tag.append(self._right_expression._make_inner_mathml())
            else:
                apply_tag.append(inner_mathml_constant(int(self._right_expression)))
        else:
            raise NotImplementedError(
                f"_inner_mathml() unimplemented for {self._relation_name} in {type(self)}"
            )

        return apply_tag

    def get_variable_set(self) -> Set[str]:
        var_set = set()
        if not is_integer(self._left_expression):
            var_set = var_set.union(self._left_expression.get_variable_set())
        if not is_integer(self._right_expression):
            var_set = var_set.union(self._right_expression.get_variable_set())
        return var_set


class UnaryRelation(Expression):
    def __init__(self, relation_name, expr):
        self._relation_name = relation_name
        self._expr: ExpressionOrInt = expr

    def rename_variables(self, name_dict: Dict[str, str]):
        return UnaryRelation(
            relation_name=self._relation_name, expr=rename_helper(self._expr, name_dict)
        )

    def is_constant(self) -> bool:
        return self._expr.is_constant()

    def eval(self, variable_dict):
        if self._relation_name == "MINUS":
            if is_integer(self._expr):
                return (-1) * self._expr
            elif type(self._expr) == Expression:
                evaluated_subexpression = self._expr.eval(variable_dict)
                if (
                    is_integer(evaluated_subexpression)
                    or evaluated_subexpression.is_constant()
                ):
                    return mod_3((-1) * int(evaluated_subexpression))
                else:
                    return (-1) * evaluated_subexpression
        else:
            raise Exception(
                "UnaryRelation in bad state with unknown unary relation name"
            )

    def __int__(self) -> int:
        if not self.is_constant():
            raise ValueError("non constant expressions can't be cast to ints")

        return cast(int, self.eval({}))

    def __str__(self) -> str:
        short_rel_name = str(self._relation_name)
        if self._relation_name == "MINUS":
            short_rel_name = "-"
        return short_rel_name + (
            "(" + str(self._expr) + ")"
            if type(self._expr) == BinaryOperation
            else str(self._expr)
        )

    __repr__ = __str__

    def as_c_expression(self):
        if is_integer(self._expr):
            c_exp = str(mod_3(self._expr))
        else:
            c_exp = self._expr.as_c_expression()

        if self._relation_name == "MINUS":
            return "-(" + c_exp + ")"
        else:
            raise Exception("Unknown binary relation: " + self._relation_name)

    def as_polynomial(self):
        if is_integer(self._expr) or self._expr.is_constant():
            poly = mod_3(int(self._expr))
        else:
            poly = self._expr.as_polynomial()

        if self._relation_name == "MINUS":
            return (-1) * poly
        else:
            raise Exception("Unknown unary relation: " + self._relation_name)

    # def as_sympy(self):
    #     """
    #     Convert to sympy expression
    #     Returns
    #     -------
    #     sympy expression
    #     """
    #
    #     relations = {"MINUS": operator.neg}
    #
    #     if self._relation_name not in relations:
    #         raise Exception("Unknown unary relation: " + self._relation_name)
    #
    #     expr = self._expr if is_integer(self._expr) else self._expr.as_sympy()
    #
    #     return relations[self._relation_name](expr)

    def as_numpy_str(self, variables):
        """
        Convert to numpy function
        Parameters
        ----------
        variables

        Returns
        -------
        str numpy-representation
        """

        relations = {"MINUS": "(-({0}))"}

        if self._relation_name not in relations:
            raise Exception("Unknown unary relation: " + self._relation_name)

        expr_str = (
            str(self._expr)
            if is_integer(self._expr)
            else self._expr.as_numpy_str(variables)
        )

        return relations[self._relation_name].format(expr_str)

    def _make_inner_mathml(self) -> Tag:
        apply_tag = Tag(name="apply", is_xml=True)

        mathml_relations = {
            "MINUS": Tag(name="minus", is_xml=True, can_be_empty_element=True),
        }

        if self._relation_name in mathml_relations:
            apply_tag.append(mathml_relations[self._relation_name])

            if isinstance(self._expr, Expression) and not self._expr.is_constant():
                apply_tag.append(self._expr._make_inner_mathml())
            else:
                apply_tag.append(inner_mathml_constant(int(self._expr)))
        else:
            raise NotImplementedError(
                f"_inner_mathml() unimplemented for {self._relation_name} in {type(self)}"
            )

        return apply_tag

    def get_variable_set(self) -> Set[str]:
        if is_integer(self._expr):
            return set()
        else:
            return self._expr.get_variable_set()


####################################################################################################


@attrs(init=False, eq=False, repr=False, str=False, order=False)
class Monomial(Expression):
    """A class to encapsulate monomials reduced by x^3-x==0 for all variables x"""

    _power_dict: Dict[str, int] = attrib()

    def __init__(self, power_dict: Dict[str, int]):
        # copy over only those terms which actually appear
        self._power_dict = {
            str(var): power_dict[var] for var in power_dict if power_dict[var] != 0
        }
        for var in self._power_dict.keys():
            # while self._power_dict[var] < 0:
            #    self._power_dict[var] += 2     <--- replace with below
            assert self._power_dict[var] > 0  # b/c x^-1 isn't exactly x (i.e. when x=0)
            # while self._power_dict[var] >= 3:
            #    self._power_dict[var] -= 2     <--- replace with below
            self._power_dict[var] = 1 + ((-1 + self._power_dict[var]) % 2)

    def rename_variables(self, name_dict: Dict[str, str]):
        # this ends up a little more complicated than I was originally thinking, b/c
        # I would like to allow two variables to be updated to the same new name
        renamed_dict = dict()
        for variable, exponent in self._power_dict.items():
            name = variable
            if variable in name_dict:
                name = name_dict[variable]
            if name in renamed_dict:
                renamed_dict[name] += self._power_dict[variable]
                renamed_dict[name] = 1 + ((-1 + renamed_dict[name]) % 2)
            else:
                renamed_dict[name] = self._power_dict[variable]
        return Monomial(power_dict=renamed_dict)

    def as_polynomial(self):
        return self

    def is_constant(self) -> bool:
        return len(self._power_dict) == 0

    def num_variables(self):
        return len(self._power_dict)

    def variable_list(self):
        return self._power_dict.keys()

    def eval(self, variable_dict: Dict) -> Expression:
        """
        Evaluates the monomial.

        Parameters
        ----------
        variable_dict
            variable_dict is expected to be a dict containing str:Expression or
            Monomial:Expression pairs. The latter are constrained to be of single-variable type.

        Returns
        -------
        Expression
        """
        if type(variable_dict) != dict:
            raise Exception("eval is not defined on this input")

        # sanitize inputs
        sanitized_variable_dict = dict()
        for variable, quantity in variable_dict.items():
            if type(variable) == str:
                sanitized_variable_dict.update({variable: variable_dict[variable]})
            elif type(variable) == Monomial:
                if variable.num_variables() != 1:
                    raise Exception(
                        "We do not know how to evaluate monomials of zero or"
                        " several variables to a single number"
                    )
                else:
                    variable_as_str = list(variable.variable_list())[0]
                    sanitized_variable_dict.update(
                        {variable_as_str: variable_dict[variable]}
                    )
        variable_dict = sanitized_variable_dict

        accumulator = Mod3Poly.one()
        for variable, quantity in self._power_dict.items():
            if variable in variable_dict.keys():
                accumulator *= variable_dict[variable] ** self._power_dict[variable]
            else:
                accumulator *= Monomial.as_var(variable) ** self._power_dict[variable]

        return accumulator

    def __int__(self) -> int:
        if not self.is_constant():
            raise ValueError("non constant expressions can't be cast to ints")

        return cast(int, self.eval({}))

    def get_variable_set(self) -> Set[str]:
        """returns a set containing all variable which occur in this monomial"""
        return {var for var in self._power_dict if self._power_dict[var] != 0}

    @staticmethod
    def unit():
        """produces the unit, 1, as a monomial"""
        return Monomial(dict())

    @staticmethod
    def as_var(var_name: str):
        return Monomial({var_name: 1})

    def __mul__(self, other) -> Expression:
        if isinstance(other, Monomial):
            result_power_dict = self._power_dict.copy()
            for key in other._power_dict.keys():
                if key in result_power_dict.keys():
                    result_power_dict[key] += other._power_dict[key]
                    while result_power_dict[key] >= 3:
                        result_power_dict[key] -= 2
                else:
                    result_power_dict[key] = other._power_dict[key]
            return Monomial(result_power_dict)
        elif isinstance(other, Mod3Poly) or is_integer(other):
            return self.as_poly() * other
        else:
            return BinaryOperation("TIMES", self, other)

    __rmul__ = __mul__

    def __neg__(self):
        return (-1) * self

    def __pow__(self, power: ExpressionOrInt, **kwargs):
        if type(power) != int:
            if power.is_constant():
                power = int(power)
            else:
                raise NotImplementedError(
                    "Cannot raise an Expression to a non-integer power"
                )

        if power == 0:
            return Monomial.unit()
        elif power == 1:
            return self
        elif power == 2:
            return self * self
        # Now handle higher powers; probably not going to happen too much for this application

        # (int) half power root
        int_root = self ** (power // 2)
        if power % 2 == 0:
            return int_root * int_root
        else:
            return int_root * int_root * self

    def as_poly(self):
        """converts this monomial to a polynomial with only one term"""
        return Mod3Poly({self: 1})

    def __add__(self, other):
        if isinstance(other, Mod3Poly):
            return other + self.as_poly()
        elif isinstance(other, Monomial):
            return self.as_poly() + other.as_poly()
        elif is_integer(other):
            return self.as_poly() + other
        elif isinstance(other, Expression):
            return BinaryOperation("PLUS", self, other)
        else:
            raise TypeError(
                "unsupported operand type(s) for +: '{}' and '{}'".format(
                    self.__class__, type(other)
                )
            )

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + ((-1) * other)

    def __rsub__(self, other):
        return ((-1) * self) + other

    def __eq__(self, other):
        if type(other) == str:
            other = Monomial.as_var(other)
        if type(other) == Monomial:
            return self._power_dict == other._power_dict
        elif type(other) == Mod3Poly:
            if len(other.coeff_dict) == 1:
                monomial, coeff = list(other.coeff_dict)[0]
                return coeff == 1 and monomial == self
            else:
                return False
        elif is_integer(other) and self == Monomial.unit():
            return other == 1
        else:
            return False

    def __ne__(self, other):
        if type(other) == str:
            other = Monomial.as_var(other)
        return not (self == other)

    def __lt__(self, other):
        self_vars = set(self._power_dict.keys())
        if type(other) == str:
            other = Monomial.as_var(other)
        other_vars = set(other._power_dict.keys())
        # if we have a var that they don't we cannot be "smaller"
        if len(self_vars - other_vars) > 0:
            return False
        # check that we do not exceed and are smaller at least once
        at_least_once_less = False
        for var in self_vars:
            if self._power_dict[var] > other._power_dict[var]:
                return False
            elif self._power_dict[var] < other._power_dict[var]:
                at_least_once_less = True
        return at_least_once_less or len(other_vars - self_vars) > 0

    def __le__(self, other):
        self_vars = set(self._power_dict.keys())
        if type(other) == str:
            other = Monomial.as_var(other)
        other_vars = set(other._power_dict.keys())
        # if we have a var that they don't we cannot be "smaller"
        if len(self_vars - other_vars) > 0:
            return False
        # check that we do not exceed
        for var in self_vars:
            if self._power_dict[var] > other._power_dict[var]:
                return False
        return True

    def __gt__(self, other):
        self_vars = set(self._power_dict.keys())
        if type(other) == str:
            other = Monomial.as_var(other)
        other_vars = set(other._power_dict.keys())
        # if they have a var that they don't we cannot be "greater"
        if len(other_vars - self_vars) > 0:
            return False
        # check that we are not smaller and are greater at least once
        at_least_once_greater = False
        for var in other_vars:
            if self._power_dict[var] < other._power_dict[var]:
                return False
            elif self._power_dict[var] > other._power_dict[var]:
                at_least_once_greater = True
        return at_least_once_greater or len(self_vars - other_vars) > 0

    def __ge__(self, other):
        self_vars = set(self._power_dict.keys())
        if type(other) == str:
            other = Monomial.as_var(other)
        other_vars = set(other._power_dict.keys())
        # if they have a var that they don't we cannot be "greater"
        if len(other_vars - self_vars) > 0:
            return False
        # check that we are not smaller
        for var in other_vars:
            if self._power_dict[var] < other._power_dict[var]:
                return False
        return True

    def __hash__(self):
        return sum(hash(k) for k in self._power_dict.keys()) + sum(
            hash(v) for v in self._power_dict.values()
        )

    def __str__(self):
        if self._power_dict == {}:
            return "1"
        else:
            variables = sorted(self._power_dict.keys())
            return "*".join(
                [
                    str(var) + "^" + str(self._power_dict[var])
                    if self._power_dict[var] > 1
                    else str(var)
                    for var in variables
                ]
            )

    __repr__ = __str__

    def as_c_expression(self):
        if self._power_dict == {}:
            return "1"
        else:
            variables = sorted(self._power_dict.keys())
            return "*".join(
                [
                    "mod3pow(" + str(var) + "," + str(self._power_dict[var]) + ")"
                    if self._power_dict[var] > 1
                    else str(var)
                    for var in variables
                    if self._power_dict[var] != 0
                ]
            )

    # def as_sympy(self):
    #     # sympy empty product is 1, consistent with power_dict
    #     return sympy.prod([sympy.Symbol(var, integer=True) ** pow
    #                        for var, pow in self._power_dict.items()])
    # Fun fact: sympy doesn't recognize Symbol(var) and Symbol(var, integer=True) to be the same

    def as_numpy_str(self, variables) -> str:
        if len(self._power_dict) == 0:
            return "1"

        return (
            "("
            + "*".join(
                [
                    "1"
                    if self._power_dict[var] == 0
                    else f"state[{variables.index(var)}]"
                    if self._power_dict[var] == 1
                    else f"(state[{variables.index(var)}]**{self._power_dict[var]})"
                    for var in self._power_dict
                ]
            )
            + ")"
        )

    def _make_inner_mathml(self) -> Tag:
        if len(self._power_dict) == 0:
            return inner_mathml_constant(1)

        if len(self._power_dict) == 1:
            # we don't need an enclosing product when there is only a single variable^power
            var, power = list(self._power_dict.items())[0]
            return single_var_to_power_inner_mathml(var, power)

        apply_tag = Tag(name="apply", is_xml=True)
        product_tag = Tag(name="times", is_xml=True, can_be_empty_element=True)
        apply_tag.append(product_tag)

        for var, power in self._power_dict.items():
            apply_tag.append(single_var_to_power_inner_mathml(var, power))

        return apply_tag


####################################################################################################


@attrs(init=False, repr=False, str=False, eq=False)
class Mod3Poly(Expression):
    """a sparse polynomial class"""

    coeff_dict: Dict[Monomial, int] = attrib()

    def __init__(self, coeffs: Union[Dict, int]):
        if type(coeffs) == dict:
            self.coeff_dict = {
                monomial: coeffs[monomial]
                for monomial in coeffs
                if coeffs[monomial] != 0
            }
        elif is_integer(coeffs):
            self.coeff_dict = {Monomial.unit(): (coeffs % 3)}
        else:
            raise TypeError(
                "unsupported initialization type for '{}': '{}'".format(
                    self.__class__, type(coeffs)
                )
            )

    def rename_variables(self, name_dict: Dict[str, str]):
        return Mod3Poly(
            coeffs={
                monomial.rename_variables(name_dict): coeff
                for monomial, coeff in self.coeff_dict.items()
            }
        )

    @staticmethod
    def zero():
        return Mod3Poly({Monomial.unit(): 0})

    @staticmethod
    def one():
        return Mod3Poly({Monomial.unit(): 1})

    def as_polynomial(self):
        return self

    def __int__(self):
        self.__clear_zero_monomials()
        if len(self.coeff_dict) > 1 or (
            len(self.coeff_dict) == 1 and Monomial.unit() not in self.coeff_dict
        ):
            raise Exception("cannot cast non-constant polynomial to int")
        if Monomial.unit() in self.coeff_dict:
            return self.coeff_dict[Monomial.unit()]
        else:
            return 0

    def eval(self, variable_dict: Dict) -> ExpressionOrInt:
        """
        Evaluates the polynomial.

        Parameters
        ----------
        variable_dict
            variable_dict is expected to be a dict containing str:Expression or
            Monomial:Expression pairs. The latter are constrained to be of single-variable type.
        Returns
        -------
        Expression
        """
        if type(variable_dict) != dict:
            raise Exception("Mod3Poly.eval is not defined on this input")

        accumulator = Mod3Poly.zero()
        for monomial, coeff in self.coeff_dict.items():
            accumulator += coeff * monomial.eval(variable_dict)
        return accumulator

    def get_variable_set(self) -> Set[str]:
        """return a set containing all variables which occur in this polynomial"""
        var_set = set()
        for monomial in self.coeff_dict:
            var_set = var_set.union(monomial.get_variable_set())
        return var_set

    def __clear_zero_monomials(self):
        """purge unneeded data"""
        self.coeff_dict = {
            monomial: self.coeff_dict[monomial]
            for monomial in self.coeff_dict
            if self.coeff_dict[monomial] != 0
        }
        # assure at least one entry
        if len(self.coeff_dict) == 0:
            self.coeff_dict = {Monomial.unit(): 0}

    def is_constant(self) -> bool:
        # possibly unnecessary
        self.__clear_zero_monomials()
        num_nonzero_monomial = len(self.coeff_dict)
        if num_nonzero_monomial > 1:
            return False
        elif num_nonzero_monomial == 0:
            return True
        else:
            # only one entry
            return Monomial.unit() in self.coeff_dict

    def __eq__(self, other):
        if isinstance(other, int):
            return self.is_constant() and int(self) == other
        elif not isinstance(other, Expression):
            return False

        if not isinstance(other, Mod3Poly):
            other_as_poly: Mod3Poly = other.as_poly()
        else:
            other_as_poly = other

        for term in self.coeff_dict:
            if (
                term not in other_as_poly.coeff_dict
                or (self.coeff_dict[term] - other_as_poly.coeff_dict[term]) % 3 != 0
            ):
                return False

        for term in other_as_poly.coeff_dict:
            if (
                term not in self.coeff_dict
                or (self.coeff_dict[term] - other_as_poly.coeff_dict[term]) % 3 != 0
            ):
                return False

        return True

    def __getitem__(self, index):
        if index in self.coeff_dict:
            return self.coeff_dict[index]
        else:
            return 0

    def __setitem__(self, index, value):
        self.coeff_dict[index] = value

    def __add__(self, other):
        if is_integer(other):
            self_copy = Mod3Poly(self.coeff_dict)
            self_copy[Monomial.unit()] = (self_copy[Monomial.unit()] + other) % 3
            return self_copy
        elif isinstance(other, Monomial):
            self_copy = Mod3Poly(self.coeff_dict)
            self_copy[other] += 1
            return self_copy
        elif isinstance(other, Mod3Poly):
            self_copy = Mod3Poly(self.coeff_dict)
            for key in other.coeff_dict.keys():
                if key in self_copy.coeff_dict.keys():
                    self_copy[key] = (self_copy[key] + other[key]) % 3
                else:
                    self_copy[key] = other[key]
            return self_copy
        elif isinstance(other, Expression):
            return BinaryOperation("PLUS", self, other)
        else:
            raise TypeError(
                "unsupported operand type(s) for +: '{}' and '{}'".format(
                    self.__class__, type(other)
                )
            )

    __radd__ = __add__

    def __sub__(self, other):
        if is_integer(other):
            self_copy = Mod3Poly(self.coeff_dict)
            self_copy[Monomial.unit()] = (self_copy[Monomial.unit()] - other) % 3
            return self_copy
        elif isinstance(other, Mod3Poly) or isinstance(other, Monomial):
            self_copy = Mod3Poly(self.coeff_dict)
            if isinstance(other, Monomial):
                other = other.as_poly()
            for key in other.coeff_dict.keys():
                if key in self_copy.coeff_dict.keys():
                    self_copy[key] = (self_copy[key] - other[key]) % 3
                else:
                    self_copy[key] = other[key]
            return self_copy
        else:
            raise TypeError(
                "unsupported operand type(s) for +: '{}' and '{}'".format(
                    self.__class__, type(other)
                )
            )

    def __rsub__(self, other):
        return other + ((-1) * self)

    def __mul__(self, other):
        if is_integer(other):
            return Mod3Poly(
                {key: (self.coeff_dict[key] * other) % 3 for key in self.coeff_dict}
            )
        elif isinstance(other, Monomial):
            return Mod3Poly(
                {
                    (other * monomial): self.coeff_dict[monomial]
                    for monomial in self.coeff_dict
                }
            )
        elif isinstance(other, Mod3Poly):
            accumulator = Mod3Poly.zero()
            for self_mono, other_mono in product(
                self.coeff_dict.keys(), other.coeff_dict.keys()
            ):
                monomial_prod = self_mono * other_mono
                accumulator[monomial_prod] = (
                    accumulator[monomial_prod] + self[self_mono] * other[other_mono]
                ) % 3
            return accumulator
        else:
            return BinaryOperation("TIMES", self, other)

    __rmul__ = __mul__

    def __pow__(self, power, **kwargs):
        if type(power) == Mod3Poly and power.is_constant():
            power = power[Monomial.unit()]
        assert is_integer(power)
        if power == 0:
            return Monomial.unit().as_poly()
        elif power == 1:
            return self
        elif power == 2:
            return self * self
        # Now handle higher powers; probably not going to happen too much for this application

        # (int) half power root
        int_root = self ** (power // 2)
        if power % 2 == 0:
            return int_root * int_root
        else:
            return int_root * int_root * self

    def __str__(self):
        accumulator = ""
        for monomial in sorted(self.coeff_dict.keys()):
            if monomial == Monomial.unit():
                if self[monomial] != 0:
                    accumulator += str(self[monomial])
            else:
                if len(accumulator) > 0 and self[monomial] != 0:
                    accumulator += "+"
                if self[monomial] == 1:
                    accumulator += str(monomial)
                elif self[monomial] == 2:
                    accumulator += "2*"
                    accumulator += str(monomial)
        if len(accumulator) > 0:
            return accumulator
        else:
            return "0"

    __repr__ = __str__

    def as_c_expression(self):
        accumulator = ""
        for monomial in sorted(self.coeff_dict.keys()):
            if monomial == Monomial.unit():
                if self[monomial] != 0:
                    accumulator += str(self[monomial])
            else:
                if len(accumulator) > 0 and self[monomial] != 0:
                    accumulator += "+"
                if self[monomial] == 1:
                    accumulator += monomial.as_c_expression()
                elif self[monomial] == 2:
                    accumulator += "2*"
                    accumulator += monomial.as_c_expression()
        if len(accumulator) > 0:
            return accumulator
        else:
            return "0"

    # def as_sympy(self):
    #     return sum([coeff * expr.as_sympy() for expr, coeff in self.coeff_dict.items()])

    def as_numpy_str(self, variables) -> str:
        return (
            "("
            + "+".join(
                [
                    "({0}*({1}))".format(coeff, expr.as_numpy_str(variables))
                    for expr, coeff in self.coeff_dict.items()
                ]
            )
            + ")"
        )

    def _make_inner_mathml(self) -> Tag:

        num_terms = len(self.coeff_dict)

        if num_terms == 0:
            return inner_mathml_constant(0)
        elif num_terms == 1:
            monomial, coefficient = list(self.coeff_dict.items())[0]
            if monomial.is_constant():
                return inner_mathml_constant(coefficient)
            apply_tag = Tag(name="apply", is_xml=True)
            apply_tag.append(Tag(name="times", is_xml=True, can_be_empty_element=True))
            apply_tag.append(inner_mathml_constant(coefficient))
            # noinspection PyProtectedMember
            apply_tag.append(monomial._make_inner_mathml())
            return apply_tag
        else:
            top_apply_tag = Tag(name="apply", is_xml=True)
            top_apply_tag.append(
                Tag(name="plus", is_xml=True, can_be_empty_element=True)
            )
            for monomial, coefficient in self.coeff_dict.items():
                if coefficient == 0:
                    top_apply_tag.append(inner_mathml_constant(0))
                elif coefficient == 1:
                    # noinspection PyProtectedMember
                    top_apply_tag.append(monomial._make_inner_mathml())
                elif monomial.is_constant():
                    top_apply_tag.append(inner_mathml_constant(coefficient))
                else:
                    inner_apply_tag = Tag(name="apply", is_xml=True)
                    inner_apply_tag.append(
                        Tag(name="times", is_xml=True, can_be_empty_element=True)
                    )
                    inner_apply_tag.append(inner_mathml_constant(coefficient))
                    # noinspection PyProtectedMember
                    inner_apply_tag.append(monomial._make_inner_mathml())
                    top_apply_tag.append(inner_apply_tag)
            return top_apply_tag
