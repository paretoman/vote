
import { calculatePreferences2 } from "./calculatePreferences2.js"
import { drawGrid } from "./drawGrid.js";

// This file is for all the UI and holds the state.

// Geometry Definition
const cases = [
  [3, 13], // 0
  [2, 3], // 1
];
const selectTest = 0;
const [num_selected, numOnSide] = cases[selectTest];
const numPoints = numOnSide * numOnSide
const quota = numPoints / num_selected
const preferences = calculatePreferences2(numOnSide);

// Canvas

const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');
const pixelSize = 10; // Size of each pixel on the canvas
canvas.width = numOnSide * pixelSize;
canvas.height = numOnSide * pixelSize;

// Buttons 
const selectElement = document.getElementById("options");
const outputDisplay = document.getElementById("output");

let lastX = 0
let lastY = 0

selectElement.addEventListener("change", updateGridFromOption);


// Event listeners for mouse interaction
canvas.addEventListener('mousedown', handleMouseDown);
canvas.addEventListener('mousemove', handleMouseMove);
canvas.addEventListener('mouseup', handleMouseUp);

let isDragging = false;

function handleMouseDown(event) {
  isDragging = true;
  updateGrid(event);
}

function handleMouseMove(event) {
  if (isDragging) {
    updateGrid(event);
  }
}

function handleMouseUp() {
  isDragging = false;
}

async function updateGrid(event) {
  const rect = canvas.getBoundingClientRect();
  const mouseX = Math.floor((event.clientX - rect.left) / pixelSize);
  const mouseY = Math.floor((event.clientY - rect.top) / pixelSize);
  lastX = mouseX
  lastY = mouseY
  const whichSolver = selectElement.value
  const output = await drawGrid(mouseX, mouseY, whichSolver, ctx, canvas, preferences, quota, numOnSide, pixelSize);
  outputDisplay.textContent = output
}

async function updateGridFromOption(event) {
  const whichSolver = selectElement.value
  const output = await drawGrid(lastX, lastY, whichSolver, ctx, canvas, preferences, quota, numOnSide, pixelSize);
  outputDisplay.textContent = output
}