import random
import sys

DRAW = "DRAW"

# Teams
BVB = "BVB"
PSG = "PSG"
FCB = "FCB"
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


class Match:

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
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


def get_random_outcome(team1, team2):
    possible_outcomes = [DRAW, team1, team2]
    return possible_outcomes[random.randint(0, 2)]


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
        Match(SCF, M05), Match(SCF, WOB), Match(SCF, KOE), Match(SCF, HEI), Match(SCF, BER)
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


def run():
    nr_of_simulations = 100000
    i = 0
    simulation_results_cl_winner = []
    simulation_results_fifth_cl_place_for_germany = []
    simulation_results_eintracht_place = []
    simulation_results_dortmund_place = []
    simulation_resutls_eintracht_in_champions_league = []
    simulation_resutls_eintracht_in_europa_league = []
    simulation_resutls_eintracht_in_conference_league = []
    simulation_resutls_eintracht_in_europa = []

    debug = False

    while i < nr_of_simulations:

        if i % 1000 == 0:
            print("%d/%d  [%0.f%%]\r" % (i, nr_of_simulations, i / nr_of_simulations * 100), end="")

        points_for_germany = 0
        points_for_england = 0

        cl_winner, points_for_germany_in_cl = simulate_cup(BVB, PSG, FCB, RM)
        points_for_germany += points_for_germany_in_cl

        simulation_results_cl_winner.append(cl_winner)

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

        simulation_results_fifth_cl_place_for_germany.append(germany_has_5th_cl_place)

        eintracht_place, dortmund_place = simulate_bundesliga()

        simulation_results_eintracht_place.append(eintracht_place)
        simulation_results_dortmund_place.append(dortmund_place)

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

        simulation_resutls_eintracht_in_champions_league.append(eintracht_in_champions_league)
        simulation_resutls_eintracht_in_europa_league.append(eintracht_in_europa_league)
        simulation_resutls_eintracht_in_conference_league.append(eintracht_in_conference_league)
        simulation_resutls_eintracht_in_europa.append(eintracht_in_europa)


    probapality_bvb_winning_the_champions_league = simulation_results_cl_winner.count(BVB) / nr_of_simulations
    probapality_fith_place_for_germany = simulation_results_fifth_cl_place_for_germany.count(True) / nr_of_simulations
    probality_eintracht_in_champions_league = simulation_resutls_eintracht_in_champions_league.count(
        True) / nr_of_simulations

    probability_eintracht_in_europa_league = simulation_resutls_eintracht_in_europa_league.count(True) / nr_of_simulations
    probability_eintracht_in_conference_league = simulation_resutls_eintracht_in_conference_league.count(True) / nr_of_simulations
    probability_eintracht_in_europa = simulation_resutls_eintracht_in_europa.count(True) / nr_of_simulations


    print("Results after %d simulations:" % nr_of_simulations)
    print("P Dortmund gewinnt CL:             %.3f" % probapality_bvb_winning_the_champions_league)
    print("P Deutschland bekommt 5. CL Platz: %.3f" % probapality_fith_place_for_germany)
    print("P Dortmund wird 5.:                %.3f" % (simulation_results_dortmund_place.count(5) / nr_of_simulations))
    print("P Eintracht wird 6.:               %.3f" % (simulation_results_eintracht_place.count(6) / nr_of_simulations))
    # print("P Eintracht wird 5.:               %.3f" % (simulation_results_eintracht_place.count(5) / nr_of_simulations))
    print("P Eintracht kommt in die CL:       %.3f" % probality_eintracht_in_champions_league)
    print("P Eintracht kommt in die EL:       %.3f" % probability_eintracht_in_europa_league)
    print("P Eintracht kommt in die ECL       %.3f" % probability_eintracht_in_conference_league)
    print("P Europacup im nächsten Jahr:      %.3f" % probability_eintracht_in_europa)


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
