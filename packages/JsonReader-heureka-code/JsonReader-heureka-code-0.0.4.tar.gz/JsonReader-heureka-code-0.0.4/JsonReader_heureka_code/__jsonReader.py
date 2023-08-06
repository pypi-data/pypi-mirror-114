import json
from os.path import isfile


__doc__ = """class JsonReader:
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
    
    // Sonst nur private Methoden
"""


class JsonReader:
    def __init__(self, file: str):
        self.__file = file
        self.__content = {}
        self.__erstellen_falls_fehlen()
        self.read()
        pass

    def read(self):
        try:
            with open(self.__file) as f:
                self.__content = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            self.write()
            self.read()
        pass

    def write(self):
        with open(self.__file, "w") as f:
            f.write(json.dumps(self.__content, indent=4))
        pass

    def get_from_path(self, path: str):
        pfad = path.split("/")
        aktuelles_dic = self.__content
        while len(pfad) > 0:
            if len(pfad) == 0:
                break
            if type(aktuelles_dic) == list:
                try:
                    aktuelles_dic = aktuelles_dic[int(pfad[0])]
                except IndexError:
                    break
                    pass
                except ValueError:
                    break
                    pass
            elif type(aktuelles_dic) == dict:
                try:
                    aktuelles_dic = aktuelles_dic[pfad[0]]
                except KeyError:
                    break
                    pass
            del pfad[0]
        return aktuelles_dic

    def set_from_path(self, path: str, value):
        aktuelles_dic = self.__content
        pfad = path.split("/")
        while len(pfad) > 0:
            try:
                if pfad[0] in aktuelles_dic.keys():
                    if aktuelles_dic[pfad[0]] in [list, dict]:
                        aktuelles_dic = aktuelles_dic[pfad[0]]
                else:
                    if len(pfad) == 1:
                        aktuelles_dic[pfad[0]] = value
                    else:
                        aktuelles_dic[pfad[0]] = {}
            except AttributeError:
                if pfad[0] == "END":
                    pfad[0] = len(aktuelles_dic)
                if len(aktuelles_dic) < int(pfad[0]):
                    if len(pfad) == 1:
                        aktuelles_dic[int(pfad[0])] = value
                    else:
                        aktuelles_dic[int(pfad[0])] = {}
                else:
                    aktuelles_dic.append(value)

            try:
                aktuelles_dic = aktuelles_dic[pfad[0]]
            except TypeError:
                aktuelles_dic = aktuelles_dic[int(pfad[0])]
            del pfad[0]
        pass

    def path_exists(self, path: str):
        return self.get_from_path(path) != self.__content

    def delete_path(self, path: str):
        try:
            pfad = path.split("/")
            aktuelles_dic = self.__content
            try:
                while len(pfad) > 1:
                    assert pfad[0] in aktuelles_dic.keys()
                    aktuelles_dic = aktuelles_dic[pfad[0]]
                    del pfad[0]
            except KeyError:
                pass
            except AssertionError:
                print(aktuelles_dic)
            try:
                del aktuelles_dic[pfad[0]]
            except TypeError:
                del aktuelles_dic[pfad[0]]
        except KeyError:
            pass
        pass

    def __erstellen_falls_fehlen(self):
        if isfile(self.__file):
            pass
        else:
            self.write()
            pass
        pass
    pass

