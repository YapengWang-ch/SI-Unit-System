from collections import defaultdict
import re

class UnitSystem:
    # 七个基本物理量
    BASE_UNITS = {'m', 'kg', 's', 'A', 'K', 'mol', 'cd'}
    
    # 单位词头
    PREFIXES = {
        'Y': 1e24,   # yotta
        'Z': 1e21,   # zetta
        'E': 1e18,   # exa
        'P': 1e15,   # peta
        'T': 1e12,   # tera
        'G': 1e9,    # giga
        'M': 1e6,    # mega
        'k': 1e3,    # kilo
        # 'h': 1e2,    # hecto
        # 'da': 1e1,   # deca
        # 'd': 1e-1,   # deci
        # 'c': 1e-2,   # centi
        'm': 1e-3,   # milli
        'μ': 1e-6,   # micro
        'n': 1e-9,   # nano
        'p': 1e-12,  # pico
        'f': 1e-15,  # femto
        'a': 1e-18,  # atto
        'z': 1e-21,  # zepto
        'y': 1e-24,  # yocto
    }
    
    # 导出单位定义: {单位名: (换算因子, 基本单位表达式)}
    DERIVED_UNITS = {
        # 长度
        'cm': (0.01, {'m': 1}),
        'dm': (0.1, {'m': 1}),
        'AU': (149597870700, {'m': 1}),  # 天文单位
        'lyr': (9.4607e15, {'m': 1}),
        
        # 质量
        'g': (0.001, {'kg': 1}),
        't': (1000, {'kg': 1}),
        'u': (1.6606e-17, {'kg': 1}),
        
        # 时间
        'min': (60, {'s': 1}),
        'h': (3600, {'s': 1}),
        'day': (86400, {'s': 1}),
        'year': (31536000, {'s': 1}),
        
        # 速度        
        # 加速度
        # 'm/s²': (1, {'m': 1, 's': -2}),
        # 'g': (9.80665, {'m': 1, 's': -2}),
        
        # 力
        'N': (1, {'kg': 1, 'm': 1, 's': -2}),
        
        # 能量
        'J': (1, {'kg': 1, 'm': 2, 's': -2}),
        'eV': (1.602176634e-19, {'kg': 1, 'm': 2, 's': -2}),
        'cal': (4.184, {'kg': 1, 'm': 2, 's': -2}),
        'kWh': (3.6e6, {'kg': 1, 'm': 2, 's': -2}),
        
        # 功率
        'W': (1, {'kg': 1, 'm': 2, 's': -3}),
        
        # 压力
        'Pa': (1, {'kg': 1, 'm': -1, 's': -2}),
        'atm': (101325, {'kg': 1, 'm': -1, 's': -2}),
        
        # 频率
        'Hz': (1, {'s': -1}),
        
        # 电磁
        'C': (1, {'A': 1, 's': 1}),
        'V': (1, {'kg': 1, 'm': 2, 's': -3, 'A': -1}),
        'T': (1, {'kg': 1, 's': -2, 'A': -1}),
        'G': (1e-4, {'kg': 1, 's': -2, 'A': -1}),  # 高斯
        'Ohm': (1, {'kg': 1, 'm': 2, 's': -3, 'A': -2}),
        'Wb': (1, {'kg': 1, 'm': 2, 's': -2, 'A': -1}),
        'F': (1, {'kg': -1, 'm': -2, 's': 4, 'A': 2}),  # 法拉
        'H': (1, {'kg': 1, 'm': 2, 's': -2, 'A': -2}),  # 亨利
    }

    # 部分英制单位
    English_UNITS = {
        'inch': (0.0254, {'m': 1}),
        'foot': (0.3048, {'m': 1}),
        'mile': (1609.344, {'m': 1}),
        
        'pound': (0.45359237, {'kg': 1}),
        'ounce': (0.02834952, {'kg': 1}),

        'mph': (0.44704, {'m': 1, 's': -1}),  # 英里每小时
        'knot': (0.514444, {'m': 1, 's': -1}),  # 海里每小时

        'gallon': (3.785411784, {'m': 1}),  # 美制加仑
        'quart': (0.946352946, {'m': 1}),  # 美制夸脱
        'pint': (0.473176473, {'m': 1}),  # 美制品脱
    }
    # 单位别名映射
    UNIT_ALIASES = {
        '1/s': 'Hz',
        'kg·m/s^2': 'N',
        'N·m': 'J',
        'J/s': 'W',
        'kg/(m·s^2)': 'Pa',
        'C/s': 'A',
        'W/A': 'V',
        'J/C': 'V',
        'V/A': 'Ohm',
        'Wb/m^2': 'T',
        'J/kg': 'Gy',
    }
    
    # # 特殊字符映射
    # SPECIAL_CHARS = {
    #     '°': 'deg',
    #     '′': "'",
    #     '″': '"',
    #     'µ': 'μ',
    #     'Ohm': 'Ohm',
    # }
    
    @classmethod
    def is_base_unit(cls, unit_name):
        return unit_name in cls.BASE_UNITS
    
    @classmethod
    def get_unit_definition(cls, unit_name):
        return cls.DERIVED_UNITS.get(unit_name, None)
    

        # 4. 尝试匹配无量纲单位

    
    @classmethod
    def units_to_string(cls, base_units):
        """将基本单位表达式转换为字符串表示"""
        # 处理无量纲情况 
        if not base_units or all(exp == 0 for exp in base_units.values()):
            return '1'
        
        numerator = []
        denominator = []
        
        for unit, exp in sorted(base_units.items()):
            if unit == '1' or exp == 0:
                continue
            if exp > 0:
                if exp == 1:
                    numerator.append(unit)
                else:
                    numerator.append(f"{unit}^{exp}")
            elif exp < 0:
                abs_exp = abs(exp)
                if abs_exp == 1:
                    denominator.append(unit)
                else:
                    denominator.append(f"{unit}^{abs_exp}")
        
        num_str = '*'.join(numerator) if numerator else '1'
        den_str = '*'.join(denominator) if denominator else None
        
        if den_str:
            # 如果分母有多个单位，用括号括起来
            if len(denominator) > 1:
                return f"{num_str}/({den_str})"
            return f"{num_str}/{den_str}"
        return num_str