import os

sprite_dir = os.listdir("C:\\Users\Miguel\PycharmProjects\MyProjects\main\games\PlataformGame\Images\KNIGHT")
l_sprite_dir = os.listdir("C:\\Users\Miguel\PycharmProjects\MyProjects\main\games\PlataformGame\Images\KNIGHT_LEFT")

e_sprite_dir = os.listdir("C:\\Users\Miguel\PycharmProjects\MyProjects\main\games\PlataformGame\Images\MINOTAUR\PNGSequences")
e_sprite_dir_l = os.listdir("C:\\Users\Miguel\PycharmProjects\MyProjects\main\games\PlataformGame\Images\MINOTAUR_LEFT\PNGSequences")

sprite_list = {'attack': sprite_dir[:10], 'die': sprite_dir[10:20], 'hurt': sprite_dir[20:30],
               'idle': sprite_dir[30:40], 'jump': sprite_dir[40:50], 'run': sprite_dir[50:60],
               'walk': sprite_dir[60:70]}

l_sprite_list = {'attack': l_sprite_dir[:10], 'die': l_sprite_dir[10:20], 'hurt': l_sprite_dir[20:30],
               'idle': l_sprite_dir[30:40], 'jump': l_sprite_dir[40:50], 'run': l_sprite_dir[50:60],
               'walk': l_sprite_dir[60:70]}

e_sprite_list = {'attack': e_sprite_dir[:11], 'die': e_sprite_dir[12:26], 'hurt': e_sprite_dir[27:38],
               'idle': e_sprite_dir[39:50], 'jump': e_sprite_dir[51:56], 'run': e_sprite_dir[52:69]}


e_sprite_list_l = {'attack': e_sprite_dir_l[:11], 'die': e_sprite_dir_l[12:26], 'hurt': e_sprite_dir_l[27:38],
               'idle': e_sprite_dir_l[39:50], 'jump': e_sprite_dir_l[51:56], 'run': e_sprite_dir_l[52:69]}
