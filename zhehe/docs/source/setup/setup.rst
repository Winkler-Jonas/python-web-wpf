Server
******

Da es sich bei dem Projekt um ein Produktionsfähiges System handelt, kann die Applikation nicht durch den
Django-Debug-Server gestartet werden. Um die verschiedenen Docker-Einheiten und damit den Server zu initialisieren,
müssen die Images aufgebaut und gestartet werden. ``Dieser Process kann einmalig 15 Minuten dauern``

.. code-block:: bash

    $ docker-compose up --build

Anschließend müssen innherhalb des Zhehe Docker-Containers verschiedene Operationen ausgeführt werden. Dies sollte
aus Sicherheitsgründen stehts von dem Verwaltenten Administrator durchgeführt werden, da dies andernfall zu einer
Sicherheitslücke führen kann.

Um die Initialisierung innherhalb des Docker-Containers zu vereinfachen habe ich ein Skript ``init.sh`` erstellt, welches
die verschiedenen Operationen durchführt. Das Skript arbeitet folgende Schritte ab.

..  admonition:: python manage.py migrate
    :class: toggle

    | Dieses Kommando erstellt die Tabellen in der Datenbank.
    | Des Weiteren wird der Name der Domain auf ``zhehe.com``` verändert,
    | sowie auch der Name bezogen auf die Webseite.

..  admonition:: python manage.py createsuperuser
    :class: toggle

    | Dieses Kommando ermöglicht es dem Administrator einen Super-User anzulegen, mit
    | welchem Benutzerdaten verwaltet werden können.

..  admonition:: python manage.py collectstatic
    :class: toggle

    | Dieses Kommando verschiebt alle statischen Dateien in den in der ``settings.py`` angegebenen
    | ``STATIC_ROOT`` Ordner, damit der Webserver diese zur Verfügung stellen kann.

