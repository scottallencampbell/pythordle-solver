import cProfile
from pstats import Stats, SortKey

from src.solver import run

if __name__ == '__main__':
    do_profiling = False
    if do_profiling:
        with cProfile.Profile() as pr:
            run()

        with open('profiling_stats.txt', 'w') as stream:
            stats = Stats(pr, stream=stream)
            stats.strip_dirs()
            stats.sort_stats('time')
            stats.dump_stats('.prof_stats')
            stats.print_stats()
    else:
        run()