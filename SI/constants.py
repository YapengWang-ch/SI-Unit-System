from .quantity import Quantity
from .unit import Unit

class Constants:
    # 常用物理常数
    g = Quantity(9.80665, Unit('m/s^2'))  # 重力加速度
    h = Quantity(6.62607015e-34, Unit('J·s'))  # 普朗克常数
    c = Quantity(299792458, Unit('m/s'))  # 光速
    m_e = Quantity(9.10938356e-31, Unit('kg'))  # 电子质量
    m_p = Quantity(1.6726219e-27, Unit('kg'))  # 质子质量
    m_n = Quantity(1.6749286e-27, Unit('kg'))  # 中子质量
    alpha = Quantity(7.2973525693e-3, Unit('1'))  # 精细结构常数
    N_A = Quantity(6.02214076e23, Unit('1/mol'))  # 阿伏伽德罗常数
    R = Quantity(8.314462618, Unit('J/(mol·K)'))  # 理想气体常数
    k_B = Quantity(1.380649e-23, Unit('J/K'))  # 玻尔兹曼常数
    epsilon_0 = Quantity(8.854187817e-12, Unit('F/m'))  # 真空介电常数
    mu_0 = Quantity(1.256637062e-6, Unit('H/m'))  # 真空磁导率
    e = Quantity(1.602176634e-19, Unit('C'))  # 元电荷