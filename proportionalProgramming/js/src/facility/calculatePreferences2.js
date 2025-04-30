
// Calculate preferences with flattened array
export function calculatePreferences2(num_on_side) {
  // 1. Create a set of integers from 1 to num_on_side
  const points = Array.from({ length: num_on_side }, (_, i) => i);

  // 2. Create a mesh grid of points
  const grid = points.map(x => points.map(y => [x, y]));

  // 3. Flatten the grid
  const flatGrid = grid.flat();

  // 4. Calculate distances between all pairs of points
  const distances = flatGrid.map(point1 =>
    flatGrid.map(point2 => Math.round((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2))
  );

  // 5. Determine preference for each point
    
  const numPoints = num_on_side ** 2
  const preferences = []
  for ( let i = 0; i < numPoints; i++) {
    preferences[i] = []
    for ( let j = 0; j < numPoints; j++) {
      preferences[i][j] = []
      for ( let k = 0; k < numPoints; k++) {
        preferences[i][j][k] = 0; // make things easier to change
      }
    }
  }
  for ( let i = 0; i < numPoints; i++) {
    for ( let j = 0; j < numPoints; j++) {
      for ( let k = 0; k < numPoints; k++) {
        preferences[j][k][i] = distances[i][j] > distances[i][k] ? 1 : 0;
      }
    }
  }

  return preferences;
}
