import numpy as np


Y_UP_TO_Z_UP = np.array(
    [[0.0, 0.0, -1.0, 0.0],
     [-1.0, 0.0, 0.0, 0.0],
     [0.0, 1.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 1.0]],
    dtype=float,
)

# The same wrist-local convention used by xteleop's WebXR preprocessor.
HAND_TO_ROBOT = np.array(
    [[0.0, -1.0, 0.0, 0.0],
     [0.0, 0.0, -1.0, 0.0],
     [1.0, 0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 1.0]],
    dtype=float,
)


def project_rotation(matrix):
    matrix = np.asarray(matrix, dtype=float).reshape(3, 3)
    u, _, vt = np.linalg.svd(matrix)
    rotation = u @ vt
    if np.linalg.det(rotation) < 0.0:
        u[:, -1] *= -1.0
        rotation = u @ vt
    return rotation


def valid_transform(matrix):
    try:
        matrix = np.asarray(matrix, dtype=float).reshape(4, 4)
    except (TypeError, ValueError):
        return False
    return bool(
        np.all(np.isfinite(matrix))
        and abs(float(np.linalg.det(matrix[:3, :3]))) > 1e-6
    )


def inverse_transform(matrix):
    matrix = np.asarray(matrix, dtype=float).reshape(4, 4)
    result = np.eye(4)
    result[:3, :3] = matrix[:3, :3].T
    result[:3, 3] = -result[:3, :3] @ matrix[:3, 3]
    return result


def webxr_transform(matrix):
    """Convert a WebXR local-to-world transform to project Z-up axes."""
    matrix = np.asarray(matrix, dtype=float).reshape(4, 4)
    converted = Y_UP_TO_Z_UP @ matrix @ inverse_transform(Y_UP_TO_Z_UP)
    converted[:3, :3] = project_rotation(converted[:3, :3])
    return converted


def webxr_hand_frame(wrist_matrix, landmarks):
    """Return the wrist pose and 25 landmarks in the xteleop hand convention."""
    wrist = webxr_transform(wrist_matrix)
    points = np.asarray(landmarks, dtype=float).reshape(25, 3)
    points_h = np.concatenate((points.T, np.ones((1, 25))), axis=0)
    points_zup = (Y_UP_TO_Z_UP @ points_h)
    local = inverse_transform(wrist) @ points_zup
    local = (HAND_TO_ROBOT.T @ local)[:3, :].T
    wrist = wrist @ HAND_TO_ROBOT
    wrist[:3, :3] = project_rotation(wrist[:3, :3])
    return wrist, local


def quaternion_xyzw(rotation):
    """Convert a proper 3x3 rotation matrix to a normalized xyzw quaternion."""
    r = project_rotation(rotation)
    trace = float(np.trace(r))
    if trace > 0.0:
        s = np.sqrt(trace + 1.0) * 2.0
        q = np.array([(r[2, 1] - r[1, 2]) / s,
                      (r[0, 2] - r[2, 0]) / s,
                      (r[1, 0] - r[0, 1]) / s,
                      0.25 * s])
    else:
        index = int(np.argmax(np.diag(r)))
        if index == 0:
            s = np.sqrt(1.0 + r[0, 0] - r[1, 1] - r[2, 2]) * 2.0
            q = np.array([0.25 * s, (r[0, 1] + r[1, 0]) / s,
                          (r[0, 2] + r[2, 0]) / s, (r[2, 1] - r[1, 2]) / s])
        elif index == 1:
            s = np.sqrt(1.0 + r[1, 1] - r[0, 0] - r[2, 2]) * 2.0
            q = np.array([(r[0, 1] + r[1, 0]) / s, 0.25 * s,
                          (r[1, 2] + r[2, 1]) / s, (r[0, 2] - r[2, 0]) / s])
        else:
            s = np.sqrt(1.0 + r[2, 2] - r[0, 0] - r[1, 1]) * 2.0
            q = np.array([(r[0, 2] + r[2, 0]) / s,
                          (r[1, 2] + r[2, 1]) / s, 0.25 * s,
                          (r[1, 0] - r[0, 1]) / s])
    return q / np.linalg.norm(q)


def rotation_from_quaternion_xyzw(quaternion):
    x, y, z, w = np.asarray(quaternion, dtype=float).reshape(4)
    norm = np.linalg.norm([x, y, z, w])
    if norm < 1e-9:
        raise ValueError("zero quaternion")
    x, y, z, w = np.array([x, y, z, w]) / norm
    return np.array([
        [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
        [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
        [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
    ])


def rotation_angle(rotation):
    value = np.clip((np.trace(project_rotation(rotation)) - 1.0) * 0.5, -1.0, 1.0)
    return float(np.arccos(value))


def limit_rotation_step(previous, target, max_angle):
    previous = project_rotation(previous)
    target = project_rotation(target)
    relative = previous.T @ target
    angle = rotation_angle(relative)
    if angle <= max_angle or angle < 1e-9:
        return target
    axis_matrix = (relative - relative.T) / (2.0 * np.sin(angle))
    axis = np.array([axis_matrix[2, 1], axis_matrix[0, 2], axis_matrix[1, 0]])
    axis /= max(np.linalg.norm(axis), 1e-9)
    x, y, z = axis
    c, s = np.cos(max_angle), np.sin(max_angle)
    one_c = 1.0 - c
    limited_relative = np.array([
        [c + x*x*one_c, x*y*one_c - z*s, x*z*one_c + y*s],
        [y*x*one_c + z*s, c + y*y*one_c, y*z*one_c - x*s],
        [z*x*one_c - y*s, z*y*one_c + x*s, c + z*z*one_c],
    ])
    return project_rotation(previous @ limited_relative)
