from avocado.core import nrunner


def main():
    task1 = nrunner.Task('1-/bin/true',
                         nrunner.Runnable('exec-test', '/bin/true'),
                         known_runners=nrunner.RunnerApp.RUNNABLE_KINDS_CAPABLE)

    for status in task1.run():
        print(status)


if __name__ == '__main__':
    main()
