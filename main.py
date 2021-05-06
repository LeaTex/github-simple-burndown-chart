
from github import Github
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

#g = Github("ghp_your_access_token_here")
g = Github()

repo = g.get_repo("LeaTex/github-simple-burndown-chart")

#open_milestones = repo.get_milestones(state='open')

# selected milestone
sprint_milestone = repo.get_milestone(1)

# sprint duration
sprint_days = 7

sprint_end_date = sprint_milestone.due_on
sprint_start_date = sprint_end_date - timedelta(days=sprint_days)
print("from {} to {}".format(str(sprint_start_date.date()), str(sprint_end_date.date())))

sprint_issues = repo.get_issues(milestone=sprint_milestone)
print("issues", sprint_issues.totalCount)

sprint_sps = sum([int(label.name[:-3]) for issue in sprint_issues for label in issue.get_labels() if label.name.endswith(" SP")])
print("story points del sprint:", sprint_sps)

sp_per_day = round(sprint_sps / sprint_days, 2)

ideal_burndown = [round(sprint_sps - (sp_per_day * d), 2) for d in range(sprint_days+1)]
actual_burndown = [sprint_sps,18,15,15,7,2,2,2]

plt.plot(range(sprint_days+1),ideal_burndown, 'o-.', label='ideal')
plt.plot(range(len(actual_burndown)),actual_burndown, 'd-', label='quemados')
plt.title('burndown chart')
plt.ylabel('sps')
plt.axis([0, sprint_days, 0, sprint_sps + 2])
plt.xlabel('days')
plt.legend()
plt.grid(linestyle='--', linewidth=0.5, alpha=0.5)
plt.grid(True)
plt.show()
#plt.savefig("sprint1_burndown.png")