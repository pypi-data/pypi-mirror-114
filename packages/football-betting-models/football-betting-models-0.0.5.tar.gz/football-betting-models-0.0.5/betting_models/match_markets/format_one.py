'''Match markets format 0 seeding model class'''

import numpy as np
import pandas as pd

from .market_model_base import MarketModelBase
from .backsolve_lambda import BacksolveLambda
from .score_model import ScoreModel


class FormatOne(MarketModelBase):
    def __init__(self, num_seeds, tol):
        super().__init__(num_seeds, tol)

    def probs_mat(self, implied_hda):
        solver = BacksolveLambda(implied_hda)
        solver.optimise()
        lambda_home, lambda_away = solver.lambdas
        score_model = ScoreModel(lambda_home, lambda_away)
        outcomes_mat = score_model.outcomes_1_mat()
        return outcomes_mat

    def seeds_2_df(self, seeds_mat):
        lines = np.where(seeds_mat > 0)
        df = pd.DataFrame()
        # Loop through the index of each combination
        for i in range(lines[0].shape[0]):
            outcomes = tuple(j[i] for j in lines)
            dict_ = {
                'homegoals': outcomes[0],
                'awaygoals': outcomes[1],
                'htsf': outcomes[2],
                'red_card': outcomes[3],
                'yellow_cards': outcomes[4],
                'halfgoal': outcomes[5],
                'num_bets': int(seeds_mat[outcomes])
            }
            df = df.append(dict_, ignore_index=True)
        
        # FTR / over 2.5 goals
        homewin = df['homegoals'] > df['awaygoals']
        draw = df['homegoals'] == df['awaygoals']
        awaywin = df['homegoals'] < df['awaygoals']
        df['result'] = np.nan
        df.loc[homewin, 'result'] = 'homewin'
        df.loc[draw, 'result'] = 'draw'
        df.loc[awaywin, 'result'] = 'awaywin'
        df['over_2.5'] = (df['homegoals'] + df['awaygoals']) > 2.5
        
        # Hometeam to score first / Red card / Over 4.5 yellows
        df['htsf'] = df['htsf'].map({0:True, 1:False})
        df['red_card'] = df['red_card'].map({0:True, 1:False}) 
        df['yellow_cards'] = df['yellow_cards'].map({0:True, 1:False})

        # Hometeam clean sheet
        df['clean_sheet'] = df['awaygoals'] == 0

        # Halfgoals
        df['firsthalfgoal'] = False
        df['secondhalfgoal'] = False
        df.loc[df['halfgoal'] == 0, 'firsthalfgoal'] = True
        df.loc[df['halfgoal'] == 1, 'firsthalfgoal'] = True
        df.loc[df['halfgoal'] == 0, 'secondhalfgoal'] = True
        df.loc[df['halfgoal'] == 2, 'secondhalfgoal'] = True
        
        out_cols = [
            'homegoals', 
            'awaygoals', 
            'result', 
            'over_2.5', 
            'htsf', 
            'red_card', 
            'yellow_cards', 
            'clean_sheet', 
            'firsthalfgoal', 
            'secondhalfgoal', 
            'num_bets'
        ]
        
        return df[out_cols]


if __name__ == '__main__':
    
    def dec_2_implied(decimal_odds):
        'Odds array to probability array'
        probs = 1 / decimal_odds
        probs_normalised = probs / np.sum(probs)
        return probs_normalised

    hda = np.array([1.714, 3.750, 5.71])
    implied_hda = dec_2_implied(hda)
    sm = FormatOne(num_seeds=100, tol=25)
    df = sm.gen_seeds(implied_hda)
        
    print(df)
