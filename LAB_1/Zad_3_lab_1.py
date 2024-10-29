#proceduralnie
# def optimizeTasksProcedural(tasks):
#     tasks.sort(key = lambda x: -x['reward'] / x['time'])
#     totalReward = 0
#     totalTime = 0
#     totalOrder = []
#
#     for task in tasks:
#         totalOrder.append(task['number'])
#         totalTime += task['time']
#         totalReward += task['reward']
#
#     return totalReward, totalOrder
#
# taskList = [
#     {'number': 1, 'time': 3, 'reward': 10},
#     {'number': 2, 'time': 2, 'reward': 5},
#     {'number': 3, 'time': 1, 'reward': 8},
#     {'number': 4, 'time': 4, 'reward': 7}
# ]
#
# print(optimizeTasks(taskList))

def optimizeTasksFunctional(tasks):
    keyFunc = lambda x: -x['reward'] / x['time']
    sortedTasks = sorted(tasks, key=keyFunc)
    totalReward = sum(map(lambda task : task ['reward'], sortedTasks))

    return totalReward, sortedTasks

taskList = [
    {'number': 1, 'time': 3, 'reward': 10},
    {'number': 2, 'time': 2, 'reward': 5},
    {'number': 3, 'time': 1, 'reward': 8},
    {'number': 4, 'time': 4, 'reward': 7}
]

print(optimizeTasksFunctional(taskList))