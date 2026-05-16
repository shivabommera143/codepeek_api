from fastapi import FastAPI
from bs4 import BeautifulSoup
import json
import re
import requests

app = FastAPI()
handler = app

@app.get("/")
def basic_info():
    return {
        "name": "CodePeek API",
        "description": "A unified REST API to fetch coding profiles from multiple competitive programming platforms",
        "version": "1.0.0",
        "platforms": ["LeetCode", "GitHub", "GeeksforGeeks", "CodeChef", "Codeforces", "HackerRank"],
        "endpoints": {
            "github": "/github/{handle}",
            "leetcode": "/leetcode/{handle}",
            "codeforces": "/codeforces/{handle}",
            "codechef": "/codechef/{handle}",
            "gfg": "/gfg/{handle}",
            "hackerrank": "/hackerrank/{handle}"
        },
        "docs": "/docs",
        "source": "https://github.com/shivabommera143/codepeek-api"
    }


@app.get("/github/{g_handle}")
def get_github(g_handle: str):
    try:
        data = requests.get(f"https://api.github.com/users/{g_handle}", timeout=10)
        if data.status_code != 200:
            return {"error": f"GitHub user '{g_handle}' not found"}
        response = data.json()
        return {
            "Name": response.get("name"),
            "Login": response.get("login"),
            "ID": response.get("id"),
            "Public Repos": response.get("public_repos"),
            "Followers": response.get("followers"),
            "Following": response.get("following"),
            "Bio": response.get("bio"),
            "Location": response.get("location"),
            "Company": response.get("company"),
            "Blog": response.get("blog"),
            "Hireable": response.get("hireable"),
            "Twitter Username": response.get("twitter_username"),
        }
    except Exception as e:
        return {"error": "Something went wrong", "details": str(e)}


@app.get("/leetcode/{lc_handle}")
def get_leetcode(lc_handle: str):
    try:
        data1 = requests.get(f"https://alfa-leetcode-api.onrender.com/{lc_handle}", timeout=10)
        data2 = requests.get(f"https://alfa-leetcode-api.onrender.com/{lc_handle}/solved", timeout=10)
        data3 = requests.get(f"https://alfa-leetcode-api.onrender.com/{lc_handle}/contest", timeout=10)

        response1 = data1.json()
        response2 = data2.json()
        response3 = data3.json()

        if "errors" in response1 or "username" not in response1:
            return {"error": f"LeetCode user '{lc_handle}' not found"}

        return {
            "Username": response1.get("username"),
            "Name": response1.get("name"),
            "About": response1.get("about"),
            "Ranking": response1.get("ranking"),
            "Total Problems Solved": response2.get("solvedProblem"),
            "Easy Problems Solved": response2.get("easySolved"),
            "Medium Problems Solved": response2.get("mediumSolved"),
            "Hard Problems Solved": response2.get("hardSolved"),
            "No.of Contests Attended": response3.get("contestAttend"),
            "Leetcode Contest Rating": response3.get("contestRating"),
            "Contest Top Percentage": response3.get("contestTopPercentage"),
            "Global Ranking": response3.get("contestGlobalRanking"),
            "Country": response1.get("country"),
            "Company": response1.get("company"),
            "School": response1.get("school"),
            "Github": response1.get("gitHub"),
            "Linkedln": response1.get("linkedIN"),
            "Twitter": response1.get("twitter"),
            "Website": response1.get("website"),
        }
    except Exception as e:
        return {"error": "Something went wrong", "details": str(e)}


@app.get("/codeforces/{cf_handle}")
def get_codeforces(cf_handle: str):
    try:
        data1 = requests.get(f"https://codeforces.com/api/user.info?handles={cf_handle}", timeout=10)
        result = data1.json()

        if result.get("status") != "OK":
            return {"error": f"Codeforces user '{cf_handle}' not found"}

        user = result["result"][0]

        data2 = requests.get(f"https://codeforces.com/api/user.status?handle={cf_handle}&from=1&count=10000", timeout=30)
        submissions = data2.json().get("result", [])

        solved = set()
        for sub in submissions:
            if sub["verdict"] == "OK":
                problem_id = str(sub["problem"].get("contestId", "")) + sub["problem"]["index"]
                solved.add(problem_id)

        return {
            "Handle": user["handle"],
            "First Name": user.get("firstName"),
            "Last Name": user.get("lastName"),
            "Organization": user.get("organization"),
            "Rating": user.get("rating", "Unrated"),
            "Rank": user.get("rank", "Unrated"),
            "Max Rating": user.get("maxRating", "Unrated"),
            "Max Rank": user.get("maxRank", "Unrated"),
            "Problems Solved": len(solved),
        }
    except Exception as e:
        return {"error": "Something went wrong", "details": str(e)}


@app.get("/codechef/{cc_handle}")
def get_codechef(cc_handle: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        data = requests.get(f"https://www.codechef.com/users/{cc_handle}", headers=headers, timeout=10)

        if data.status_code != 200:
            return {"error": f"CodeChef user '{cc_handle}' not found"}

        soup = BeautifulSoup(data.text, "html.parser")

        username = soup.find("span", class_="m-username--link")
        name = soup.find("h1", class_="h2-style")
        country = soup.find("span", class_="user-country-name")

        if not username:
            return {"error": f"CodeChef user '{cc_handle}' not found"}

        rating_block = soup.find("div", id="rating-block-all")
        rating_number = rating_block.find("div", class_="rating-number") if rating_block else None
        rating_text = rating_number.get_text(" ", strip=True) if rating_number else ""
        rating_match = re.search(r"\d+", rating_text)
        rating = rating_match.group() if rating_match else "Unrated"

        highest_rating_text = rating_block.find("small") if rating_block else None
        highest_rating_match = re.search(r"\d+", highest_rating_text.text) if highest_rating_text else None
        highest_rating = highest_rating_match.group() if highest_rating_match else None

        ranks_block = rating_block.find("div", class_="rating-ranks") if rating_block else None
        ranks = ranks_block.find_all("strong") if ranks_block else []

        script_match = re.search(r'var all_rating = (\[.*?\]);', data.text, re.DOTALL)
        try:
            contests = len(json.loads(script_match.group(1))) if script_match else 0
        except json.JSONDecodeError:
            contests = 0

        problem_section = soup.find("section", class_="rating-data-section problems-solved")
        headings = problem_section.find_all("h3") if problem_section else []
        solved_heading = next((h for h in headings if "Total Problems Solved" in h.text), None)
        solved_numbers = re.findall(r"\d+", solved_heading.text) if solved_heading else []
        total_solved = int(solved_numbers[0]) if solved_numbers else 0

        return {
            "Username": username.text.strip() if username else cc_handle,
            "Name": name.text.strip() if name else None,
            "Country": country.text.strip() if country else None,
            "Rating": rating,
            "Highest Rating": highest_rating,
            "Global Rank": ranks[0].text.strip() if len(ranks) > 0 else None,
            "Country Rank": ranks[1].text.strip() if len(ranks) > 1 else None,
            "Contests Participated": contests,
            "Total Problems Solved": total_solved,
        }
    except Exception as e:
        return {"error": "Something went wrong", "details": str(e)}


@app.get("/gfg/{gfg_handle}")
def get_gfg(gfg_handle: str):
    try:
        data = requests.get(f"https://authapi.geeksforgeeks.org/api-get/user-profile-info/?handle={gfg_handle}&article_count=false&redirect=true", timeout=10)
        response = data.json()

        if response.get("status") != "success":
            return {"error": f"GFG user '{gfg_handle}' not found"}

        user = response["data"]
        return {
            "Name": user.get("name"),
            "Institute": user.get("institute_name"),
            "Designation": user.get("designation"),
            "Score": user.get("score"),
            "Monthly Score": user.get("monthly_score"),
            "Total Problems Solved": user.get("total_problems_solved"),
            "Institute Rank": user.get("institute_rank"),
            "Organization Name": user.get("organization_name"),
        }
    except Exception as e:
        return {"error": "Something went wrong", "details": str(e)}


@app.get("/hackerrank/{hr_handle}")
def get_hackerrank(hr_handle: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
        }
        data = requests.get(f"https://www.hackerrank.com/rest/hackers/{hr_handle}", headers=headers, timeout=10)

        if data.status_code != 200:
            return {"error": f"HackerRank user '{hr_handle}' not found"}

        response = data.json()
        if not response.get("status"):
            return {"error": f"HackerRank user '{hr_handle}' not found"}

        user = response.get("model", {})

        # Fetch scores per track
        data2 = requests.get(f"https://www.hackerrank.com/rest/hackers/{hr_handle}/scores_elo", headers=headers, timeout=20)
        tracks = data2.json() if data2.status_code == 200 else []

        total_score = sum(track.get("practice", {}).get("score", 0) for track in tracks)
        track_scores = {
        track["name"]: track["practice"]["score"]
        for track in tracks
            if track.get("practice", {}).get("score", 0) > 0
        }       

        return {
            "ID": user.get("id"),
            "Username": user.get("username"),
            "Name": user.get("name"),
            "First Name": user.get("personal_first_name"),
            "Last Name": user.get("personal_last_name"),
            "Email": user.get("email"),
            "Country": user.get("country"),
            "School": user.get("school"),
            "Company": user.get("company"),
            "Job Title": user.get("job_title"),
            "Jobs Headline": user.get("jobs_headline"),
            "Level": user.get("level"),
            "Website": user.get("website"),
            "Short Bio": user.get("short_bio"),
            "Total Score": total_score,
            "Track Scores": track_scores,
        }
    except Exception as e:
        return {"error": "Something went wrong", "details": str(e)}