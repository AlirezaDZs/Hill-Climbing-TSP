import networkx as nx
import random
import math

iran_cities = {
    'Azarbaijan Sharghi': [('Ardebil', 215), ('Zanjan', 295), ('Azarbaijan Gharbi', 150)],
    'Azarbaijan Gharbi': [('Azarbaijan Sharghi', 150), ('Kordestan', 235), ('Zanjan', 310)],
    'Ardebil': [('Azarbaijan Sharghi', 215), ('Gilan', 185), ('Zanjan', 370)],
    'Esfahan': [('Chaharmahal Bakhtiari', 95), ('Kohgiluyeh', 330), ('Fars', 480),
                ('Yazd', 325), ('Qom', 265), ('Markazi', 330), ('Khorasan Jonubi', 560)],
    'Alborz': [('Tehran', 50), ('Mazandaran', 180), ('Qazvin', 100)],
    'Ilam': [('Kermanshah', 135), ('Khoozestan', 295), ('Lorestan', 300)],
    'Bushehr': [('Fars', 340), ('Khoozestan', 490), ('Kohgiluyeh', 230), ('Hormozgan', 480)],
    'Tehran': [('Alborz', 50), ('Mazandaran', 250), ('Semnan', 220), ('Qom', 150)],
    'Chaharmahal Bakhtiari': [('Esfahan', 95), ('Kohgiluyeh', 175), ('Khoozestan', 280), ('Lorestan', 240)],
    'Khorasan Jonubi': [('Khorasan Razavi', 510), ('Yazd', 300), ('Sistan Baluchestan', 550), ('Esfahan', 560)],
    'Khorasan Razavi': [('Khorasan Shomali', 235), ('Khorasan Jonubi', 510), ('Semnan', 700), ('Golestan', 600)],
    'Khorasan Shomali': [('Golestan', 300), ('Khorasan Razavi', 235), ('Semnan', 480)],
    'Khoozestan': [('Ilam', 295), ('Kohgiluyeh', 250), ('Bushehr', 490), ('Chaharmahal Bakhtiari', 280), ('Lorestan', 220)],
    'Zanjan': [('Azarbaijan Sharghi', 295), ('Azarbaijan Gharbi', 310), ('Kordestan', 200), ('Qazvin', 160), ('Hamedan', 260)],
    'Sistan Baluchestan': [('Kerman', 500), ('Hormozgan', 720), ('Khorasan Jonubi', 550)],
    'Fars': [('Esfahan', 480), ('Bushehr', 340), ('Kohgiluyeh', 220), ('Hormozgan', 570)],
    'Qazvin': [('Zanjan', 160), ('Gilan', 150), ('Alborz', 100), ('Hamedan', 280)],
    'Qom': [('Esfahan', 265), ('Markazi', 150), ('Tehran', 150), ('Semnan', 320)],
    'Kordestan': [('Kermanshah', 135), ('Hamedan', 190), ('Zanjan', 200), ('Azarbaijan Gharbi', 235)],
    'Kerman': [('Sistan Baluchestan', 500), ('Yazd', 380), ('Khorasan Jonubi', 300), ('Hormozgan', 400)],
    'Kermanshah': [('Kordestan', 135), ('Ilam', 135), ('Hamedan', 190), ('Lorestan', 230)],
    'Kohgiluyeh': [('Fars', 220), ('Bushehr', 230), ('Khoozestan', 250), ('Esfahan', 330)],
    'Golestan': [('Khorasan Shomali', 300), ('Semnan', 400), ('Mazandaran', 110)],
    'Gilan': [('Ardebil', 185), ('Mazandaran', 300), ('Qazvin', 150)],
    'Lorestan': [('Kermanshah', 230), ('Khoozestan', 220), ('Ilam', 300), ('Chaharmahal Bakhtiari', 240), ('Esfahan', 350)],
    'Mazandaran': [('Golestan', 110), ('Tehran', 250), ('Gilan', 300), ('Alborz', 180)],
    'Markazi': [('Qom', 150), ('Hamedan', 200), ('Lorestan', 290), ('Esfahan', 330)],
    'Hormozgan': [('Kerman', 400), ('Sistan Baluchestan', 720), ('Bushehr', 480), ('Fars', 570)],
    'Hamedan': [('Kordestan', 190), ('Zanjan', 260), ('Markazi', 200), ('Lorestan', 230), ('Kermanshah', 190)],
    'Yazd': [('Esfahan', 325), ('Kerman', 380), ('Khorasan Jonubi', 300), ('Fars', 370)],
    'Semnan': [('Tehran', 220), ('Mazandaran', 250), ('Golestan', 400), ('Khorasan Shomali', 480), ('Khorasan Razavi', 700), ('Qom', 320)]
}

def hill_climbing(G):
    current_p  = list(G.nodes)
    random.shuffle(current_p)
    current_c = cost(G,current_p)
    improving = True
    while improving:
        improving = False
        for i in range(len(current_p)):
            for j in range(i,len(current_p)):
                new_p = current_p
                new_p[i], new_p[j] = new_p[j], new_p[i]
                new_c = cost(G,new_p)
                if new_c < current_c:
                    current_c = new_c
                    current_p = new_p
                    improving = True
    return current_p, current_c



def cost(G,path):
    cost = 0
    for i in range(len(path)-1):
        try:
            cost += G[path[i-1]][path[i]]['weight']
        except KeyError:
            cost += 1e6
    return cost

def normalize_distance(c):
    all_d = []
    for k,v in c.items():
        all_d.extend(d[1] for d in v)
        # print(all_d)
    
    min_d = min(all_d)
    max_d = max(all_d)
    
    normal_d = {}
    for k, v in c.items():
        n = [
            (neighbor, round((d-min_d)/(max_d-min_d),4))
            for neighbor, d in v
        ]
        normal_d[k] = n
    return normal_d

normalize_cities = normalize_distance(iran_cities)

G = nx.Graph()

for k in normalize_cities.keys():
    G.add_node(k)

for k,v in normalize_cities.items():
    for i in v:
        G.add_edge(k,i[0], weight=i[1])

    
final_hill_p, final_hill_c = hill_climbing(G)

"میتونیم حلقه زیر رو اجرا کنیم تا مطمئن شیم دور بدست میاد"
# while final_hill_c > 1e6:
#     final_hill_p, final_hill_c = hill_climbing(G)

print(f"Hill climbing: {final_hill_p} {final_hill_c}")



