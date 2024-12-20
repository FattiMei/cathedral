import numpy as np
from scipy.fft import fft, ifft
import pyopencl as cl
import matplotlib.pyplot as plt


def xcorr(x, shift):
    # only overlapping part is computed and result is normalized with the number of samples under the window
    return np.dot(x[shift:], x[:(x.size-shift)]) / (x.size - shift)


def correlogram(x: np.array, maxshift, method='fft'):
    assert(0 < maxshift < len(x))

    if method == 'fft':
        X = fft(x)
        P = np.abs(X) ** 2

        corr = ifft(P).real
        corr = corr / corr[0]

        return corr[0:maxshift]

    elif method == 'serial':
        corr = np.zeros(maxshift)

        x = np.asarray(x, np.float32)
        x = x - np.mean(x)

        for i in range(maxshift):
            corr[i] = xcorr(x, i)

        return corr

    else:
        ValueError("Supported methods are {'fft, 'serial'}")


def setup_opencl_runtime():
    ctx   = cl.create_some_context()
    queue = cl.CommandQueue(ctx, properties = cl.command_queue_properties.PROFILING_ENABLE)

    program = cl.Program(ctx, """
        __kernel void matvec(
                        const	int 	n,
                        const   int     rows,
            __global	const	float 	*x,
            __global		    float 	*result
        ) {
            const int i = get_global_id(0);

            if (i < rows) {
                float acc = 0.0;

                for (int j = 0; j < n - i; ++j) {
                    acc += x[i + j] * x[j];
                }

                result[i] = acc;
            }
        }
    """).build()

    return (ctx, queue, program)


def invert_delay_opencl(x, max_shift):
    # assumes this function gets called once
    result = np.zeros(max_shift, dtype = np.float32)
    x  = np.asarray(x, np.float32)
    x -= np.mean(x)

    ctx, queue, program = setup_opencl_runtime()

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

    program.matvec(queue, result.shape, None, np.int32(x.size), np.int32(result.size), d_x, d_result)
    cl.enqueue_copy(queue, result, d_result)

    return result


if __name__ == '__main__':
    ctx, queue, program = setup_opencl_runtime()

    x = np.random.rand(100000)
    x -= np.mean(x)
    result = np.empty_like(x)

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

    # my machine won't let me use local sizes greater than 64
    # TODO: query max local_group_size
    local_sizes = [1, 2, 4, 8, 16, 32, 64]

    events = [
        program.matvec(
            queue,
            (result.size + result.size % local_size,),
            (local_size,),
            np.int32(x.size),
            np.int32(result.size),
            d_x,
            d_result
        )
        for local_size in local_sizes
    ]
    events[-1].wait()

    times = [1e-9 * (e.profile.end - e.profile.start) for e in events]

    plt.bar([str(x) for x in local_sizes], times)
    plt.title('Local group size performance')
    plt.xlabel('group size')
    plt.ylabel('time [s]')
    plt.show()
