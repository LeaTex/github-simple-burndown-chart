
from github import Github
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as tck 

def get_sp_from_issue(issue):
    return sum([int(label.name[:-3]) for label in issue.get_labels() if label.name.endswith(" SP")])

g = Github()
#g = Github("ghp_your_access_token_here")

repo = g.get_repo("LeaTex/github-simple-burndown-chart")

#open_milestones = repo.get_milestones(state='open')

# selected milestone
sprint_milestone = repo.get_milestone(1)
print(sprint_milestone.title)

# sprint duration
sprint_days = 7

sprint_end_date = sprint_milestone.due_on
sprint_start_date = sprint_end_date - timedelta(days=sprint_days)
print("from {} to {}".format(str(sprint_start_date.date()), str(sprint_end_date.date())))

sprint_issues = repo.get_issues(milestone=sprint_milestone, state='all')
print("issues", sprint_issues.totalCount)

sprint_sps = sum([get_sp_from_issue(issue) for issue in sprint_issues])
print("story points del sprint:", sprint_sps)

sprint_dates = [str((sprint_start_date + timedelta(days=x)).date()) for x in range(sprint_days+1)]
print(sprint_dates)
# sprint_dates = {str((sprint_start_date + timedelta(days=x)).date()) : sprint_sps for x in range(sprint_days+1)}
# print(sprint_dates.items())

sp_per_day = round(sprint_sps / sprint_days, 2)
ideal_burndown = [round(sprint_sps - (sp_per_day * d), 2) for d in range(sprint_days+1)]

actual_burndown = []
burned = 0
for date in sprint_dates:
    for issue in sprint_issues:
        if issue.closed_at and str(issue.closed_at.date()) == date:
            burned += get_sp_from_issue(issue)
    actual_burndown.append(sprint_sps-burned)

plt.plot(sprint_dates, ideal_burndown, 'o-.', label='ideal')
plt.plot(range(len(actual_burndown)), actual_burndown, 'd-', label='quemados')
plt.title(sprint_milestone.title + ' - Burndown Chart')

plt.ylabel('SPs')
plt.gca().yaxis.set_major_locator(tck.MultipleLocator(1))

plt.axis([0, sprint_days, 0, sprint_sps + 1])
plt.xlabel('Dates')
plt.xticks(fontsize=8, rotation=30)

plt.legend()
plt.grid(linestyle='--', linewidth=0.5, alpha=0.5)
plt.grid(True)
plt.show()
#plt.savefig(sprint_milestone.title.strip().lower().replace(' ', '_') + '_burndown.png')