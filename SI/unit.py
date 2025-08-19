from .unitsystem import UnitSystem
from collections import defaultdict
import re

class Unit:
    def __init__(self, name, factor=1.0, base_units=None, prefer_derived=True):
        self.name = name
        self.factor = factor
        self.prefer_derived = prefer_derived
        self._unitdict_raw = None

        expr = name.strip()
        # 判断是否有乘除等运算符
        if not any(op in expr for op in ('*', '·', '/', '(', ')', '^')):
            # 没有运算符，直接用_basical_unit
            u = self._basical_unit(expr)
            self.name = u.name
            self.factor = u.factor
            self.base_units = u.base_units
            self._unitdict_raw = u._unitdict_raw
            return
        if base_units is None:
            # 新增：用表达式解析器
            u = self.parse_expr(name)
            self.name = u.name
            self.factor = u.factor
            self.base_units = u.base_units
            self._unitdict_raw = u._unitdict_raw
        else:
            self.base_units = dict(base_units)  # <--- 补上这句，确保是字典
            self._unitdict_raw = {k: v for k, v in base_units.items() if v != 0}
    @classmethod
    def parse_expr(cls, expr):
        """
        解析复杂单位表达式，返回Unit对象
        支持括号、乘除、幂次
        """
        def to_rpn(expr):
            # 表达式转逆波兰
            expr = expr.replace(' ', '')
            tokens = re.findall(r'[A-Za-zμ1]+(?:\^\-?\d+)?|\d+|[·*/()]', expr)
            output = []
            stack = []
            precedence = {'*': 1, '·': 1, '/': 1}
            for token in tokens:
                if re.match(r'[A-Za-zμ1]+(?:\^\-?\d+)?', token):
                    output.append(token)
                elif token in ('*', '·', '/'):
                    while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence[token]:
                        output.append(stack.pop())
                    stack.append(token)
                elif token == '(':
                    stack.append(token)
                elif token == ')':
                    while stack and stack[-1] != '(':
                        output.append(stack.pop())
                    stack.pop()
            while stack:
                output.append(stack.pop())
            return output

        def eval_rpn(rpn):
            stack = []
            for token in rpn:
                if re.match(r'[A-Za-zμ1]+(?:\^\-?\d+)?', token):
                    if '^' in token:
                        base, exp = token.split('^')
                        u = Unit(base)
                        stack.append(u ** int(exp))
                    else:
                        stack.append(Unit(token))
                elif token in ('*', '·'):
                    if len(stack) < 2:
                        raise ValueError(f"Invalid expression: not enough operands for '{token}'")
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a * b)
                elif token == '/':
                    if len(stack) < 2:
                        raise ValueError(f"Invalid expression: not enough operands for '/'")
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a / b)
            if len(stack) != 1:
                raise ValueError(f"Invalid expression: leftover stack {stack}")
            return stack[0]

        rpn = to_rpn(expr)
        # print(f"RPN: {rpn}")
        return eval_rpn(rpn)

    def _build_from_unitdict(self):
        """
        根据 _unitdict_raw 展开到基本单位，并计算总 factor。
        """
        expanded = defaultdict(int)
        total_factor = self.factor   # 外部可能已乘过一个因子

        for unit, exp in self._unitdict_raw.items():
            if unit == '1':
                continue

            # f, base 
            baseunit = self._basical_unit(unit)
            f= baseunit.factor
            base = baseunit.base_units
            total_factor *= f ** exp
            for b, e in base.items():
                expanded[b] += e * exp
        # 清除指数为0的单位
        expanded = {k: v for k, v in expanded.items() if v != 0 and k != '1'}
        if not expanded:
            expanded = {'1': 1} 
        
        self.base_units = dict(expanded)
        self.factor = total_factor
        # self.base_units = self._unitdict_expanded


    @classmethod
    def _from_unitdict(cls, unitdict):
        unitdict = {k: v for k, v in unitdict.items() if v != 0}
        obj = cls.__new__(cls)   # 跳过 __init__
        obj._unitdict_raw = dict(unitdict)
        obj.name = UnitSystem.units_to_string(unitdict)
        obj.factor = 1.0
        obj._build_from_unitdict()
        return obj

    @classmethod
    def _basical_unit(cls,unit_name):

        if unit_name == '1':
            obj = cls.__new__(cls)
            obj._unitdict_raw = {'1': 1}
            obj.name = '1'
            obj.factor = 1.0
            obj.base_units = {'1': 1}
            return obj
    
        obj = cls.__new__(cls)
        obj._unitdict_raw = dict({unit_name: 1})
        obj.name = unit_name

        if unit_name in UnitSystem.BASE_UNITS:
            obj.factor = 1.0
            obj.base_units = {unit_name: 1}
            return obj

        if unit_name in UnitSystem.DERIVED_UNITS:
            factor, base = UnitSystem.DERIVED_UNITS[unit_name]
            obj.factor = factor
            obj.base_units = base.copy()
            return obj

        if unit_name in UnitSystem.English_UNITS:
            factor, base = UnitSystem.English_UNITS[unit_name]
            obj.factor = factor
            obj.base_units = base.copy()
            return obj

        # 带词头单位
        for prefix, factor in sorted(UnitSystem.PREFIXES.items(), key=lambda x: -len(x[0])):
            if unit_name.startswith(prefix):
                base_name = unit_name[len(prefix):]
                baseunit = Unit._basical_unit(base_name)
                obj.factor = factor * baseunit.factor
                obj.base_units = baseunit.base_units.copy()
                return obj
                # return factor * f, base

        raise ValueError(f"Undefined unit: {unit_name}")
    def to_derived_unit(self):
        """
        返回 (换算因子, 导出单位)
        """
        # 单量纲且只有1阶
        new_base = {k: v for k, v in self._unitdict_raw.items() if v != 0 and k != '1'}
        if len(new_base) == 1 and sum(new_base.values()) == 1:
            return 1, self

        normalized_base = {k: v for k, v in sorted(self.base_units.items()) if v != 0}
        if len(normalized_base) == 1 and sum(normalized_base.values()) == 1:
            unit_name = next(iter(normalized_base))
            return self.factor, Unit(unit_name)
        #     return 1, self
        # 1. 首先尝试查找精确匹配
        for unit_name, (factor, unit_def) in UnitSystem.DERIVED_UNITS.items():
            if unit_def == normalized_base:
                return self.factor/factor, Unit(unit_name)

        if not normalized_base or normalized_base == {'1': 1}:
            return 1, Unit("1")

        # 量纲约化
        units_temp = {}
        for unit_name, exp in self._unitdict_raw.items():
            if exp != 0:
                kt = 0
                for unit, exp2 in units_temp.items():
                    if Unit(unit).is_compatible(unit_name):
                        units_temp[unit] += exp
                        kt = 1
                        break
                if not kt:
                    units_temp[unit_name] = exp
        uunit = Unit._from_unitdict(units_temp)
        return self.factor / uunit.factor, uunit
    # def to_derived_unit(self):
    #     return self.convert_to(UnitSystem.find_derived_unit(self))

    def to_base_units(self):
        # """转换为基本单位表示，返回Quantity对象"""
        name = UnitSystem.units_to_string(self.base_units)
        base_unit = Unit(name)
        return self.factor, base_unit
    
    def convert_to(self, target_unit):
        """转换到目标单位"""
        if not isinstance(target_unit, Unit):
            target_unit = Unit(target_unit)
        if not self.is_compatible(target_unit):
            raise ValueError(f"Incompatible units: {self} and {target_unit}")
        
        return self.factor / target_unit.factor
    
    def __rmul__(self, other):
        """支持标量 * 单位 (如 5 * m)"""
        from .quantity import Quantity
        return Quantity(other, self)
    
    def __mul__(self, other):
        if isinstance(other, Unit):
            new_base = defaultdict(int)
            for unit, exp in self._unitdict_raw.items():
                new_base[unit] += exp
            for unit, exp in other._unitdict_raw.items():
                new_base[unit] += exp
            # 清除指数为0的单位
            new_base = {k: v for k, v in new_base.items() if v != 0 and k != '1'}
            if not new_base:
                new_base = {'1': 1}
            return Unit._from_unitdict(new_base)
        elif isinstance(other, (int, float)):
            return other * self

    def __pow__(self, power):
        new_base = {unit: exp * power for unit, exp in self._unitdict_raw.items()}
        new_base = {k: v for k, v in new_base.items() if v != 0 and k != '1'}
        if not new_base:
            new_base = {'1': 1}
        return Unit._from_unitdict(new_base)
    
    def __truediv__(self, other):
        """支持单位 / 单位"""
        if isinstance(other, Unit):
            return self * (other ** -1)
        else:
            # 支持单位 / 标量 (如 m / 5)
            from .quantity import Quantity
            return Quantity(1.0 / other, self)
    
    def __rtruediv__(self, other):
        """支持标量 / 单位 (如 5 / m)"""
        from .quantity import Quantity
        return Quantity(other , (self ** -1))
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Unit('{self.name}', factor={self.factor}, base_units={self.base_units})"
    
    def __eq__(self, other):
        if not isinstance(other, Unit):
            return False
        return self.base_units == other.base_units and self.factor == other.factor
    
    def is_compatible(self, other):
        if not isinstance(other, Unit):
            other = Unit(other)
        if not isinstance(self.base_units, dict) or not isinstance(other.base_units, dict):
            raise TypeError("base_units must be dict for compatibility check")
        return self.base_units == other.base_units