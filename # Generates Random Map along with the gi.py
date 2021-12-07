# Generates Random Map along with the given obstacle list
MaxIter = 80000
CCvariation = 0.01
randomLevel = 0.0001
dcells = 2
timeout = 10   # [seconds]

importance = False
notEqualPortions = False
visualization = False

h = 10
w = 10
center = (float((h-1)/2), float((w-1)/2))
number_of_robots = 3
param_dataset = []
image_dataset = []
for i in range(5):
    
    count = 0
    map = np.ones((h,w))
    radius = random_seed()
    circular, map_list, random_obstacles, obstacle_list = create_mask(h,w, center, radius)

    # Generates 3 list of initial poses. 
    initial_poses = seed_positions(number_of_robots, obstacle_list, map)
    initial_positions = list(list_To_coords(initial_poses, h))
    portions = list(np.ones(len(initial_poses))*1/len(initial_poses))
    obstacles_positions = list(list_To_coords(obstacle_list, h))
    initial_positions = list(list_To_coords(initial_poses, h))
    #print(initial_poses)
    #print(initial_positions)

    #MatPlot Visualizer for generated Maps
    map = writespots(obstacle_list, np.ones((h,w)), 0)
    map = writespots(initial_poses, map, 2)
    #paint_map(map)
    solved_map = []

    data_iteration = []
    image_iteration = []
    from interruptingcow import timeout
    
    try:
        with timeout(5, exception=RuntimeError):
            while True:
                poly = darpinPoly.DARPinPoly(h, w, MaxIter, CCvariation, randomLevel, dcells, importance, notEqualPortions, initial_positions, portions, obstacles_positions, visualization)   
                count =  count + 1             
                solved_map = poly.A

                currentFig = plt.gcf()
                plt.axis('off')            # Change MAP???
                plt.imshow(solved_map)
                plt.show()
                savedim = currentFig.savefig('current_map' + str(count) + '.png')
                
                # fudge= plt.imread(savedim)
                # plt.imshow(fudge)

                stdv = std_map(solved_map, 3) #calculates std between areas occupied
                data_iteration.append(stdv)
                image_iteration.append(savedim)
                data_iteration.append(initial_positions)
                data_iteration.append(covisiblity_calculation(solved_map))
                
                break
    except RuntimeError:
        pass
    
    param_dataset.append(data_iteration)
    image_dataset.append(image_iteration)


# Get file name of new dataset
param_data = store_runs(param_dataset)
image_data = store_runs(image_dataset)

# Make Image Data set Also
# print(poly.A)
