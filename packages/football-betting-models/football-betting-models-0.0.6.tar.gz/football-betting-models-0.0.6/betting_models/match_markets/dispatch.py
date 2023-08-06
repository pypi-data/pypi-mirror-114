'''Dispatch match markets seeding model.'''

import numpy as np


def dec_2_implied(decimal_odds):
    'Convert odds array to implied probability array'
    probs = 1 / decimal_odds
    probs_normalised = probs / np.sum(probs)
    return probs_normalised


def main(dec_odds, num_seeds, tol, format_num):
    'Choose model format and return seeding bets dataframe'
    if format_num == 0:
        from .format_zero import FormatZero
        model = FormatZero
    elif format_num == 1:
        from .format_one import FormatOne
        model = FormatOne
    else:
        raise ValueError('Format number not implemented.')
    
    implied_hda = dec_2_implied(dec_odds)
    seeds_df, fig = model(num_seeds, tol).gen_seeds(implied_hda)
    return seeds_df, fig


if __name__ == '__main__':
    
    hda = np.array([1.714, 3.750, 5.71])
    num_seeds = 100
    tol = 50
    format_num = 0
    vis_status = True

    seeds_df, fig = main(hda, num_seeds, tol, format_num)
    print(seeds_df)
    
    import matplotlib.pyplot as plt
    plt.savefig('c:/users/micha/desktop/test_output.png')
