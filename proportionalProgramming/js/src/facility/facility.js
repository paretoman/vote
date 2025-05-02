
import { calculatePreferences2 } from "./calculatePreferences2.js"
import { drawGrid } from "./drawGrid.js";

// This file is for all the UI and holds the state.



// Geometry Definition //

// Buttons 
const selectElement = document.getElementById("options");
const seatsElement = document.getElementById("seats");
const pixelsElement = document.getElementById("pixels");
const outputDisplay = document.getElementById("output");

selectElement.addEventListener("change", handleSolver);
seatsElement.addEventListener("change", handleSeats);
pixelsElement.addEventListener("change", handlePixels);

// Canvas

const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');
const pixelSize = 10; // Size of each pixel on the canvas

canvas.addEventListener('mousedown', handleMouseDown);
canvas.addEventListener('mousemove', handleMouseMove);
canvas.addEventListener('mouseup', handleMouseUp);

// Button Handlers
function handleSeats(event) {
  updateGeometry()
  updateGrid()
}

function handlePixels() {
  updateGeometry()
  updateGrid()
}

let num_selected
let quota
let preferences
let numOnSide
function updateGeometry() {
  num_selected = seatsElement.valueAsNumber  // 2 or 3 or so
  numOnSide = pixelsElement.valueAsNumber // 13 or so
  const numPoints = numOnSide * numOnSide
  quota = numPoints / num_selected
  preferences = calculatePreferences2(numOnSide);
  canvas.width = numOnSide * pixelSize;
  canvas.height = numOnSide * pixelSize;
}

// Mouse //


// Mouse Interaction Handlers

let isDragging = false;
let lastX = 0
let lastY = 0

function handleMouseDown(event) {
  isDragging = true;
  updateMouse(event);
  updateGrid()
}

function handleMouseMove(event) {
  if (isDragging) {
    updateMouse(event);
    updateGrid()
  }
}

function handleMouseUp() {
  isDragging = false;
}

let mouseX
let mouseY
function updateMouse(event) {
  const rect = canvas.getBoundingClientRect();
  mouseX = Math.floor((event.clientX - rect.left) / pixelSize);
  mouseY = Math.floor((event.clientY - rect.top) / pixelSize);
  lastX = mouseX
  lastY = mouseY
}

function handleSolver(event) {
  updateSolver()
  updateGrid()
}

let whichSolver
function updateSolver() {
  whichSolver = selectElement.value
}

async function updateGrid(event) {
  const output = await drawGrid(lastX, lastY, whichSolver, ctx, canvas, preferences, quota, numOnSide, pixelSize);
  outputDisplay.textContent = "" // output[0]
}

function init() {
  updateGeometry()
  updateSolver()
}

init()