Příklady
========

Jednoduchý grafický model
-------------------------

.. code-block:: python

    from alex.infer.node import DiscreteVariableNode, DiscreteFactorNode
    from alex.infer.factor import Factor
    from alex.infer.lbp import LBP

    #
    # Proměnné pro první obrátku.
    #
    hid_1 = DiscreteVariableNode('food_1', ['chinese', 'indian'])
    obs_1 = DiscreteVariableNode('food_obs_1', ['chinese', 'indian'])

    obs_factor_1 = DiscreteFactorNode('food_obs_factor_1', Factor(
        ['food_1', 'food_obs_1'],
        {
            'food_1': ['chinese', 'indian'],
            'food_obs_1': ['chinese', 'indian'],
        },
        {
            ('chinese', 'chinese'): 0.9,
            ('chinese', 'indian'): 0.1,
            ('indian', 'chinese'): 0.1,
            ('indian', 'indian'): 0.9,
        }))

    #
    # Proměnné pro druhou obrátku.
    #
    hid_2 = DiscreteVariableNode('food_2', ['chinese', 'indian'])
    obs_2 = DiscreteVariableNode('food_obs_2', ['chinese', 'indian'])

    obs_factor_2 = DiscreteFactorNode('food_obs_factor_2', Factor(
        ['food_2', 'food_obs_2'],
        {
            'food_2': ['chinese', 'indian'],
            'food_obs_2': ['chinese', 'indian'],
        },
        {
            ('chinese', 'chinese'): 0.9,
            ('chinese', 'indian'): 0.1,
            ('indian', 'chinese'): 0.1,
            ('indian', 'indian'): 0.9,
        }))

    #
    # Přechodový faktor spojující skryté proměnné z první a druhé obrátky.
    #
    trans_factor = DiscreteFactorNode('food_trans_factor', Factor(
        ['food_1', 'food_2'],
        {
            'food_1': ['chinese', 'indian'],
            'food_2': ['chinese', 'indian'],
        },
        {
            ('chinese', 'chinese'): 0.99,
            ('chinese', 'indian'): 0.01,
            ('indian', 'chinese'): 0.01,
            ('indian', 'indian'): 0.99,
        }))

    #
    # Propojení jednotlivých vrcholů v modelu.
    #
    obs_factor_1.connect(hid_1, parent=True)
    obs_factor_1.connect(obs_1, parent=False)

    obs_factor_2.connect(hid_2, parent=True)
    obs_factor_2.connect(obs_2, parent=False)

    trans_factor.connect(hid_1, parent=True)
    trans_factor.connect(hid_2, parent=False)

    #
    # Nastavení pozorovaných hodnot.
    #
    obs_1.observed({
        ('chinese',): 0.6,
        ('indian',): 0.4,
    })

    obs_2.observed({
        ('chinese',): 0.5,
        ('indian',): 0.5,
    })

    #
    # Inference
    #
    lbp = LBP(strategy='tree')
    lbp.add_nodes([obs_1, obs_2, hid_1, hid_2, obs_factor_1, obs_factor_2,
                   trans_factor])
    lbp.run()

    #
    # Vypsat nejpravděpodobnější hodnotu z druhé obrátky a její pravděpodobnost.
    #
    print hid_2.belief.most_probable(n=1)

Model s trénovatelnými parametry
--------------------------------

.. code-block:: python

    from alex.ml.bn.node import (DiscreteVariableNode, DiscreteFactorNode,
                                DirichletParameterNode,
                                DirichletFactorNode)
    from alex.ml.bn.factor import Factor
    from alex.ml.bn.lbp import LBP

    obs_probability = {
        ('chinese', 'chinese'): 0.9,
        ('chinese', 'indian'): 0.1,
        ('indian', 'chinese'): 0.1,
        ('indian', 'indian'): 0.9,
    }

    #
    # Proměnné pro první obrátku.
    #
    hid_1 = DiscreteVariableNode('food_1', ['chinese', 'indian'])
    obs_1 = DiscreteVariableNode('food_obs_1', ['chinese', 'indian'])

    obs_factor_1 = DiscreteFactorNode('food_obs_factor_1', Factor(
        ['food_1', 'food_obs_1'],
        {
            'food_1': ['chinese', 'indian'],
            'food_obs_1': ['chinese', 'indian'],
        },
        obs_probability))

    #
    # Proměnné pro druhou obrátku.
    #
    hid_2 = DiscreteVariableNode('food_2', ['chinese', 'indian'])
    obs_2 = DiscreteVariableNode('food_obs_2', ['chinese', 'indian'])

    obs_factor_2 = DiscreteFactorNode('food_obs_factor_2', Factor(
        ['food_2', 'food_obs_2'],
        {
            'food_2': ['chinese', 'indian'],
            'food_obs_2': ['chinese', 'indian'],
        },
        obs_probability))

    #
    # Faktor pro přechodovou pravděpodobnost a jeho parametr.
    #
    trans_factor = DirichletFactorNode('food_trans_factor')
    trans_param = DirichletParameterNode('food_trans_param', Factor(
        ['food_1', 'food_2'],
        {
            'food_1': ['chinese', 'indian'],
            'food_2': ['chinese', 'indian'],
        },
        {
            ('chinese', 'chinese'): 2,
            ('chinese', 'indian'): 1,
            ('indian', 'chinese'): 1,
            ('indian', 'indian'): 2,
        }))

    #
    # Propojení uzlů do grafického modelu.
    #
    obs_factor_1.connect(hid_1, parent=True)
    obs_factor_1.connect(obs_1, parent=False)

    obs_factor_2.connect(hid_2, parent=True)
    obs_factor_2.connect(obs_2, parent=False)

    trans_factor.connect(hid_1, parent=True)
    trans_factor.connect(hid_2, parent=False)
    trans_factor.connect(trans_param)

    #
    # Nastavení pozorovaných hodnot.
    #
    obs_1.observed({
        ('chinese',): 0.9,
        ('indian',): 0.1,
    })

    obs_2.observed({
        ('chinese',): 0.8,
        ('indian',): 0.2,
    })

    #
    # Inference
    #
    lbp = LBP(strategy='tree')
    lbp.add_nodes([obs_1, obs_2, hid_1, hid_2, obs_factor_1, obs_factor_2,
                    trans_factor])
    lbp.run()
