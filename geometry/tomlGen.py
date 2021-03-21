#import toml
import os

def deleteOldDirs():
    try:
        for i in range(len(os.listdir('geometries'))):
            try:
                os.remove('geometries/clover' + str(i) + '/octoclover.toml')
            except:
                pass

            try:
                os.rmdir('geometries/clover' + str(i))
            except:
                pass
    except:
        pass
    
    try: 
        os.rmdir('geometries/')
    except:
        pass


def generateFiles(_drones, DRONE_SIZE, BASE_SIZE):

    path = os.path.abspath(__file__)
    os.chdir(path[:path.rfind('/')])
    deleteOldDirs()

    rotors_names = ['front_right', 'rear_left', 'front_left', 'rear_right']
    print ('Drone size = ', DRONE_SIZE)
    print('Base size = ', BASE_SIZE)
    print(_drones)

    main_drone = _drones[0]
    for i in _drones[1:]:
        i['x'] = i['x'] - main_drone['x']
        i['y'] = i['y'] - main_drone['y']
        i['x'], i['y'] = i['y'], i['x']

    main_drone['x'], main_drone['y'] = 0.0, 0.0

    print(_drones)
    if len(_drones) > 1:
        Ct = float(max([abs(i['x']) for i in _drones] + [abs(i['y']) for i in _drones]) / DRONE_SIZE + 0.5)
    else:
        Ct = 1.0
    print(Ct)

    for i, drone in enumerate(_drones):
        os.makedirs('geometries/clover' + str(i))
        new_file = open(f'geometries/clover{i}/octoclover.toml', 'w')
        new_file.write('#Octoclover' + str(i) + '\n\n')
        new_file.write('[info] \n' + 'key = "mclover_part" \n' + 'description = "Multiclover"\n\n')
        new_file.write('[rotor_default]\n' + 'axis = [0.0, 0.0, -1.0]\n' + f'Ct = {Ct} \n' + 'Cm = 0.05 \n\n')
        
        #new_file.write('[[rotors]]\n' + 'name = "front_right"\n' + '')
        for j, k in enumerate([[0.5, 0.5], [-0.5, -0.5], [0.5, -0.5], [-0.5, 0.5]]):
            x = 3/2 * (drone['x'] + k[0] * BASE_SIZE) / (Ct * DRONE_SIZE)
            y = 3/2 * (drone['y'] + k[1] * BASE_SIZE) / (Ct * DRONE_SIZE)
            z = 0.0

            new_file.write(f'[[rotors]]\nname = "{rotors_names[j]}"\nposition = [{x}, {y}, {z}]\n')

    
    new_file.close()


