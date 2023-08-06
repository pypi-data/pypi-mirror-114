import asyncio

from avocado.core import nrunner


@asyncio.coroutine
def main():
    task1 = nrunner.Task('1-/bin/true',
                         nrunner.Runnable('exec-test', '/bin/true'),
                         known_runners=nrunner.RunnerApp.RUNNABLE_KINDS_CAPABLE)

    task2 = nrunner.Task('2-/bin/false',
                         nrunner.Runnable('exec-test', '/bin/false'),
                         known_runners=nrunner.RunnerApp.RUNNABLE_KINDS_CAPABLE)

    task3 = nrunner.Task('3-/bin/sleep 60',
                         nrunner.Runnable('exec-test', '/bin/sleep', '60'),
                         known_runners=nrunner.RunnerApp.RUNNABLE_KINDS_CAPABLE)

    spawner = nrunner.ProcessSpawner()
    spawn_manager = nrunner.SpawnManager(spawner, [task3, task2, task1])

    while True:
        try:
            yield from spawn_manager.spawn_next()
            print("---------------------------------------------")
            print("Task spanwed")
            print("Pending:")
            print(
                "\n".join(["\t%s" % t.identifier for t in spawn_manager.pending_tasks]))
            print("Spawned:")
            print(
                "\n".join(["\t%s" % t.identifier for t in spawn_manager.spawned_tasks]))
            print()
            # FIXME: there's currently no task being put into completed
            if spawn_manager.completed_tasks:
                print("Completed:")
                print(
                    "\n".join(["\t%s" % t.identifier for t in spawn_manager.completed_tasks]))
            if spawn_manager.suspicious_spawned_tasks:
                print("Suspicious:")
                print("\n".join(
                    ["\t%s" % t.identifier for t in spawn_manager.suspicious_spawned_tasks]))

            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print()
        except IndexError:
            break

    # Now we need to make sure there's no more pending tasks
    # while True:


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
