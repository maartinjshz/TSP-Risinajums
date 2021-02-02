
import time
import pygame
import random
import math
import numpy as np
#screen ir kerams, kur visu ziimee!
screen = pygame.display.set_mode((1024, 768))

#Tiek iedoti 2 tupli ar punktu koordinatem un ar pitagou dod atpakal attalumu
def attalums(A,B):
    rez = 0
    rez = math.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)
    return rez




running = 1


skaits = int(input('Ievadi punktu skaitu: '))


# Izveido matricu feromona daudzumam
# Sāk ar feromona daudzumu 1 katrā no posmiem!
# Savādāk rekinot iespejamibu, rodas dalisana ar nulli

feromons = []

for i in range(skaits):
    a = []
    for ii in range(skaits):
        a.append(1)
    feromons.append(a)

#Liste ar punktiem pec kartas
punkti = []
for i in range(skaits):
    punkti.append(i)

kord = []
 
attalumi = []

#ivert ir liste, kur ir iestie attalumi
ivert = []

#liste kord ievieto tuples, kuri ir dazado punktu koordinates
for i in range(skaits):
    app = ((random.randint(10, 900))/200,(random.randint(10, 700))/200)
    kord.append(app)
    ivert.append((app[0]*200 , app[1]*200))
    
#Tiek izveidota matrica, kurā ir attālumi starp punktiem!
for i in  kord:
    kol = []
    for ii in  kord:
        kol.append(attalums(i,ii))
    attalumi.append(kol)


# Izmanto tālāk rēķinot varbūtību
#  No konrkēta punkta tiek saskaitīts
# Attālums * 1 / Feromons noteiktajā posmā
# Uz visiem blakus esošajiem punktiem
def dalitajs(lokacija, saraksts):
    rez = 0
    for i in saraksts:
        rez +=  ((feromons[lokacija][i])**3 * ((20/(attalumi[lokacija][i])))**3)

    return rez
summ = 0

# Nomaina linijas krasu atkariba no feromona skaita 
def linija(korde, kord2):
    summ = 0
    for j in range(skaits):
        if korde ==j:
            continue
        summ = summ + (feromons[korde][j])
    rez = 255 - ((feromons[korde][kord2])/summ) * 255
    return (rez,rez,rez)


apgriezieni = 0

#_____________________________
# Sākas pats algoritms
while running :
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running =0



    #Ekrāns un tā krāsas
    # Uzliku violētu, lai redzētu baltās līnijas
    screen.fill((221,23,228))


# Tiek sazīmēti punkti un līnijas
# Līnijām krāsu rēķina funkcijā, atarībā no feromona tajā posmā

    for i in  ivert:
        for ii in  ivert:
            pygame.draw.line(screen, linija( ivert.index(i),  ivert.index(ii)), i, ii,3)

# Sazīmē punktus, pirmo iesīmē sarkanu
    for i in  ivert:
        if ivert.index(i) == 0:
            pygame.draw.circle(screen,  (255,0,0),i, 6) 
        else:
            pygame.draw.circle(screen,  (0,0,0),i, 6)       


#Ik pēc 50 cikla izpildes reizēm,
# Tiek izdrukāta feromona tabula
# Un parādīts līnijas

    if apgriezieni == 50:
        pygame.display.flip() 
        apgriezieni = 0
            
        print("   ")
        for i in feromons:
            print(i)
        print("Ir veikti 50 apgriezieni")
        print("   ")
         
    else:
        apgriezieni += 1

    # No šejienes sākas rēķināšana

    cela_garums = 0 
    saraksts = list(punkti)
    lokacija = 0
    Cela_posmi = []
    iespejamiba = []
    

# Tiek Starp visiem punktiem, uz kuriem skudra vēl nav aizgājusi
# Tiek aplūkota varbūtība, kāda ir doties uz katru posmu
# Ar funkciju np.random.choice pēc dotās varbūtības tiek pateikts nākamais posms
#  Svarīgi, ka nevar vienā ciklā apmeklēt vienu un to pašu punktu divreiz
# (Izņemot pirmo, jo tas ir arī pēdējais.)

    while len(saraksts) !=0 :
        iespejamiba = []
        saraksts.remove(lokacija)

        if len(saraksts) == 0:
            Cela_posmi.append(lokacija)
            break
        else:
            saucejs= dalitajs(lokacija, saraksts)
        for i in saraksts:
            iespejamiba.append(((feromons[lokacija][i])**3 * ((20/(attalumi[lokacija][i])))**3)/ saucejs  )
        Cela_posmi.append(lokacija)
        JaunsP = (np.random.choice(saraksts, 1, p = iespejamiba))[0]
        cela_garums += attalumi[lokacija][JaunsP]
        lokacija = JaunsP
    cela_garums += attalumi[lokacija][0]
    


# Notiek visa feromona izgarošana
    for i in range(skaits):
        for ii in range(skaits):
            feromons[i][ii] =feromons[i][ii] * 0.7


# Tiek papildināts feromons posmos, pa kuriem pārvietojās skudras

    for i,ii in zip( Cela_posmi,  Cela_posmi[1:]+[ Cela_posmi[0]]):
        feromons[i][ii] += 1 /  cela_garums
        feromons[ii][i] += 1 /  cela_garums



    elements = 0 
    seciba = []
    Max_seciba = []


# Papildus līnijas, kas apzīmē īsāko ceļu tiek uzzīmētas sarkanā krāsā

    for i in range(skaits):
        fersar  = list(feromons[elements])
        seciba.append(elements)
        for i in seciba:
            fersar[i] = 0
        if sum(fersar) == 0:
            break
        else:
            nakamais = fersar.index(max(fersar))
            Max_seciba.append((elements, nakamais))
            elements = nakamais
    Max_seciba.append((elements, 0))
    for i in Max_seciba:
        pygame.draw.line(screen, (255,0,0), ivert[i[0]], ivert[i[1]],3)
        #pass

    # Lai noņemtu sarkanās līnijas, 
    #  201 rindu izkomentē un atkomentē 202 rindu
            

    pygame.display.flip() 





                
