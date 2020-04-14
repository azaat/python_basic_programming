import cv2
import base64
import estimation_config as cfg


def get_points(output, frame):
    H = output.shape[2]
    W = output.shape[3]

    points = []
    for i in range(cfg.n_points):
        # Body parts confidence map
        prob_map = output[0, i, :, :]

        min_val, prob, min_loc, point = cv2.minMaxLoc(prob_map)

        x = (frame.shape[1] * point[0]) / W
        y = (frame.shape[0] * point[1]) / H

        if prob > cfg.threshold:
            points.append((int(x), int(y)))
        else:
            points.append(None)
    return points


def draw_points(img_path):
    # Read the network into Memory
    net = cv2.dnn.readNetFromCaffe(cfg.proto_file, cfg.weights_file)

    # Read image
    frame = cv2.imread(img_path)
    if frame is None:
        raise ValueError('Input image is corrupt')

    # Prepare the frame to be fed to the network
    inp_blob = cv2.dnn.blobFromImage(
        frame, 1.0 / 255,
        (cfg.in_width, cfg.in_height),
        (0, 0, 0), swapRB=False, crop=False
    )

    net.setInput(inp_blob)
    output = net.forward()
    points = get_points(output, frame)

    # Draw points
    for pair in cfg.pose_pairs:
        partA = pair[0]
        partB = pair[1]

        if points[partA] and points[partB]:
            cv2.line(frame, points[partA], points[partB], (0, 255, 255), 1)
            cv2.circle(
                frame, points[partA], 2, (255, 255, 255),
                thickness=-1, lineType=cv2.FILLED
            )
    frame = cv2.imencode('.jpg', frame)[1]
    return base64.b64encode(frame).decode('utf-8', 'strict')
