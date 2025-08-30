import os
import glob
import json

# -----------------------------
# Đường dẫn
# -----------------------------
query_dir = "public/queries-pack-0"
object_dir = "public/objects"
result_dir = "data/result"

os.makedirs(result_dir, exist_ok=True)

# -----------------------------
# Đọc tất cả query file
# -----------------------------
query_files = sorted(glob.glob(os.path.join(query_dir, "*.txt")))
print(f"Đã tìm thấy {len(query_files)} query file.")

# -----------------------------
# Duyệt từng query
# -----------------------------
for qf in query_files:
    query_name = os.path.splitext(os.path.basename(qf))[0]  # vd: query-p1-01
    query_outdir = os.path.join(result_dir, query_name)
    os.makedirs(query_outdir, exist_ok=True)

    with open(qf, "r", encoding="utf-8") as f:
        query_text = f.read().strip().lower()

    print(f"\n=== Xử lý query: {query_name} ({query_text}) ===")

    matches = []

    # -----------------------------
    # Tìm trong object JSON
    # -----------------------------
    all_json_files = sorted(glob.glob(os.path.join(object_dir, "*", "*.json")))
    for jf in all_json_files:
        with open(jf, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                text = json.dumps(data).lower()
                if query_text in text:
                    matches.append(jf)
            except Exception as e:
                print(f"Lỗi đọc {jf}: {e}")

    print(f"Tìm thấy {len(matches)} file match cho query {query_name}")

    # -----------------------------
    # Lưu kết quả ra file
    # -----------------------------
    result_file = os.path.join(query_outdir, "result.json")
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(matches, f, indent=2, ensure_ascii=False)

    print(f"  -> Đã lưu kết quả vào {result_file}")
