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
  welche anstelle von Merkmals Vektoren Programme oder Funktionen
  als Elemente einer Population haben


Allen Genetischen Algorithmen liegen liegen die Komponenten der Evolution
zu Grunde.

1. Es gibt eine Population
2. Es gibt Replikation/Fortpflanzung mit Mutation
3. Es gibt Selektion (in der Natur - Überlebend bis Fortpflanzung/Replikation)

Eigenschaften des Algorithmus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* parallele Suche in einer Population von möglichen Lösungen,
  sodass immer mehrere potentielle Lösungen gefunden werden
* benötigen kaum Problem wissen,
  insbesondere keine Gradienten Information, können also auch bei
  diskontinuierlichen Problemen angewendet werden
* gehören zur Klasse der stochastischen Such verfahren
  und ermöglichen damit auch die Behandlung von Problemen,
  die mit traditionellen Optimierung Methoden nicht mehr handhabbar sind.
* Evolutionäre Algorithmen bieten im Allgemeinen keine Garantie,
  das globale Optimum in vernünftiger Zeit zu finden.
* Großer Nachteil der EAs ist der oft sehr große Rechenzeit bedarf


Ein einfaches Beispiel
----------------------

Zu Demonstration zwecken soll mittels eines Genetischen Programms die
Funktion `f(a, b)=sqrt(a*a + b*b)` angenährt werden.

Dazu stehen die folgenden Funktionsbausteine zur Verfügung

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
  :pyobject: main

Als Betrachtungs-grundlage werden 3 Arten
der Evaluierung gegenüber gestellt.


**code generator basierte Evaluation**

  .. literalinclude:: ./funfind.py
    :language: python
    :pyobject: eval_code


**visitor basierte Evaluation**

  .. literalinclude:: ./funfind.py
    :language: python
    :pyobject: visit_node

  .. literalinclude:: ./funfind.py
    :language: python
    :pyobject: eval_visit


**operator list basierte Evaluation**


  .. literalinclude:: ./funfind.py
    :language: python
    :pyobject: nodeops

  .. literalinclude:: ./funfind.py
    :language: python
    :pyobject: _nodeops

  .. literalinclude:: ./funfind.py
    :language: python
    :pyobject: eval_stack



Resultate des Geschwindigkeit Vergleiches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Um einen Eindruck über die Geschwindigkeit der Verschiedenen Evaluierung Methoden
zu gewinnen, wurden sie vor das gleiche Problem gestellt.
Zusätzlich wurde neben dem normalen Python Interpreter
auch PyPy in den Vergleich mit einbezogen, um einen Eindruck zu gewinnen,
welchen Einfluss ein Python Interpreter mit JIT hat.

.. literalinclude:: speed.rst


Demonstration der Eigenheiten des Algorithmus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Um diverse Eigenheiten zu demonstrieren,
wurden gewinnende Individuen aus Verschiedenen Generationen entnommen

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

  In diesem Beispiel ist die Sequenz `sub(b, b)` der "Fehler"
  es ist ein typischer Auslöschung Fehler, der das eigentliche Ergebnis nicht ändert


2. Fehler Daten bei zuwenig Generationen

  Folgend ist das beste Individuum bei einem lauf mit 50 Fenerationen

  es ist unschwer zu erkennen, dass es weit vom Optimum entfernt ist

  .. code-block:: python

    sqrt(add(
      sqrt(mul(sub(b, b), mul(b, a))),
      add(
        mul(sub(b, b), sqrt(b)),
        add(mul(a, a), mul(b, b)))))


3. Fehler Daten bei zu geringer Population

  Folgend ist das beste Individuum wenn die Populationsgrösse stark reduziert ist

  .. code-block:: python

    add(
      sqrt(add(
        mul(sqrt(b), add(b, b)),
        sub(sqrt(b), a))), 
      sqrt(sub(a, sqrt(a))))



Resultat eines Erfolgreichen Durchlaufes
-----------------------------------------

500 Generationen
  .. code-block:: python

    sqrt(sub(
      sub(add(mul(a, a), mul(b, b)), a), a))

1000 Generationen
  sqrt(add(add(mul(b, b), mul(a, a)), mul(sub(b, b), mul(sub(a, a), sub(b, a)))))
2000 Generationen 2000 Population
  sqrt(add(add(mul(b, b), mul(a, a)), mul(add(add(b, a), a), mul(mul(a, a), sub(a, a)))))

40 gen, 2000 Items, Kosten für Tiefe
  sqrt(add(mul(b, b), mul(a, a)))



Beispiel schneller erfolgreicher Durchlaufe::

  $ PYTHONPATH=../pyevolve/ pypy-bin funfind.py stack \
  >           --generations 2000 \
  >           --population 2000 \
  >           --height-weight=0.00000001
  Gen. 0 (0.00%): Max/Min/Avg Fitness(Raw) [1575.10(640067.30)/1312.04(0.72)/1312.58(1312.58)]
  Gen. 20 (1.00%): Max/Min/Avg Fitness(Raw) [5.18(927.35)/4.32(0.70)/4.32(4.32)]
  Gen. 40 (2.00%): Max/Min/Avg Fitness(Raw) [6.80(1388.24)/5.66(0.61)/5.67(5.67)]
  Gen. 60 (3.00%): Max/Min/Avg Fitness(Raw) [6.52(3972.74)/5.43(0.00)/5.43(5.43)]
  ^C
    A break was detected, you have interrupted the evolution !

  Gen. 72 (3.60%): Max/Min/Avg Fitness(Raw) [4.99(1178.43)/4.16(0.00)/4.16(4.16)]
  Total time elapsed: 21.301 seconds.
  sqrt(add(mul(b, b), mul(a, a)))
  


Der grosse kombinatorische Test
=================================

Um das Verhalten des Algorithmus besser zu verstehen,
wurde er für eine grosse Menge an Konfigurationen jeweils komplett durchgeführt.


Dabei wurden folgende fixen Achsen verwendet:

:crossover rate: 1.0
:mutation rate: 0.08
:height shift: -3

Die `height shift` ist dabei der Wert um den die Baum höhe
verändert wird, bevor sie in die Gewichtung eingeht.

.. literalinclude:: ./funfind.py
  :language: python
  :pyobject: eval_height

Der Wert von -3 wurde gewählt, weil die optimale Baum höhe im
Beispiel ist und versucht wird, das Bewertung Ergebnis zu minimieren.

Die Dynamischen Achsen sind:

:height-weight: [-2,-1,-0.1,-0.01,-0.001,0,0.001,0.01,0.1,1,2]
:generations: [20,50,100,300,500,1000,1500,2000,3000,5000]
:population: [20,50,100,300,500,1000,1500,2000,3000,5000]

`height-weight` gibt dabei ein, wie stark die bereits erwähnte Baum höhe
in die Bewertung mit eingeht.


Um einen groben Überblick zu erlangen,
wurden für alle Kombinationen von height-weight,
Plots über Generationen X Population erstellt,
und korrekte/inkorrekte Resultate markiert.

Dabei wurde nur ein optimales Ergebnis als korrekt angesehen
(i.e. `sqrt(add(mul(a, a), mul(b, b)))`
oder `sqrt(add(mul(b, b) mul(a, a)))`).

Alle Plots sind in der zugefügten `datei <./fill_run.html>`_ einsehbar.

Da alle Ergebnisse grosse Ähnlichkeit aufweisen
(weight_height scheint keinen visuell feststellbaren Einfluss zu haben),
wurde das Beispiel mit der Gewichtung 0 gewählt.

.. raw:: html
  :file: fill_run_fragment.html




Fazit
======

Anhand des Datensatzes ist recht einleuchtend der Effekt von Zufallstreffern,
sowie zunehmender Menge von Generationen und Population zu erkennen.

Die gewonnenen Daten legen nahe,
dass die Qualität des Ergebnisses in direkter Relation mit
der Menge an Generationen und Population steht.

Die Gewichtung der Baum höhe hatte keinen Effekt.



Selbstkritik
============

Bisher konnten weitere interessante Grössen zur Parametrisierung noch
nicht analysiert werden.
Besonders interessant sind dabei cross-over rate und Mutationsrate.

Entgegen der auf den Beispielen für Eigenarten basierenden Erwartung,
dass die Höhe des Baumes einen Einfluss hat,
stellte sich heraus, dass sie keinen hat.

Weiterhin ist nicht klar,
welchen Einfluss die Komplexität der Funktion auf das Ergebnis hat.

Der hohe Aufwand an Rechenzeit legt weitere Projekte nahe.
