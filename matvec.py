import pyopencl as cl
import numpy as np
import matplotlib.pyplot as plt


def round_to_upper_multiple(x, mod):
    # maybe there are more clever implementations
    if mod is None:
        return x
    elif x % mod == 0:
        return mod
    else:
        return x + (mod - x % mod)


class Matvec:
    def __init__(self, ctx):
        self.name = 'matvec'
        self.kernel = None

    def __call__(self, queue, track, result, block_size):
        pass

    def profile_group_size(self, queue, track, result, block_sizes):
        events = [self.__call__(queue, track, result, size) for size in block_sizes]
        events[-1].wait()

        return 1e-9 * np.array([e.profile.end - e.profile.start for e in events])


class NaiveMatvec(Matvec):
    def __init__(self, ctx):
        self.name = 'naive'
        self.kernel = cl.Program(
            ctx,
            """
            __kernel void matvec(
                const int n,
                const int rows,
                __global const float *x,
                __global float *result
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

    # we are assuming the storage type of the buffers
    # this is wrong and won't be fit for exploring possible improvements
    # in transfer time and computation time using different precision than float
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


class EarlyExitMatvec(Matvec):
    def __init__(self, ctx):
        self.name = 'early exit'
        self.kernel = cl.Program(
            ctx,
            """
            __kernel void matvec(
                const int n,
                const int rows,
                __global const float *x,
                __global float *result
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
            """
        ).build().matvec

    # we are assuming the storage type of the buffers
    # this is wrong and won't be fit for exploring possible improvements
    # in transfer time and computation time using different precision than float
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


class TilingMatvec(Matvec):
    # for now assume no left over iterations
    def __init__(self, ctx):
        self.name = 'tiling'
        self.kernel = cl.Program(
            ctx,
            """
            __kernel void matvec(
                const int n,
                const int rows,
                __global const float *x,
                __global float *result,
                __local  float *buffer
            ) {
                const int i = get_global_id(0);

                if (i < rows) {
                    float acc = 0.0;

                    const int tile_size = get_local_size(0);
                    const int ntiles = n / tile_size;

                    for (int tile = 0; tile < ntiles; ++tile) {
                        const int read_index = tile * tile_size + get_local_id(0);
                        buffer[get_local_id(0)] = x[read_index];

                        barrier(CLK_LOCAL_MEM_FENCE);

                        for (int j = 0; j < tile_size; ++j) {
                            acc += x[tile * tile_size + j] * buffer[j];
                        }
                    }

                    result[i] = acc;
                }
            }
            """
        ).build().matvec

    # we are assuming the storage type of the buffers
    # this is wrong and won't be fit for exploring possible improvements
    # in transfer time and computation time using different precision than float
    def __call__(self, queue, track, result, block_size):
        return self.kernel(
            queue,
            (round_to_upper_multiple(result.size // 4, block_size),),
            (block_size,),
            np.int32(track.size // 4),
            np.int32(result.size // 4),
            track,
            result,
            cl.LocalMemory(4 * block_size)
        )


class ReuseMatvec(Matvec):
    # for now assume no left over iterations
    def __init__(self, ctx):
        self.name = 'reuse'
        self.kernel = cl.Program(
            ctx,
            """
            __kernel void matvec(
                const int n,
                const int rows,
                __global const float *x,
                __global float *result,
                __local  float *buffer
            ) {
                const int i = get_global_id(0);
                const int local_id = get_local_id(0);

                if (i < rows) {
                    const int block_size = get_local_size(0);
                    float acc = 0.0;

                    buffer[local_id] = x[i + local_id];
                    barrier(CLK_LOCAL_MEM_FENCE);

                    for (int j = 0; j < n - i; ++j) {
                        acc += buffer[j % block_size] * x[j];

                        if (local_id == 0) {
                            if (j + block_size < n) {
                                buffer[j % block_size] = x[j + block_size];
                            }
                            else {
                                buffer[j % block_size] = 0;
                            }
                        }
                    }

                    result[i] = acc;
                }
            }
            """
        ).build().matvec

    # we are assuming the storage type of the buffers
    # this is wrong and won't be fit for exploring possible improvements
    # in transfer time and computation time using different precision than float
    def __call__(self, queue, track, result, block_size):
        return self.kernel(
            queue,
            (round_to_upper_multiple(result.size // 4, block_size),),
            (block_size,),
            np.int32(track.size // 4),
            np.int32(result.size // 4),
            track,
            result,
            cl.LocalMemory(4 * block_size)
        )


if __name__ == '__main__':
    ctx   = cl.create_some_context()
    queue = cl.CommandQueue(ctx, properties = cl.command_queue_properties.PROFILING_ENABLE)

    track = cl.Buffer(
        ctx,
        cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
        hostbuf = np.asarray(np.random.rand(2 ** 17), dtype = np.float32)
    )

    result = cl.Buffer(
        ctx,
        cl.mem_flags.WRITE_ONLY,
        size = 4 * 1024
    )

    block_sizes = np.array([2, 4, 8, 16, 32, 64, 128, 256])
    block_label = [str(x) for x in block_sizes]

    for method in [NaiveMatvec, EarlyExitMatvec, TilingMatvec, ReuseMatvec]:
        kernel = method(ctx)
        times = kernel.profile_group_size(queue, track, result, block_sizes)

        plt.plot(block_label, times, 'o-', label = kernel.name)


    plt.title('Local group size performance')
    plt.legend()
    plt.xlabel('group size')
    plt.ylabel('time [s]')
    plt.show()
