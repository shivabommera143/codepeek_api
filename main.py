from fastapi import FastAPI
from bs4 import BeautifulSoup
import json
import re
import requests

app = FastAPI()
handler=app

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
    data = requests.get(f"https://api.github.com/users/{g_handle}")
    response = data.json()
    return {
        "Name": response["name"],
        "Login": response["login"],
        "ID": response["id"],
        "Public Repos": response["public_repos"],
        "Followers": response["followers"],
        "Following": response["following"],
        "Bio": response["bio"],
        "Location": response["location"],
        "Company": response["company"],
        "Blog": response["blog"],
        "Hireable": response["hireable"],
        "Twitter Username": response["twitter_username"],
    }

@app.get("/leetcode/{lc_handle}")
def get_leetcode(lc_handle: str):
    data1 = requests.get(f"https://alfa-leetcode-api.onrender.com/{lc_handle}")
    response1 = data1.json()

    data2 = requests.get(f"https://alfa-leetcode-api.onrender.com/{lc_handle}/solved")
    response2 = data2.json()

    data3 = requests.get(f"https://alfa-leetcode-api.onrender.com/{lc_handle}/contest")
    response3 = data3.json()

    return {
        "Username": response1["username"],
        "Name": response1["name"],
        "About": response1["about"],
        "Ranking": response1["ranking"],
        "Total Problems Solved": response2["solvedProblem"],
        "Easy Problems Solved": response2["easySolved"],
        "Medium Problems Solved": response2["mediumSolved"],
        "Hard Problems Solved": response2["hardSolved"],
        "No.of Contests Attended": response3["contestAttend"],
        "Leetcode Contest Rating": response3["contestRating"],
        "Contest Top Percentage": response3["contestTopPercentage"],
        "Global Ranking": response3["contestGlobalRanking"],
        "Country": response1["country"],
        "Company": response1["company"],
        "School": response1["school"],
        "Github": response1["gitHub"],
        "Linkedln": response1["linkedIN"],
        "Twitter": response1["twitter"],
        "Website": response1["website"],
    }

@app.get("/codeforces/{cf_handle}")
def get_codeforces(cf_handle: str):
    data1 = requests.get(f"https://codeforces.com/api/user.info?handles={cf_handle}")
    user = data1.json()["result"][0]

    data2 = requests.get(f"https://codeforces.com/api/user.status?handle={cf_handle}&from=1&count=10000")
    submissions = data2.json().get("result", [])
    solved = set()
    for sub in submissions:
        if sub["verdict"] == "OK":
            problem_id = str(sub["problem"].get("contestId", "")) + sub["problem"]["index"]
            solved.add(problem_id)
            
    return {
        "Handle": user["handle"],
        "First Name": user.get("firstName", None),
        "Last Name": user.get("lastName", None),
        "Organization": user.get("organization", None),
        "Rating": user.get("rating", "Unrated"),
        "Rank": user.get("rank", "Unrated"),
        "Max Rating": user.get("maxRating", "Unrated"),
        "Max Rank": user.get("maxRank", "Unrated"),
        "Problems Solved": len(solved),
    }

@app.get("/codechef/{cc_handle}")
def get_codechef(cc_handle: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    try:
        data = requests.get(f"https://www.codechef.com/users/{cc_handle}", headers=headers, timeout=10)
    except requests.RequestException as error:
        return {"error": "Could not fetch CodeChef profile", "details": str(error)}

    if data.status_code != 200:
        return {"error": "User doesn't exist or CodeChef blocked the request"}

    soup = BeautifulSoup(data.text, "html.parser")

    username = soup.find("span", class_="m-username--link")
    name = soup.find("h1", class_="h2-style")
    country = soup.find("span", class_="user-country-name")

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

@app.get("/gfg/{gfg_handle}")
def get_gfg(gfg_handle: str):
    data = requests.get(f"https://authapi.geeksforgeeks.org/api-get/user-profile-info/?handle={gfg_handle}&article_count=false&redirect=true")
    response = data.json()

    user = response["data"]
    return {
        "Name": user["name"],
        "Institute": user["institute_name"],
        "Designation": user["designation"],
        "Score": user["score"],
        "Monthly Score": user["monthly_score"],
        "Total Problems Solved": user["total_problems_solved"],
        "Institute Rank": user["institute_rank"],
        "Organization Name": user["organization_name"],
    }

@app.get("/hackerrank/{hr_handle}")
def get_hackerrank(hr_handle: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }

    data = requests.get(
        f"https://www.hackerrank.com/rest/hackers/{hr_handle}",
        headers=headers,
        timeout=10,
    )
    data.raise_for_status()
    response = data.json()

    user = response.get("model", {})
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
    }
