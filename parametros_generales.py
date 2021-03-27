MONEDAS_INICIALES = 30
ENERGIA_PLANTAR = 5
VEL_MOVIMIENTO = 4
ENERGIA_JUGADOR= 100
ENERGIA_DORMIR = 100
PROB_ARBOL = 0.5
PROB_ORO = 0.2
DURACION_LENA = 30
DURACION_ORO = 30
N = 27

    # Se almacena en un diccionario las rutas de imágenes del personaje
sprites_paths = {
    ('walk', 'U', 1): "sprites/personaje/up_1.png",
    ('walk', 'U', 2): 'sprites/personaje/up_2.png',
    ('walk', 'U', 3): 'sprites/personaje/up_3.png',
    ('walk', 'U', 4): 'sprites/personaje/up_4.png',
    ('walk', 'L', 1): 'sprites/personaje/left_1.png',
    ('walk', 'L', 2): 'sprites/personaje/left_2.png',
    ('walk', 'L', 3): 'sprites/personaje/left_3.png',
    ('walk', 'L', 4): 'sprites/personaje/left_4.png',
    ('walk', 'R', 1): 'sprites/personaje/right_1.png',
    ('walk', 'R', 2): 'sprites/personaje/right_2.png',
    ('walk', 'R', 3): 'sprites/personaje/right_3.png',
    ('walk', 'R', 4): 'sprites/personaje/right_4.png',
    ('walk', 'D', 1): 'sprites/personaje/down_1.png',
    ('walk', 'D', 2): 'sprites/personaje/down_2.png',
    ('walk', 'D', 3): 'sprites/personaje/down_3.png',
    ('walk', 'D', 4): 'sprites/personaje/down_4.png'
    }
objetos_paths = {
    "azada" : "sprites/otros/hoe.png",
    "hacha" : "sprites/otros/axe.png",
    "seed_alcachofa" : "sprites/cultivos/alcachofa/seeds.png",
    "seed_choclo" : "sprites/cultivos/choclo/seeds.png",
    "alca" : "sprites/recursos/artichoke.png",
    "choclo" : "sprites/recursos/corn.png",
    "madera" : "sprites/recursos/wood.png",
    "oro" : "sprites/recursos/gold.png",
    "ticket":"sprites/otros/ticket.png",
    "" : ""
}

stages_alca = {
    "1" : 'sprites/cultivos/alcachofa/stage_1',
    "2" : 'sprites/cultivos/alcachofa/stage_2',
    "3" : 'sprites/cultivos/alcachofa/stage_3',
    "4" : 'sprites/cultivos/alcachofa/stage_4',
    "5" : 'sprites/cultivos/alcachofa/stage_5',
    "6" : 'sprites/cultivos/alcachofa/stage_6'

}

stages_choclo = {
    "1" : 'sprites/cultivos/choclo/stage_1',
    "2" : 'sprites/cultivos/choclo/stage_2',
    "3" : 'sprites/cultivos/choclo/stage_3',
    "4" : 'sprites/cultivos/choclo/stage_4',
    "5" : 'sprites/cultivos/choclo/stage_5',
    "6" : 'sprites/cultivos/choclo/stage_6',
    "7" : 'sprites/cultivos/choclo/stage_7'

}
