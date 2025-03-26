import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import pulp
from matplotlib import collections as mc

# test cases
# index, selected, facilities, customers
#         n se fa cu
cases = [(0, 4, 5, 3),
         (1, 4 ,3 ,3),
         (2, 4, 3, 5),
         (3, 2, 3, 5),
         (4, 3, 3, 5),
         (5, 9, 7, 3),
         (6, 16, 9, 3),
         (7, 16, 11, 3),
         (8, 16, 8, 3),
         (9, 16, 8, 4),
         (10, 9, 9, 4),
         (11, 4, 11, 3),
         (12, 12, 9, 4),
         (13, 8, 9, 4),
         (14, 8, 11, 6), # too long
         (15, 8, 9, 6), # too long
         ]

selectTest = 0
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
initial_facilities = []
for i in range(side_n_facilities): 
    for j in range(side_n_facilities): 
        x = (j * facility_square_size) + (facility_square_size/ 2) 
        y = (i * facility_square_size) + (facility_square_size/ 2) 
        initial_facilities.append([x,y]) 
initial_facilities = np.array(initial_facilities) 

# Calculate distances between customers and facilities 
distances = cdist(customers, initial_facilities) 

# Create the optimization problem 
prob = pulp.LpProblem("Facility Assignment", pulp.LpMaximize)
               

# Decision variables 

 
# a[i,j] = 1 if customer i is assigned to facility j 
a = pulp.LpVariable.dicts("assign", 
    ((i, j) for i in range(len(customers)) 
    for j in range(len(initial_facilities))), 
    lowBound=0)

x_binary = True 
if x_binary: 
    x = pulp.LpVariable.dicts("select",
        ( (j) for j in range(len(initial_facilities))), 
        cat='Binary')                    
else: 
    x = pulp.LpVariable.dicts("select",
        ( (j) for j in range(len(initial_facilities))), 
        lowBound=0, upBound=1)                 

# Minimum score variable to maximize 
min_score = pulp.LpVariable("min_score") 

# Objective: Maximize the minimum score 
prob += min_score 

# Constraints 
# Each customer must be assigned to exactly one facility 
for i in range(len(customers)): 
    prob += pulp.lpSum(a[i,j] for j in range(len(initial_facilities)) )  == 1

# For each customer and each pair of facilities, if customer is assigned to facility j, 
# the distance difference to other facilities must be at least min score 
do_minimax = True
if do_minimax:
    max_possible = num_customers / num_selected
    for j in range(len(initial_facilities)):
        for k in range(len(initial_facilities)):
            if j == k:
                continue
            score = 0
            for i in range(len(customers)):
                jcloser = distances[i,k] - distances[i,j] > 0
                if jcloser:
                    score += a[i,j]
                    # if j is closer, than assigning to j will increase j' s score against k
            prob += min_score <= score + (1 - x[j]) * max_possible
            # j's score agains k
else:
    max_possible = (num_facilities - 1) * num_customers / num_selected
    for j in range(len(initial_facilities)):
        score = 0
        for k in range(len(initial_facilities)):
            if j == k:
                continue
            for i in range(len(customers)):
                jcloser = distances[i,k] - distances[i,j] > 0
                if jcloser:
                    score += a[i,j]
                    # if j is closer, than assigning to j will increase j' s score against k
        prob += min_score <= score + (1 - x[j]) * max_possible
        # j's borda score


# Each facility is limited to an equal amount of customers 
for j in range(len(initial_facilities)):
    prob += pulp.lpSum(a[i,j] for i in range(len(customers))) <= num_customers / num_selected





# Only selected facilities have customers 
for i in range(len(customers)): 
    for j in range(len(initial_facilities)): 
        prob += a[i,j] <= x[j]

prob += pulp.lpSum(x[j] for j in range(len(initial_facilities)) ) <= num_selected

# Solve the problem 
prob.solve() 
print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Optimal minimum score: {pulp.value(min_score)}")

# Get assignments 

chosen  = [pulp.value(x[j]) for j in range(len(initial_facilities))] 
sf = [idx for idx, v in enumerate(chosen) if v] 

# Plot results 
nsf = len(sf) 
npl = nsf+4 

plt.figure(figsize=(18,3))

# Plot facilities 
# no tick marks
ax = plt.subplot(1, npl, 1, xticks=[], yticks=[]) 
plt.axis( 'equal') 
plt.scatter(initial_facilities[:,0], initial_facilities[:,1],
    color='grey', s = 10, marker='*', label="Facilities")
plt.scatter(initial_facilities[sf,0], initial_facilities[sf,1],
    color='red', s = 100, marker='*', label="Facilities")

# Plot customer assignments with different colors 
# colors = plt.cm.rainbow(np.linspace(0,1,len(initial_facilities)))
# for i in range(len(initial_facilities)): 
#     mask = assignments == i
#     plt.scatter(np.array(customer_x)[mask], np.array(customer_y)[mask], 
#         color=colors[i], s=100, alpha=0.5, label=f' Facility {i} customers')
    
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
    for j, fac in enumerate(initial_facilities): 
        if np.all(cust == fac): 
            continue 
        aval = pulp.value(a[i,j]) 
        if aval > 0: 
            lines.append((cust, fac)) 
            alphas.append(aval) 
lines = np.array(lines) 
alphas = np.array(alphas) 
lc = mc.LineCollection(lines, alpha=alphas) 
ax.add_collection(lc) 

assigners = np.zeros((len(customers),len(initial_facilities)) ) 
for i in range(len(customers)): 
    for j in range(len(initial_facilities)): 
        assigners[i,j] = pulp.value(a[i,j])

# check constraints 
plt.subplot(1, npl, 2, xticks=[], yticks=[]) 
plt.imshow(np.sum(assigners,axis=0).reshape(side_n_facilities,side_n_facilities))
plt.title("Fa") 

plt.subplot(1, npl, 3, xticks=[], yticks=[]) 
plt.imshow(np.sum(assigners,axis=1).reshape(side_n_customers,side_n_customers),clim=(0,2))
plt.title("Cu") 

for i in range(nsf): 
    sfi = sf[i]
    plt.subplot(1,npl,i+4,xticks=[],yticks=[])
    plt.imshow(assigners[:,sfi].reshape(side_n_customers,side_n_customers),clim=(0,1),extent=(0,1,1,0))
    x = initial_facilities[sfi,0]
    y = initial_facilities[sfi,1]
    plt.scatter(x,y,color='black')
    plt.title(f"F {sfi}")

best = 100 * pulp.value(min_score) / max_possible
print(f"{round(best,1)} %")

plt.show()

print("done")