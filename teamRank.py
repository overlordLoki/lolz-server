import pandas as pd
import database as db


def update_elo(winner_elo, loser_elo):

    expected_win = expected_result(winner_elo, loser_elo)
    change_in_elo = k_factor * (1-expected_win)
    winner_elo += change_in_elo
    loser_elo -= change_in_elo
    return winner_elo, loser_elo

def expected_result(elo_a, elo_b):
    expect_a = 1.0/(1+10**((elo_b - elo_a)/elo_width))
    return expect_a

def update_end_of_season(elos):

    diff_from_mean = elos - mean_elo
    elos -= diff_from_mean/3
    return elos

