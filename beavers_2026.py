# Brookside Beavers — 2026 Summer national team (GameChanger).
# https://web.gc.com/teams/ohCbq6OU84HI/2026-summer-brookside-beavers
# NWLA National Tournament, Sat Aug 15 2026, St. Louis, MO. Record 2-5 (RF 20, RA 49).
# Format: games 1-4 Pool Play, game 5 Death Bracket, games 6-7 Bracket Play.
#
# Transcribed from box-score screenshots. Beavers lines cross-checked against
# team totals and the 2B/3B/HR/TB notes and reconcile exactly. Opponent lines:
# every opponent PITCHING line ties out (runs allowed = Beavers runs scored);
# opponent BATTING is best-effort from the same screenshots — H and extra-base
# hits are pinned by the TB/HR notes, and a few R/RBI cells were reconciled to
# the printed team total (see per-game "opp_note").
#
# bat row:  name, AB, R, H, RBI, BB, SO, 2B, 3B, HR
# pit row:  name, IPouts, H, R, ER, BB, SO, W, L, SV   (GameChanger books every run earned)

BEAVERS_2026 = {
    "team": "Brookside Beavers",
    "meta": {"season": "2026 Summer", "event": "NWLA National Tournament",
             "site": "GameChanger", "location": "St. Louis, MO", "level": "18O",
             "date": "2026-08-15", "record": {"W": 2, "L": 5}},
    "alias": {"Dan Brady": "Daniel Brady"},
    "games": [
        {
            "g": 1, "phase": "Pool Play", "opp": "Leroy Legends", "ha": "A",
            "res": "L", "rf": 2, "ra": 10, "time": "8:00 AM", "innings": 3,
            "gid": "1b1875c9-4fd6-4eaa-87f4-4a3b44cb7dcd",
            "line_bea": [2, 0, 0], "line_opp": [10, 0], "he_bea": [0, 0], "he_opp": [4, 0],
            "opp_note": "Leroy RBI reconciled to the printed team total (10).",
            "bat": [
                ["Peter Fraioli", 2, 1, 0, 0, 1, 1, 0, 0, 0],
                ["James Duffelmeyer", 2, 0, 0, 0, 1, 0, 0, 0, 0],
                ["Parker Gibbons", 0, 1, 0, 0, 3, 0, 0, 0, 0],
                ["Brandon McDowell", 1, 0, 0, 0, 2, 1, 0, 0, 0],
                ["Victor Cottini", 2, 0, 0, 1, 1, 2, 0, 0, 0],
                ["Dan Brady", 2, 0, 0, 1, 1, 2, 0, 0, 0],
            ],
            "pit": [
                ["Parker Gibbons", 1, 1, 8, 8, 8, 0, 0, 1, 0],
                ["James Duffelmeyer", 5, 3, 2, 2, 2, 2, 0, 0, 0],
            ],
            "opp_bat": [
                ["Jackson Buzea", 1, 3, 1, 3, 3, 0, 0, 0, 0],
                ["Jared Jonkman", 1, 2, 0, 1, 2, 0, 0, 0, 0],
                ["Ryan Voges", 2, 1, 2, 3, 2, 0, 1, 0, 0],
                ["Erik Detmar", 3, 2, 1, 2, 1, 2, 0, 0, 0],
                ["Ethan Bumgardner", 1, 2, 0, 1, 2, 0, 0, 0, 0],
            ],
            "opp_pit": [
                ["Dylan Knutson", 6, 0, 2, 2, 7, 3, 1, 0, 0],
                ["Ethan Bumgardner", 3, 0, 0, 0, 2, 3, 0, 0, 0],
            ],
        },
        {
            "g": 2, "phase": "Pool Play", "opp": "HRL Dream Team", "ha": "H",
            "res": "W", "rf": 4, "ra": 3, "time": "9:00 AM", "innings": 3,
            "gid": "e00a55a7-01f6-441c-80d0-c0f4e9b075fe",
            "line_bea": [3, 1], "line_opp": [3, 0, 0], "he_bea": [2, 0], "he_opp": [3, 0],
            "opp_note": "HRL RBI reconciled to the printed team total (3).",
            "bat": [
                ["Peter Fraioli", 3, 0, 1, 0, 0, 1, 0, 0, 0],
                ["Parker Gibbons", 1, 1, 1, 2, 2, 0, 0, 0, 0],
                ["James Duffelmeyer", 2, 1, 0, 0, 1, 0, 0, 0, 0],
                ["Brandon McDowell", 1, 1, 0, 0, 1, 1, 0, 0, 0],
                ["Victor Cottini", 1, 0, 0, 1, 1, 1, 0, 0, 0],
                ["Vinny Spoto", 0, 1, 0, 1, 2, 0, 0, 0, 0],
            ],
            "pit": [
                ["Peter Fraioli", 9, 3, 3, 3, 5, 1, 1, 0, 0],
            ],
            "opp_bat": [
                ["Evan Sibbet", 3, 0, 2, 2, 1, 0, 0, 0, 0],
                ["Will Grass", 4, 1, 1, 0, 0, 1, 0, 0, 0],
                ["Luke Thompson", 2, 1, 0, 0, 1, 0, 0, 0, 0],
                ["Matthew Stalboerger", 2, 1, 0, 0, 1, 0, 0, 0, 0],
                ["Wade Cooper", 1, 0, 0, 1, 2, 0, 0, 0, 0],
            ],
            "opp_pit": [
                ["Caleb Groth", 1, 0, 3, 3, 5, 1, 0, 0, 0],
                ["Kevin Pabon Jr", 5, 2, 1, 1, 2, 2, 0, 1, 0],
            ],
        },
        {
            "g": 3, "phase": "Pool Play", "opp": "WILL Waves", "ha": "A",
            "res": "L", "rf": 2, "ra": 6, "time": "1:00 PM", "innings": 3,
            "gid": "0f05e9ac-2383-4485-8721-62876db53ac1",
            "line_bea": [1, 1, 0], "line_opp": [3, 3], "he_bea": [4, 0], "he_opp": [1, 0],
            "opp_note": "WILL runs reconciled to the printed team total (6).",
            "bat": [
                ["AJ Cefaloni", 2, 1, 0, 0, 1, 1, 0, 0, 0],
                ["Parker Gibbons", 1, 1, 1, 1, 2, 0, 0, 0, 1],
                ["James Duffelmeyer", 2, 0, 0, 0, 1, 0, 0, 0, 0],
                ["Brandon McDowell", 3, 0, 0, 0, 0, 1, 0, 0, 0],
                ["Victor Cottini", 3, 0, 3, 1, 0, 0, 1, 0, 0],
                ["Trevor Meyler", 1, 0, 0, 0, 1, 1, 0, 0, 0],
                ["Peter Fraioli", 1, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "pit": [
                ["Parker Gibbons", 2, 0, 3, 3, 6, 0, 0, 1, 0],
                ["Dan Brady", 4, 1, 3, 3, 3, 1, 0, 0, 0],
            ],
            "opp_bat": [
                ["Jake Davey", 2, 1, 0, 1, 2, 1, 0, 0, 0],
                ["Chris Sarnowski", 2, 2, 1, 3, 2, 0, 0, 0, 0],
                ["Chase Oliver", 2, 1, 0, 1, 2, 0, 0, 0, 0],
                ["Steve Keelon", 0, 2, 0, 1, 3, 0, 0, 0, 0],
            ],
            "opp_pit": [
                ["Chase Oliver", 9, 4, 2, 2, 5, 3, 1, 0, 0],
            ],
        },
        {
            "g": 4, "phase": "Pool Play", "opp": "Ridley Park Longballs", "ha": "H",
            "res": "L", "rf": 0, "ra": 12, "time": "2:00 PM", "innings": 3,
            "gid": "93742eca-1b7c-4473-9c97-322eccca9b6e",
            "line_bea": [0, 0, 0], "line_opp": [8, 0, 4], "he_bea": [0, 0], "he_opp": [7, 0],
            "bat": [
                ["Peter Fraioli", 2, 0, 0, 0, 0, 2, 0, 0, 0],
                ["Parker Gibbons", 2, 0, 0, 0, 0, 2, 0, 0, 0],
                ["James Duffelmeyer", 2, 0, 0, 0, 0, 1, 0, 0, 0],
                ["Victor Cottini", 1, 0, 0, 0, 0, 1, 0, 0, 0],
                ["Trevor Meyler", 1, 0, 0, 0, 0, 1, 0, 0, 0],
                ["Dan Brady", 1, 0, 0, 0, 1, 0, 0, 0, 0],
                ["Austin Corvino", 0, 0, 0, 0, 1, 0, 0, 0, 0],
            ],
            "pit": [
                ["Vinny Spoto", 0, 1, 8, 8, 7, 0, 0, 1, 0],
                ["James Duffelmeyer", 3, 1, 0, 0, 0, 1, 0, 0, 0],
                ["Dan Brady", 3, 1, 0, 0, 0, 1, 0, 0, 0],
                ["Trevor Meyler", 3, 4, 4, 4, 1, 1, 0, 0, 0],
            ],
            "opp_bat": [
                ["Cam Farro", 4, 3, 4, 6, 1, 0, 0, 0, 0],
                ["Teddy Drecher", 3, 3, 1, 1, 2, 0, 0, 0, 0],
                ["Colin Pollag", 2, 3, 1, 3, 3, 0, 1, 0, 0],
                ["Sean Bingnear", 1, 0, 0, 0, 0, 1, 0, 0, 0],
                ["Brandon Boas", 1, 0, 1, 0, 0, 0, 0, 0, 0],
                ["Zane Johnston", 3, 3, 0, 2, 2, 2, 0, 0, 0],
                ["Frankie Campanile", 1, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "opp_pit": [
                ["Tommy Loftus", 3, 0, 0, 0, 0, 2, 1, 0, 0],
                ["Sean Bingnear", 6, 0, 0, 0, 2, 5, 0, 0, 0],
            ],
        },
        {
            "g": 5, "phase": "Death Bracket", "opp": "EWL Excel", "ha": "H",
            "res": "W", "rf": 10, "ra": 9, "time": "4:15 PM", "innings": 5,
            "gid": "72026a4b-7fcb-4f89-83b3-493cab9ec3ca",
            "line_bea": [3, 5, 2, 0], "line_opp": [0, 1, 8, 0, 0], "he_bea": [8, 0], "he_opp": [8, 0],
            "bat": [
                ["Peter Fraioli", 1, 2, 0, 1, 2, 1, 0, 0, 0],
                ["Dan Brady", 2, 1, 2, 0, 0, 0, 1, 0, 0],
                ["Parker Gibbons", 3, 3, 1, 3, 2, 2, 0, 0, 1],
                ["James Duffelmeyer", 4, 1, 0, 0, 1, 4, 0, 0, 0],
                ["Victor Cottini", 4, 1, 3, 6, 1, 1, 1, 1, 0],
                ["Brandon McDowell", 2, 1, 1, 0, 2, 1, 0, 0, 0],
                ["Vinny Spoto", 4, 1, 1, 0, 0, 2, 0, 0, 0],
            ],
            "pit": [
                ["Peter Fraioli", 7, 4, 5, 5, 2, 4, 0, 0, 0],
                ["Dan Brady", 2, 1, 4, 4, 4, 0, 1, 0, 0],
                ["Parker Gibbons", 6, 3, 0, 0, 0, 2, 0, 0, 0],
            ],
            "opp_bat": [
                ["Jackson Niehaus", 7, 3, 3, 3, 1, 3, 0, 0, 2],
                ["Drew Maurer", 6, 2, 2, 5, 1, 1, 0, 0, 2],
                ["Sam Huber", 6, 1, 2, 1, 1, 0, 0, 0, 1],
                ["Jackson Huber", 2, 0, 0, 0, 0, 2, 0, 0, 0],
                ["Evan Stark", 2, 3, 1, 0, 3, 0, 0, 0, 0],
            ],
            "opp_pit": [
                ["Sarah Huber", 0, 1, 3, 3, 3, 0, 0, 0, 0],
                ["Drew Maurer", 4, 1, 4, 4, 4, 3, 0, 0, 0],
                ["Nick Klaustermeier", 8, 6, 3, 3, 1, 8, 0, 1, 0],
            ],
        },
        {
            "g": 6, "phase": "Bracket Play", "opp": "CCW Skullcrushers", "ha": "A",
            "res": "L", "rf": 0, "ra": 4, "time": "6:00 PM", "innings": 5,
            "gid": "74705bf3-e429-45c2-b469-f01e417f6e31",
            "line_bea": [0, 0, 0, 0, 0], "line_opp": [2, 2, 0, 0], "he_bea": [1, 0], "he_opp": [7, 0],
            "bat": [
                ["Peter Fraioli", 2, 0, 0, 0, 1, 2, 0, 0, 0],
                ["Trevor Meyler", 1, 0, 0, 0, 0, 1, 0, 0, 0],
                ["Parker Gibbons", 2, 0, 1, 0, 1, 1, 0, 0, 0],
                ["Dan Brady", 1, 0, 0, 0, 0, 1, 0, 0, 0],
                ["Victor Cottini", 3, 0, 0, 0, 0, 1, 0, 0, 0],
                ["James Duffelmeyer", 3, 0, 0, 0, 0, 3, 0, 0, 0],
                ["Brandon McDowell", 1, 0, 0, 0, 1, 1, 0, 0, 0],
                ["Austin Corvino", 1, 0, 0, 0, 0, 1, 0, 0, 0],
                ["AJ Cefaloni", 2, 0, 0, 0, 1, 2, 0, 0, 0],
            ],
            "pit": [
                ["Parker Gibbons", 6, 5, 4, 4, 5, 0, 0, 1, 0],
                ["James Duffelmeyer", 6, 2, 0, 0, 2, 1, 0, 0, 0],
            ],
            "opp_bat": [
                ["Will Smithey", 4, 1, 1, 0, 3, 0, 0, 0, 0],
                ["Brendan Dudas", 6, 1, 2, 2, 0, 1, 0, 1, 0],
                ["Dylan Jones", 5, 0, 3, 2, 1, 0, 0, 0, 0],
                ["Reid Werner", 3, 2, 1, 0, 3, 0, 0, 0, 0],
            ],
            "opp_pit": [
                ["Will Smithey", 15, 1, 0, 0, 4, 13, 1, 0, 0],
            ],
        },
        {
            "g": 7, "phase": "Bracket Play", "opp": "SHW Steel City Sluggers", "ha": "A",
            "res": "L", "rf": 2, "ra": 5, "time": "7:00 PM", "innings": 5,
            "gid": "dfcee11d-e3cb-4aac-8eb8-2b08bf298fdd",
            "line_bea": [0, 1, 1, 0, 0], "line_opp": [0, 0, 4, 1], "he_bea": [4, 0], "he_opp": [5, 0],
            "opp_note": "SHW batting: ~2 runs and 1 strikeout in the screenshot could not be tied to a hitter (team line reads 5 R / 6 SO).",
            "bat": [
                ["Parker Gibbons", 2, 2, 1, 0, 2, 1, 1, 0, 0],
                ["Victor Cottini", 3, 0, 0, 0, 1, 1, 0, 0, 0],
                ["James Duffelmeyer", 4, 0, 2, 2, 0, 1, 0, 0, 0],
                ["Brandon McDowell", 2, 0, 0, 0, 2, 0, 0, 0, 0],
                ["AJ Cefaloni", 4, 0, 1, 0, 0, 0, 0, 0, 0],
                ["Peter Fraioli", 2, 0, 0, 0, 0, 0, 0, 0, 0],
                ["Vinny Spoto", 2, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "pit": [
                ["Peter Fraioli", 5, 1, 0, 0, 2, 3, 0, 0, 0],
                ["James Duffelmeyer", 1, 3, 3, 3, 1, 0, 0, 1, 0],
                ["Parker Gibbons", 6, 1, 2, 2, 4, 3, 0, 0, 0],
            ],
            "opp_bat": [
                ["Zeke Daure", 2, 0, 1, 1, 4, 0, 0, 0, 0],
                ["Dakota Romantino", 5, 0, 1, 2, 1, 1, 0, 0, 0],
                ["George Schroeder", 2, 0, 0, 0, 0, 0, 0, 0, 0],
                ["Aidan Schroeder", 3, 1, 1, 1, 1, 1, 0, 0, 0],
                ["Ethan Marchese", 5, 2, 2, 1, 1, 3, 0, 0, 1],
            ],
            "opp_pit": [
                ["Roman Keaney", 15, 4, 2, 2, 5, 3, 1, 0, 0],
            ],
        },
    ],
}
