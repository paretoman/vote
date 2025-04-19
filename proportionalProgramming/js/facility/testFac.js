import { calculatePreferences2 } from "./calculatePreferences2.js";
// import { solveMyLP } from "./solveMyLP.js";
import { solveLP } from "./solveLP.js";
// import { solveSCS } from "./solveSCS.js";


// Geometry Definition
const cases = [
    [2, 13], // 0
    [2, 3], // 1
]; 
const selectTest = 1;
const [num_selected, numOnSide] = cases[selectTest];

const preferences = calculatePreferences2(numOnSide);

const num_points = numOnSide ** 2;
const quota = num_points / num_selected;

// const map_scale = p => [(p[0] + 0.5) / numOnSide, (p[1] + 0.5) / numOnSide];

// Solve
const prefs = preferences[0]
const results = solveMyLP(prefs, quota);
// const results = solveSCS(prefs, quota);
console.log(results); // Check results.feasible, results.result, etc. 
