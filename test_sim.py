from unittest import TestCase

from sim import simulate_match, SimulationResults


class Test(TestCase):
    def test_simulate_match_sge_fcb(self):
        self.simulate_multiple("SGE", 76, "FCB", 84)

    def test_simulate_match_sge_scf(self):
        self.simulate_multiple("SGE", 76, "SCF", 76)

    def test_simulate_match_sge_d98(self):
        self.simulate_multiple("SGE", 76, "D98", 71)

    def test_simulate_match_psg_fcg(self):
        self.simulate_multiple("PSG", 76, "FCG", 10)

    def test_simulate_match_psg_fcb(self):
        self.simulate_multiple("PSG", 84, "FCB", 85)

    def simulate_multiple(self, team1, team1_rating, team2, team2_rating):
        results = []
        i = 0
        while i < 10000:
            result = simulate_match(team1, team1_rating, team2, team2_rating)
            results.append(result)
            i += 1
        print("Wenn sie %d mal gegeneinander Spielen: Siege %s: %.2f, Siege %s: %.2f, DRAW: %.2f" % (
            len(results), team1, results.count(team1) / len(results), team2, results.count(team2) / len(results),
            results.count("DRAW") / len(results)))


class TestSimulationResults(TestCase):
    def test_to_string_diff(self):

        tsr = SimulationResults(1000, "recent run")
        tsr.probability_bvb_winning_the_champions_league = 0.5
        tsr2 = SimulationResults(1000, "older run")
        tsr2.probability_bvb_winning_the_champions_league = 0.7

        out = tsr.format(diff=tsr2)
        print(out)

    def test_to_string_nodiff(self):

        tsr = SimulationResults(1000, "recent run")
        tsr.probability_bvb_winning_the_champions_league = 0.5

        out = tsr.format()
        print(out)
