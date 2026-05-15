# 🧑‍💻 Coding Profile Wrapper API

A unified REST API that aggregates coding profile data from multiple competitive programming platforms — built with **FastAPI** and **Python**.

## 🌐 Platforms Supported

| Platform | Method |
|---|---|
| GitHub | Official API |
| LeetCode | alfa-leetcode-api |
| Codeforces | Official API |
| CodeChef | Web Scraping |
| GeeksforGeeks | Internal API |
| HackerRank | Internal API |

---

## 🚀 Live API

> Base URL: `https://your-deployment-url.com`

---

## 📦 Endpoints

### GitHub
```
GET /github/{g_handle}
```
Returns name, repos, followers, bio, location, and more.

**Example:** `/github/shivabommera143`

---

### LeetCode
```
GET /leetcode/{lc_handle}
```
Returns problems solved (easy/medium/hard), contest rating, ranking, and more.

**Example:** `/leetcode/shivabommera0143`

---

### Codeforces
```
GET /codeforces/{cf_handle}
```
Returns rating, rank, max rating, and organization.

**Example:** `/codeforces/shiva_bommera`

---

### CodeChef
```
GET /codechef/{cc_handle}
```
Returns rating, division, global rank, country rank, and contests participated.

**Example:** `/codechef/shiva_bommera`

---

### GeeksforGeeks
```
GET /gfg/{gfg_handle}
```
Returns score, monthly score, problems solved, and institute rank.

**Example:** `/gfg/shivabommera143`

---

### HackerRank
```
GET /hackerrank/{hr_handle}
```
Returns name, level, company, job title, and more.

**Example:** `/hackerrank/shivabommera0143`

---

## 🛠️ Run Locally

### Prerequisites
- Python 3.8+
- pip

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/your-username/coding-profile-api.git
cd coding-profile-api
```

**2. Create a virtual environment**
```bash
python -m venv venv
```

Activate it:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the server**
```bash
uvicorn main:app --reload
```

**5. Open in browser**
```
http://localhost:8000
```

Interactive API docs available at:
```
http://localhost:8000/docs
```

---

## 📁 Project Structure

```
coding-profile-api/
├── main.py           # All API endpoints
├── requirements.txt  # Dependencies
└── README.md         # Documentation
```

---

## ⚠️ Notes

- **CodeChef** endpoint uses web scraping — may break if CodeChef updates their UI.
- **LeetCode** data is fetched via [alfa-leetcode-api](https://github.com/alfaarghya/alfa-leetcode-api) — subject to their rate limits.
- For production use with high traffic, consider self-hosting the LeetCode API via Docker.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT
