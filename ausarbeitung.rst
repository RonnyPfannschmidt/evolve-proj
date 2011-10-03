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

* parallele Suche in einer Population von möglichen Lösungen, sodass immer mehrere potentielle Lösungen gefunden werden
* benötigen kaum Problemwissen, insbesondere keine Gradienteninformation, können also z.B. auch bei diskontinuierlichen Problemen angewendet werden
* gehören zur Klasse der stochastischen Suchverfahren und ermöglichen damit auch die Behandlung von Problemen,
  die mit traditionellen Optimierungsmethoden nicht mehr handhabbar sind.
* Evolutionäre Algorithmen bieten im Allgemeinen keine Garantie,
  das globale Optimum in vernünftiger Zeit zu finden.
* Großer Nachteil der EAs ist der oft sehr große Rechenzeitbedarf


Ein einfaches Beispiel
----------------------

Zu demonstrationszwecken soll mittels eines Genetischen Programms die
funktion `f(a, b)=sqrt(a*a + b*b)` angenährt werden.

dazu stehen die folgenden funktionsbausteine zur verfuegung

.. literalinclude:: ./funfind.py
  :language: python
  :start-after: import sys
  :end-before: def eval_node


um einen einfachen performance-vergleich zu erhalten,
werden die folgenden implemenationen von bewertungsfunktionen
auf pypy und cpython vergleichen

**visitor basierte evaluierung**

  .. literalinclude:: ./funfind.py
    :language: python
    :pyobject: eval_node

  .. literalinclude:: ./funfind.py
    :language: python
    :pyobject: eval_nodes

**code generator basierte evaluierung**

  .. literalinclude:: ./funfind.py
    :language: python
    :pyobject: eval_code


Den Hauptteil des Programmes stellt dabei

.. literalinclude:: ./funfind.py
  :language: python
  :pyobject: main_run







* titelliste

* basics erklaeren
* perf vergleich python pypy
  * optimierungen erlaeutern/vergleichen
* multicpu
* network
* transformation von merkmalsvektoren (wie zum geier abbilden):
