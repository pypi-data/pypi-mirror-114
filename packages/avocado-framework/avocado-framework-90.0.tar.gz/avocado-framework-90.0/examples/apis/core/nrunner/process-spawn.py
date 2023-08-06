import asyncio

from avocado.core import nrunner


def main():
    task1 = nrunner.Task('1-/bin/true',
                         nrunner.Runnable('exec-test', '/bin/true'),
                         known_runners=nrunner.RunnerApp.RUNNABLE_KINDS_CAPABLE)

    spawner = nrunner.ProcessSpawner()
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(spawner.spawn(task1))
    print(result)
    print(spawner.is_alive(task1))


if __name__ == '__main__':
    main()
