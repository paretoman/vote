# %% Import
import numpy as np
import matplotlib.pyplot as plt
# from scipy.spatial.distance import cdist
import pulp
from matplotlib import collections as mc
import cvxpy as cvx

# 
# Geometry Definition
# test cases
# index, selected, facilities, customers
#         n se fa cu
cases = [(0, 4, 5, 3),
         (1, 4 ,3 ,3),
         (2, 4, 3, 5),
         (3, 2, 3, 5),
         (4, 3, 3, 5),
         (5, 9, 7, 3), # nice
         (6, 16, 9, 3),
         (7, 16, 11, 3),
         (8, 16, 8, 3),
         (9, 16, 8, 4),
         (10, 9, 9, 4),
         (11, 4, 11, 3),
         (12, 12, 9, 4), # cool
         (13, 8, 9, 4),
         (14, 8, 11, 6), # now possible
         (15, 8, 9, 6), 
         (16, 5, 5, 3), # good
         (17, 5, 9, 6),
         (18, 8, 9, 9),
         (19, 2, 9, 9), # shape
         ]

selectTest = 19
(_,ts,tf,tc) = cases[selectTest]

num_selected = ts
side_n_facilities = tf
side_n_customers = tc
facility_square_size = 1/side_n_facilities
num_facilities = side_n_facilities ** 2

# Generate customer grid points 
customer_x = []
customer_y = []
for i in range(side_n_customers): 
    for j in range(side_n_customers): 
        x = (j/side_n_customers) + (1/ (2* side_n_customers)) 
        y = (i/side_n_customers) + (1/ (2* side_n_customers)) 
        customer_x.append(x) 
        customer_y.append(y) 

customers = np.column_stack((customer_x, customer_y) ) 

num_customers = side_n_customers ** 2

# Initial facility positions 
facilities = []
for i in range(side_n_facilities): 
    for j in range(side_n_facilities): 
        x = (j * facility_square_size) + (facility_square_size/ 2) 
        y = (i * facility_square_size) + (facility_square_size/ 2) 
        facilities.append([x,y]) 
facilities = np.array(facilities) 

# Calculate distances between customers and facilities 
# distances = cdist(customers, facilities) 
distances = np.zeros((num_customers,num_facilities))
for i in range(num_customers): 
    for j in range(num_facilities): 
        distances[i,j] = np.sum((customers[i] - facilities[j])**2)

# Problem Definition

# Define the variables
a = cvx.Variable(num_customers)
min_score = cvx.Variable()


# Parameters
u = cvx.Parameter(num_customers, nonneg=True)
b = cvx.Parameter((num_customers,num_facilities), nonneg=True)

# Objective
# obj = cvx.Minimize(cvx.norm2(a @ (1-b)))
obj = cvx.Minimize(cvx.log_sum_exp(.1 * a @ (1-b)))
# use an extra term to spread support
# obj = cvx.Maximize(cvx.min(a @ b) + .1 * (cvx.sum(a) - cvx.sum(a**2)))

# Constraints
constraints = [
    0 <= a,
    a <= 1 - u,
    cvx.sum(a) == num_customers / num_selected
]
constraints_final = [
    a == 1 - u
]

prob = cvx.Problem(obj,constraints)

# Solve Problem

# keep track of satisfied customersa and chosen facilities
used = np.zeros(num_customers)
facilities_remaining = list(np.arange(num_facilities)) # 0 to n-1
winners = []
winnerScores = []
assignment = np.zeros((num_customers,num_facilities))

for round_count in range(num_selected):
    scores = np.zeros(num_facilities)
    ayes = np.zeros((num_customers,num_facilities))
    u.value = used
    if round_count == num_selected - 1: # final round
        prob = cvx.Problem(obj,constraints_final)
    for j in facilities_remaining:
        prefs = distances[:,[j]] <= distances
        b.value = prefs * 1
        prob.solve()
        if (prob.status != "optimal"):
            print(prob.status)
        scores[j] = prob.value
        ayes[:,j] = a.value
    
    # compare all scores and find the index of the largest
    largest_of_remaining = np.argmin(scores[facilities_remaining])
    winner = facilities_remaining[largest_of_remaining]
    del facilities_remaining[largest_of_remaining]
    
    # store the facility in a list of winners
    winners.append(winner)
    winnerScores.append(scores[winner])
    assignment[:,winner] = ayes[:,winner]
    used = used + assignment[:,winner]
    used = np.minimum(used,1)
    used = np.maximum(used,0)
    
    max_possible = num_customers / num_selected
    best = 100 * scores[winner] / max_possible
    print(winner, round(scores[winner],6),f"{round(best,1)} %")


# Output


# Plot results 
n_winners = len(winners) 
npl = n_winners+4 

plt.style.use("dark_background")
plt.figure(figsize=(12,3))

# Plot facilities 
# no tick marks
ax = plt.subplot(1, npl, 1, xticks=[], yticks=[]) 
plt.axis( 'equal') 
plt.scatter(facilities[:,0], facilities[:,1],
    color='grey', s = 10, marker='*', label="Facilities")
plt.scatter(facilities[winners,0], facilities[winners,1],
    color='red', s = 100, marker='*', label="Facilities")

plt.scatter(np.array(customer_x), np.array(customer_y), 
        color='grey', s=100, alpha=0.5, label=f' Facility {i} customers')

plt.xlim(0,1)
plt.ylim(0,1)
# plt.title( 'Optimal Customer Assignment to Facilities') 
plt.title("Cu & Fa" ) 
ax.invert_yaxis() 

lines = []
alphas = []
for i, cust in enumerate(customers): 
    for j, fac in enumerate(facilities): 
        if np.all(cust == fac): 
            continue 
        aval = assignment[i,j] 
        if aval > 0: 
            lines.append((cust, fac)) 
            alphas.append(aval) 
lines = np.array(lines) 
alphas = np.array(alphas) 
alphas = np.round(alphas,2)
lc = mc.LineCollection(lines, alpha=alphas) 
ax.add_collection(lc) 

# check constraints 
plt.subplot(1, npl, 2, xticks=[], yticks=[]) 
plt.imshow(np.sum(assignment,axis=0).reshape(side_n_facilities,side_n_facilities))
plt.title("Fa") 

plt.subplot(1, npl, 3, xticks=[], yticks=[]) 
plt.imshow(np.sum(assignment,axis=1).reshape(side_n_customers,side_n_customers),clim=(0,2))
plt.title("Cu") 

for i in range(n_winners): 
    winner = winners[i]
    plt.subplot(1,npl,i+4,xticks=[],yticks=[])
    plt.imshow(assignment[:,winner].reshape(side_n_customers,side_n_customers),clim=(0,1),extent=(0,1,1,0))
    x = facilities[winner,0]
    y = facilities[winner,1]
    plt.scatter(x,y,color='black')
    plt.title(f"F {winner}")

max_possible = num_customers / num_selected
best = 100 * min(winnerScores) / max_possible
print(f"{round(best,1)} %")

plt.show()

print("done")
# %%
