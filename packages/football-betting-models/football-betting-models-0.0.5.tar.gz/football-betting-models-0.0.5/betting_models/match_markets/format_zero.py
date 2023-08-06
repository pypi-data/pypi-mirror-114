'''Match markets format 0 seeding model class'''

import numpy as np
import pandas as pd

from .market_model_base import MarketModelBase
from .backsolve_lambda import BacksolveLambda
from .score_model import ScoreModel


class FormatZero(MarketModelBase):
    def __init__(self, num_seeds, tol):
        super().__init__(num_seeds, tol)

    def probs_mat(self, implied_hda):
        solver = BacksolveLambda(implied_hda)
        solver.optimise()
        lambda_home, lambda_away = solver.lambdas
        # Generate outcomes_mat from lambdas
        score_model = ScoreModel(lambda_home, lambda_away)
        outcomes_mat = score_model.outcomes_0_mat()        
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
                'halfgoal': outcomes[2],
                'num_bets': int(seeds_mat[outcomes])
            }
            df = df.append(dict_, ignore_index=True)
        #df['halfgoal'] = df['halfgoal'].map({0:'Y_Y', 1:'Y_N', 2:'N_Y', 3:'N_N'})
        df['firsthalfgoal'] = False
        df['secondhalfgoal'] = False
        df.loc[df['halfgoal'] == 0, 'firsthalfgoal'] = True
        df.loc[df['halfgoal'] == 1, 'firsthalfgoal'] = True
        df.loc[df['halfgoal'] == 0, 'secondhalfgoal'] = True
        df.loc[df['halfgoal'] == 2, 'secondhalfgoal'] = True
        
        homewin = df['homegoals'] > df['awaygoals']
        draw = df['homegoals'] == df['awaygoals']
        awaywin = df['homegoals'] < df['awaygoals']
        
        # BTTS / OTAAHG / Goal first half / Goal second half column
        df['result'] = np.nan
        df.loc[homewin, 'result'] = 'homewin'
        df.loc[draw, 'result'] = 'draw'
        df.loc[awaywin, 'result'] = 'awaywin'
        df['BTTS'] = (df['homegoals'] > 0) & (df['awaygoals'] > 0)
        df['over_2.5'] = (df['homegoals'] + df['awaygoals']) > 2.5
        
        return df[['homegoals', 'awaygoals', 'result', 'BTTS', 
                'over_2.5', 'firsthalfgoal', 'secondhalfgoal', 'num_bets']]


if __name__ == '__main__':
    
    def dec_2_implied(decimal_odds):
        'Odds array to probability array'
        probs = 1 / decimal_odds
        probs_normalised = probs / np.sum(probs)
        return probs_normalised

    hda = np.array([1.714, 3.750, 5.71])
    implied_hda = dec_2_implied(hda)
    sm = FormatZero(num_seeds=100, tol=25)
    df = sm.gen_seeds(implied_hda)
    
    print(df)
