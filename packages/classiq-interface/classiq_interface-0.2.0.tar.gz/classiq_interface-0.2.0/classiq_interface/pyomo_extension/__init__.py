import pyomo.core

from classiq_interface.pyomo_extension import (
    equality_expression,
    inequality_expression,
    set_pprint,
)

pyomo.core.expr.logical_expr.InequalityExpression.getname = (
    inequality_expression.getname
)

pyomo.core.expr.logical_expr.EqualityExpression.getname = equality_expression.getname

pyomo.core.base.set.Set._pprint_members = staticmethod(set_pprint.pprint_members)
