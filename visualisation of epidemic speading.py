# -*- coding: utf-8 -*-
"""
@author: Lukasz
"""
# %%

'''
    WIZUALIZACJA
'''

from simulation import graph
import pycxsimulator

# funkcja inicjalizujaca na potrzeby symulacji z wizualizacjÄ…
def init():
    global g
    global N, k
    global contact_prob_floor
    global contact_prob_ceiling
    global infect_proc
    global rewire_prob
    global immunity_prob_floor
    global immunity_prob_ceiling
    
    g = graph(N, k, (contact_prob_floor, contact_prob_ceiling), (immunity_prob_floor, immunity_prob_ceiling), rewire_prob)
    g.infect_random(infect_proc)
    
def draw():
    g.draw()
def step():
    g.simulation_step()
    
# funkcje na portrzeby mozliwosci modyfikacji zmiennych w interfejsie graficznym symulacji
def liczba_agentow(new_value = 30):
    global N; N = int(new_value); return N
# wykorzystywany przy tworzeniu sieci malego swiata jako parametr
def stopien_polaczen_lokalnych(new_value = 4):
    global k; k = int(new_value); return k
def prawd_przepiecia_wierzcholkow(new_value = 0.3):
    global rewire_prob; rewire_prob = new_value; return rewire_prob
# procent zarazonych agentow na poczatku symulacji
def procent_pocz_zarazonych(new_value = 0.2):
    global infect_proc; infect_proc = new_value; return infect_proc
# prawdopodobienstwo kontaktu pomiedzy agentami w jednym kroku iteracji losowane jest
# z rozkladu jednostajnego w przedziale (floor, ceiling), ponizsze 2 funkcje
# sluza do mozliwosci modyfikowania tych wartosci w symulacji
def prawd_kontaktu_floor(new_value = 0.2):
    global contact_prob_floor; contact_prob_floor = new_value; return contact_prob_floor 
def prawd_kontaktu_ceiling(new_value = 0.4):
    global contact_prob_ceiling; contact_prob_ceiling = new_value; return contact_prob_ceiling 
# dolna i gorna granicy z ktore losowana jest poczatkowa odpornosc agentow
def odpornosc_floor(new_value = 0):
    global immunity_prob_floor; immunity_prob_floor = new_value; return immunity_prob_floor
def odpornosc_ceiling(new_value = 1):
    global immunity_prob_ceiling; immunity_prob_ceiling = new_value; return immunity_prob_ceiling    

    

pycxsimulator.GUI(parameterSetters = [liczba_agentow, stopien_polaczen_lokalnych, prawd_przepiecia_wierzcholkow,
                                      procent_pocz_zarazonych, prawd_kontaktu_floor, prawd_kontaktu_ceiling,
                                      odpornosc_floor, odpornosc_ceiling],
                  title='Informacja w sieci',interval=2 ).start(func=[init,draw,step])
