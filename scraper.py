import requests
from bs4 import BeautifulSoup
import re

URL = "https://en.wikipedia.org/wiki/2026_NRL_season_results"

def clean_team(name):
    result = ""
    inside = False
    for ch in name:
        if ch == "[":
            inside = True
        elif ch == "]":
            inside = False
            continue
        if not inside:
            result += ch
    return result.strip()

def parse_score(cell):
    text = cell.get_text(strip=True)
    m = re.match(r"(\d+)[–-](\d+)", text)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None

def main():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36"
    }

    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    teams = {}
    next_id = 0
    matches = []
    current_round = None

    # Walk through the page in order
    for element in soup.find_all(["h3", "table"]):

        # Detect round headers
        if element.name == "h3":
            text = element.get_text(" ", strip=True)
            m = re.match(r"Round\s+(\d+)", text)
            if m:
                current_round = int(m.group(1))
            continue

        # Parse match tables
        if element.name == "table" and "wikitable" in element.get("class", []):
            if current_round is None:
                continue

            for row in element.find_all("tr"):
                cells = row.find_all(["td", "th"])
                if len(cells) < 3:
                    continue

                # Find score cell dynamically
                score_idx = None
                for i, c in enumerate(cells):
                    if parse_score(c) is not None:
                        score_idx = i
                        break

                if score_idx is None:
                    continue

                home = clean_team(cells[score_idx - 1].get_text())
                away = clean_team(cells[score_idx + 1].get_text())
                score = parse_score(cells[score_idx])

                if home not in teams:
                    teams[home] = next_id
                    next_id += 1
                if away not in teams:
                    teams[away] = next_id
                    next_id += 1

                home_id = teams[home]
                away_id = teams[away]
                home_score, away_score = score

                matches.append((current_round, home_id, away_id, home_score, away_score))

    # Write match file
    with open("matches.txt", "w") as f:
        f.write("round home_team away_team home_team_score away_team_score\n")
        for m in matches:
            f.write(f"{m[0]} {m[1]} {m[2]} {m[3]} {m[4]}\n")

    # Write team ID map
    with open("teams.txt", "w") as f:
        for name, tid in sorted(teams.items(), key=lambda x: x[1]):
            f.write(f"{tid} {name}\n")

    print("Done. Wrote matches.txt and teams.txt")

if __name__ == "__main__":
    main()

