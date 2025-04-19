export default {
    optimizeDeps: {
      exclude: [
        // 'highs',
        'scs-solver',
        'highs/build/highs.wasm',
        // 'scs-solver/dist/scs.wasm'
      ]
    }
  }