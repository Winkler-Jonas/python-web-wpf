Server
******

Da es sich bei dem Projekt um ein Produktionsfähiges System handelt, kann die Applikation nicht durch den
Django-Debug-Server gestartet werden. Um die verschiedenen Docker-Einheiten und damit den Server zu initialisieren,
müssen die Images aufgebaut und gestartet werden. ``Dieser Process kann einmalig bis zu 15 Minuten dauern``

.. code-block:: bash

    $ docker-compose up --build

Anschließend müssen innherhalb des Zhehe Docker-Containers verschiedene Operationen ausgeführt werden. Dies sollte
aus Sicherheitsgründen stehts von dem Verwaltenten Administrator durchgeführt werden, da dies andernfall zu einer
Sicherheitslücke führen kann.

Wenn Docker den Aufbau der Images fertiggestellt hat, welchseln Sie in ein neues Fenster und geben Sie folgenden
Befehl ein, um zu sehen welche Images auf Ihrem System derzeit laufen.

.. code-block:: bash

    $ docker ps

Der Output des Befehls sollte in etwa so aussehen.

.. image:: /_static/img/setup/docker_ps_output.png
    :scale: 40 %
    :align: center

Ganz links sehen Sie die ``ID`` des Containers und in der zweiten Spalte den ``Namen`` des Images.
Wecheln Sie jetzt in den Container mit dem Namen **python-web-wpf-zhehe** mit folgendem Befehl.
Ändern Sie die ID des Containers ensprechend Ihrer ``docker ps`` Ausgabe.

.. code-block:: bash

    $ docker exec -it e430143a6129 bash

Sie befinden sich nun innerhalb des Docker-Containers. Führen Sie nun nur die ``init.sh`` aus
und füllen Sie die Daten für den Superuser aus.

Um die Initialisierung innherhalb des Docker-Containers zu vereinfachen habe ich ein Skript ``init.sh`` erstellt, welches
die verschiedenen Operationen durchführt. Das Skript arbeitet folgende Schritte ab.

..  admonition:: python manage.py migrate
    :class: toggle

    | Dieses Kommando erstellt die Tabellen in der Datenbank.
    | Des Weiteren wird der Name der Domain auf ``zhehe.com`` verändert,
    | sowie auch der Name bezogen auf die Webseite.

..  admonition:: python manage.py createsuperuser
    :class: toggle

    | Dieses Kommando ermöglicht es dem Administrator einen Super-User anzulegen, mit
    | welchem Benutzerdaten verwaltet werden können.

..  admonition:: python manage.py collectstatic
    :class: toggle

    | Dieses Kommando verschiebt alle statischen Dateien in den in der ``settings.py`` angegebenen
    | ``STATIC_ROOT`` Ordner, damit der Webserver diese zur Verfügung stellen kann.

Nach der Ausführung der Initialisierung kann die Webseite nun unter ``0.0.0.0:8080`` aufgefunden und ausgeführt werden.