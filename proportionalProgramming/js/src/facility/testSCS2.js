import createSCS from 'scs-solver';
import createSCSData from './createSCSData.js';
import createSCSData2 from './createSCSData2.js';

async function main() {
    const SCS = await createSCS();
    
    const quota = 1
    
    const A = [[1,1],[1,1]];
    const {data,cone} = createSCSData2(A,quota)

    const settings = new SCS.ScsSettings();
    SCS.setDefaultSettings(settings);
    settings.epsAbs = 1e-9;
    settings.epsRel = 1e-9;

    const solution = SCS.solve(data, cone, settings);
    console.log(solution);

    // // re-solve using warm start (will be faster)
    settings.warmStart = true;
    const solution2 = SCS.solve(data, cone, settings, solution);


    const x = [...(solution.x).slice(1)];

    console.log(x)

}

main();