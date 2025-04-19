import { solveLP } from "./solveLP.js";
const A = [
  [2, 5, 1],
  [3, 1, 4],
  [1, 6, 2],
];
const quota = 3;

const x = solveLP(A,quota)
console.log(x)