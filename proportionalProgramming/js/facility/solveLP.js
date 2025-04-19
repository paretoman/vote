import LPModel from "lp-model"
import jsLPSolver from "javascript-lp-solver"
import HIGHS from "highs"
import GLPK from "glpk.js";

// const highs = await Module()
const highs = await HIGHS()
const glpk = await GLPK()

// optionally load the solvers
export async function solveLP(A,quota, whichSolver) {
    const numRows = A.length;
    const numCols = A[0].length; // Assuming A is a valid matrix

    const model = new LPModel.Model();

    const x = []
    for (let j = 0; j < numCols; j++) {
      x[j] = model.addVar({lb: 0, ub:1, name: `x${j}`})
    }
    const z = model.addVar({name: 'z'})

    // sum of x = quota
    model.addConstr(x,'>=',quota)

    // sum of x * A <= z
    for (let i = 0; i < numRows; i++) {
        const ax = []
        for (let j = 0; j < numCols; j++) {
            ax[j] = [A[i][j], x[j]]
        }
        model.addConstr(ax,'<=',[z])
    }

    model.setObjective([z],"MINIMIZE")
    
    // console.log(model.toLPFormat());
    

    if (whichSolver == "Javascript LP Solver") {
      model.solve(jsLPSolver);
    } else if (whichSolver == "Highs") {
      const options = {"solver":"ipm"}
      // https://ergo-code.github.io/HiGHS/dev/options/definitions/
      // const options = {}
      // model.solve(highs);
      model.solve(highs,options);
    } else {
      const options = {}
      await model.solve(glpk,options);
      // await model.solve(glpk);
    }
    
    // console.log(`Solver finished with status: ${model.status}`);
    // console.log(`Objective value: ${model.ObjVal}`);
    
    // console.log(`z = ${z.value}`);
    // for (let j = 0; j < numCols; j++) {
    //   console.log(`x${j} = ${x[j].value}`);
    // }

    const realX = x.map(a => a.value)
    return realX

}

// delete this once done
const A = [
  [2, 5, 1],
  [3, 1, 4],
  [1, 6, 2],
];
const quota = 2;

const x = solveLP(A,quota)
console.log(x)