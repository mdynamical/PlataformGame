import os

sprite_dir = os.listdir("C:\\Users\Miguel\PycharmProjects\MyProjects\main\games\PlataformGame\Images\KNIGHT")
l_sprite_dir = os.listdir("C:\\Users\Miguel\PycharmProjects\MyProjects\main\games\PlataformGame\Images\KNIGHT_LEFT")

sprite_list = {'attack': sprite_dir[:10], 'die': sprite_dir[10:20], 'hurt': sprite_dir[20:30],
               'idle': sprite_dir[30:40], 'jump': sprite_dir[40:50], 'run': sprite_dir[50:60],
               'walk': sprite_dir[60:70]}

l_sprite_list = {'attack': l_sprite_dir[:10], 'die': l_sprite_dir[10:20], 'hurt': l_sprite_dir[20:30],
               'idle': l_sprite_dir[30:40], 'jump': l_sprite_dir[40:50], 'run': l_sprite_dir[50:60],
               'walk': l_sprite_dir[60:70]}