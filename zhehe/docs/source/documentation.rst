Read The Docs
*************

.. image:: /_static/img/documentation/read-the-docs-logo.png
    :scale: 40 %
    :align: left
    :target: https://pbs.twimg.com/profile_images/525686734760067072/OhsWgbsr_400x400.png

`ReadTheDocs.org`_ ist nicht nur verantwortlich für das gleichnamige Sphinx-Theme. Hier kann auch jeder Entwickler mit
einem Git-Repository seine erstelle Dokumentation hosten. Readthedocs erhebt hierbei keine Kosten. Ein neuer push auf
das Repository wird hier automatisch verarbeitet und in die Webseite mit aufgenommen. Das Theme kann hier ebenfalls
frei eingestellt werden :ref:`(vgl. Read the Docs, Inc & contributors o. J.b)<Literaturverzeichnis>`. Leider ist es jedoch nicht für GitLab
Projekte auf den Servern der Hochschule Augsburg geeignet, da keine geeignete Log-in-Funktion für Private Server
angeboten wird. Aus diesen Gründen habe ich mich für dieses Projekt für ein GitHub Repository entschieden.

.. _ReadTheDocs.org: https://readthedocs.org/

Einstellungen
-------------

Um ReadTheDocs mit einer eigenen Konfigurationsdatei verwenden zu können ist zu beachten, dass ReadTheDocs unter
Defaulteinstellungen nach einer **contents.rst** Datei sucht. Default von Sphinx ist hier jedoch die **index.rst** Datei.
Aus Designgründen habe ich mich in diesem Projekt für die Sphinx-Umgebung entschieden. Dafür muss in der **config.py**
ein Eintrag für das Master-Dokument hinzugefügt werden.

.. code-block:: python

    master_doc = 'index'

Durch diesen Einschub sucht ReadTheDocs nach einer index.rst Datei und die Dokumentation kann erzeugt werden.

Besonderheiten
**************

Literaturverzeichnis
--------------------

Da zitieren mit Sphinx nicht klassisch implementiert ist, muss man hier eigene Wege gehen. Ich habe mich in diesem
Projekt dazu entschieden **ref** Links zu verwenden. **Reflinks** ermöglichen es Hyperlinks zu erzeugen, welche auf
Stellen in anderen Dokumenten verweißen.

..  admonition:: Beispiel
    :class: toggle

    | Zunächst benötigt man das Schlüsselwort **ref**.
    | Anschließen kommt der Hyperlink Text in (\`).
    | Jetzt wird der Verweiß in einem anderen Dokument in \<Verweiß\> angegeben.
    | Und zuletzt wird die Anweißung wieder mit (\`) geschlossen.

    .. code-block:: bash

        # Referezlink
        :ref:`HyperlinkText<Referenz-in-anderem-Dokument>`
        # Beispiel für Referenz-in anderem Dokument
        .. _Referenz-in-anderem-Dokument

Dadurch ist es möglich ein Literaturverzeichnis in einer eigenen Datei anzulegen. Dieser Zustand macht das Verzeichnis
einfacher zu verwalten und Trennt die verschiedenen Einheiten der Dokumentation.