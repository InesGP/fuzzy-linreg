import numpy
import math


def read_transfo(file_name):
    """Read a 4x4 transformation matrix produced by FSL.

    Args:
        file_name: file containing the transformation matrix

    Returns:
        numpy array containing the transformation matrix
    """
    transfo = numpy.zeros(shape=(4, 4))
    transfo_line = 0
    with open(file_name) as f:
        for line in f:
            line = line.strip()
            elements = line.split()
            assert (
                len(elements) == 4
            ), "Wrong format in transformation line: {0} (file name: {1})".format(
                line, file_name
            )
            for i in range(0, 4):
                transfo[transfo_line][i] = float(elements[i].strip().replace(";", ""))
            transfo_line = transfo_line + 1

    transfo_mat = numpy.matrix(
        [
            [transfo[0][0], transfo[0][1], transfo[0][2], transfo[0][3]],
            [transfo[1][0], transfo[1][1], transfo[1][2], transfo[1][3]],
            [transfo[2][0], transfo[2][1], transfo[2][2], transfo[2][3]],
            [0, 0, 0, 1],
        ]
    )

    return transfo_mat


def get_rot_angle_vec(rot_mat):
    """Return the rotation angle and vector from a transformation matrix.

    Args:
        rot_mat: 4x4 transformation matrix

    Returns:
        rotation angle, rotation vector
    """
    # See http://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToAngle/
    cos = (rot_mat.item(0, 0) + rot_mat.item(1, 1) + rot_mat.item(2, 2) - 1) / 2
    if cos > 1:
        print("Warning: cos is larger than 1: {0}".format(cos))
        cos = 1
    rot_angle = math.acos(cos)
    x = (rot_mat.item(2, 1) - rot_mat.item(1, 2)) / math.sqrt(
        (rot_mat.item(2, 1) - rot_mat.item(1, 2)) ** 2
        + (rot_mat.item(0, 2) - rot_mat.item(2, 0)) ** 2
        + (rot_mat.item(1, 0) - rot_mat.item(0, 1)) ** 2
    )
    y = (rot_mat.item(0, 2) - rot_mat.item(2, 0)) / math.sqrt(
        (rot_mat.item(2, 1) - rot_mat.item(1, 2)) ** 2
        + (rot_mat.item(0, 2) - rot_mat.item(2, 0)) ** 2
        + (rot_mat.item(1, 0) - rot_mat.item(0, 1)) ** 2
    )
    z = (rot_mat.item(1, 0) - rot_mat.item(0, 1)) / math.sqrt(
        (rot_mat.item(2, 1) - rot_mat.item(1, 2)) ** 2
        + (rot_mat.item(0, 2) - rot_mat.item(2, 0)) ** 2
        + (rot_mat.item(1, 0) - rot_mat.item(0, 1)) ** 2
    )
    rot_vec = numpy.array([x, y, z])
    return rot_angle, rot_vec


def get_rot_mat(transfo_mat):
    """Return the rotation matrix from a transformation matrix.

    Args:
        transfo_mat: 4x4 transformation matrix

    Returns:
        Rotation matrix
    """
    rot_mat = numpy.matrix(
        [
            [transfo_mat.item(0, 0), transfo_mat.item(0, 1), transfo_mat.item(0, 2)],
            [transfo_mat.item(1, 0), transfo_mat.item(1, 1), transfo_mat.item(1, 2)],
            [transfo_mat.item(2, 0), transfo_mat.item(2, 1), transfo_mat.item(2, 2)],
        ]
    )
    return rot_mat


def get_tr_vec(transfo_mat):
    """Return translation vector from transformation matrix

    Args:
        transfo_mat: 4x4 transformation matrix

    Returns:
        Translation vector
    """
    tr_vec = numpy.array(
        [transfo_mat.item(0, 3), transfo_mat.item(1, 3), transfo_mat.item(2, 3)]
    )
    return tr_vec


def get_transfo_vector(transfo_mat):
    """Return transformation vector from transformation matrix

    Args:
        transfo_mat: 4x4 transformation matrix

    Returns:
        Transformation vector [tx, ty, tz, rx, ry, rz]
    """
    tx, ty, tz = get_tr_vec(transfo_mat)
    rx, ry, rz = get_euler_angles(transfo_mat)
    return [tx, ty, tz, rx, ry, rz]


def get_euler_angles(transfo_mat):
    """Compute Euler angles from transformation matrix

    Args:
        transfo_mat: 4x4 transformation matrix

    Returns:
        Euler angles rx, ry, rz
    """
    # From http://nghiaho.com/?page_id=846
    rx = math.atan2(transfo_mat.item(2, 1), transfo_mat.item(2, 2))
    ry = math.atan2(
        -transfo_mat.item(2, 0),
        math.sqrt(transfo_mat.item(2, 1) ** 2 + transfo_mat.item(2, 2) ** 2),
    )
    rz = math.atan2(transfo_mat.item(1, 0), transfo_mat.item(0, 0))
    return rx, ry, rz


def get_transfo_mat(x):
    """Return transformation matrix from transformation veector

    Args:
        x: transformation vector [tx, ty, tz, rx, ry, rz]

    Returns:
        4x4 transformation matrix
    """
    tx, ty, tz, rx, ry, rz = x
    x = numpy.matrix([[1, 0, 0], [0, cos(rx), -sin(rx)], [0, sin(rx), cos(rx)]])
    y = numpy.matrix([[cos(ry), 0, sin(ry)], [0, 1, 0], [-sin(ry), 0, cos(ry)]])
    z = numpy.matrix([[cos(rz), -sin(rz), 0], [sin(rz), cos(rz), 0], [0, 0, 1]])
    r = x * y * z
    mat = numpy.matrix(
        [
            [r.item(0, 0), r.item(0, 1), r.item(0, 2), tx],
            [r.item(1, 0), r.item(1, 1), r.item(1, 2), ty],
            [r.item(2, 0), r.item(2, 1), r.item(2, 2), tz],
            [0, 0, 0, 1],
        ]
    )
    return mat


def compare_transfos(mat1, mat2):
    """Return residual transformation vector between input matrices

    Args:
        mat1: 4x4 transformation matrix
        mat2: 4x4 transformation matrix

    Returns:
        Transformation vector representing mat1.I*mat2
    """
    residual_mat = mat1.I * mat2
    return get_transfo_vector(residual_mat)
