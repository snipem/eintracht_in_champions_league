import json
import locale
import math
import random
import subprocess
import sys
from datetime import datetime, timedelta

DRAW = "DRAW"

# Teams
BVB = "BVB"
PSG = "PSG"
FCB = "FCB"
FCB2 = "FCB2"
RM = "RM"

# EL
B04 = "B04"

# CfL
AST = "AST"

# Buli

RBL = "RBL"
HOF = "HOF"
WER = "WER"
SGE = "SGE"
FCA = "FCA"
M05 = "M05"
D98 = "D98"
BMG = "BMG"
VFB = "VFB"
BOC = "BOC"
SCF = "SCF"
WOB = "WOB"
KOE = "KOE"
HEI = "HEI"
BER = "BER"

team_ovr_rating = {
    BVB: 81,
    PSG: 83,
    FCB: 84,
    FCB2: 75,
    RM: 85,
    B04: 80,
    AST: 80,
    RBL: 80,
    HOF: 76,
    WER: 74,
    SGE: 76,
    FCA: 74,
    M05: 72,
    D98: 71,
    BMG: 75,
    VFB: 78,
    BOC: 73,
    SCF: 76,
    WOB: 74,
    KOE: 72,
    HEI: 74,
    BER: 74,
}


class Match:

    def __init__(self, team1, team2, outcome=None):
        self.team1 = team1
        self.team2 = team2

        if outcome:
            # Use the known outcome
            self.outcome = outcome
        else:
            self.outcome = self.simulate_outcome()
            if self.outcome == DRAW:
                self.overtime_winner = self.simulate_overtime_winner()

    def simulate_outcome(self):
        return get_random_outcome(self.team1, self.team2)

    def simulate_overtime_winner(self):
        while True:
            random_outcome = get_random_outcome(self.team1, self.team2)
            if random_outcome != DRAW:
                return random_outcome

    def is_win_of_team(self, team):
        if self.outcome == team:
            return True
        else:
            return False

    def is_draw_of_team(self, team):
        if self.outcome == DRAW:
            if self.team1 == team or self.team2 == team:
                return True
            else:
                return False
        return False

    def is_lose_of_team(self, team):
        if self.team1 == team or self.team2 == team:
            if self.outcome != DRAW and self.outcome != team:
                return True
            else:
                return False


def calculate_outcome_probability(rating1, rating2):
    rating_difference = rating1 - rating2

    # Define base probabilities for win, draw, and loss
    base_win_prob = 0.375
    base_draw_prob = 0.25
    base_loss_prob = 0.375

    # Adjust probabilities based on rating difference
    if rating_difference > 0:
        win_prob = base_win_prob + (rating_difference * 0.03)
        draw_prob = base_draw_prob - (rating_difference * 0.005)
        loss_prob = base_loss_prob - (rating_difference * 0.005)
    elif rating_difference < 0:
        win_prob = base_win_prob - (abs(rating_difference) * 0.03)
        draw_prob = base_draw_prob + (abs(rating_difference) * 0.005)
        loss_prob = base_loss_prob + (abs(rating_difference) * 0.005)
    else:
        win_prob = base_win_prob
        draw_prob = base_draw_prob
        loss_prob = base_loss_prob

    # Ensure probabilities sum up to 1
    total_prob = win_prob + draw_prob + loss_prob
    win_prob /= total_prob
    draw_prob /= total_prob
    loss_prob /= total_prob

    return win_prob, draw_prob, loss_prob


def simulate_match(team1: str, team1_rating: int, team2: str, team2_rating: int):
    win_prob, draw_prob, loss_prob = calculate_outcome_probability(team1_rating, team2_rating)
    outcome = random.choices([team1, 'DRAW', team2], weights=[win_prob, draw_prob, loss_prob])[0]
    return outcome


def get_random_outcome(team1, team2):
    team1_rating = 0
    team2_rating = 0

    if team1 in team_ovr_rating:
        team1_rating = team_ovr_rating[team1]

    if team2 in team_ovr_rating:
        team2_rating = team_ovr_rating[team2]

    # Use the same rating if either one is 0
    if team1_rating == 0 and team2_rating == 0:
        team1_rating = 70
        team2_rating = 70
    elif team1_rating == 0:
        team1_rating = team2_rating
    elif team2_rating == 0:
        team2_rating = team1_rating

    outcome = simulate_match(team1, team1_rating, team2, team2_rating)
    return outcome


def is_german_team(team):
    if team == BVB or team == FCB or team == B04:
        return True
    elif team == AST:  # works for now
        return True
    else:
        return False


def is_english_team(team):
    if team == AST:
        return True
    else:
        return False


def get_git_revision_short_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()


def who_goes_to_next_round(m1, m2):
    if m1.outcome == DRAW and m2.outcome == DRAW:
        return m2.overtime_winner
    elif m1.outcome == DRAW:
        return m2.outcome
    elif m2.outcome == DRAW:
        return m1.outcome
    elif m1.outcome != m2.outcome:
        return m2.simulate_overtime_winner()
    elif m1.outcome == m2.outcome:
        return m1.outcome
    else:
        print("Unexpcted outcome")
        sys.exit(1)


def get_points_for_germany_by_matches(matches):
    points = 0
    for match in matches:
        if match.outcome == DRAW and (is_german_team(match.team1) or is_german_team(match.team2)):
            points = points + 1
        if is_german_team(match.outcome):
            points = points + 2
    return points


def get_points_for_england_by_matches(matches):
    points = 0
    for match in matches:
        if match.outcome == DRAW and (is_english_team(match.team1) or is_english_team(match.team2)):
            points = points + 1
        if is_german_team(match.outcome):
            points = points + 2
    return points


def simulate_bundesliga() -> (int, int):
    place_eintracht = 6
    place_dortmund = 5

    # 21.04.24
    top_standing_in_this_list = 4
    standings = {
        RBL: 59.9,
        BVB: 57.7,
        SGE: 45.4,
        FCA: 39.3,
        HOF: 39.2,
        SCF: 39.1,
    }

    matches = [
        # End of 30. Spieltag
        # Leipzig
        Match(RBL, BVB), Match(RBL, HOF), Match(RBL, WER), Match(RBL, SGE),
        # Dortmund
        Match(BVB, FCA), Match(BVB, M05), Match(BVB, D98),  # Direktes Duell gegen Leipzig
        # Eintracht
        Match(SGE, FCB), Match(SGE, B04), Match(SGE, BMG),  # Direktes Duell gegen Leipzig
        # Augsburg
        Match(FCA, WER), Match(FCA, VFB), Match(FCA, B04),  # Direktes Duell gegen Dortmund
        # Hoffenheim
        Match(HOF, BOC), Match(HOF, D98), Match(HOF, FCB),  # Direktes Duell gegen Leipzig
        # Freiburg
        Match(SCF, M05, outcome=DRAW), Match(SCF, WOB), Match(SCF, KOE), Match(SCF, HEI), Match(SCF, BER)
    ]

    # Get Points for matches
    for match in matches:
        for team in standings:

            if match.is_win_of_team(team):
                standings[team] = standings[team] + 3
            elif match.is_draw_of_team(team):
                standings[team] = standings[team] + 1
            elif match.is_lose_of_team(team):
                pass

    sorted_standings = sorted(standings.items(), key=lambda x: x[1])
    sorted_standings.reverse()

    # print(sorted_standings)

    for sorted_standing in sorted_standings:
        if sorted_standing[0] == BVB:
            place_dortmund = sorted_standings.index(sorted_standing) + top_standing_in_this_list
        if sorted_standing[0] == SGE:
            place_eintracht = sorted_standings.index(sorted_standing) + top_standing_in_this_list

    return place_eintracht, place_dortmund


class SimulationRawData:
    def __init__(self):
        self.cl_winner = []
        self.fifth_cl_place_for_germany = []
        self.eintracht_place = []
        self.dortmund_place = []
        self.eintracht_in_champions_league = []
        self.eintracht_in_europa_league = []
        self.eintracht_in_conference_league = []
        self.eintracht_in_europa = []



class SimulationResults:

    def __init__(self, nr_of_simulations, description=""):

        self.probability_eintracht_in_europa = 0
        self.probability_eintracht_in_conference_league = 0
        self.probability_eintracht_in_europa_league = 0
        self.probability_eintracht_in_champions_league = 0
        self.probability_fifth_cl_starter_for_germany = 0
        self.probability_bvb_winning_the_champions_league = 0
        self.probability_eintracht_place = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0,
                                            13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0}
        self.probability_dortmund_place = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0,
                                           13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0}

        self.start_time = datetime.now()
        self.revision = get_git_revision_short_hash()
        self.description = description

        self.nr_of_simulations = nr_of_simulations

        self.end_time = None
        self.duration = None

    def end(self):
        self.end_time = datetime.now()
        self.duration = self.end_time - self.start_time

    def to_json(self):
        data = self.__dict__.copy()
        data['start_time'] = self.start_time.isoformat()
        data['end_time'] = self.end_time.isoformat() if self.end_time else None
        data['duration'] = self.duration.total_seconds() if self.duration else None
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        obj = cls(data['nr_of_simulations'])
        obj.__dict__.update(data)
        obj.start_time = datetime.fromisoformat(data['start_time'])
        obj.end_time = datetime.fromisoformat(data['end_time']) if data['end_time'] else None
        obj.duration = timedelta(seconds=data['duration']) if data['duration'] else None

        probability_eintracht_place_int = {}
        probability_dortmund_place_int = {}

        for key, value in data['probability_eintracht_place'].items():
            probability_eintracht_place_int[int(key)] = value
        for key, value in data['probability_dortmund_place'].items():
            probability_dortmund_place_int[int(key)] = value

        obj.probability_dortmund_place = probability_dortmund_place_int
        obj.probability_eintracht_place = probability_eintracht_place_int

        return obj

    def calculate_probabilities(self, raw_data: SimulationRawData):
        self.probability_bvb_winning_the_champions_league = raw_data.cl_winner.count(BVB) / self.nr_of_simulations
        self.probability_fifth_cl_starter_for_germany = raw_data.fifth_cl_place_for_germany.count(
            True) / self.nr_of_simulations
        self.probability_eintracht_in_champions_league = raw_data.eintracht_in_champions_league.count(
            True) / self.nr_of_simulations

        self.probability_eintracht_in_europa_league = raw_data.eintracht_in_europa_league.count(
            True) / self.nr_of_simulations
        self.probability_eintracht_in_conference_league = raw_data.eintracht_in_conference_league.count(
            True) / self.nr_of_simulations
        self.probability_eintracht_in_europa = raw_data.eintracht_in_europa.count(True) / self.nr_of_simulations

        for i in range(1, 18):
            self.probability_eintracht_place[i] = raw_data.eintracht_place.count(i) / self.nr_of_simulations

        for i in range(1, 18):
            self.probability_dortmund_place[i] = raw_data.dortmund_place.count(i) / self.nr_of_simulations

    def to_string(self):
        rs = ""
        rs += "\n```"
        rs += ("Ergebnisse nach %s Simulationen mit Powerranking:\n" % millify(self.nr_of_simulations) +
               "P BVB gewinnt CL: %.3f\n" % self.probability_bvb_winning_the_champions_league +
               "P 5. CL Platz:     %.3f\n" % self.probability_fifth_cl_starter_for_germany +
               "P BVB wird 5.:     %.3f\n" % self.probability_dortmund_place[5] +
               "P SGE wird 5.:     %.3f\n" % self.probability_eintracht_place[5] +
               "P SGE wird 6.:     %.3f\n" % self.probability_eintracht_place[6] +
               "P SGE wird 7.:     %.3f\n" % self.probability_eintracht_place[7] +
               "P SGE wird 8.:     %.3f\n" % self.probability_eintracht_place[8] +
               "P SGE wird 9.:     %.3f\n" % self.probability_eintracht_place[9] +
               "P SGE in CL:       %.3f\n" % self.probability_eintracht_in_champions_league +
               "P SGE in EL:       %.3f\n" % self.probability_eintracht_in_europa_league +
               "P SGE in ECL:      %.3f\n" % self.probability_eintracht_in_conference_league +
               "P Europacup 24/25: %.3f\n" % self.probability_eintracht_in_europa +
               "```")

        return rs

    def format(self, diff=None):
        # return _format_probability(self, "probability_bvb_winning_the_champions_league", diff)
        rs = ""
        rs += "\n```\n"
        rs += "Ergebnisse nach %s Simulationen mit Powerranking:\n" % millify(self.nr_of_simulations)
        rs += "Lauf '%s' vom %s\n" % (self.description, self.start_time.strftime("%d.%m. %H:%M"))

        if diff:
            rs += "Vergleich '%s' vom %s\n" % (diff.description, diff.start_time.strftime("%d.%m. %H:%M"))


        rs += ("\nP BVB gewinnt CL:       " + _format_probability(self, "probability_bvb_winning_the_champions_league", diff) +
              "\nP DFB mit 5. CL Platz:  " + _format_probability(self, "probability_fifth_cl_starter_for_germany", diff) +
              "\nP BVB wird 5.:          " + _format_probability(self, ["probability_dortmund_place",5], diff) +
              "\nP SGE wird 5.:          " + _format_probability(self, ["probability_eintracht_place",5], diff) +
              "\nP SGE wird 6.:          " + _format_probability(self, ["probability_eintracht_place",6], diff) +
              "\nP SGE wird 7.:          " + _format_probability(self, ["probability_eintracht_place",7], diff) +
              "\nP SGE wird 8.:          " + _format_probability(self, ["probability_eintracht_place",8], diff) +
              "\nP SGE wird 9.:          " + _format_probability(self, ["probability_eintracht_place",9], diff) +
              "\nP SGE kommt in die CL:  " + _format_probability(self, "probability_eintracht_in_champions_league", diff) +
              "\nP SGE kommt in die EL:  " + _format_probability(self, "probability_eintracht_in_europa_league", diff) +
              "\nP SGE kommt in die ECL: " + _format_probability(self, "probability_eintracht_in_conference_league", diff) +
              "\nP SGE in Europa 24/25:  " + _format_probability(self, "probability_eintracht_in_europa", diff) +
              "\n```")
        return rs


def diff_value_relevant(diff_value: float) -> bool:
    if abs(diff_value) <= 0.25:
        return False

    return True


def _format_probability(sr: SimulationResults, param, compare_sr: SimulationResults = None):

    if isinstance(param, list):
        if compare_sr:

            diff_value = sr.__dict__[param[0]][param[1]] - compare_sr.__dict__[param[0]][param[1]]

            if diff_value_relevant(diff_value):

                if diff_value > 0:
                    sign = "+"
                else:
                    sign = "-"

                return "%03.1f%% (%s%.1f%%)" % (sr.__dict__[param[0]][param[1]]*100, sign, abs(diff_value))
            else:
                return "%03.1f%%" % (sr.__dict__[param[0]][param[1]]*100)
        else:
            return "%03.1f%%" % (sr.__dict__[param[0]][param[1]]*100)


    if compare_sr:
        diff_value = 100*(sr.__dict__[param] - compare_sr.__dict__[param])
        if  diff_value_relevant(diff_value):

            if diff_value > 0:
                sign = "+"
            else:
                sign = "-"

            return "%03.1f%% (%s%.1f%%)" % (sr.__dict__[param]*100, sign, abs(diff_value))
        else:
            return "%03.1f%%" % (sr.__dict__[param]*100)
    else:
        return "%03.1f%%" % (sr.__dict__[param]*100)


def run():
    if len(sys.argv) < 2:
        print("Usage: python sim.py <nr_of_simulations> <optional_description>")
        sys.exit(1)

    if len(sys.argv) >= 3:
        description = sys.argv[2]
    else:
        description = ""

    if len(sys.argv) == 4:
        history_filename = sys.argv[3]
        print(history_filename)
        with open(history_filename, 'r') as file:
            data = file.read().rstrip()
            history_file = SimulationResults.from_json(data)
    else:
        history_file = None

    nr_of_simulations = int(sys.argv[1])

    simulation_results = SimulationResults(nr_of_simulations, description)
    raw_data = SimulationRawData()

    i = 0

    debug = False

    while i < nr_of_simulations:

        if i % 1000 == 0:
            print("%d/%d  [%0.f%%]\n" % (i, nr_of_simulations, i / nr_of_simulations * 100), end="")

        points_for_germany = 0
        points_for_england = 0

        cl_winner, points_for_germany_in_cl = simulate_cup(BVB, PSG, FCB, RM)
        points_for_germany += points_for_germany_in_cl

        if debug:
            print(i, cl_winner, points_for_germany)

        # EL
        _, points_for_germany_in_el = simulate_cup(B04, "Team2", "Team3", "Team4")
        points_for_germany += points_for_germany_in_el

        _, points_for_england_in_chl = simulate_cup(AST, "Team2", "Team3", "Team4")
        points_for_england += points_for_england_in_chl

        if points_for_germany > 4:
            germany_has_5th_cl_place = True
        elif points_for_england < 4:
            germany_has_5th_cl_place = True
        else:  # TODO add france
            germany_has_5th_cl_place = False

        i += 1

        if debug:
            print("Points for Germany: %d" % points_for_germany)
            print("Points for England: %d" % points_for_england)
            print("Germany has 5th CL place: %s" % germany_has_5th_cl_place)

        eintracht_place, dortmund_place = simulate_bundesliga()

        # Setup europa places
        el_place = 5
        ecl_place = 6

        if cl_winner == BVB and germany_has_5th_cl_place and dortmund_place >= 5:
            el_place += 2
            ecl_place += 2
        elif germany_has_5th_cl_place:
            el_place += 1
            ecl_place += 1

        eintracht_in_champions_league = False
        eintracht_in_europa_league = False
        eintracht_in_conference_league = False
        eintracht_in_europa = False

        if cl_winner == BVB and germany_has_5th_cl_place and eintracht_place == 6 and dortmund_place == 5:
            eintracht_in_champions_league = True
        elif eintracht_place <= 4:
            eintracht_in_champions_league = True
        elif germany_has_5th_cl_place and eintracht_place == 5:
            eintracht_in_champions_league = True
        elif eintracht_place <= el_place:
            eintracht_in_europa_league = True
        elif eintracht_place <= ecl_place:
            eintracht_in_conference_league = True

        if eintracht_in_champions_league or eintracht_in_europa_league or eintracht_in_conference_league:
            eintracht_in_europa = True

        raw_data.cl_winner.append(cl_winner)

        raw_data.eintracht_place.append(eintracht_place)
        raw_data.dortmund_place.append(dortmund_place)
        raw_data.fifth_cl_place_for_germany.append(germany_has_5th_cl_place)

        raw_data.eintracht_in_champions_league.append(eintracht_in_champions_league)
        raw_data.eintracht_in_europa_league.append(eintracht_in_europa_league)
        raw_data.eintracht_in_conference_league.append(eintracht_in_conference_league)
        raw_data.eintracht_in_europa.append(eintracht_in_europa)

    simulation_results.end()
    simulation_results.calculate_probabilities(raw_data)
    print(simulation_results.format(diff=history_file))

    # Serialize to JSON
    json_data = simulation_results.to_json()
    filename = "results/sim_result_%s_%s.json" % (simulation_results.start_time, simulation_results.revision)
    with open(filename, "w") as text_file:
        text_file.write(json_data)



def millify(n):
    millnames = ['', '.000', ' Millionen', ' Billionen', ' Trillionen']
    n = float(n)
    millidx = max(0, min(len(millnames) - 1,
                         int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))

    return '{:.0f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])


def simulate_cup(team1, team2, team3, team4):
    points_for_germany = 0
    cl_matchces = []
    # Champions League
    m1 = Match(team1, team2)
    m2 = Match(team3, team4)
    m3 = Match(team1, team2)
    m4 = Match(team3, team4)
    final_team_1 = who_goes_to_next_round(m1, m3)
    final_team_2 = who_goes_to_next_round(m2, m4)
    cl_final = Match(final_team_1, final_team_2)

    if is_german_team(final_team_1):
        points_for_germany = + 1
    if is_german_team(final_team_2):
        points_for_germany = + 1

    cl_matchces = [m1, m2, m3, m4]
    if cl_final.outcome == DRAW:
        cl_winner = cl_final.overtime_winner
    else:
        cl_winner = cl_final.outcome

    points_for_germany = get_points_for_germany_by_matches(cl_matchces)

    if is_german_team(cl_winner):
        points_for_germany = + 2

    return cl_winner, points_for_germany


if __name__ == "__main__":
    run()
