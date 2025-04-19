# %% 
# Shape of Assignment
import numpy as np
import cvxpy as cvx
import matplotlib.pyplot as plt

# Geometry Definition

#         n select num_on_side
cases = [(3, 13), # 0 perfect
         (1.6, 13), # 1 cool pattern
         (2, 13), # 2 
         (18, 13), # 3 
         ]
test_num = 3
(num_selected, num_on_side) = cases[test_num]

num_points = num_on_side ** 2
quota = num_points / num_selected

# Points
points = []
h = int((num_on_side - 1) / 2)
for i in range(num_on_side): 
    for j in range(num_on_side): 
        points.append([j,i]) 
        # points.append([j-h,i-h]) 
points = np.array(points) 

map_scale = lambda p: [(p[0] + 0.5) / num_on_side, (p[1] + 0.5) / num_on_side]

# not sure
# map_scale = lambda p: [(p[0]) / num_on_side + .5, (p[1]) / num_on_side + .5]



# Calculate distances between points
distances = np.zeros((num_points,num_points))
for i in range(num_points): 
    for j in range(num_points): 
        distances[i,j] = np.sum((points[i] - points[j])**2)

middle = int(np.round(num_points / 2))
if num_points % 2 == 0:
    middle = int(middle - num_on_side * 0.5 - 1)
# preferences = 1 * (distances[:,[middle]] <= distances )
# preferences = 2 * (distances[:,[middle]] < distances ) + 1 * (distances[:,[middle]] == distances )
preferences = 1 * (distances[:,[middle]] < distances ) - 1 * (distances[:,[middle]] > distances ) 

# Problem Definition

# Define the variables
a = cvx.Variable(num_points)
b = preferences # b for ballot, or better
w = 1 - preferences # worse
# g = cvx.Parameter()

# Objective
# a @ b is how many voters prefer us to each candidate
obj = cvx.Minimize(cvx.norm2(a @ w))
# obj = cvx.Minimize(cvx.sum(a @ w))
# obj = cvx.Minimize(cvx.norm(a @ w,10))
# obj = cvx.Minimize(cvx.norm(a @ w,'inf'))
# obj = cvx.Minimize(cvx.log_sum_exp(1.5 * a @ w))
# obj = cvx.Minimize(cvx.log_sum_exp(g * a @ w))
# use an extra term to spread support
# obj = cvx.Maximize(cvx.min(a @ b) + .1 * (cvx.sum(a) - cvx.sum(a**2)))
# obj = cvx.Maximize(cvx.min(a @ b))

# Constraints
constraints = [
    a >= 0,
    a <= 1,
    cvx.sum(a) == quota
]

prob = cvx.Problem(obj,constraints)

#

# g.value = .01

# Solve Problem

prob.solve()
if (prob.status != "optimal"):
    print(prob.status)
score = prob.value
assignment = a.value
    
    
max_possible = quota
best = 100 * score / max_possible
print(round(score,6),f"{round(best,1)} %")

# Output


# Plot results
plt.style.use("dark_background")

# Plot points 
plt.subplot(1,1,1,xticks=[],yticks=[])
plt.imshow(assignment.reshape(num_on_side,num_on_side),clim=(0,1),extent=(0,1,1,0))
x,y = map_scale(points[middle,:])
plt.scatter(x,y,color='black')
plt.title("Assignment")

plt.show()


# %%

# sanity check

plt.subplot(1,1,1,xticks=[],yticks=[])
pt = 32
plt.imshow(preferences[:,pt].reshape(num_on_side,num_on_side),clim=(0,1),extent=(0,1,1,0))
x,y = map_scale(points[pt])
plt.scatter(x,y,color='black')
plt.title("Preference Versus One")

plt.show()


print("done")

# %%

# tricky array indexing
a = [[1, 2], [3, 4]]
a = np.array(a)
print(a[:,0])
print(a[:,[0]])
print(a[0,:])
print(a[[0],:])


# %%


plt.subplot(1,1,1,xticks=[],yticks=[])
plt.imshow(np.sum(preferences,axis=0).reshape(num_on_side,num_on_side),extent=(0,1,1,0))
plt.colorbar()
x,y = map_scale(points[middle,:])
plt.scatter(x,y,color='black')
plt.title("Votes for us versus other Candidate at Point")
# there is an edge effect that shows up throughout

plt.show()


print("done")
# %%

plt.subplot(1,1,1,xticks=[],yticks=[])
offset = 5 + 13 * 5
offset = 1 + 13 * 1
# don't let the dark circles overlap
# plt.imshow(np.sum(preferences[[middle+offset,middle-offset],:],axis=0).reshape(num_on_side,num_on_side),extent=(0,1,1,0))
plt.imshow((assignment @ preferences).reshape(num_on_side,num_on_side),extent=(0,1,1,0))
plt.colorbar()
x,y = map_scale(points[middle,:])
plt.scatter(x,y,color='white')
plt.title("Votes for us versus other Candidate at Point")
# there is an edge effect that shows up throughout

plt.show()


# %%
