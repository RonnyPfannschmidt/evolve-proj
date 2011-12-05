Betrachtung Genetischer Programmierung
======================================

:Author: Ronny Pfannschmidt
:Matr Nr: 250154


Grundlagen
----------

Begriffe
~~~~~~~~

Genetische Algorithmen
  Klasse von Algorithmen,
  welche die Prinzipien der Evolution Anwenden
  um Problemlöser zu Finden
Genetische Programmierung
  Klasse von Genetischen Algorithmen,
  welche anstelle von Merkmalsvektoren Programme oder Funktionen
  als Elemente einer Population haben


Allen Genetischen Algorithmen liegen liegen die Komponenten der Evolution
zu grunde.

1. Es gibt eine Population
2. Es gibt Replikaton/Fortpflanzung mit Mutation
3. Es gibt Selektion (in der Natur - Überlebung bis Fortpflanzung/Replikation)

Eigenschaften des Algorithmus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* parallele Suche in einer Population von möglichen Lösungen,
  sodass immer mehrere potentielle Lösungen gefunden werden
* benötigen kaum Problemwissen,
  insbesondere keine Gradienteninformation,
  können also z.B. auch bei diskontinuierlichen Problemen
  angewendet werden
* gehören zur Klasse der stochastischen Suchverfahren
  und ermöglichen damit auch die Behandlung von Problemen,
  die mit traditionellen Optimierungsmethoden nicht mehr handhabbar sind.
* Evolutionäre Algorithmen bieten im Allgemeinen keine Garantie,
  das globale Optimum in vernünftiger Zeit zu finden.
* Großer Nachteil der EAs ist der oft sehr große Rechenzeitbedarf


Ein einfaches Beispiel
----------------------

Zu Demonstrationszwecken soll mittels eines Genetischen Programms die
funktion `f(a, b)=sqrt(a*a + b*b)` angenährt werden.

dazu stehen die folgenden Funktionsbausteine zur verfuegung

.. literalinclude:: ./funfind.py
  :language: python
  :start-after: import sys
  :end-before: def visit_node


Den Hauptteil des Programmes stellt dabei

.. literalinclude:: ./funfind.py
  :language: python
  :pyobject: main_run

.. literalinclude:: ./funfind.py
  :language: python
  :start

Als Betrachtungsgrundlage werden 3 Arten
der Evaluierung gegenüber gestellt.


**code generator basierte evaluierung**

  .. literalinclude:: ./funfind.py
    :language: python
    :pyobject: eval_code


**visitor basierte evaluierung**

  .. literalinclude:: ./funfind.py
    :language: python
    :pyobject: visit_node

  .. literalinclude:: ./funfind.py
    :language: python
    :pyobject: eval_visit


**operator list basierte evaluation**


  .. literalinclude:: ./funfind.py
    :language: python
    :pyobject: nodeops

  .. literalinclude:: ./funfind.py
    :language: python
    :pyobject: _nodeops

  .. literalinclude:: ./funfind.py
    :language: python
    :pyobject: eval_stack



Resultate des Geschwindigkeitsvergleiches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: speed.rst


Demonstration der Eigenheiten des Algorithmus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Um diverse Eigenheiten zu demonstrieren,
werden gewinnene Individuen aus Verschiedenen generationen entnommen

1. Tote Teile des Genoms
  
  .. code-block:: python

    add(
      mul(
        sub(
          sub(add(a, b), mul(b, a)),
          sub(sqrt(a), sub(b, b))),
        sqrt(sub(mul(a, b), mul(a, b)))),
      sqrt(add(
        add(mul(a, b), mul(b, b)),
        mul(sub(a, b), a))))

  in diesem beispiel ist die sequenz `sub(b, b)` der "fehler"
  es ist ein typischer Auslöschungsfehler


2. fehlerdaten bei zuwenig generationen

  folgend ist das beste individuum bei einem lauf mit 50 generationen

  es ist unschwer zu erkennen, dass es weit vom optimum ist

  .. code-block:: python

   sqrt(add(
     sqrt(mul(sub(b, b), mul(b, a))),
     add(
       mul(sub(b, b), sqrt(b)),
       add(mul(a, a), mul(b, b)))))


3. fehlerdaten bei zu geringer population
  
  folgend ist das beste individuum wenn die populationsgroesse stark reduziert ist

  .. code:: python
    add(
      sqrt(add(
        mul(sqrt(b), add(b, b)),
        sub(sqrt(b), a))), 
      sqrt(sub(a, sqrt(a))))



Resultat eines Erfolreichen Durchlaufes
-----------------------------------------

500 generationen
  .. code:: python

    sqrt(sub(
      sub(add(mul(a, a), mul(b, b)), a), a))

1000 generationen
  sqrt(add(add(mul(b, b), mul(a, a)), mul(sub(b, b), mul(sub(a, a), sub(b, a)))))
2000 generationen 2000 pop
  sqrt(add(add(mul(b, b), mul(a, a)), mul(add(add(b, a), a), mul(mul(a, a), sub(a, a)))))


40 gen, 2000 items, kosten fuer tiefe
  sqrt(add(mul(b, b), mul(a, a)))






Beispiel schneller erfolgreicher run:w::

  $ PYTHONPATH=../pyevolve/ pypy-bin funfind.py stack --generations 2000 --population 2000 --height-weight=0.00000001
  Gen. 0 (0.00%): Max/Min/Avg Fitness(Raw) [1575.10(640067.30)/1312.04(0.72)/1312.58(1312.58)]
  Gen. 20 (1.00%): Max/Min/Avg Fitness(Raw) [5.18(927.35)/4.32(0.70)/4.32(4.32)]
  Gen. 40 (2.00%): Max/Min/Avg Fitness(Raw) [6.80(1388.24)/5.66(0.61)/5.67(5.67)]
  Gen. 60 (3.00%): Max/Min/Avg Fitness(Raw) [6.52(3972.74)/5.43(0.00)/5.43(5.43)]
  ^C
    A break was detected, you have interrupted the evolution !

  Gen. 72 (3.60%): Max/Min/Avg Fitness(Raw) [4.99(1178.43)/4.16(0.00)/4.16(4.16)]
  Total time elapsed: 21.301 seconds.
  sqrt(add(mul(b, b), mul(a, a)))
  




spiel



* titelliste

* basics erklaeren
* perf vergleich python pypy
  
  * optimierungen erlaeutern/vergleichen


* problem des zufalls erlautern


* multicpu
  auf pypy und cpython vergleichen

* network
* transformation von merkmalsvektoren (wie zum geier abbilden):
