"""
Module containing functions for creation and manipulation of progress bars.
"""
from rich.progress import Progress, BarColumn, TaskID, TimeElapsedColumn

COLOR_BAR_PER_LOOP = ['blue', 'red', 'green', 'yellow', 'cyan', 'magenta']
"""List of colors for each nested loop (Working for up to 6 loops)"""


def create_progress_bar() -> Progress:
    """
    Create a progress bar using rich library.

    :return: Progress bar
    """
    prog_bar = Progress("[progress.description]{task.description}",
                        BarColumn(),
                        "[progress.percentage]{task.percentage:>3.0f}%",
                        TimeElapsedColumn(),
                        refresh_per_second=20,
                        speed_estimate_period=20, transient=False)
    return prog_bar


def add_task(progress: Progress, text: str, size: int) -> TaskID:
    """
    Add a task to the progress bar. Add a color to the task progress bar, depending on how many tasks you have.

    :param progress: Progress bar
    :param text: Text of the progress bar
    :param size: Size of the progress bar
    :return: Task ID
    """
    num_tasks = len(progress.tasks)
    color_plus_text = '[{}]{}'.format(COLOR_BAR_PER_LOOP[num_tasks], text)
    task = progress.add_task(description=color_plus_text, total=size)

    return task


def update_task(progress: Progress, task_id: TaskID, advance=1):
    """
    Update the progress bar task.

    :param progress: Progress bar
    :param task_id: Task ID
    :param advance: Step to advance
    :return:
    """
    progress.update(task_id, advance=advance)


def remove_task(progress: Progress, task_id: TaskID):
    """
    Remove a task from the progress bar.

    :param progress: Progress bar
    :param task_id: Task ID
    :return:
    """
    progress.remove_task(task_id)


if __name__ == '__main__':
    from time import sleep

    progress_bar = create_progress_bar()

    with progress_bar:
        # Add an outer task with a total of 10
        outer_task: TaskID = add_task(progress=progress_bar, text="Outer Loop", size=10)
        # Start the outer loop
        for i in range(10):
            # Add an inner task with a total of 20 for each iteration of the outer loop
            inner_task: TaskID = add_task(progress=progress_bar, text="Inner Loop", size=20)
            # Start the inner loop
            for j in range(20):
                # Simulate some work
                sleep(0.1)

                update_task(progress_bar, inner_task, advance=1)
            remove_task(progress_bar, inner_task)

            # Update the outer task progress
            update_task(progress_bar, outer_task, advance=1)
        remove_task(progress_bar, outer_task)
