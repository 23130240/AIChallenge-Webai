import os
import glob
import json
import torch
from src.video.video_processor import VideoProcessor

# -----------------------------
# Đường dẫn
# -----------------------------
query_dir = "public/queries-pack-0"
video_dir = "public/video"
result_dir = "data/result"

os.makedirs(result_dir, exist_ok=True)

# -----------------------------
# Khởi tạo processor
# -----------------------------
vp = VideoProcessor()
device = "cuda" if torch.cuda.is_available() else "cpu"

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
        query_text = f.read().strip()

    print(f"\n=== Xử lý query: {query_name} ({query_text}) ===")

    # Lấy tất cả video trong public/video
    all_videos = sorted(glob.glob(os.path.join(video_dir, "*V001.mp4")))
    matches = []

    for vf in all_videos:
        print(f"  -> Đang xử lý video: {vf}")
        processed_frames = vp.process_video_smart(vf, query_outdir)

        # -----------------------------
        # Tìm theo các hướng khác nhau
        # -----------------------------
        keyword_hits = vp.search_keyframes_by_keyword(processed_frames, query_text)
        qa_hits = vp.search_keyframes_by_QA(processed_frames, query_text)

        # giả sử query_text có nhiều event cách nhau bởi dấu "\n"
        events = [e.strip() for e in query_text.split("\n") if e.strip()]
        trake_hits = []
        if len(events) > 1:  # chỉ test trake khi query là chuỗi sự kiện
            trake_hits = vp.search_keyframes_by_trake(processed_frames, events)

        if keyword_hits or qa_hits or trake_hits:
            matches.append({
                "video": vf,
                "keyword_hits": keyword_hits,
                "qa_hits": qa_hits,
                "trake_hits": trake_hits
            })

            # copy keyframes matched vào folder result
            for hit in keyword_hits + qa_hits:
                src = hit["frame_path"]
                dst = os.path.join(query_outdir, os.path.basename(src))
                if os.path.exists(src):
                    import shutil
                    shutil.copy(src, dst)

    # -----------------------------
    # Lưu kết quả ra file JSON
    # -----------------------------
    result_file = os.path.join(query_outdir, "result.json")
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(matches, f, indent=2, ensure_ascii=False)

    print(f"  -> Đã lưu kết quả vào {result_file}")
