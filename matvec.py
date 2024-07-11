import pyopencl as cl
import numpy as np
import matplotlib.pyplot as plt


def round_to_upper_multiple(x, mod):
    if x % mod == 0:
        return mod
    else:
        return x + (mod - x % mod)


class Matvec:
    def __init__(self, ctx):
        self.kernel = None

    def __call__(self, queue, track, result, block_size):
        pass

    def profile_group_size(self, queue, track, result, block_sizes):
        events = [self.__call__(queue, track, result, size) for size in block_sizes]
        events[-1].wait()

        return 1e-9 * np.array([e.profile.end - e.profile.start for e in events])


class NaiveMatvec(Matvec):
    def __init__(self, ctx):
        self.kernel = cl.Program(
            ctx,
            """
            __kernel void matvec(
                            const	int 	n,
                            const   int     rows,
                __global	const	float 	*x,
                __global		    float 	*result
            ) {
                const int i = get_global_id(0);

                if (i < rows) {
                    float acc = 0.0;

                    for (int j = 0; j < n; ++j) {
                        if (i + j < n) {
                            acc += x[i + j] * x[j];
                        }
                    }

                    result[i] = acc;
                }
            }
            """
        ).build().matvec

    def __call__(self, queue, track, result, block_size):
        return self.kernel(
            queue,
            (round_to_upper_multiple(result.size // 4, block_size),),
            (block_size,),
            np.int32(track.size // 4),
            np.int32(result.size // 4),
            track,
            result
        )


if __name__ == '__main__':
    ctx   = cl.create_some_context()
    queue = cl.CommandQueue(ctx, properties = cl.command_queue_properties.PROFILING_ENABLE)

    track = cl.Buffer(
        ctx,
        cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
        hostbuf = np.asarray(np.random.rand(100000), dtype = np.float32)
    )

    result = cl.Buffer(
        ctx,
        cl.mem_flags.WRITE_ONLY,
        size = 4 * 100
    )

    block_sizes = np.array([2, 4, 8, 16, 32, 64, 128, 256])
    times = NaiveMatvec(ctx).profile_group_size(queue, track, result, block_sizes)

    plt.bar([str(x) for x in block_sizes], times)
    plt.title('Local group size performance')
    plt.xlabel('group size')
    plt.ylabel('time [s]')
    plt.show()
