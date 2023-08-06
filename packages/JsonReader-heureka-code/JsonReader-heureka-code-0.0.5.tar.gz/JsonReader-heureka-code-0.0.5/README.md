# Dieses Packet verarbeitet "Pfade" um Json-Informationen abzufragen

##class JsonReader:

    // init
    // Nimmt das Argument:
    // * file, ein String, der den Dateipfad zur Json-Datei darstellt.
    def __init__(self, file: str)
    
    // write
    // Nimmt keine Argumente
    // Und schreibt den aktuellen Stand des Arbeits-Dictionarys in die Datei
    def write(self)
    
    // read
    // Nimmt keine Argumente
    // Und liest die Datei ein
    def read(self)
    
    // get_from_path
    // Nimmt das Argument:
    //  * path, der Pfad zur Json-Information
    def get_from_path(self, path: str)
    
    // set_from_path
    // Nimmt die Argumente:
    //  * path, der Pfad zu der zu erstellenden Information
    //  * value, der Wert auf den es gesetzt wird
    def set_from_path(self, path: str, value)
    
    // delete_path
    // Nimmt das Argument:
    //  * path, der Pfad, der gelöscht werden soll
    def delete_path(self, path: str)

    // path_exists
    // Nimmt das Argument
    // * path, der Pfad der geprueft werden soll
    def path_exists(self, path: str)
    
    // Sonst nur private Methoden
