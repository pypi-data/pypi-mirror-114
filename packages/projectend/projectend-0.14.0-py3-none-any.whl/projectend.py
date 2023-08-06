import codecs
import os
from datetime import timedelta

import click
import toml
from intervaltree import IntervalTree


def get_effort(tasks):
    effort = 0
    for task in tasks:
        effort += task["effort"]
    return effort


def date_key(date):
    return date.strftime("%Y%m%d")


def make_optional_set(data, key):
    data = data.get(key)
    if data:
        data = set(data)
    else:
        data = set()
    return data


def get_resource_intervals(resources):
    intervals = IntervalTree()
    for resource in resources:
        assert "name" in resource
        from_ = resource["from"]
        to_ = resource["to"]
        resource["exceptions"] = make_optional_set(resource, "exceptions")
        resource["weekdays"] = make_optional_set(resource, "weekdays")
        intervals[from_:to_] = resource
    return intervals


def get_freedays(freedays):
    ret = set()
    for freeday in freedays:
        key = date_key(freeday["date"])
        ret.add(key)
    return ret


def is_weekend(date):
    return date.weekday() in [5, 6]


def day_name(date):
    return date.strftime("%a")


def get_week(date):
    return date.isocalendar()[1]


def is_active(day, days):
    if not days:
        return True
    if day.weekday() in days:
        return True
    return False


def simulate(verbose, project, effort, intervals, freedays):
    print(f"Simulating project: {project['name']}\n")
    day = project["start"]
    i = 0
    delta_day = timedelta(hours=24)
    workday = project["workday"]
    first = True
    last_week = get_week(day) - 1
    while effort > 0 and i < 1000:
        week = get_week(day)
        i += 1
        old_effort = effort
        usings = []
        if not (is_weekend(day) or date_key(day) in freedays):
            for resource in intervals[day]:
                resource = resource.data
                exceptions = resource["exceptions"]
                hours = resource["hours"]
                if day not in exceptions and is_active(day, resource["weekdays"]):
                    if verbose:
                        res_name = resource["name"]
                        usings.append(
                            f"    Using {hours:7.1f} hours from {res_name:>17}"
                        )
                    effort -= hours
        if old_effort != effort:
            if week != last_week:
                if not first:
                    print("")
                print(f"Week {week:2d}")
            first = False
            name = day_name(day)
            days = effort / workday
            report = f"{name} {day} {days:6.1f} days ({round(effort):6d} hours) left"
            print(report)
            if verbose:
                for using in usings:
                    print(using)
                if os.isatty(1):
                    print("━" * len(report))
                else:
                    print("-" * len(report))
            last_week = week
        day += delta_day
    if effort > 0:
        print("\nReached limit without achieving the goal")
        print(f"{day} {effort/24:.1f} days ({round(effort)} hours) left")
    else:
        print(f"\nThe project ends on {day - delta_day}")


def run(verbose, project, freedays):
    effort = get_effort(project["tasks"])
    intervals = get_resource_intervals(project["resources"])
    freedays = get_freedays(freedays)
    simulate(verbose, project, effort, intervals, freedays)


@click.command()
@click.option("--verbose/--no-verbose", default=False)
@click.argument("project-description", type=click.Path(exists=True, readable=True))
def cmd(verbose, project_description):
    """calculate the end of projects.

    PROJECT_DESCRIPTION       See example.toml"""
    with codecs.open(project_description, "r", encoding="UTF-8") as f:
        t = toml.load(f)
        run(verbose, t["project"], t["freedays"])


if __name__ == "__main__":
    cmd()
