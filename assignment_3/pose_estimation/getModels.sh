# ------------------------- BODY, FOOT, FACE, AND HAND MODELS -------------------------
# Downloading body pose (COCO and MPI), face and hand models
OPENPOSE_URL="http://posefs1.perception.cs.cmu.edu/OpenPose/models/"

WEIGTHS_URL="http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/mpi/pose_iter_160000.caffemodel"
PROTO_URL="https://raw.githubusercontent.com/CMU-Perceptual-Computing-Lab/openpose/master/models/pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"


# Body (MPI)
MPI_FOLDER=${POSE_FOLDER}"mpi/"
wget -c ${WEIGTHS_URL} -P ${MPI_FOLDER}
wget -c ${PROTO_URL} -P ${MPI_FOLDER}

