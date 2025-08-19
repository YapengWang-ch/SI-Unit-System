from .unit import Unit
from collections import defaultdict

class Quantity:
    """物理量类，包含数值和单位"""
    def __init__(self, value, unit):
        if not isinstance(unit, Unit):
            unit = Unit(unit)
        self.value = value
        self.unit = unit
    
    def to_derived_unit(self):
        """转换为匹配的导出单位表示"""
        # 先转换单位部分
        factor,dunit= self.unit.to_derived_unit()
        # 然后乘以数值
        return Quantity(self.value * factor, dunit)

    def to(self, target_unit):
        """转换到目标单位"""
        if not isinstance(target_unit, Unit):
            target_unit = Unit(target_unit)
        
        if not self.unit.is_compatible(target_unit):
            raise ValueError(f"Incompatible units: {self.unit} and {target_unit}")
        
        conversion_factor = self.unit.convert_to(target_unit)
        return Quantity(self.value * conversion_factor, target_unit)
    
    def toMeV(self):
        from .constants import Constants
        if self.unit.is_compatible(Unit("kg")):
            return (self*Constants.c**2).to("MeV")
        if self.unit.is_compatible(Unit("kg*m/s")):
            return (self*Constants.c).to("MeV")
        if self.unit.is_compatible(Unit("MeV")):
            return self.to("MeV")
        raise ValueError(f"Unit can't convert to MeV: {self.unit} ")
    
    def tonm(self):
        from .constants import Constants
        if self.unit.is_compatible(Unit("m")):
            return self.to("nm")
        elif self.unit.is_compatible(Unit("eV")):
            return (Constants.h*Constants.c/self).to("nm")
        raise ValueError(f"Unit can't convert to nm: {self.unit} ")
    
    def toeV(self):
        from .constants import Constants
        if self.unit.is_compatible(Unit("m")):
            return (Constants.h*Constants.c/self).to("eV")
        elif self.unit.is_compatible(Unit("eV")):
            return self.to("nm")
        raise ValueError(f"Unit can't convert to nm: {self.unit} ")
    
    def __mul__(self, other):
        if isinstance(other, Quantity):
            unit_mul=self.unit * other.unit
            return Quantity(self.value * other.value ,unit_mul).to_derived_unit()
        elif isinstance(other, Unit):
            unit_mul=self.unit * other
            return Quantity(self.value , unit_mul).to_derived_unit()
        else:
            return Quantity(self.value * other, self.unit)
    
    def __rmul__(self, other):
        return self * other
    
    def __truediv__(self, other):
        if isinstance(other, Quantity):
            unit_sub=self.unit / other.unit
            return Quantity(self.value / other.value, unit_sub).to_derived_unit()
        elif isinstance(other, Unit):
            return self*(1/other)
        else:
            return Quantity(self.value / other, self.unit)
    
    def __rtruediv__(self, other):
        return other * (self ** -1)
    
    def __add__(self, other):
        if other.unit.is_compatible(self.unit):
            return Quantity(self.value+other.to(self.unit).value,self.unit)
        raise ValueError(f"Unit {self.unit} & {other.unit} can't be added")

    def __sub__(self,other):
        if other.unit.is_compatible(self.unit):
            return Quantity(self.value-other.to(self.unit).value,self.unit)
        raise ValueError(f"Unit {self.unit} & {other.unit} can't be substracted")
    def __pow__(self, power):
        return Quantity((self.value ** power) , (self.unit ** power))
    
    def __str__(self):
        # 简化无量纲单位的显示
        if self.unit.name == '1':
            return f"{round(self.value,6)}"
        return f"{round(self.value,6)} {self.unit.name}"
    
    def __repr__(self):
        return f"Quantity({self.value}, {repr(self.unit)})"