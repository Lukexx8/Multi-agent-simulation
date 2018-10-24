# -*- coding: utf-8 -*-
"""
Created on Wed May 23 13:08:58 2018

@author: Lukasz
"""
import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

  

# Opakowanie dla wszystkiego co robimy z grafem
class graph():
    # N - liczba agentow
    # k - liczba polaczen lokalnych w sieci malego swiata
    # contact_prob - tuple dolna i gorna granica rozkladu z ktorego
    # losowane jest prawdopodobienstwo kontaktu pomiedzy agentami (wierzcholkami)
    # immunity_prob - tuple dolna i gorna granica rozkladu z ktorego
    # losowana jest odpornosc agentow na zarazenie
    def __init__(self, N, k, contact_prob, immunity_prob, rewire_prob, seed = None):
        # tworzenie grafu
        self.g = nx.watts_strogatz_graph(N, k, rewire_prob, seed=seed)
        
        # tworzymy wagi pomiedzy wierzcholkami, symbolizujace prawdopodobienstwo kontaktu
        # prawdopodobienstwo jest losowane z rozkladu jednostajnego z przedzialu (0,1)
        for u, v in self.g.edges():
            self.g[u][v]['weight'] = np.random.uniform(contact_prob[0], contact_prob[1])
        # ustawianie dla kazdego wierzchilka odpornosci jako zminnej losowej
        # z rozkladu jednostajnego (0,1)
        # oraz stanu poczatkowego 'zdrowy
        nx.set_node_attributes(self.g, 'state', 'healthy')
        nx.set_node_attributes(self.g, 'immunity', {n : np.random.uniform(immunity_prob[0], immunity_prob[1])
                                for n in self.g.nodes_iter()})
            
        # dla celow wyswietlania wierzcholkow po okregu
        self.pos = nx.shell_layout(self.g)
        # na cele odpowiedniego ustawienia kolorow przy rysowaniu wierzcholkow w funkcji draw
        self.color_dict = {'healthy':'yellow', 'infected':'red', 'dead':'black'}
    
    # na poczatku losowo infekujemy okreslony procent agentow     
    def infect_random(self, infect_perc):
        N = self.g.number_of_nodes()
        # losujemy agentow ktorzy zostana zarazeni
        infected_agents_id = random.sample(range(0,N), int(N * infect_perc))
        nx.set_node_attributes(self.g, 'state', {n: 'infected' for n in infected_agents_id})
        
        
    def draw(self):
        plt.cla()
        # rysowanie wierzcholkow
        nx.draw(self.g, self.pos, node_color = [self.color_dict[self.g.node[n]['state']] for n in self.g.nodes_iter()])
        # rysowanie etykiet wezlow
        nx.draw_networkx_labels(self.g, self.pos,
            {n : str(n) for n in self.g.nodes_iter()}, font_size=16)
        # rysowanie etykiet krawedzi (prawdopodobienstwa kontaktu pomiedzy osobami/wezlami)
        nx.draw_networkx_edge_labels(self.g, self.pos, 
                                     {edge : str(round(self.g[edge[0]][edge[1]]['weight']*100))+'%' for edge in self.g.edges_iter() })
        
    def simulation_step(self):
        states = {'healthy': 0, 'infected' : 0, 'dead' : 0}
        for n in self.g.nodes_iter():
            # zliczanie ile wierzcholkow znajduje sie w poszczegolnym stanie
            states[self.g.node[n]['state']] += 1
            
            # dla agentow zarazonych
            if self.g.node[n]['state'] == 'infected':
                # prawdopodobienstwo smierci jako zmienna losowa z rozkladu wykladniczego
                # z parametrem scale = 0.1 skorygowanym o indywidualna odpornosc agenta
                prob_of_death = np.random.exponential(0.02) * (1 - self.g.node[n]['immunity'])
                
                # z prawdopodobienstwem prob_of_death agent umiera
                if np.random.uniform(0, 1) < prob_of_death:
                    self.g.node[n]['state'] = 'dead'
                else: # jezeli nie umarl losujemy wyzdrowienie
                    # prawdopodobienstwo wyzdrowienia jako zmienna losowa z rozkladu wykladniczego
                    # z parametrem scale = 0.1 skorygowanym o indywidualna odpornosc agenta               
                    prob_of_heal = np.random.exponential(0.1) * self.g.node[n]['immunity']
                    
                    if np.random.uniform(0, 1) < prob_of_heal:
                        self.g.node[n]['state'] = 'healthy'
                        # po wyzdrowieniu odpornosc rosnie o 30%, zastosowano min
                        # aby odpornosc nie przekroczyla 100%
                        self.g.node[n]['immunity'] = min(1, self.g.node[n]['immunity'] * 1.1)
            
            # jezeli agent mimo zarazenia nie umarl ani nie wyzdrowial (jest wciaz zarazony)   
            # zaraza wierzcholki z ktorymi jest polaczony z pewnym prawd.
            # (prawdopodobienstwo spotkania zdefiniowane jest w krawedzi), 
            # prawdopodobienstwo zarazenia skorygowane jest o indywidualna odpornosc agenta
            if self.g.node[n]['state'] == 'infected':
                for neighbour in self.g.neighbors(n):
                    
                    # pomijamy martwych sasiadow i tak sie nie zaraza:)
                    if self.g.node[neighbour]['state'] != 'dead':
                        prob_of_infection =  self.g[n][neighbour]['weight'] * (1 - self.g.node[neighbour]['immunity'])

                        if np.random.uniform(0, 1) < prob_of_infection:
                            self.g.node[neighbour]['state'] = 'infected'
                            
        return states
                            
# %%
'''
    WIELOKROTNE WYWOLANIE SYMULACJI I RAPORT
'''
import pandas as pd

def simulate(iterations = 100):
    N, k = 100, 4
    contact_prob_floor = 0.2
    contact_prob_ceiling = 0.4
    infect_proc = 0.2
    rewire_prob = 0.3
    immunity_prob_floor = 0
    immunity_prob_ceiling = 1
 
    g = graph(N, k, (contact_prob_floor, contact_prob_ceiling), (immunity_prob_floor, immunity_prob_ceiling), rewire_prob)
    g.infect_random(infect_proc)
    
    states_summary = pd.DataFrame( index = range(0, iterations), columns = ['healthy', 'infected', 'dead'])
    for i in range(0, iterations):
        states_summary.iloc[i] = g.simulation_step()
    
    # w ktorej iteracji zakonczyla sie epidemia (pierwszy wiersz dla ktorych liczba infected = 0)
    # jezeli nie zakonczyla sie to -1
    if states_summary['infected'].min() > 0:
        end_of_emidemic = -1
    else:
        end_of_emidemic = states_summary['infected'].idxmin()
    
    return states_summary, end_of_emidemic

# wykonuje wielokrotna symulacje
# n_simulations - ile wykonac symulacji
# iterations - ile wykonac iteracji w kazdej symulacji
def multitime_simulation(n_simulations = 10, iterations = 100):
    # alokujemy sobie pamiec dla podsumowan
    aggregated_states = np.zeros((n_simulations, iterations, 3))
    end_of_emidemics = pd.Series([0]*n_simulations)
        
    for n in range(n_simulations):
        states_summary, end_of_emidemic = simulate(iterations)
        aggregated_states[n] = np.array(states_summary)
        end_of_emidemics[n] = end_of_emidemic
        
    return aggregated_states, end_of_emidemics
    

    
# aggregated_summaries - tablica 3 wymiarowa posiadajaca zagregowane informacje
# kazdej symulacji (stany dla kazdej iteracji w symulacji)
# end_of_emidemics - Series zawierjace nr iteracji w ktorej zakonczyla sie epidemia
# jezeli zakonczyla sie przed osiagnieciem ostatniej iteracji, -1 jezeli epidemia nie zakonczyla sie
aggregated_summaries, end_of_emidemics = multitime_simulation (10, 200)
# usredniona wartosc liczby stanow dla wszytskich symulacji
mean_states = pd.DataFrame( aggregated_summaries.mean(axis = 0), columns =  ['healthy', 'infected', 'dead'])

print( end_of_emidemics )
print( mean_states )

mean_states.plot()


