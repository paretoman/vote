export default {
    optimizeDeps: {
      exclude: [
        // 'highs',
        'scs-solver',
        'highs/build/highs.wasm',
        // 'scs-solver/dist/scs.wasm'
      ]
    },
    build: {
      rollupOptions: {
        input: {
          main: './index.html',
          facility: './src/facility/facility.html',
          pixelChooser: './src/facility/pixelChooser2.html',
        }
      }
    }
  }