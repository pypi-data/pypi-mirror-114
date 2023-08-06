# -*- coding: utf-8 -*-

from json import dumps

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .seeding_model import SeedingModel


class ModelDispatch:
    def __init__(self):
        pass
    
    @staticmethod
    def json_encode(matchids, leagueid, seeds):
        'Convert seed allocation array into json'
        packet = {}
        packet['LeagueId'] = leagueid
        packet['Lines'] = []
        
        # Loop through all non-zero betting combinations
        lines = np.where(seeds > 0)
        for i in range(lines[0].shape[0]):    
            outcomes = tuple(j[i] for j in lines)
            value = int(seeds[outcomes])  # int required for json encoder
            # Map outcomes to WKW input
            WKW_map = {0:1, 1:0, 2:2}
            WKW_outcomes = list(outcomes)
            WKW_outcomes = tuple(map(WKW_map.get, WKW_outcomes))
            
            zipped = zip(matchids, WKW_outcomes)
            
            line = {}
            line['Predictions'] = []
            line['NumberOfBets'] = value
            
            # For each match bet in line, extract matchid and outcome
            for matchid, WKW_outcome in zipped:
                event = {}
                event['MatchId'] = matchid
                event['Prediction'] = int(WKW_outcome)
                line['Predictions'].append(event)
            # For each betting combination add a line
            packet['Lines'].append(line)
        # JSON encode output
        json = dumps(packet)
        return json
    
    @staticmethod
    def implied_2_tensor(implied_probs):
        'Converts implied probabilities list of arrays to n-dimensional tensor'
        implied_tensor = 1
        for T in implied_probs:
            implied_tensor = np.tensordot(implied_tensor, T, axes=0)
        return implied_tensor

    @staticmethod
    def plot_allocation(df):        
        'Plot betting allocation vs implied probability of outcomes'
        fig, ax = plt.subplots()
        for col in df.columns:    
            ax.plot(df.index,
                    df[col],
                    label=col,
                    #color='blue',
                    #alpha=1
                    )
            ax.legend()
            ax.set_title('Seed allocation')
        return fig

    @staticmethod
    def print_status(prob_list, seeds):
        'Visualises status of seed given batch split, outcome probas etc...'
        n_seeds = np.sum(seeds)
        
        # Plot relative allocation
        seed_alloc = seeds / n_seeds
        implied_probs_tensor = ModelDispatch.implied_2_tensor(prob_list)
        seed_alloc = seed_alloc.reshape((-1,1))
        implied_probs_tensor = implied_probs_tensor.reshape((-1,1))
        data = (implied_probs_tensor, seed_alloc)
        zipped = np.concatenate(data, axis=1)
        
        cols = ['implied_probability', 'seed_allocation']
        allocation_df = pd.DataFrame(zipped, columns=cols)
        allocation_df.sort_values('implied_probability', ascending=False, inplace=True)
        allocation_df.reset_index(drop=True, inplace=True)
        fig = ModelDispatch.plot_allocation(allocation_df)  # return your plot as compatible data
        
        # Info printouts
        #print(f'Total seeds: {n_seeds}')
        #print(f'Max seeding bet: {max_seed}')
        return fig

    @staticmethod
    def generate_seeds(
        n_seeds, 
        tol, 
        prob_list,
        matchids, 
        leagueid, 
        random_seed=False
    ):
        'Add first seeding batch to league'
        sm = SeedingModel(n_seeds, tol) 
        # Get tailed seed bets if random seed specified, otherwise vanilla
        if random_seed:
            _, _, seeds = sm.get_tailed_seeds_pct(prob_list, random_seed=random_seed)
        else:
            _, _, seeds = sm.get_seeds(prob_list)
        json = ModelDispatch.json_encode(matchids, leagueid, seeds)
        fig = ModelDispatch.print_status(prob_list, seeds)
        return json, fig


def decimal_2_probs(decimal_odds_arr):
        probs_arr = 1 / decimal_odds_arr
        adjusted_probs_arr = probs_arr / np.sum(probs_arr)
        return adjusted_probs_arr


def main(n_seeds, tol, odds_list, matchids, leagueid, random_seed):
    'Wrapper to allow package level __init__ to access gen_seeds directly'
    prob_list = list(map(decimal_2_probs, odds_list))
    json, fig = ModelDispatch.generate_seeds(
            n_seeds, 
            tol, 
            prob_list,
            matchids, 
            leagueid,
            random_seed
        )
    return json, fig


if __name__ == '__main__':
     
    # Seeding config
    T1 = np.array([4.35, 3.82, 1.84])           # Slovan
    #T2 = np.array([6.58, 4.82, 1.458])          # Airdrionians
    #T3 = np.array([6.11, 5.08, 1.462])          # Brora
    #T4 = np.array([1.552, 4.47, 5.69])          # Livingston
    #T5 = np.array([8.54, 5.53, 1.338])          # Montrose
    #T6 = np.array([1.211, 6.5, 15.82])          # Warsaw
    #T7 = np.array([1.159, 7.96, 18.99])         # Olympiakos
    #T8 = np.array([1.555, 4.22, 6.36])          # PSV
    
    prob_list = [T1]#, T2, T3, T4, T5, T6, T7, T8]  
    prob_list = list(map(decimal_2_probs, prob_list))
    
    matchids = ['05ece93f-7de6-4ca1-8679-75a972fffa90_9m3zl56oifilmmpwq2sshxkb8',   
                #'cb828189-8d9c-4611-9ea9-1ea766cdf840_cxphwagi3ntfxflgwfi7dttzo',
                #'b95a1da0-6e85-49d5-9e26-89b4efaedd54_dcr4up1qmhfkodr4oj5xhi39w',
                #'d369db62-1fca-499d-94e1-0b958a910f34_2549mggi8ebj6j54pbkezytqs',
                #'d259b870-f630-49bf-8ae6-4fd1e117a589_dctpasuspmjba1q4dp6n6x7h0',
                #'a1fb79ab-ea8f-4b4a-9647-679ed55854d5_9m7w5zqntwwjcivys6hxxfw9g',
                #'3dcf522d-cba7-49ce-9fdf-4cd549f63ccf_9merpwyn4jpca8eagu8csydqs',
                #'f7f227b2-fb69-45db-be19-085e0c4b6b23_9n5is7qvta8rfto3w37muvs44'
                ]

    leagueid = '05358b17-2879-4d66-865e-51ab8f6a593a_05358b17-2879-4d66-865e-51ab8f6a593a'
    n_batch_splits = 1
    
    n_seeds = 40
    tol = 10
    
    # Add first batch
    output, fig = ModelDispatch.generate_seeds(n_seeds, tol, prob_list, matchids, leagueid)
    
    # Save figure
    plt.savefig('c:/users/micha/desktop/test_output.png')

    output_filename = 'c:/users/micha/desktop/test_output.txt'
    with open(output_filename, "x") as f:
        f.write(output)
    