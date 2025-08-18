from SI import Unit, Quantity, Constants
from math import sqrt

# d= 10*Unit("cm")
# v= 2*Unit("m/s")
# t= d/v
# print(t.to("ms"))

# d=1.30*Unit("m")
# t=d/Constants.c*1.33
# print(t.to("ns"))

# s = 100 *Unit("cm^2")
# print(s**0.5)
# aa= 3 * Unit("s")
# print(aa.unit.base_units)

def test_complex_unit_ops():
    print("\n==== 复杂单位运算与转化 ====")
    # 1. 功率 = 力 * 速度
    force = Quantity(10, Unit("N"))         # 10 N
    velocity = Quantity(3, Unit("m/s"))     # 3 m/s
    power = force * velocity                # 应为 30 W
    print("power =", power, "->", power.to("W"))

    # 2. 压强 = 力 / 面积
    area = Quantity(2, Unit("m^2"))
    pressure = force / area                 # 应为 5 Pa
    print("pressure =", pressure, "->", pressure.to("Pa"))

    # 3. 能量 = 功率 * 时间
    time = Quantity(2, Unit("h"))           # 2 小时
    energy = power * time                   # 应为 30*2*3600 J
    print("energy =", energy, "->", energy.to("kWh"))

    # 4. 速度单位换算
    v1 = Quantity(36, Unit("km/h"))
    print("36 km/h =", v1.to("m/s"))

    # 5. 复杂单位表达式
    u = Unit("kg*m^2/(A^2*s^3)")
    print("u =", u)
    print("u base_units =", u.base_units)
    print("u factor =", u.factor)

    # 6. 词头与导出单位混合
    q = Quantity(1, Unit("kJ"))
    print("1 kJ =", q.to("J"))

    # 7. 复合单位乘除
    q1 = Quantity(2, Unit("N*m"))
    q2 = Quantity(4, Unit("J"))
    print(q1," == ", q1.to("J"))
    print(q2," == ", q2.to("N*m"))

    # 8. 无量纲
    q3 = Quantity(1, Unit("m") ) / Quantity(1, Unit("m"))
    print("m/m =", q3, "unit:", q3.unit)


if __name__ == "__main__":
    test_complex_unit_ops()