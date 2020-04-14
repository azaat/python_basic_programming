# Model files
proto_file = "../mpi/pose_deploy_linevec_faster_4_stages.prototxt"
weights_file = "../mpi/pose_iter_160000.caffemodel"

# Resize input to the following width and height
in_width = 400
in_height = 400

# Estimation threshold
threshold = 0.1

# Point configuration
n_points = 15
pose_pairs = [
    [0, 1],   [1, 2], [2, 3],  [3, 4],
    [1, 5],   [5, 6], [6, 7],  [1, 14],
    [14, 8],  [8, 9], [9, 10], [14, 11],
    [11, 12], [12, 13]
]
