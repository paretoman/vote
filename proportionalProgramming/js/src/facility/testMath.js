// npm install mathjs
import {matrix} from 'mathjs'
// const { matrix } = require('mathjs');
// or import { matrix } from 'mathjs';
// or <script src="https://unpkg.com/mathjs@14.0.1/lib/browser/math.js"></script>

const A = matrix([
    [1, 0],
    [0, 1],
    [1, 1]
], 'sparse');

const P = matrix([
    [3, 0],
    [0, 2]
], 'sparse');

const data = {
    m: 3,
    n: 2,
    A_x: A._values,
    A_i: A._index,
    A_p: A._ptr,
    P_x: P._values,
    P_i: P._index,
    P_p: P._ptr,
    b: [-1.0, 0.3, -0.5],
    c: [-1.0, -1.0]
};

console.log(data)