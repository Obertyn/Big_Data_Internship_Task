#Algorytm działania programu w dużym uproszczeniu:
#1. Program decyduje, która tabela, będzie tabelą główną, a która poboczną (w tabeli głównej w kolumnie łączącej mogą występować powtórzenia).
#2. Tabela główna jest tak modyfikowana, że zostaje przekształcona w tabele, która powinna być wynikiem operacji join.
#3. Najpierw powiększany lub pomniejszany jest rozmiar tabeli głównej (w zależności od tego, jaką wybraliśmy komendę oraz od tego, która w kolejności tabela (czy pierwsza czy druga) została tabelą główną).
#4. Korzystając z wartości z tabeli pobocznej tworzona jest tablica numpy - jej rozmiar i wartości są zależne od tego, jaka komenda została wybrana (np. jeśli użytkownik wybrał komendę "inner join" to tablica numpy może zostać zmniejszona o niepotrzebne wiersze).
#5. Na końcu wartości z tablicy numpy zostają w odpowiedni sposób przepisane do pustych kolumn z tablicy głównej.

import numpy as np
from numpy.random import randint
import sys
from os.path import exists
import pandas as pd

koniec = 0
while koniec < 1: #jeśli komenda będzie poprawna, pętla zostanie zakończona
    a1=0
    a2=0
    a3=0 #jeśli wszystkie 5 zmiennych będzie równe 1, to oznacza, że nie ma żadnych błędów i pętla zostanie zakończona
    a4=0 #każda z 5 zmiennych odpowiada innym błędom
    a5=0
    txt = input("Podaj komende: ")

    x = txt.split()
    
    if len(x)>4: #jeśli słów w komendzie będzie za mało, należy wpisać nową komondę

        if x[0] != "join":
            print("nieprawidlowa pierwsza instrukcja, prosze wpisac join")
        else:
            a1=1
    
        file_exists1 = exists(x[1])
        file_exists2 = exists(x[2])
    
        if file_exists1 == True and file_exists2 == True: #sprawdza czy pliki podane przez użytkownika istnieją
            a2=1

            fo = open(x[1], "r")

            line1 = fo.readlines(1)
    
            fo = open(x[2], "r")

            line2 = fo.readlines(1)
    
            if x[3] in str(line1): #sprawdza czy nazwa kolumny znajduje się w pierwszym wierszu plika
                a4=1
            else:
                print("nie znaleziono nazwy kolumny w pierwszym pliku")
                  
            if x[3] in str(line2):
                a3=1
            else:
                print("nie znaleziono nazwy kolumny w drugim pliku")
    
            if x[4] == "inner" or x[4] == "left" or x[4] == "right":
                a5=1
            else:
                print("nieprawidlowa ostatnia instrukcja, prosze wpisac 'inner','left' lub 'right'")            
            
        else:
            print("nieprawidlowe sciezki do plikow")
    
    else:
        print("za krotka komenda")
     
    if a1==1 and a2==1 and a3==1 and a4==1 and a5==1:
        koniec = 1
        
        
df1 = pd.read_csv(x[1], sep=',')
df2 = pd.read_csv(x[2], sep=',')
lista1 = pd.DataFrame(df1) #pobieram liste wyników z kolumny łączącej, żeby sprawdzić czy są powtórzenia
lista1=lista1[x[3]]
lista2 = pd.DataFrame(df2)
lista2=lista2[x[3]]

def czysapowtorzenia(lista3): #funkcja sprawdzająca czy są powtórzenia w liście
    if len(lista3) == len(set(lista3)):
        return False
    else:
        return True
        
#d3 to tabela "główna" (będzie wyświetlona po lewej stronie), która posiada powtórzenia w kolumnie łączącej
#d4 to tabela "poboczna" (będzie wyświetlona po prawej stronie), która nie posiada powtórzeń w kolumnie łączącej
if czysapowtorzenia(lista1)==False and czysapowtorzenia(lista2)==True:
    df3=df2
    df4=df1
elif czysapowtorzenia(lista1)==True and czysapowtorzenia(lista2)==False:
    df3=df1
    df4=df2
elif czysapowtorzenia(lista1)==False and czysapowtorzenia(lista2)==False:
    df3=df1 #jeśli obie kolumny nie posiadają powtórzeń, to wszystko jedno która tabela zostanie "główną", a która "poboczną"
    df4=df2
elif czysapowtorzenia(lista1)==True and czysapowtorzenia(lista2)==True:
    #nie można połączyć ze sobą dwóch tabel, jeśli obydwie kolumny łączące tabele posiadają powtórzenia
    print("Nie da się połączyć tabel, ponieważ obydwie kolumny łączące posiadają powtórzenia")
    exit=input("naciśnij enter żeby zakończyć działanie programu ")
    sys.exit()

ilosc_df4k=len(df4.columns)-1 #ilość kolumn w tabeli pobocznej "-1" bo nie biorę po uwagę kolumny łączącej

ilosc_df4w=len(df4.index) # ilość wierszy w tabeli pobocznej

bbb=df3.keys() #lista zawierająca nazwy kolumn z tabeli głównej
bbb=bbb.tolist()

index = bbb.index(x[3]) #zapisuje które miejsce na liście ma nazwa kolumny łączącej

klucz = df4[x[3]].values.tolist() #wartości będące w kolumnie łączącej

p=0
qwe=[]
if x[4] == 'inner': #jeśli użytkownik korzysta z komendy "inner join"
#usuwa wiersze znajdujące się w tabeli głównej, których wartości znajdujące się w kolumnie łączącej,
#nie znajdują się w kolumnie łączącej tabeli pobocznej
    for row in df3.itertuples(index=False): #zapisuje wiersze do usunięcia

        if row[index] not in klucz:
            qwe.append(p)
            #df3=df3.drop(df3.index[p])
        p=p+1
        
if x[4] == 'inner': #usuwa wiersze
    df3=df3.drop(df3.index[qwe])
    
zm=0

if x[4] == 'left':
#jeśli użytkownik korzysta z komendy "left join" i tabela główna jest tabelą "right"
#to usuniemy w tabeli "right" wiersze, w których znajdują się wartości, których nie ma w kolumnie łączącej, w tabeli "left" 
    if czysapowtorzenia(lista1)==False and czysapowtorzenia(lista2)==True:
        zm=1
    elif czysapowtorzenia(lista1)==True and czysapowtorzenia(lista2)==False:
        zm=0
    elif czysapowtorzenia(lista1)==False and czysapowtorzenia(lista2)==False:
        zm=1
        
if x[4] == 'right':
#jeśli użytkownik korzysta z komendy "right join" i tabela główna jest tabelą "right"
#to usuniemy w tabeli "left" wiersze, w których znajdują się wartości, których nie ma w kolumnie łączącej, w tabeli "right"
    if czysapowtorzenia(lista1)==False and czysapowtorzenia(lista2)==True:
        zm=0
    elif czysapowtorzenia(lista1)==True and czysapowtorzenia(lista2)==False:
        zm=1
    elif czysapowtorzenia(lista1)==False and czysapowtorzenia(lista2)==False:
        zm=0
        
p=0
qwe=[]
if zm==1: #zapisuje wiersze do usunięcia
    for row in df3.itertuples(index=False):
        if row[index] not in klucz:
            qwe.append(p)
            #df3=df3.drop(df3.index[p])
        p=p+1
        
if zm==1: #usuwa wiersze
    df3=df3.drop(df3.index[qwe])
   
#resetuje numery na lewej kolumnie z numerami wierszy, bo mogą być nie po kolei, co spowoduje błąd   
df3.reset_index(drop=True, inplace=True)

ilosc_df3w=len(df3.index) #ilość wierszy w tabeli głównej

#w tym miejscu zwiększana jest ilość wierszy w tabeli głównej, w sytuacji gdy w tabeli pobocznej w kolumnie łączącej,
#znajdują się wartości których nie ma w tabeli głównej
#ilość dodanych wierszy jest tożsama z ilością wartości w tabeli pobocznej w kolumnie łączącej, których nie ma w tabeli głównej
#dodatkowo w nowych wierszach dodawane są wartości znajdujące się w tabeli pobocznej w kolumnie łączącej, 
#których nie ma w tabeli głównej
if zm==1:
    d=np.zeros(ilosc_df3w)
    list1 = d.tolist()
    d = list(map(int, d))
    i=0
    zespol=d
    for row in df3.itertuples(index=False): #lista zawierająca wartości w kolumnie łączącej w tabeli głównej
        zespol[i]=row[index]
        i=i+1
    klucz = df4[x[3]].values.tolist() #lista zawierająca wartości w kolumnie łączącej w tabeli pobocznej
    tab0=[]
    for i in range(len(klucz)):
        if klucz[i] not in zespol:
            tab0.append(klucz[i]) #lista zawierająca wartości z tabeli pobocznej, których nie ma w tabeli głównej
    len_tab0=len(tab0) #ilość wartości w liście, która określi ile zostanie dodanych wierszy to tabeli głównej
    
    for i in range(ilosc_df3w,ilosc_df3w+len_tab0):
        df3.loc[i] = list(randint(-456768, -456767, size=len(bbb)))
    hh=0 #wszystkie komórki w nowych wierszach, przyjmują wartość -456768 (to mogłaby być jakakolwiek wartość)
    
    
    for row in df3.itertuples(index=False): #w nowych wierszach w kolumnie łączącej zostają dodane wartości
        if row[index]==-456768: #będące w tabeli pobocznej, których nie ma w tabeli głównej
            df3.at[ilosc_df3w+hh,x[3]]=tab0[hh]
            hh=hh+1
    df3=df3.replace(to_replace =-456768, value ='') #zmienia pola z "-456768" na puste pola
    
#muszę znowu pobrać wartość oznaczającą liczbę wierszy w tabeli głównej, bo ta liczba mogła się zmienić
ilosc_df3w=len(df3.index) 

kk=df4.columns #nazwy kolumn w tabeli pobocznej

xx=[]
for i in range(ilosc_df4k+1): #lista, która zawiera tyle wartości ile jest kolumn w tabeli pobocznej
    xx.append(i) #"+1" ponieważ na początku od tej wartości odjęliśmy 1
    
for i in range(ilosc_df4k+1): #zmiana struktury danych z indexu na liste, bo numpy nie chce współpracować z indexem
    xx[i]=kk[i]
    
xx.remove(x[3]) #lista zawierająca nazwy kolumn z tabeli pobocznej oprócz kolumny łączącej

ss=[]
for i in range(ilosc_df3w): #tworzy liste z zerami, w której ilość wartości w tej liście, jest tożsama z ilością wierszy w tabeli głównej
    ss.append(0)
    
df3.reset_index(drop=True, inplace=True)
#znowu resetuje numery na lewej kolumnie z numerami wierszy, bo mogą być nie po kolei, co spowoduje błąd

i=0 #powiększa ilość kolumn w tabeli głównej (wszystkie nowe komórki przyjmują wartość zero)
for row in df3.itertuples(index=False): #ilość nowych kolumn jest równa ilości kolumn w tabeli pobocznej minus 1,
    df3.at[i, xx] = ss[i] #bo nie ma sensu dwa razy wyświetlać kolumny łączącej
    i=i+1
    
arr = np.zeros([ilosc_df4k,ilosc_df3w],dtype='str') #pusta tablica numpy 
#której rozmiar jest równy: ilość kolum w tabeli pobocznej x ilość wierszy w tabeli głównej
#to właśnie w tej tablicy zostaną zapisane wartości pobrane z tablicy pobocznej, które zostaną dołączone do tablicy głównej

arr = arr.tolist() #zmienia tablice numpy na liste

d=np.zeros(ilosc_df3w)
list1 = d.tolist()
d = list(map(int, d))

bbb=df3.keys() #wczytuje nazwy kolumn z tablicy głównej

bbb=bbb.tolist()

index = bbb.index(x[3]) #zapisuje wartość, pokazującą która z kolei jest kolumna łącząca w tabeli głównej

i=0
zespol=d #zapisuje liste w której znajdują się wszystkie wartości w kolumnie łączącej
for row in df3.itertuples(index=False):
    zespol[i]=row[index]
    i=i+1
    
#zapisuje liste w której znajdują się wszystkie wartości w kolumnie łączącej w tabeli pobocznej
klucz = df4[x[3]].values.tolist()

#zapisuje tablice numpy w której zostaną zapisane wszystkie wartości z tabeli pobocznej, nie licząc kolumny łączącej
dp = np.zeros([ilosc_df4k,ilosc_df4w],dtype='object')

for i in range(ilosc_df4k):
    dp[i] = df4[xx[i]].values.tolist()
    
dp = dp.tolist()

#wynikiem tej pętli będzie tablica z wartościami z tabeli pobocznej, które będą mogły zostać wstawione do tabeli głównej
for i in range(ilosc_df3w):
    for j in range(ilosc_df4w):
        if zespol[i]==klucz[j]: #jeśli wartość z kolumny łączącej jest taka sama
            for k in range(ilosc_df4k): #to wartości z tablicy pobocznej zostaną dołączone do danego wiersza z tablicy głównej
                arr[k][i]=dp[k][j]
                
c=0
for row in df3.itertuples(index=False):
    for i in range(ilosc_df4k): #ilość kolumn z tabeli pobocznej
        df3.at[c, xx[i:i+1]] = arr[i][c] #'[c, xx[i:i+1]]' określa numer kolumny i wiersza
#xx to lista zawierająca nazwy pustych kolumn z tabeli pobocznej, w których edytowane są komórki
    c=c+1

print()
print(df3)
print()

exit=input("naciśnij enter żeby zakończyć działanie programu ")