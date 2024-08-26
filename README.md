# llocker - Applying logic Locking to Various Circuits

## Discription

The respository contains the results of applying a series of logic locking algorithms to 6 small Veriog circuits:

- kmStLN
- koStln
- kSLn
- wmStLN
- woStLN
- c432 

For each example circuit, we attempted to apply the following algorithms:

- full_lock 
- full_lock_mux 
- lut_lock 
- mux_lock 
- random_lut_lock 
- sfll_flex 
- sfll_hd 
- trll 
- tt_lock
- tt_lock_sen 
- xor_lock

_See the documentation at the [logiclocking](https://circuitgraph.github.io/logiclocking/locks.html) submodule's documentation for details and citations for each lock algorithm_