Balíček :mod:`infer`
====================

Modul :mod:`factor`
-------------------

.. module:: alex.infer.factor

Modul :mod:`~alex.infer.factor` obsahuje implementaci faktorů pro počítání s
diskrétními pravděpodobnostními rozděleními.

.. exception:: FactorError

    Výjimka značící chybu při manipulaci s faktorem.

.. class:: Factor

    Třída reprezentující diskrétní faktor s definovanými operacemi.

    Je možné použít všechny standardní matematické operátory (+, -, \*, /,
    \*\*). Operátor je možné aplikovat na dva faktory, anebo na faktor a
    skalární hodnotu.

    .. method:: Factor.__init__(variables, variable_values, prob_table[, logarithmetic=True])

        Vytvoření nového faktoru.

        .. code-block:: python

            f = Factor(['A', 'B'],
                {'A': ['a1', 'a2'], 'B': ['b1', 'b2']},
                {
                    ('a1', 'b1'): 0.8,
                    ('a1', 'b2'): 0.2,
                    ('a2', 'b1'): 0.3,
                    ('a2', 'b2'): 0.7
                })

        :arg variables: seznam proměnných ve faktoru.
        :arg variable_values: slovník obsahující pro každou proměnnou seznam možných hodnot.
        :arg prob_table: slovník možných přiřazení proměnných a jejich ohodnocení.
        :arg logarithmetic: přepínač určující, zda-li použít aritmetiku nad zlogaritmovanými hodnotami.


    .. method:: Factor.__getitem__(assignment)

        Získání ohodnocení pro dané přiřazení.

        .. code-block:: python

            >>> f = Factor(['A', 'B'],
            ...     {'A': ['a1', 'a2'], 'B': ['b1', 'b2']},
            ...     {
            ...         ('a1', 'b1'): 0.8,
            ...         ('a1', 'b2'): 0.2,
            ...         ('a2', 'b1'): 0.3,
            ...         ('a2', 'b2'): 0.7
            ...     }) 
            >>> f[('a2', 'b1')]
            0.3

        :arg assignment: přiřazení proměnných.
        :returns: hodnotu dotazovaného přiřazení.


    .. method:: Factor.__setitem__(assignment, value)

        Nastavení hodnoty pro přiřazení proměnných.

        .. code-block:: python

            >>> f = Factor(['A', 'B'],
            ...     {'A': ['a1', 'a2'], 'B': ['b1', 'b2']},
            ...     {
            ...         ('a1', 'b1'): 0.8,
            ...         ('a1', 'b2'): 0.2,
            ...         ('a2', 'b1'): 0.3,
            ...         ('a2', 'b2'): 0.7
            ...     })
            >>> f[('a2', 'b1')] = 0.4
            >>> f[('a2', 'b1')]
            0.4

        :arg assignment: přiřazení proměnných.
        :arg value: nová hodnota.


    .. method:: Factor.pretty_print(width=79, precision=10)

        Vypsání faktoru ve formě tabulky.

        .. code-block:: python

            >>> f = Factor(['A', 'B'],
            ...     {'A': ['a1', 'a2'], 'B': ['b1', 'b2']},
            ...     {
            ...         ('a1', 'b1'): 0.8,
            ...         ('a1', 'b2'): 0.2,
            ...         ('a2', 'b1'): 0.3,
            ...         ('a2', 'b2'): 0.7
            ...     })
            >>> print f.pretty_print(50, 2)
            --------------------------------------------------
                A               B             Value      
            --------------------------------------------------
                a1              b1             0.8       
                a1              b2             0.2       
                a2              b1             0.3       
                a2              b2             0.7       
            --------------------------------------------------

        :arg width: šířka tabulky.
        :arg precision: počet desetinných míst.
        :returns: řetězec s naformátovanou tabulkou.


    .. method:: Factor.__iter__()

        Iterace přes jednotlivé hodnoty přiřazení.

        .. code-block:: python

            >>> f = Factor(['A', 'B'],
            ...     {'A': ['a1', 'a2'], 'B': ['b1', 'b2']},
            ...     {
            ...         ('a1', 'b1'): 0.8,
            ...         ('a1', 'b2'): 0.2,
            ...         ('a2', 'b1'): 0.3,
            ...         ('a2', 'b2'): 0.7
            ...     })
            >>> for (assignment, value) in f:
            ...     print assignment, '->', value
            ('a1', 'b1') -> 0.8
            ('a1', 'b2') -> 0.2
            ('a2', 'b1') -> 0.3
            ('a2', 'b2') -> 0.7


    .. method:: Factor.observed(assignment_dict)

        Nastavení pozorovaných hodnot.

        .. code-block:: python

            >>> f = Factor(['A', 'B'],
            ...     {'A': ['a1', 'a2'], 'B': ['b1', 'b2']},
            ...     {
            ...         ('a1', 'b1'): 0.8,
            ...         ('a1', 'b2'): 0.2,
            ...         ('a2', 'b1'): 0.3,
            ...         ('a2', 'b2'): 0.7
            ...     })
            >>> f.observed({
            ...     ('a1', 'b1'): 0.6,
            ...     ('a1', 'b2'): 0.4,
            ... })
            >>> print f.pretty_print(50, 2)
            --------------------------------------------------
                A               B             Value      
            --------------------------------------------------
                a1              b1             0.6       
                a1              b2             0.4       
                a2              b1             0.0       
                a2              b2             0.0       
            --------------------------------------------------

        :arg assignment_dict: slovník s pozorovanými přiřazeními a jejich ohodnocením.

    .. method:: Factor.normalize([parents])

        Normalizace hodnot ve faktoru, aby jejich součet byl roven 1.

        Pokud je specifikován parametr ``parents``, pak musí být součet všech
        proměnných, které mají stejné přiřazení pro proměnné z ``parents``, roven
        1.

        .. code-block:: python

            >>> f = Factor(['A', 'B'],
            ...     {'A': ['a1', 'a2'], 'B': ['b1', 'b2']},
            ...     {
            ...         ('a1', 'b1'): 1,
            ...         ('a1', 'b2'): 3,
            ...         ('a2', 'b1'): 2,
            ...         ('a2', 'b2'): 2,
            ...     })
            >>> f.normalize(parents=['A'])
            >>> print f.pretty_print(50, 2)
            --------------------------------------------------
                A               B             Value      
            --------------------------------------------------
                a1              b1             0.25       
                a1              b2             0.75       
                a2              b1             0.5       
                a2              b2             0.5       
            --------------------------------------------------

        :arg parents: seznam rodičovských proměnných.

    .. method:: Factor.marginalize(keep)

        Vysčítání proměnných tak, aby zůstaly pouze proměnné z ``keep``.

        .. code-block:: python

            >>> f = Factor(['A', 'B'],
            ...     {'A': ['a1', 'a2'], 'B': ['b1', 'b2']},
            ...     {
            ...         ('a1', 'b1'): 0.8,
            ...         ('a1', 'b2'): 0.2,
            ...         ('a2', 'b1'): 0.3,
            ...         ('a2', 'b2'): 0.7,
            ...     })
            >>> g = f.marginalize(keep=['A'])
            >>> print g.pretty_print(50, 2)
            --------------------------------------------------
                        A                      Value          
            --------------------------------------------------
                       a1                       1.0           
                       a2                       1.0           
            --------------------------------------------------

        :arg keep: seznam proměnných, které mají zůstat.

    .. method:: Factor.most_probable([n])

        Nalezení nejpravděpodobnějších přiřazení proměnných.

        .. code-block:: python

            >>> f = Factor(['A'],
            ...     {'A': ['a1', 'a2']},
            ...     {
            ...         ('a1',): 0.8,
            ...         ('a2',): 0.2,
            ...     })
            >>> f.most_probable(2)
            [('a1', 0.8), ('a2', 0.2)]

        :arg n: počet požadovaných nejpravděpodobnějších přiřazení.
        :returns: seznam nejpravděpodobnějších přiřazení a jejich hodnot.

    .. method:: Factor.rename_variables(mapping)

        Přejmenování proměnných.

        Může se stát, že je potřeba přejmenovat proměnné, aby odpovídaly proměnným v jiném faktoru.

        .. code-block:: python

            >>> f = Factor(['A', 'B'],
            ...     {'A': ['a1', 'a2'], 'B': ['b1', 'b2']},
            ...     {
            ...         ('a1', 'b1'): 0.8,
            ...         ('a1', 'b2'): 0.2,
            ...         ('a2', 'b1'): 0.3,
            ...         ('a2', 'b2'): 0.7,
            ...     })
            >>> f.rename_variables({'A': 'X', 'B': 'Y'})
            >>> print f.pretty_print(50, 2)
            --------------------------------------------------
                X               Y             Value      
            --------------------------------------------------
                a1              b1             0.8       
                a1              b2             0.2       
                a2              b1             0.3       
                a2              b2             0.7       
            --------------------------------------------------

        :arg mapping: slovník se zobrazením ze stávajících názvů proměnných do nových názvů.


    **Příklady matematických operací**

    Násobení::

        >>> f1 = Factor(['A', 'B'],
        ...     {'A': ['a1', 'a2'], 'B': ['b1', 'b2']},
        ...     {
        ...         ('a1', 'b1'): 0.8,
        ...         ('a1', 'b2'): 0.2,
        ...         ('a2', 'b1'): 0.3,
        ...         ('a2', 'b2'): 0.7
        ...     })
        >>> f2 = Factor(['B', 'C'],
        ...     {'B': ['b1', 'b2'], 'C': ['c1', 'c2']},
        ...     {
        ...         ('b1','c1'): 0.3,
        ...         ('b1','c2'): 0.7,
        ...         ('b2','c1'): 0.5,
        ...         ('b2','c2'): 0.5,
        ...     })
        >>> fr = f1 * f2
        >>> print fr.pretty_print(50, 2)
        --------------------------------------------------
            A           B           C         Value    
        --------------------------------------------------
            a1          b1          c1         0.24    
            a1          b1          c2         0.56    
            a1          b2          c1         0.10    
            a1          b2          c2         0.10    
            a2          b1          c1         0.09    
            a2          b1          c2         0.21    
            a2          b2          c1         0.35    
            a2          b2          c2         0.35    
        --------------------------------------------------

    Umocnění::

        >>> f1 = Factor(['A', 'B'],
        ...     {'A': ['a1', 'a2'], 'B': ['b1', 'b2']},
        ...     {
        ...         ('a1', 'b1'): 0.8,
        ...         ('a1', 'b2'): 0.2,
        ...         ('a2', 'b1'): 0.3,
        ...         ('a2', 'b2'): 0.7
        ...     })
        >>> fr = f1 ** 2
        >>> print fr.pretty_print(50, 2)
        --------------------------------------------------
            A               B             Value      
        --------------------------------------------------
            a1              b1             0.64      
            a1              b2             0.04      
            a2              b1             0.09      
            a2              b2             0.49      
        --------------------------------------------------

Modul :mod:`node`
-----------------

Modul obsahuje implementace vrcholů tvořících grafický model.
Pro výpočty jsou používány třídy z modulu :mod:`~alex.infer.factor`.

.. class:: alex.infer.node.Node

    Abstraktní třída pro reprezentaci vrcholů.

    Obsahuje definice základních metod, které musí obsahovat každá implementace vrcholu.

    .. method:: __init__(name[, aliases])

        Vytvoření nového vrcholu.

        Při vytvoření vrcholu je třeba zadat jeho jméno, pod kterým bude možné
        jej nalézt při inferenci a je možné předat aliasy pro proměnné. Aliasy pro
        proměnné slouží k přejmenování proměnných ve zprávách, které přicházejí
        do vrcholu.

        :arg name: jméno vrcholu.
        :arg aliases: zobrazení ze jmen proměnných, které se mohou objevit ve zprávě, do proměnných v parametru.

    .. method:: add_neighbor(node, \*\*options)

        Přidání souseda.

        Pro většinu vrcholů bude stačit pouze vrchol, zůstává tu ovšem možnost přidat implementačně závislé parametry.

        :arg node: sousední vrchol.
        :arg options: implementačně závislé parametry.

    .. method:: connect(node, \*\*options)

        Propojení dvou vrcholů.

        Propojení dvou vrcholů, stačí zavolat pouze jednou pro dvojici vrcholů.
        Interně zavolá metodu :meth:`add_neighbor` a předá jí parametry.

        :arg node: sousední vrchol.
        :arg options: implementačně závislé parametry.

    .. method:: init_messages()

        Inicializace všech zpráv mezi vrcholem a jeho sousedy.

    .. method:: message_from(node, message)

        Přijmutí zprávy ze sousedního vrcholu.

        Zpráva je uložena a použita při dalších výpočtech.

        :arg node: sousední vrchol.
        :arg message: zpráva ze sousedního vrcholu.

    .. method:: message_to(node)

        Poslání zprávy do sousedního vrcholu.

        :arg node: sousední vrchol, kterému má být zpráva zaslána.

    .. method:: normalize([parents])

        Normalizace pravděpodobnostního rozdělení.

        Při počítání nejsou zprávy normalizované, proto ani výsledek nemusí být
        normalizovaný a je tedy třeba jej normalizovat před jakýmkoliv dalším
        použitím. Pro normalizaci je možné zadat, které proměnné jsou rodiče,
        pak musí být suma ohodnocení všech přiřazení se stejnými rodiči rovna
        jedné.

        :arg parents: seznam proměnných, které jsou rodiči vrcholu.

    .. method:: update()

        Aktualizace interní pravděpodobnostní distribuce.

        Příchozí zprávy jsou pouze uloženy a je potřeba aktualizovat interní
        reprezentaci jejich součinu před počítáním odchozích zpráv.

.. class:: alex.infer.node.FactorNode

    Předek: :class:`alex.infer.node.Node`

    Abstraktní třída reprezentující vrcholy pro faktory.


.. class:: alex.infer.node.VariableNode

    Předek: :class:`alex.infer.node.Node`

    Abstraktní třída reprezentující vrcholy pro proměnné.

Vrcholy pro diskrétní vrcholy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. class:: alex.infer.node.DiscreteVariableNode

    Předek: :class:`alex.infer.node.VariableNode`

    Reprezentace diskrétních proměnných.

    .. attribute:: belief

        Marginální pravděpodobnostní rozdělení pro proměnnou. Typu :class:`Factor`.

    .. method:: __init__(name, values, logarithmetic=True)

        Vytvoření nového vrcholu pro diskrétní proměnné.

        Pro vytvoření je třeba jméno proměnné a hodnoty, kterých může nabývat.

        Také je možné zadat, jestli používat při výpočtech trik s aritmetikou nad zlogaritmovanými čísly.
        Je třeba, aby všechny vrcholy v grafickém modelu byly nastaveny stejně.

        :arg name: název proměnné.
        :arg values: seznam možných hodnot.
        :arg logarithmetic: zda-li používat trik s logaritmy.

    .. method:: add_neighbor(node)

        Přidání souseda.

        :arg node: sousední vrchol.

    .. method:: connect(node, \*\*options)

        Propojení dvou vrcholů.

        Propojení dvou vrcholů, stačí zavolat pouze jednou pro dvojici vrcholů.
        Interně zavolá metodu :meth:`add_neighbor` a předá jí parametry.

        :arg node: sousední vrchol.

    .. method:: init_messages()

        Inicializace všech zpráv mezi vrcholem a jeho sousedy.

    .. method:: message_from(node, message)

        Přijmutí zprávy ze sousedního vrcholu.

        Zpráva je uložena a použita při dalších výpočtech.

        :arg node: sousední vrchol.
        :arg message: zpráva ze sousedního vrcholu.

    .. method:: message_to(node)

        Poslání zprávy do sousedního vrcholu.

        :arg node: sousední vrchol, kterému má být zpráva zaslána.

    .. method:: normalize()

        Normalizace pravděpodobnostního rozdělení.

        Při počítání nejsou zprávy normalizované, proto ani výsledek nemusí být
        normalizovaný a je tedy jej třeba normalizovat před jakýmkoliv dalším
        použitím.

    .. method:: update()

        Aktualizace marginální pravděpodobnostní distribuce.

        Příchozí zprávy jsou pouze uloženy a je potřeba aktualizovat interní
        reprezentaci jejich součinu před počítáním odchozích zpráv.

    .. method:: observed(assignment_dict)

        Nastavení pozorovaných hodnot.

        Proměnná je nastavená na pozorované rozdělení. Pravděpodobnost nepozorovaných hodnot
        je nulová.

        :arg assignment_dict: slovník se zobrazením z hodnot do jejich pravděpodobností.

    .. method:: most_probable(n)

        Získání nejpravděpodobnějších hodnot.

        :arg n: počet nejpravděpodobnějších hodnot, které mají být vráceny.
        :returns: seznam dvojic ve tvaru (hodnota, její pravděpodobnost) seřazený podle pravděpodobnosti.

.. class:: alex.infer.node.DiscreteFactorNode

    Předek: :class:`alex.infer.node.FactorNode`

    Vrchol pro diskrétní faktor, reprezentující diskrétní pravděpodobnostní rozdělení.

    .. method:: __init__(name, factor)

        Vytvoření nového vrcholu pro diskrétní faktor.

        Pro vytvoření je třeba jméno faktoru a samotný faktor.

        Také je možné zadat, jestli používat při výpočtech trik s aritmetikou nad zlogaritmovanými čísly.
        Je třeba, aby všechny vrcholy v grafickém modelu byly nastaveny stejně.

        :arg name: název proměnné.
        :arg factor: faktor reprezentující diskrétní pravděpodobnostní rozdělení.
        :type factor: :class:`Factor`

    .. method:: add_neighbor(node)

        Přidání souseda.

        :arg node: sousední vrchol.

    .. method:: connect(node)

        Propojení dvou vrcholů.

        Propojení dvou vrcholů, stačí zavolat pouze jednou pro dvojici vrcholů.
        Interně zavolá metodu :meth:`add_neighbor` obou vrcholů a předá jí parametry.

        :arg node: sousední vrchol.

    .. method:: init_messages()

        Inicializace všech zpráv mezi vrcholem a jeho sousedy.

    .. method:: message_from(node, message)

        Přijmutí zprávy ze sousedního vrcholu.

        Zpráva je uložena a použita při dalších výpočtech.

        :arg node: sousední vrchol.
        :arg message: zpráva ze sousedního vrcholu.

    .. method:: message_to(node)

        Poslání zprávy do sousedního vrcholu.

        :arg node: sousední vrchol, kterému má být zpráva zaslána.

    .. method:: normalize([parents])

        Normalizace pravděpodobnostního rozdělení.

        Při počítání nejsou zprávy normalizované, proto ani výsledek nemusí být
        normalizovaný a je tedy jej třeba normalizovat před jakýmkoliv dalším
        použitím. Pro normalizaci je možné zadat, které proměnné jsou rodiče,
        pak musí být suma ohodnocení všech přiřazení se stejnými rodiči rovna
        jedné.

        :arg parents: seznam proměnných, které jsou rodiči vrcholu. 

    .. method:: update()

        Aktualizace interní reprezentace.

        Příchozí zprávy jsou pouze uloženy a je potřeba aktualizovat interní
        reprezentaci jejich součinu před počítáním odchozích zpráv.

Vrcholy pro Dirichletovské parametry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. class:: alex.infer.node.DirichletParameterNode

    Předek: :class:`alex.infer.node.VariableNode`

    Reprezentace parametrů Dirichletovského rozdělení.

    .. attribute:: alpha

        Parametry dirichletovského rozdělení. Typu :class:`Factor`.

    .. method:: __init__(name, alpha[, aliases])

        Vytvoření nového vrcholu pro parametry Dirichletovského rozdělení.

        Pro vytvoření je třeba jméno proměnné a parametry.
        Aliasy pro proměnné slouží k přejmenování proměnných ve zprávách, které
        přicházejí do vrcholu.                                                             

        :arg name: název proměnné.
        :arg alpha: parametry Dirichletovského rozdělení.
        :type alpha: :class:`~alex.infer.factor.Factor`
        :arg aliases: zobrazení ze jmen proměnných, které se mohou objevit ve zprávě, do proměnných v parametru.

    .. method:: add_neighbor(node)

        Přidání souseda.

        :arg node: sousední vrchol.
        :type node: :class:`~alex.infer.node.DirichletFactorNode`

    .. method:: connect(node, \*\*options)

        Propojení dvou vrcholů.

        Propojení dvou vrcholů, stačí zavolat pouze jednou pro dvojici vrcholů.
        Interně zavolá metodu :meth:`add_neighbor` a předá jí parametry.

        :arg node: sousední vrchol.
        :type node: :class:`~alex.infer.node.DirichletFactorNode`

    .. method:: init_messages()

        Inicializace všech zpráv mezi vrcholem a jeho sousedy.

    .. method:: message_from(node, message)

        Přijmutí zprávy ze sousedního vrcholu.

        Zpráva je uložena a použita při dalších výpočtech.

        :arg node: sousední vrchol.
        :arg message: zpráva ze sousedního vrcholu.

    .. method:: message_to(node)

        Poslání zprávy do sousedního vrcholu.

        :arg node: sousední vrchol, kterému má být zpráva zaslána.


.. class:: alex.infer.node.DirichletFactorNode

    Předek: :class:`alex.infer.node.FactorNode`

    Diskrétní faktor, který ovšem bere své parametry z
    :class:`~alex.infer.node.DirichletParameterNode` vrcholu.

    .. method:: __init__(name[, aliases])

        Vytvoření nového vrcholu pro faktor.

        Pro vytvoření je třeba jméno faktoru.

        Aliasy pro proměnné slouží k přejmenování proměnných ve zprávách, které
        přicházejí do vrcholu.

        :arg name: název faktoru.
            :arg aliases: zobrazení ze jmen proměnných, které se mohou objevit ve zprávě do proměnných ve faktoru.

    .. method:: add_neighbor(node)

        Přidání souseda.

        :arg node: sousední vrchol.

    .. method:: connect(node)

        Propojení dvou vrcholů.

        Propojení dvou vrcholů, stačí zavolat pouze jednou pro dvojici vrcholů.
        Interně zavolá metodu :meth:`add_neighbor` obou vrcholů a předá jí parametry.

        :arg node: sousední vrchol.

    .. method:: init_messages()

        Inicializace všech zpráv mezi vrcholem a jeho sousedy.

    .. method:: message_from(node, message)

        Přijmutí zprávy ze sousedního vrcholu.

        Zpráva je uložena a použita při dalších výpočtech.

        :arg node: sousední vrchol.
        :arg message: zpráva ze sousedního vrcholu.

    .. method:: message_to(node)

        Poslání zprávy do sousedního vrcholu.

        :arg node: sousední vrchol, kterému má být zpráva zaslána.

    .. method:: update()

        Aktualizace interní reprezentace.

        Příchozí zprávy jsou pouze uloženy a je potřeba aktualizovat interní
        reprezentaci jejich součinu před počítáním odchozích zpráv.


Modul :mod:`lbp`
-----------------

.. exception:: alex.infer.lbp.LBPError

    Výjimka pro chyby při inferenci.

.. class:: alex.infer.lbp.LBP

    Inference v grafickém modelu pomocí Loopy Belief Propagation.

    .. method:: __init__(strategy='sequential')

        Vytvoření nové instance LBP algoritmu.
        
        Je možné nastavit strategii výběru vrcholů:

        * *sequential* -- vrcholy jsou vybírány v takovém pořadí, v jakém byly vloženy,
        * *tree* -- grafický model je ve formě stromu,
        * *layers* -- inference na Dynamické Bayesovské síti.

        :arg strategy: strategie, která má být použita pro výběr vrcholů.

    .. method:: add_nodes(nodes)

        Přidání vrcholů k inferenci.

        :arg nodes: seznam vrcholů.

    .. method:: add_layer(layer)

        Přidání vrstvy na konec grafického modelu.

        :arg layer: seznam vrcholů tvořících jednu vrstvu.

    .. method:: add_layers(layers)

        Přidání vrstev na konec grafického modelu.

        :arg layers: seznam seznamů s vrcholy.

    .. method:: clear_nodes()

        Smazání všech vrcholů.

    .. method:: clear_layers()

        Smazání všech vrstev.

    .. method:: init_messages()

        Inicializace zpráv pro všechny vrcholy.

    .. method:: run(n_iterations=1, from_layer])

        Spustit inferenci v grafickém modelu.

        Je možné nastavit počet iterací, po kterém se má inference zastavit.
        U stromu není třeba zadávat počet iterací, bude provedena pouze jedna.

        U vrstev je možné zadat od které vrstvy inferenci provádět. 
        Popřípadě budou zprávy propagovány od začátku.

        :arg n_iterations: počet iterací.
        :arg from_layer: vrstva, od které se mají zprávy propagovat.

