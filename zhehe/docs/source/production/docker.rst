Docker - Django
***************

.. image:: /_static/img/docker/docker_django_label.png
    :scale: 50 %
    :align: center
    :target: https://miro.medium.com/max/1400/1*h205DQBt-f7ikKiPpP4Gxg.png

In diesem Projekt wird versucht, Docker in Verbindung mit dem Python Django Framework für das Deployment auf einem
Server einzurichten. Hierfür werden verschiedene Docker-Container (Nginx, Python, GUnicorn, PostgreSqlDB..) erstellt
und mit Docker-Compose ein komplettes System zusammen gesetzt, welches Systemunabhängig auf dem Server eines Kunden
deployed werden kann.

.. rubric:: Inhalt

- Installation

    - `Linux Mint`_
    - `Andere Betriebssysteme`_
    - `Projektstruktur`_
    - `Django`_
    - `Docker-Compose`_

Installation
------------

Im nachfolgenden Projekt wird der APT-Packetmanager verwendet, falls Sie einen anderen Packetmanager verwenden, lesen Sie
bitte die `Installationsdokumentation von Docker`_ an.

.. _Installationsdokumentation von Docker: https://docs.docker.com/get-docker/

Um die neueste Version von Docker zu installieren, sollten zunächst alle vorherigen Docker-Installationen vom Ihrem
System entfernt werden.

.. code-block:: bash

    $ sudo apt-get remove docker docker-engine docker.io containerd runc

Linux Mint
----------

Wie Docker auf der Homepage erwähnt, untstützt und tested die Docker-Community Installationen lediglich auf Mainstream
Plattformen wie Ubunut, Debian, Windows usw. Linux Mint ist ein Abkömmling von Ubuntu mit einer eignen Oberfläche und
eigenen Settings und Ressourcen. Aus diesem Grund funktioniert die Installationsanleitung von Docker nicht für Linux Mint,
wesshalb ich hier eine kurze Installationsanleitung verfasst habe.

1. Das System auf den neusten Stand bringen

    .. code-block:: bash

        $ sudo apt-get update

2. Site-Packages für den Zugriff über Https

    .. code-block:: bash

        $ sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common

3. Hinzufügen des Docker GPG-Keys

    .. code-block:: bash

        $ sudo apt-get install apt-transport-https ca-certificates

4. Den Key verifizieren

    .. code-block:: bash

        $ sudo apt-key fingerprint 0EBFCD88

5. Repository hinzufügen

    .. code-block:: bash

        $ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"

6. Den Packetmanager neu laden

    .. code-block:: bash

        $ sudo apt-get update

7. Docker und Docker-Compose installieren

    .. code-block:: bash

        $ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose

Andere Betriebssysteme
----------------------

Für die meisten anderen Betriebssystem kann der `Intstallationsanleitung <https://docs.docker.com/get-docker/>`_ der
Docker Dokumentation gefolgt werden, um Docker und Docker-Compose zu installieren.

Projektstruktur
---------------

.. image:: /_static/img/docker/project_structure.png
    :scale: 100 %
    :align: right

Die Django Application besteht aus dem Namen der Application sowie einer App mit selbigem Namen. Hier im Beispiel
`django_app`. In der App befinden sich die verschiedene Dateien für Einstellungen der App, auf die ich hier nicht weiter
eingehen werde -> `Informationen zu Django <https://www.djangoproject.com/start/>`_. Des Weiteren ein Docker Ordner
`docker` für die Dockerfiles sowie Aufbauskripten und Konfigurationsdateien, welche die Initialisierung des Servers
übernimmt. Um Docker-Compose einzurichten, wird noch eine `docker-compose.yml`_ Datei verwendet, hier wurden zwei
unterschiedliche `.yml` Dateien angelegt, um den Development und dem Produktion Service zu starten.

docker-compose.yml
^^^^^^^^^^^^^^^^^^

Die `docker-compose.yml` Datei dient des Aufbaus für Docker-Compose. Hier werden einige Konfigurationsdaten eingestellt.
Es wird eine Datenbank benötigt, auf welche die Applikation zugreifen kann, um beispielsweiße Userdaten oder ähnliches
abzuspeichern. Zusätzlich wird die Dango-Applikation in einem Container gestartet. Dazu benötigen wir eine eigenz
kozipierte DockerFile, um lokal Daten zu verarbeiten. Des Weiteren wird ein GUnicorn-Wsgi-Webserver benötigt, um die
Tasks von Django zu verarbeitent. Dieser startet dann die Webapplikation. Um Statische Dateien konventionell ablegen
zu können, benötigen wir noch einen Web-Server, hier Nginx.

.. code-block:: yaml

    version: '3.1'
    volumes:
      pgdata:
      static_files:                                         # Volume für static files
      media_content:                                        # Volume für media files
    services:
      postgre_db:                                           # DNS für Datenbank-Service
        image: library/postgres:latest                      # Image für Postgre-DB
        environment:
          POSTGRES_DB: postgreDB                            # Datenbank Name
          POSTGRES_USER: user                               # Datenbank User Name
          POSTGRES_PASSWORD: password                       # Datenbank User Passwort
        volumes:
          - pgdata:/var/utils/posgresql/data                # Default Volume für Postgres Datenbank
        ports:
          - 5432:5432                                       # Port für Zugriff auf die Datenbank
      django_app:                                           # DNS für Web-Applikation
          build:
            context: .                                      # Root Verzeichnis des Projekts
            dockerfile: docker/webapp/Dockerfile            # Dockerfile, wird benötigt, um Container zu bauen
          restart: always                                   # Starte Applikation neu, wenn Fehler auftritt
          volumes:
          - ./webapp:/webapp                                # Das Volumen/Die App, welche eingebunden werden soll
          - static_files:/static_files                      # Volumen für static file
          - media_content:/media_content                    # Volumen für media files
          ports:
          - 8000:8000                                           # Port, auf welchem die Webseite ereicht werden kann
          command: gunicorn -w 4 webapp.wsgi -b 0.0.0.0:8000    # GUnicorn Middleware-Webserver für Produktion
      nginx:                                                    # DNS für Nginx Server
          build:
            context: .                                      # Root Verzeichnis für Nginx Server
            dockerfile: docker/nginx/Dockerfile             # Dockerfile, wird benötigt um Server zu konfigurieren
          volumes:
            - static_files:/static_files                    # shared volume mit django-web-applikation für static files
            - media_content:/media_content                  # shared volume mit django-web-applikation für media files
          ports:
            - 8080:80                                       # Leitet port 8080 an Port 80 weiter

nginx Verzeichnis
^^^^^^^^^^^^^^^^^

Das `Nginx Verzeichnis` beinhaltet alle wichtigen Dateien, um den Webserver zu starten.
Sowie das Image, welches für Docker verwendet wird.

DockerFile
""""""""""

Um einen eigenn Docker-Container zu erzeugen, wird eine `DockerFile` benötigt. Es sind verschiedene Kommandos möglich
und die Datei folgt einer strikten Syntax. Mehr über die DockerFile kann hier in der `DockerFile-Dokumentation`_ in
Erfahrung gebracht werden.

.. _DockerFile-Dokumentation: https://docs.docker.com/engine/reference/builder/

.. code-block:: docker

    FROM nginx:latest                                           # Docker Image für Nginx-Web-Server

    RUN rm /etc/nginx/conf.d/default.conf                       # Löschen der Standart Konfigurationsdatei

    COPY ./docker/nginx/webapp.conf /etc/nginx/conf.d/          # Kopieren unserer Konfigurationsdatei

Nginx-Konfiguration
"""""""""""""""""""
Um den Server mit den nötigen Einstellungen auszustatten, wie beispielsweiße dem nötigen Static und Media Kontent
abzuspeichern, muss der Server konfiguriert werden. Dies lässt sich mit einer `.conf` Datei bewältigen.
Mehr über die Konfiguration von Nginx kann in der `Nginx-Dokumentation`_ nachgelesen werden.

.. _Nginx-Dokumentation: http://nginx.org/en/docs/beginners_guide.html

.. code-block:: nginx

    server {
    listen 80;                                  # Port auf dem http requests eingehen
    server_name localhost;                      # Name des Servers
    access_log  /var/log/nginx/example.log;     # Verzeichnis für logs
    server_tokens off;                          # Verhindert, dass Serverinformationen nach außen sichtbar sind.

    location /media/ {                          # Verzeichnis für media content
        autoindex off;                          # Abschalten der automatisch generierten Index Seite (Dort werden die Dateien im Verzeichnis angezeigt: html, css, ...)
        alias /media_content/;                  # Weiterleitung an den tatsächlichen Speicherort
    }

    location /static/ {                         # Wie bei media Dateien
        autoindex off;
        alias /static_files/;
    }

    location / {                                # Root Verzeichnis
        try_files $uri $uri/ @python_django;    # Wenn requested URI eine Datei oder ein Ordner ist, wird dieser versandt. Andernfalls weiterleitung an @python_django
    }

    location @python_django {
        proxy_pass http://django_app:8000;                              # Weiterleitung an GUnicorn Server auf Port 8000
        proxy_pass_request_headers on;                                  # Der Host wird geforwarded (Beispiel -> Django_app.com)
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;    # Der Request wird an Django weitergeleitet (Django hat keine Ahnung von Proxy, deshalb werden IP's weitergeleitet werden)
        proxy_set_header Host $http_host;                               # Proxy kennt den Host-Header nicht, deshalb muss auch dieser weitergeleitet werden
        proxy_set_header X-Forwarded-Proto $scheme;                     # Beispiel wenn nginx hat ssl proxy, dann muss das an django weitergeleitet werden
        proxy_redirect off;                                             # Sollte von Django übernommen werden
    }
    }

django_app Verzeichnis
^^^^^^^^^^^^^^^^^^^^^^

In diesem Verzeichnis werden alle DockerFile für das Deployment sowie für die Entwicklung hinterlegt. Besonders für die
Entwicklung wird eine spezielle Konfiguration benötigt.

.. rubric:: DockerFile

.. code-block:: docker

    FROM python:3.8.3-buster
    MAINTAINER user@localhost

    COPY ./django_app /django_app

    WORKDIR /django_app

    RUN pip install -r requirements/deploy.txt                  # hier requirements/deploy.txt oder requirements/dev.txt
                                                                # Um die benötigten Python-Packages zu installieren.
                                                                # deploy.txt benötigt beispielsweiße gunicorn, dev jedoch nicht.
    COPY ./docker/webapp/entrypoint.sh /entrypoint.sh

    RUN chmod +x /entrypoint.sh

    ENTRYPOINT ["/entrypoint.sh"]

Um beim Start des Dockers eine Ausgabe auf der Konsole zu sehen, macht es Sinn ein solches Entryskript zu verwenden.

**entrypoint.sh**

.. code-block:: bash

    #!/bin/bash

    echo "Running command '$*'"
    exec /bin/bash -c "$*"

Django
------

Auch in Django müssen ein paar Änderungen vorgenommen werden. Zunächst muss die Datenbank richtig initialisiert werden.
In diesem Beispiel verwenden wir eine `Postgresql Datenbank`_. Eine relationale Datenbank, die von den Django Entwicklern
empfohlen wird. Um da zu bewerkstelligen, muss die Datenbank in der `settings.py` eingerichtet werden.

.. _Postgresql Datenbank: https://www.postgresql.org/

.. code-block:: python

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'database_name',
        'USER': 'user_name',
        'PASSWORD': 'user_password',
        'HOST': 'postgre_db',           # Der Hostname, welcher in der docker-compose.yml als Service für die Datenbank eingetragen wurde
        'PORT': '5432',                 # Der Port, welcher für die Datenbank gedacht wurde --> docker-compose.yml
        }
    }

Des weiteren müssen die `Static und Media Files` noch umgeleitet werden. Dazu benötigen wir die Volumes, welche in der
docker-compose.yml festgelegt wurden. In diesem Projekt, sähe das wie folgt in der `settings.py` Datei aus.

.. code-block:: python

    STATIC_ROOT = '/static_files/'
    MEDIA_ROOT = '/media_content/'

Zu guterletzt sollte der Debugmodus von Django noch deaktiviert werden. Dies kann ebenfall in der `settings.py` vorgenommen
werden.

.. code-block:: python

    DEBUG = False

Docker-Compose
--------------

Um die die Docker-Container jetzt zusammenzusetzen benötigen wir `docker compose`. Um die Umgebung für die Produktion
zu erstellen, muss dieses zunächst `gebuilded` werden.

.. code-block:: bash

    $ docker-compose build

Um den Service nun zustarten, genügt es in der Konsole folgenden Befehl einzugeben.

.. code-block:: bash

    $ docker-compose up

Der Nginx-Webserver läuft jetzt mit 4 Gunicorn Workern stabil und kann auf einem beliebiegen Server installiert werden.