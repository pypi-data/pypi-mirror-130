from adxbw.node import *


def newton(f, x_k, tol=1.0e-16, max_it=1000, lr=1):
    """
    Newton optimizer for single independent variable: can be scalar or vector
    :param f: str representation of the function to evaluate
    :param x_k: an AD object represents initial guess
    :param tol: Tolerance to check if optimization finished
    :param max_it: number of max iteration
    :param lr: learning rate / step size
    :return: int/float/numpy array
    """
    root = None

    for k in range(max_it):
        temp_node = eval(f)
        f_val = temp_node.val
        J_x = temp_node.partial_ders
        dx_k = (-f_val / J_x) * lr
        if np.all(abs(dx_k) < tol):
            root = x_k.val + dx_k
            print(f"Found root {root} at iteration {k + 1}")
            break
        print(f"Iteration {k + 1}: Delta x = {dx_k}")
        x_k.val += dx_k

    return root


def newton_multi(f, x_k, tol=1.0e-16, max_it=1000, lr=1):
    """
    Newton optimizer for multiple independent variables: only scalar allowed
    :param f: str representation of the function to evaluate
    :param x_k: dict of AD objects represent initial guess
    :param tol: Tolerance to check if optimization finished
    :param max_it: number of max iteration
    :param lr: learning rate / step size
    :return: int/float/numpy array
    """

    keys = list(x_k.keys())
    root = np.array([1.0] * len(keys))

    f = _format_funct(f, x_k)

    for k in range(max_it):
        temp_node = eval(f)
        f_val = temp_node.val
        J_x = temp_node.partial_ders
        dx_k = (-f_val / J_x) * lr

        for i in range(len(keys)):
            if np.all(np.abs(dx_k) < tol):
                for j in range(len(keys)):
                    root[j] = x_k[keys[j]].val + dx_k[j]
                    print(f"Found root {root[j]:e} for {keys[j]} at iteration {k + 1}")
                return root
            else:
                print(f"Iteration {k + 1}: Delta x = {dx_k[i]:e}")
                x_k[keys[i]].val += dx_k[i]

    return root


def _format_funct(funct, temp_dict):
    for node in temp_dict.keys():
        funct = funct.replace(node, f"x_k['{node}']")
    return funct
