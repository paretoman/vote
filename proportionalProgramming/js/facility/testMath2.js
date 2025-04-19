import {matrix, index, concat, ones, multiply, zeros} from 'mathjs'
const A = matrix([[1, 2], [3, 4]], 'sparse');
const B = matrix([[5, 6], [7, 8]]);
const C = matrix([
    [A.subset(index([0, 1], [0, 1])), B.subset(index([0, 1], [0, 1]))],
    [B.subset(index([0, 1], [0, 1])), A.subset(index([0, 1], [0, 1]))]
  ]);
console.log(C.toString())


// Define the four matrices
const matrix1 = matrix([[1, 2], [3, 4]]);
const matrix2 = matrix([[5, 6], [7, 8]]);
const matrix3 = matrix([[9, 10], [11, 12]]);
const matrix4 = matrix([[13, 14], [15, 16]]);

// Method 1: Concatenating horizontally then vertically
const combinedMatrix1 = concat(concat(matrix1, matrix2, 1), concat(matrix3, matrix4, 1), 0);

// Method 2: Creating a block matrix
// const combinedMatrix2 = block([
//   [matrix1, matrix2],
//   [matrix3, matrix4]
// ]);

// Print the combined matrices
console.log("Combined Matrix (Method 1):");
console.log(combinedMatrix1.toString());

// console.log("\nCombined Matrix (Method 2):");
// console.log(combinedMatrix2.toString());
