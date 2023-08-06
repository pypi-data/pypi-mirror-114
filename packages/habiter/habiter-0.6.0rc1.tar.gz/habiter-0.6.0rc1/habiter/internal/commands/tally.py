import click
from datetime import datetime

from habiter.internal.utils.consts import HAB_TRACE_FPATH, HAB_DATE_FORMAT
from habiter.internal.utils.messenger import echo_failure, echo_success
from habiter.internal.file.operations import SQLiteDataFileOperations


@click.command(short_help='increment the number of occurrences for some habit(s)')
@click.argument('habits', required=True, nargs=-1)
@click.option('-n', '--num', default=1)
@click.option('-z', '--zero', is_flag=True)
def tally(habits, num, zero):
    # Cast to set to remove possible duplicates
    habits = set(habits)

    with SQLiteDataFileOperations(HAB_TRACE_FPATH) as fop:
        for habit_name in habits:
            fop.cur.execute('SELECT habit_id, curr_tally, total_tally '
                            'FROM habit WHERE habit_name=?',
                            (habit_name,))
            row = fop.cur.fetchone()

            if row is not None:
                if zero and row['curr_tally'] > 0:
                    echo_failure(
                        f"Habit \"{habit_name}\" contains occurrences.")
                    continue
                prev_tally = row['curr_tally']
                curr_tally = row['curr_tally'] + num
                total_tally = row['total_tally'] + num
                is_active = True
                last_updated = datetime.now().strftime(HAB_DATE_FORMAT)

                fop.cur.execute('UPDATE habit SET curr_tally=?, '
                                'total_tally=?, is_active=?, '
                                'last_updated=?, prev_tally=? '
                                'WHERE habit_id = ?',
                                (curr_tally, total_tally, is_active,
                                 last_updated, prev_tally, row['habit_id']))
                echo_success("Habit \"{}\" tally updated from {} to {}."
                             .format(habit_name,
                                     prev_tally,
                                     curr_tally))
            else:
                echo_failure(f"No habit with the name \"{habit_name}\".")
