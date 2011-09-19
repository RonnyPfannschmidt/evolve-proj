Betrachtung Genetischer Programmierung
======================================

Begriffe
--------

Genetische Algorithmen
  Klasse von Algorithmen,
  welche die Prinzipien der Evolution Anwenden
  um Problemlöser zu Finden
Genetische Programmierung
  Klasse von Genetischen Algorithmen,
  welche anstelle von Merkmalsvektoren Programme oder Funktionen
  als Elemente einer Population haben

Grundlagen
----------

Allen Genetischen Algorithmen liegen liegen die Komponenten der Evolution
zu grunde.

1. Es gibt eine Population
2. Es gibt Replikaton/Fortpflanzung mit Mutation
3. Es gibt Selektion (in der Natur - Überlebung bis Fortpflanzung/Replikation)

Vorteile
~~~~~~~~

* in der Lage höchst optimierte Lösungen zu finden
* in der Lage unerwartete Lösungen zu finden



Nachteile
~~~~~~~~~~

* 'blind', Tendenz in lokalen minima/maxima Steckenzubleiben
* nimmt nur eine Bewertung des Gesammtgenoms eines Individuums vor,
  schlechte/nutzlose Teile des Genoms werden nicht erkannt
* Große Menge an notwendigen Validierungen/Bewertungn
  (für jedes Individuum jeder Generation muss bewertet werden)





Ein einfaches Beispiel
----------------------

Zu demonstrationszwecken soll mittels eines Genetischen Programms die
funktion `f(a, b)=sqrt(a*a + b*b)` angenährt werden.

dazu stehen die folgenden funktionsbausteine zur verfuegung

.. literalinclude:: ./funfind.py
  :language: python
  :start-after: import sys
  :end-before: def eval_node



verglichen werden visitor basierte evaluierung


.. literalinclude:: ./funfind.py
  :language: python
  :pyobject: eval_node

.. literalinclude:: ./funfind.py
  :language: python
  :pyobject: eval_nodes




* titelliste

* basics erklaeren
* perf vergleich python pypy
  * optimierungen erlaeutern/vergleichen
* multicpu
* network
* transformation von merkmalsvektoren (wie zum geier abbilden):
