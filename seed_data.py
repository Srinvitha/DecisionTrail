"""
DecisionTrail demo dataset.

Three interconnected story threads for a fictional company "BuildTrack"
(construction project management SaaS). Each event is a fragment -
no single event states "the decision" outright. The point is that
Hindsight should be able to reconstruct the full decision narrative
from these scattered, dated, tagged fragments.

Threads:
  1. dark_mode           - requested -> estimated -> debated -> postponed
  2. dashboard_perf      - complaints -> investigation -> investor concern -> fix approved
  3. csv_export          - request -> small effort -> approved -> adoption increase
  4. opinion_shift_sarah - one stakeholder's priorities change over 3 months
"""

events = [

    # ============================================================
    # THREAD 1: DARK MODE  (requested -> estimated -> debated -> postponed)
    # ============================================================
    {
        "date": "2026-01-05",
        "thread": "dark_mode",
        "context": "customer_feedback",
        "metadata": {"source": "customer", "stakeholder": "Sarah (Acme Corp)", "department": "customer_success"},
        "content": "Sarah from Acme Corp requested dark mode for BuildTrack, explaining that her site supervisors review dashboards at night and the bright UI causes eye strain during late-shift inspections."
    },
    {
        "date": "2026-01-06",
        "thread": "dark_mode",
        "context": "customer_feedback",
        "metadata": {"source": "customer", "stakeholder": "David (NorthStar Construction)", "department": "customer_success"},
        "content": "David from NorthStar Construction separately asked support whether BuildTrack has a dark theme, saying his team works night shifts on active job sites and finds the current interface too bright."
    },
    {
        "date": "2026-01-08",
        "thread": "dark_mode",
        "context": "engineering_estimate",
        "metadata": {"source": "engineering", "stakeholder": "Rahul (Engineering Lead)", "department": "engineering"},
        "content": "Rahul, the engineering lead, estimated that implementing a full dark mode across BuildTrack's dashboard, reports, and mobile app would take approximately 5 weeks of frontend work, since many components use hardcoded color values."
    },
    {
        "date": "2026-01-10",
        "thread": "dark_mode",
        "context": "internal_discussion",
        "metadata": {"source": "slack", "stakeholder": "Priya (Designer)", "department": "design"},
        "content": "Priya, the product designer, noted in the design channel that dark mode would also require reworking the chart color palette, since the current chart colors don't have enough contrast on dark backgrounds."
    },
    {
        "date": "2026-01-20",
        "thread": "dark_mode",
        "context": "roadmap_meeting",
        "metadata": {"source": "meeting", "stakeholder": "Maria (Head of Product)", "department": "product"},
        "content": "During the roadmap review, Maria, the Head of Product, presented data showing the mobile redesign would impact 40% of active users across all customer segments, compared to dark mode which had been requested by only 2 customers so far."
    },
    {
        "date": "2026-01-22",
        "thread": "dark_mode",
        "context": "leadership_decision",
        "metadata": {"source": "meeting", "stakeholder": "CEO", "department": "leadership"},
        "content": "Leadership decided to postpone dark mode and prioritize the mobile redesign for Q1, citing the 5-week engineering estimate for dark mode and the broader reach of the mobile redesign across the user base."
    },
    {
        "date": "2026-01-22",
        "thread": "dark_mode",
        "context": "leadership_decision",
        "metadata": {"source": "meeting", "stakeholder": "Rahul (Engineering Lead)", "department": "engineering"},
        "content": "Rahul agreed with postponing dark mode, but flagged that the engineering team should revisit it once the mobile redesign's component library is in place, since the new components would make a dark theme much faster to implement."
    },
    {
        "date": "2026-02-15",
        "thread": "dark_mode",
        "context": "customer_feedback",
        "metadata": {"source": "customer", "stakeholder": "Sarah (Acme Corp)", "department": "customer_success"},
        "content": "Sarah from Acme Corp followed up asking for a timeline on dark mode, mentioning that two other site supervisors on her team have started requesting it as well."
    },
    {
        "date": "2026-02-16",
        "thread": "dark_mode",
        "context": "internal_discussion",
        "metadata": {"source": "slack", "stakeholder": "Tom (Account Manager)", "department": "sales"},
        "content": "Tom, the account manager for Acme Corp, mentioned that Acme's contract renewal (worth $120k annually) is coming up in Q2, and dark mode has come up twice in recent calls with their team."
    },

    # ============================================================
    # THREAD 2: DASHBOARD PERFORMANCE
    # (complaints -> investigation -> investor concern -> fix approved)
    # ============================================================
    {
        "date": "2026-01-12",
        "thread": "dashboard_perf",
        "context": "customer_feedback",
        "metadata": {"source": "customer", "stakeholder": "Lisa (Site Manager, Concrete Plus)", "department": "customer_success"},
        "content": "Lisa, a site manager at Concrete Plus, reported that the project dashboard takes 8-10 seconds to load each morning, which is frustrating when she's trying to quickly check overnight equipment alerts before a site meeting."
    },
    {
        "date": "2026-01-14",
        "thread": "dashboard_perf",
        "context": "support_ticket",
        "metadata": {"source": "support", "stakeholder": "support_team", "department": "customer_success"},
        "content": "Support logged three additional tickets this week about slow dashboard load times, all from customers with large numbers of active projects (50+ projects per account)."
    },
    {
        "date": "2026-01-16",
        "thread": "dashboard_perf",
        "context": "engineering_investigation",
        "metadata": {"source": "engineering", "stakeholder": "Aisha (Backend Engineer)", "department": "engineering"},
        "content": "Aisha investigated the dashboard slowness and found the root cause: the summary view runs an unindexed aggregation query across all project tasks every time the dashboard loads, which scales poorly for accounts with many projects."
    },
    {
        "date": "2026-01-17",
        "thread": "dashboard_perf",
        "context": "engineering_estimate",
        "metadata": {"source": "engineering", "stakeholder": "Aisha (Backend Engineer)", "department": "engineering"},
        "content": "Aisha estimated that fixing the dashboard performance issue by adding proper indexes and caching the aggregation results would take about 1.5 weeks, much less than the dark mode work."
    },
    {
        "date": "2026-01-25",
        "thread": "dashboard_perf",
        "context": "data_analysis",
        "metadata": {"source": "internal_report", "stakeholder": "Maria (Head of Product)", "department": "product"},
        "content": "Maria's analysis of usage data showed that 32% of active accounts have 50 or more projects and are therefore experiencing the slow dashboard load times described in support tickets."
    },
    {
        "date": "2026-02-02",
        "thread": "dashboard_perf",
        "context": "investor_meeting",
        "metadata": {"source": "investor", "stakeholder": "Investor (Northbridge Ventures)", "department": "leadership"},
        "content": "During the monthly investor update, a partner from Northbridge Ventures raised concerns about retention risk, specifically pointing out that performance issues on core workflows like the dashboard should be prioritized over new visual features, since slow tools are a common churn driver in construction software."
    },
    {
        "date": "2026-02-04",
        "thread": "dashboard_perf",
        "context": "leadership_decision",
        "metadata": {"source": "meeting", "stakeholder": "CEO", "department": "leadership"},
        "content": "Following the investor feedback and the support ticket data, leadership approved the dashboard performance fix to be scheduled immediately, ahead of other minor feature work, given the relatively small 1.5-week estimate and the retention risk identified by Northbridge Ventures."
    },
    {
        "date": "2026-02-10",
        "thread": "dashboard_perf",
        "context": "engineering_update",
        "metadata": {"source": "engineering", "stakeholder": "Aisha (Backend Engineer)", "department": "engineering"},
        "content": "Aisha shipped the dashboard performance fix; load times for accounts with 50+ projects dropped from 8-10 seconds to under 1 second after the new caching layer and indexes went live."
    },
    {
        "date": "2026-02-12",
        "thread": "dashboard_perf",
        "context": "customer_feedback",
        "metadata": {"source": "customer", "stakeholder": "Lisa (Site Manager, Concrete Plus)", "department": "customer_success"},
        "content": "Lisa from Concrete Plus emailed support to say the dashboard now loads instantly and thanked the team, noting it's made her morning routine much smoother."
    },

    # ============================================================
    # THREAD 3: CSV EXPORT  (request -> small effort -> approved -> adoption increase)
    # ============================================================
    {
        "date": "2026-01-09",
        "thread": "csv_export",
        "context": "customer_feedback",
        "metadata": {"source": "customer", "stakeholder": "James (Operations Director, FinEdge Builders)", "department": "customer_success"},
        "content": "James, operations director at FinEdge Builders, requested the ability to export project task lists to CSV, explaining that his finance team needs to import task data into their existing budgeting spreadsheets and currently has to copy data manually from screenshots."
    },
    {
        "date": "2026-01-11",
        "thread": "csv_export",
        "context": "internal_discussion",
        "metadata": {"source": "slack", "stakeholder": "Tom (Account Manager)", "department": "sales"},
        "content": "Tom mentioned that two other prospects in recent sales calls also asked about CSV export, specifically for integrating BuildTrack data with their accounting software."
    },
    {
        "date": "2026-01-13",
        "thread": "csv_export",
        "context": "engineering_estimate",
        "metadata": {"source": "engineering", "stakeholder": "Rahul (Engineering Lead)", "department": "engineering"},
        "content": "Rahul estimated that adding a CSV export button for the task list view would take roughly 2 days, since the data is already structured and just needs a serialization endpoint."
    },
    {
        "date": "2026-01-15",
        "thread": "csv_export",
        "context": "leadership_decision",
        "metadata": {"source": "meeting", "stakeholder": "Maria (Head of Product)", "department": "product"},
        "content": "Maria approved the CSV export feature for the next sprint, noting it was a low-effort, high-value request that didn't compete for the same engineering resources as the dark mode or dashboard performance work."
    },
    {
        "date": "2026-01-23",
        "thread": "csv_export",
        "context": "engineering_update",
        "metadata": {"source": "engineering", "stakeholder": "Rahul (Engineering Lead)", "department": "engineering"},
        "content": "Rahul's team shipped CSV export for task lists, available from the project dashboard's export menu."
    },
    {
        "date": "2026-02-20",
        "thread": "csv_export",
        "context": "data_analysis",
        "metadata": {"source": "internal_report", "stakeholder": "Maria (Head of Product)", "department": "product"},
        "content": "Usage analytics showed CSV export was used by 28% of active accounts within its first month, and accounts that used it at least once showed a noticeably higher weekly login rate than accounts that didn't."
    },
    {
        "date": "2026-02-22",
        "thread": "csv_export",
        "context": "customer_feedback",
        "metadata": {"source": "customer", "stakeholder": "James (Operations Director, FinEdge Builders)", "department": "customer_success"},
        "content": "James from FinEdge Builders told the account manager that CSV export has become a core part of his team's weekly reporting workflow, and asked whether a scheduled/automatic export could be considered in the future."
    },

    # ============================================================
    # OPINION SHIFT: Sarah's stance changes over time
    # (Jan: dark mode is urgent -> Mar: performance matters more)
    # ============================================================
    {
        "date": "2026-01-05",
        "thread": "opinion_shift_sarah",
        "context": "customer_feedback",
        "metadata": {"source": "customer", "stakeholder": "Sarah (Acme Corp)", "department": "customer_success"},
        "content": "Sarah from Acme Corp told her account manager that dark mode is urgently needed for her night-shift supervisors and that it's currently her team's top complaint about BuildTrack."
    },
    {
        "date": "2026-02-18",
        "thread": "opinion_shift_sarah",
        "context": "support_ticket",
        "metadata": {"source": "support", "stakeholder": "Sarah (Acme Corp)", "department": "customer_success"},
        "content": "Sarah opened a support ticket complaining that the dashboard has become slow to load for her team's larger projects, and asked when this would be addressed."
    },
    {
        "date": "2026-03-10",
        "thread": "opinion_shift_sarah",
        "context": "customer_feedback",
        "metadata": {"source": "customer", "stakeholder": "Sarah (Acme Corp)", "department": "customer_success"},
        "content": "In a quarterly check-in call, Sarah told the account manager that while dark mode would still be nice, dashboard performance and reliability matter more to her team right now, since several supervisors had been frustrated by slow load times during busy periods."
    },

    # ============================================================
    # CROSS-THREAD: a later event that ties dark mode back into play
    # ============================================================
    {
        "date": "2026-03-01",
        "thread": "dark_mode",
        "context": "roadmap_meeting",
        "metadata": {"source": "meeting", "stakeholder": "Maria (Head of Product)", "department": "product"},
        "content": "With the mobile redesign's new component library now in place and the dashboard performance issue resolved, Maria proposed revisiting dark mode for the Q2 roadmap, referencing Tom's earlier note about Acme Corp's upcoming renewal and continued customer requests."
    },
]


if __name__ == "__main__":
    print(f"Total events: {len(events)}")
    threads = {}
    for e in events:
        threads.setdefault(e["thread"], 0)
        threads[e["thread"]] += 1
    for t, c in threads.items():
        print(f"  {t}: {c} events")