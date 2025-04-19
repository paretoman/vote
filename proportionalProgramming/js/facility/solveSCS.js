import createSCS from 'scs-solver';
// import createSCSData from './createSCSData.js';
import createSCSData2 from './createSCSData2.js';


const SCS = await createSCS();

export function solveSCS(A,quota) {
    
    const {data,cone} = createSCSData2(A,quota)

    const settings = new SCS.ScsSettings();
    SCS.setDefaultSettings(settings);
    settings.epsAbs = 1e-9;
    settings.epsRel = 1e-9;
    settings.maxIters = 500

    const solution = SCS.solve(data, cone, settings);
    const x = [...(solution.x).slice(1)];
    // const x = [...(solution.y).slice(1)];
    return x
}


const quota = 1
    
const A = [[1,1],[1,1]];

const x = solveSCS(A,quota)

console.log(x)