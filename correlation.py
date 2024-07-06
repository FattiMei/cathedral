import numpy as np
import pyopencl as cl


def cross_correlation(x, shift):
    # only overlapping part is computed
    # normalize with the number of samples under the window
    return np.dot(x[shift:], x[:(x.size-shift)]) / (x.size - shift)


def invert_delay_serial(x, max_shift):
    result = np.zeros(max_shift)
    x  = np.asarray(x, np.float32)
    x -= np.mean(x)

    for i in range(result.size):
        result[i] = cross_correlation(x, i)

    return result


def invert_delay_opencl(x, max_shift):
    result = np.zeros(max_shift, dtype = np.float32)
    x  = np.asarray(x, np.float32)
    x -= np.mean(x)

    # we are assuming that this function gets called once in the program
    ctx   = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    d_x = cl.Buffer(
        ctx,
        cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
        hostbuf = x
    )

    d_result = cl.Buffer(
        ctx,
        cl.mem_flags.WRITE_ONLY,
        result.nbytes
    )

    program = cl.Program(ctx, """
        __kernel void matvec(
                        const	int 	n,
            __global	const	float 	*x,
            __global		    float 	*result
        ) {
            const int shift = get_global_id(0);
            float acc = 0.0;

            for (int i = 0; i < n; ++i) {
                if (shift + i < n) {
                    acc += x[shift + i] * x[i];
                }
            }

            result[shift] = acc / (float) (n - shift);
        }
    """).build()

    program.matvec(queue, result.shape, None, np.int32(x.size), d_x, d_result)
    cl.enqueue_copy(queue, result, d_result)

    return result
