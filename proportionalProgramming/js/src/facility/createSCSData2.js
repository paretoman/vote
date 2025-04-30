import { matrix, index, concat, ones, multiply, zeros, identity } from 'mathjs'

export default function createSCSData2(D, quota) {

  const Dm = D.length
  const Dn = D[0].length

  const oTop = ones([1, Dn])
  const r1 = concat([[0]], oTop, 1)
  // [ 0  1 ]

  const oLeft = ones([Dm, 1])
  const noLeft = multiply(-1, oLeft)
  const r2 = concat(noLeft, D, 1)
  // [ -1 D ]
  const A2 = matrix(concat(r1, r2, 0), 'sparse')
  console.log(A2.toString())

  const zn = zeros([Dn, 1])
  const I = identity(Dn)
  const nI = multiply(-1, I)
  const r3 = concat(zn, nI, 1)
  // [ 0  -I ]
  const A3 = concat(A2, r3, 0)

  const r4 = concat(zn, I, 1)
  // [ 0 I ]
  const A4 = concat(A3, r4, 0)

  const A = matrix(A4, 'sparse')
  // [ 0  1 ]
  // [-1  D ]
  // [ 0 -I ]
  // [ 0  I ]

  const m = 1 + Dm + 2 * Dn
  const n = 1 + Dn

  const zm = zeros([Dm, 1])
  const b1 = concat([[quota]], zm, 0)
  const b2 = concat(b1, zm, 0)
  const b3 = concat(b2, oLeft, 0)
  // [  quota ]
  // [  0     ]
  // [  0     ]
  // [  1     ]
  // console.log(b3.toString())
  const b = b3

  // const b = new Array(m).fill(0);
  // b[0] = 1;
  // // Set the last Dn elements to -1
  // for (let i = m - Dn; i < m; i++) {
  //   b[i] = 1;
  // }
  // console.log(b); 



  const c = concat([[1]], zm, 0)

  // const c = new Array(n).fill(0)
  // c[0] = 1;
  // [ 1 ]
  // [ 0 ]

  const P = matrix(zeros([n,n]),'sparse')

  const data = {
    m,
    n,
    A_x: A._values,
    A_i: A._index,
    A_p: A._ptr,
    // P_x: P._values,
    // P_i: P._index,
    // P_p: P._ptr,
    b,
    c
  };
  // console.log(data)
  // console.log('done')

  const cone = {
    z: 1,
    l: m - 1,
  }


  return { data, cone }
}

const D = [[1, 1], [1, 1]];
console.log(createSCSData2(D, 2))
console.log('hi')