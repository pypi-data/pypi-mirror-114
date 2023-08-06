# -*- coding: utf-8 -*-
from typing import List, Callable, Any, Optional

from pip_services3_expressions.calculator.functions.IFunction import IFunction
from pip_services3_expressions.variants.IVariantOperations import IVariantOperations
from pip_services3_expressions.variants.Variant import Variant


class DelegatedFunction(IFunction):

    def __init__(self, name: str, calculator: Callable[[List[Variant], IVariantOperations], Variant],
                 context: Optional[Any] = None):
        """
        Constructs this function class with specified parameters.

        :param name: The name of this function.
        :param calculator: The function calculator delegate.
        """
        if name is None:
            raise Exception('Name parameter cannot be null')
        if calculator is None:
            raise Exception('Calculator parameter cannot be null')
        self.__name: str = name
        self.__calculator: Callable[[List[Variant], IVariantOperations], Variant] = calculator
        self.__context = context

    @property
    def name(self) -> str:
        """
        The function name.
        """
        return self.__name

    def __calculate_with_context(self, context: Any, params: List[Variant],
                                 variant_operations: IVariantOperations) -> Variant:
        # update context current object
        self.__dict__.update(context.__dict__)

        return self.__calculator(params, variant_operations)

    def calculate(self, params: List[Variant], variant_operations: IVariantOperations) -> Variant:
        """
        The function calculation method.
        
        :param params: an array with function parameters.
        :param variant_operations: Variants operations manager.
        :return: return function result.
        """
        if self.__context is None:
            return self.__calculator(params, variant_operations)
        else:
            return self.__calculate_with_context(self.__context, params, variant_operations)
