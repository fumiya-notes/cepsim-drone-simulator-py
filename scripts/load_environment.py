# scripts/load_environment.py
import numpy as np

def load_cepsim(filepath):
    """
    CEPSim形式の環境データファイルを読み込む
    
    戻り値:
        metadata: ヘッダー情報の辞書
        positions: 位置データ (N, 3) のnumpy配列
        vectors: ベクトルデータ (N, 3) のnumpy配列
    """
    metadata = {}
    data_points = []
    current_key = None
    reading_data = False

    with open(filepath, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        # 空行はスキップ
        if not line:
            continue

        # セクションヘッダー
        if line.startswith('# '):
            current_key = line[2:]
            if current_key == 'Data':
                reading_data = True
            continue

        # データ本体
        if reading_data:
            values = [float(v) for v in line.split(',')]
            data_points.append(values)
        else:
            # メタデータの値
            if current_key:
                metadata[current_key] = line

    # numpy配列に変換
    data = np.array(data_points)
    positions = data[:, 0:3]   # x, y, z
    vectors   = data[:, 3:6]   # vx, vy, vz

    return metadata, positions, vectors


# 動作確認
if __name__ == "__main__":
    filepath = "data/wind_updraft.txt"
    metadata, positions, vectors = load_cepsim(filepath)

    print("=== メタデータ ===")
    for key, value in metadata.items():
        print(f"  {key}: {value}")

    print("\n=== データ確認 ===")
    print(f"  データ点数: {len(positions)}")
    print(f"  位置データ shape: {positions.shape}")
    print(f"  ベクトルデータ shape: {vectors.shape}")

    print("\n=== 風速確認 ===")
    vz_max = np.max(vectors[:, 2])
    vz_min = np.min(vectors[:, 2])
    print(f"  上向き風速(vz)の最大値: {vz_max} m/s")
    print(f"  上向き風速(vz)の最小値: {vz_min} m/s")

    print("\n=== 最初の3点 ===")
    for i in range(3):
        print(f"  位置{positions[i]} → 風速{vectors[i]}")

    print("\n=== x=10の点(最大上昇気流) ===")
    max_x_mask = positions[:, 0] == 10.0
    max_x_vectors = vectors[max_x_mask]
    print(f"  風速(vz): {max_x_vectors[0, 2]} m/s")
    print(f"  → x=10 × 5.0 = 50.0 と一致するはず ✓")