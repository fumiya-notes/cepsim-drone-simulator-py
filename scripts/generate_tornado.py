import numpy as np

def generate_tornado(
    x_range=(-5, 5),
    y_range=(-5, 5),
    z_values=None,
    strength=5.0       # 強さの係数
):
    # z_valuesが指定されなければ0〜10で11層作る
    if z_values is None:
        z_values = list(range(0, 11))

    lines = []

    # ヘッダー
    lines.append("# Origin")
    lines.append("0,0,0")
    lines.append("")
    lines.append("# DataFormat")
    lines.append("1")
    lines.append("")
    lines.append("# PlatformNumber")
    lines.append("1")
    lines.append("")
    lines.append("# DataKind")
    lines.append("wind [m/s]")
    lines.append("")
    lines.append("# FlagLocationFixed")
    lines.append("1")
    lines.append("")
    lines.append("# Data")

    # データ本体
    for x in range(x_range[0], x_range[1] + 1):
        for y in range(y_range[0], y_range[1] + 1):
            for z in z_values:

                # 竜巻: 中心から離れるほど強くなる
                vx = -y * strength
                vy =  x * strength
                vz = 0.0

                lines.append(
                    f"{float(x)},{float(y)},{float(z)},"
                    f"{vx:.4f},{vy:.4f},{vz:.4f}"
                )

    return "\n".join(lines)

# ファイルに書き出す
content = generate_tornado()
with open("data/my_tornado.txt", "w") as f:
    f.write(content)

print("生成完了!")