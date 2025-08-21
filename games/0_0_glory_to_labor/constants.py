rtp = 0.965
wincap = 10000.0
regular_bonus_cost = 100.0
super_bonus_cost = 200.0

free_game_hr = 180 # 1 in 180 spins should trigger a free game
wincap_from_base_game_hr = 5000000 # 1 in 5,000,000 spins should trigger a win cap
wincap_from_base_game_rtp = wincap / wincap_from_base_game_hr
wincap_from_regular_bonus_hr = 4500000 # 1 in 4,500,000 spins should trigger a win cap
wincap_from_regular_bonus_rtp = (wincap / regular_bonus_cost) / wincap_from_regular_bonus_hr
wincap_from_super_bonus_hr = 2500000 # 1 in 2,500,000 spins should trigger a win cap
wincap_from_super_bonus_rtp = (wincap / super_bonus_cost) / wincap_from_super_bonus_hr