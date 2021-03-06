# awesomesauce

Awesomesauce is an agent-based testing framework for Ethereum Smart Contracts.

It is used by SKALE to provide large-scale formally defined agent-based testing and simulation of SKALE network.

Agents: delegators, validators, nodes, dapp developers.

Awesomesauce uses Mesa agent-based modelling framework.  

https://mesa.readthedocs.io/en/master/

As well as  Finite State Machine library transitions 

https://github.com/pytransitions/transitions


## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.


## How to Run without the GUI

To run the model in console run `python run_console.py` in this directory.



## License

[![License](https://img.shields.io/github/license/skalenetwork/sgx.py.svg)](LICENSE)

Copyright (C) 2020-present SKALE Labs
