
import { solveLP } from "./solveLP.js"
import { solveSCS } from "./solveSCS.js"

// Function to draw the grid based on preferences against a point

export async function drawGrid(refPointX, refPointY, whichSolver, ctx, canvas, preferences, quota, numOnSide, pixelSize) {
    const me = refPointY * numOnSide + refPointX

    let prefs = preferences[me] // customer col chose facility row over me

    let assignment
    if (whichSolver == "SCS") {
        assignment = await solveSCS(prefs, quota)
    } else {
        assignment = await solveLP(prefs, quota, whichSolver)
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.save()
    ctx.fillStyle = "black"
    for (let i = 0; i < numOnSide * numOnSide; i++) {
        const row = Math.floor(i / numOnSide);
        const col = i % numOnSide;
        let a = assignment[i]
        // let pref = preferences[me][0][i]
        if (a > 0) {
            ctx.globalAlpha = a
            ctx.fillRect(col * pixelSize, row * pixelSize, pixelSize, pixelSize);
        }
    }

    ctx.globalAlpha = 1
    ctx.fillStyle = "#0aa"
    const row = Math.floor(me / numOnSide);
    const col = me % numOnSide;
    ctx.beginPath()
    ctx.arc((col+.5)*pixelSize,(row+.5) * pixelSize,pixelSize*.5*.8, 0, 2 * 3.14159)
    ctx.fill()
    // ctx.stroke()
    // ctx.fillRect(col * pixelSize, row * pixelSize, pixelSize, pixelSize);
    ctx.restore()
    return assignment.toString();
}