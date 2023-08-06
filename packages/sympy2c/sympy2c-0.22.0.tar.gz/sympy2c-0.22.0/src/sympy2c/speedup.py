import multiprocessing

from sympy import Matrix


def _jacobian(args):
    expressions, variables = args
    return expressions.jacobian(variables)


def jacobian(expressions, variables, N=4):
    if expressions.rows < 4 * N:
        return expressions.jacobian(variables)
    blocks = [Matrix(expressions[i::N]) for i in range(N)]
    args = [(b, variables) for b in blocks]
    with multiprocessing.Pool(N) as pool:
        partial_results = pool.map(_jacobian, args)

    result = [partial_results[i % N][i // N, :] for i in range(expressions.rows)]
    return Matrix(result)
