import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

data = [
    [0, 0, 0, 0, 0, 3, 0],
    [4, 0, 0, 3, 4, 4, 3],
    [5, 5, 0, 3, 4, 4, 3],
    [5, 5, 1, 1, 5, 5, 3],
    [5, 5, 2, 0, 5, 5, 5]
]

# Plotting heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(data, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Portfolio Heatmap')

plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Automation \nLevel', 'Release \nFrequency', 'Failure\n Rate', 'Monitoring & \nLogging', 'IaC','Security \nPractices','Scalability'],rotation=0)
plt.xlabel('Pipeline Maturity Parameters')

plt.yticks([0, 1, 2, 3, 4], ['CRM', 'Browse \n And Shop', 'Self \n Service', 'Supplier\n(Front-end)', 'Supplier\n(Back-end)'],rotation=0)
plt.ylabel('Portfolios')
plt.show()