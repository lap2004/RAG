import json
import requests

API_URL = "http://localhost:8000/chat"

# Load dữ liệu
with open("./backend/data/new_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Tạo tập câu hỏi kiểm thử từ các bản ghi hợp lệ
test_set = []
for item in data:
    # Kiểm tra khóa bắt buộc
    if not all(k in item for k in ("title", "section", "content")):
        continue

    nganh = item["title"]
    section = item["section"]
    content = item["content"].strip()

    # Xây câu hỏi theo từng loại section
    if section == "Mô tả ngành":
        question = f"Ngành {nganh.lower()} học gì?"
    elif section == "Tổ hợp môn xét tuyển":
        question = f"Ngành {nganh.lower()} xét tuyển những tổ hợp môn nào?"
    elif section == "Triển vọng nghề nghiệp":
        question = f"Ngành {nganh.lower()} ra trường làm gì?"
    else:
        continue

    test_set.append({
        "question": question,
        "ground_truth": content
    })

# Đánh giá bằng cách gửi từng câu hỏi
results = []
for item in test_set:
    q = item["question"]
    gt = item["ground_truth"]

    try:
        response = requests.post(API_URL, json={"query": q})
        res_text = response.json().get("response", "")
        match = gt[:100].lower() in res_text.lower()
    except Exception as e:
        res_text = str(e)
        match = False

    results.append({
        "question": q,
        "expected": gt[:100] + "...",
        "response": res_text[:100] + "...",
        "match": match
    })

# Tính accuracy
accuracy = sum(1 for r in results if r["match"]) / len(results)
print(f"\n✅ Accuracy: {accuracy:.2%} ({sum(r['match'] for r in results)} / {len(results)})")

# Lưu log
with open("./backend/data/eval_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
