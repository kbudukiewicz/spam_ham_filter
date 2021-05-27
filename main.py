import glob
from xml.dom import minidom
import pystempel


class mail(object):
    def __init__(self):
        # self.filename = " "
        self.nadawca = " "
        self.odbiorca = " "
        self.data = " "
        self.temat = " "
        self.tresc = " "

    def wyswietlanie_maila(self):
        # print("Nazwa pliku: ", self.filename)
        print("Nadawca: ", self.nadawca)
        print("Odbiorca: ", self.odbiorca)
        print("Data: ", self.data)
        print("Temat: ", self.temat)
        print("Tresc: ", self.tresc)

    def wczytanie_z_pliku(self, filename):
        plik = open(filename, mode='r', encoding='ANSI')
        plik_read = plik.read()
        podzielony = plik_read.split("\n")
        self.filename = filename
        self.nadawca = podzielony[0].split(':')[1].strip()
        self.odbiorca = podzielony[1].split(':')[1].strip()
        self.data = podzielony[2].split(':')[1].strip() + ':' + podzielony[2].split(':')[2].strip()
        self.temat = podzielony[3].split(':')[1].strip()
        text = podzielony[4].split(":")[1].strip()
        self.tresc = text
        text = text.lower()
        text = text.replace(",", "")
        text = text.replace(".", " ")
        text = text.replace("?", " ")
        text = text.replace("\n", "")
        text_list = text.split(" ")
        return text_list


obj_spam = []
obj_ham = []
ham_dict = {}
spam_dict = {}
liczba_plikow_spam = 0
liczba_plikow_ham = 0
k = 2
slowa_wszystkie = []

for filename in glob.glob('C:/Users/User/PycharmProjects/lab5_wno2/spam/spam *.txt'):
    liczba_plikow_spam = liczba_plikow_spam + 1
    # print("-------------------------------------------------------------------")

    ob_spam = mail()
    tekst_s = ob_spam.wczytanie_z_pliku(filename)
    # ob_spam.wyswietlanie_maila()
    obj_spam.append(ob_spam)

    for string in tekst_s:
        slowa_wszystkie.append(string)
        if string[:-1] in spam_dict:
            spam_dict[string[:-1]] += 1
        else:
            spam_dict[string[:-1]] = 1

for filename in glob.glob('C:/Users/User/PycharmProjects/lab5_wno2/spam/ham *.txt'):
    liczba_plikow_ham = liczba_plikow_ham + 1
    # print("-------------------------------------------------------------------")

    ob_ham = mail()
    tekst_h = ob_ham.wczytanie_z_pliku(filename)
    # ob_ham.wyswietlanie_maila()
    obj_ham.append(ob_ham)

    for string in tekst_h:
        slowa_wszystkie.append(string)
        if string[:-1] in ham_dict:
            ham_dict[string[:-1]] += 1
        else:
            ham_dict[string[:-1]] = 1


print("Slowa w slowniku spam i ilosc wystepowania: ", spam_dict)
print("Slowa w slowniku ham i ilosc wystepowania: ", ham_dict)

suma_slow_ham = sum(ham_dict.values())
suma_slow_spam = sum(spam_dict.values())

# P(SPAM) i P(HAM) zwykle
prawd_ham_zwykle = suma_slow_ham / (suma_slow_ham + suma_slow_spam)
prawd_spam_zwykle = suma_slow_spam /(suma_slow_ham + suma_slow_spam)

# P(SPAM) i P(HAM) z wygladzeniem Laplace
prawd_ham = (liczba_plikow_ham + k) / (liczba_plikow_ham + liczba_plikow_spam + k * k)
prawd_spam = (liczba_plikow_spam + k) / (liczba_plikow_ham + liczba_plikow_spam + k * k)

praw_slowo_ham = {}
praw_slowo_spam = {}

for word in list(ham_dict.keys()):
    praw_slowo_ham[word] = ham_dict[word] / (suma_slow_ham + k * k)

for word in list(spam_dict.keys()):
    praw_slowo_spam[word] = spam_dict[word] / (suma_slow_spam + k * k)

print("Slowa w slowniku spam i ich prawdopodobienstwo: ", praw_slowo_spam)
print("Slowa w slowniku ham i ich prawdopodobienstwo: ", praw_slowo_ham)

print("Wyswietlanie e-mail:")
print("-------------------------------------------------------------------")
ob_ex = mail()
example_list = ob_ex.wczytanie_z_pliku('C:/Users/User/PycharmProjects/lab5_wno2/spam/example.txt')
ob_ex.wyswietlanie_maila()
print("-------------------------------------------------------------------")

example_dict_spam = {}
example_dict_ham = {}

for word in example_list:
    if word[:-1] in praw_slowo_spam:
        if not word[:-1] in example_dict_spam:
            example_dict_spam[word[:-1]] = praw_slowo_spam[word[:-1]]
        else:
            example_dict_spam[word[:-1]] = example_dict_spam[word[:-1]] + praw_slowo_spam[word[:-1]]

    if word[:-1] in praw_slowo_ham:
        if not word[:-1] in example_dict_ham:
            example_dict_ham[word[:-1]] = praw_slowo_ham[word[:-1]]
        else:
            example_dict_ham[word[:-1]] = example_dict_ham[word[:-1]] + praw_slowo_ham[word[:-1]]


koncowe_ham = sum(example_dict_ham.values()) * prawd_ham / (
            sum(example_dict_ham.values()) + sum(example_dict_spam.values()))
koncowe_spam = sum(example_dict_spam.values()) * prawd_spam / (
            sum(example_dict_ham.values()) + sum(example_dict_spam.values()))

print("Praowdopodobiensto, ze e-mail jest ham wynosi: ", koncowe_ham)
print("Praowdopodobiensto, ze e-mail jest spam wynosi: ", koncowe_spam)

if (koncowe_ham > koncowe_spam):
    print("Plik example.txt nalezy do hamu")
else:
    print("Plik example.txt nalezy do spamu")

mydoc = minidom.parse('C:/Users/User/PycharmProjects/lab5_wno2/spam/dict.xml')
prawd_new = mydoc.getElementsByTagName('word')
for elem in prawd_new:
    print(elem.attributes['probabilty'].value)

nowe_slowa = []
for slowo in slowa_wszystkie:
    nowe_slowa.append(slowo.stemmer.stem(slowo))

print(nowe_slowa)
