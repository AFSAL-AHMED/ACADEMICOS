"""
log.py — Daily Learning Journal CLI
Run this every day to log your progress to Notion.

Usage:
  python log.py           → Add today's log (interactive)
  python log.py today     → View today's entry
  python log.py week      → View last 7 days
  python log.py stats     → View all-time stats
  python log.py topic     → Search by topic
"""

import sys
from server import (
    add_learning_log,
    get_todays_log,
    list_recent_logs,
    get_stats,
    search_logs_by_topic,
)

DIVIDER = "=" * 45
TOPICS  = ["Programming", "AI / ML", "Web Dev", "Math / DSA", "DevOps", "Reading", "Soft Skills", "Other"]
MOODS   = ["Fired Up", "Good", "Okay", "Tired"]


def pick_from_list(prompt, options):
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        choice = input("Enter number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("  Invalid choice. Try again.")


def interactive_log():
    print(f"\n{DIVIDER}")
    print("   📖 DAILY LEARNING JOURNAL")
    print(f"{DIVIDER}")
    print("Let's log what you learned today!\n")

    day_title     = input("Day title (e.g. 'Day 2 — Python OOP'): ").strip()
    topic         = pick_from_list("What did you study?", TOPICS)
    hours_input   = input("How many hours? (e.g. 1.5): ").strip()
    hours_spent   = float(hours_input) if hours_input else 1.0
    mood          = pick_from_list("How was your mood?", MOODS)
    key_takeaways = input("\nKey Takeaways (what you learned): ").strip()
    resources     = input("Resources used (books, videos, links): ").strip()
    tmr_goal      = input("Tomorrow's goal: ").strip()
    streak_input  = input("Streak day # (e.g. 2): ").strip()
    streak_day    = int(streak_input) if streak_input.isdigit() else 1

    print("\nSaving to Notion...")
    result = add_learning_log(
        day_title=day_title,
        topic=topic,
        hours_spent=hours_spent,
        mood=mood,
        key_takeaways=key_takeaways,
        resources_used=resources,
        tomorrows_goal=tmr_goal,
        streak_day=streak_day,
    )
    print(f"\n{result}")
    print(f"\n{DIVIDER}")
    print("Keep going! See you tomorrow. 🚀")
    print(f"{DIVIDER}\n")


def main():
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "add"

    if cmd == "today":
        print(get_todays_log())

    elif cmd == "week":
        print(list_recent_logs(7))

    elif cmd == "stats":
        print(get_stats())

    elif cmd == "topic":
        t = input("Enter topic to search: ").strip()
        print(search_logs_by_topic(t))

    else:
        # default — interactive add
        interactive_log()


if __name__ == "__main__":
    main()
