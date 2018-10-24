### Symulacja wieloagentowa umieralności oraz czasu trwania epidemii

Symulacja przedstawia rozprzestrzeniania się epidemii choroby wśród społeczeństwa reprezentowanego siecią społeczną małego świata. Każdy wierzchołek reprezentuje odrębną osobę (agenta) a wagi połączeń pomiędzy wierzchołkami reprezentują częstość kontaktu z daną osobą (prawdopodobieństwo kontaktu w jednym kroku iteracji). Symulacja ma na celu analizę liczby umieralności wśród społeczeństwa oraz czas trwania epidemii w zależności od parametrów:
* Liczba początkowa ludności (agentów)
* Stopień połączeń lokalny w sieci (parametr k w funkcji tworzącej graf małego swiata)
* Procent połączeń dalekich (parametr p prawdopodobieństwo przepięcia każdego z węzłów)
* Procent początkowo zarażonych agentów
* Prawdopodobieństwo kontaktu pomiędzy agentami w jednym kroku iteracji
* Początkowy poziom odporność (na zarażenie i śmierć)

Podstawowe założenia:
* Agent zarażony w każdym kroku iteracji może wyzdrowieć, umrzeć, dalej być chory
* Agent który jest chory zaraża
* Agent martwy nie zaraża
* Agent chory w każdym kroku iteracji może umrzeć z pewnym prawdopodobieństwem. Prawdopodobienstwo śmierci jest produktem zmiennej losowej z rozkładu wykładniczego o parametrze scale = 0.1 oraz indywidualnej odporności agenta
* Prawdopodobieństwo_zgonu = random.exponential(scale=0.1) * (1 – odporność)
* Jeżeli agent nie umrze w danym kroku iteracji może wyzdrowieć. Prawdopodobienstwo wyzdrowienia charakteryzują podobne zaleznosci:
Prawdopodobieństwo_wyzdrowienia = random.exponential(scale=0.1) \* odporność
* Jeżeli agent był zarażony a nie umarł ani nie wyzdrowiał w danym kroku iteracji to zaraża z  pewnym prawdopodobieństwem każdego ze swoich sąsiadów (wierzchołki z ktorym istnieje polaczenie). Prawdopodobieństwo zarażenia sąsiada X zależy od dwóch czynników: prawdopodobieństwa kontaktu oraz indywidualnej odporności na chorobę. (Prawd. kontaktu jest reprezentowane w krawędziach miedzy wierzchołkami)
Prawdopodobieństwo_zarazenia = prawdopodobieństwo_kontaktu[u][v] * (1 - odporność[v]).
W tym przypadku u jest wierzchołkiem zainfekowanym i probuje zainfekować wierzchołek v.
* Odporność agenta na chorobę który był zainfekowany a wyzdrowiał rośnie o 30%
* Jeden krok iteracji może reprezentować jeden dzień/ tydzień what ever.

