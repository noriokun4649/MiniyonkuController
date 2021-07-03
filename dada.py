import numpy as np
import matplotlib.pyplot as plt

fs = 44100  # サンプリング周波数
t = np.arange(0, 0.01, 1/fs)  # 離散化された時間
print(t)
