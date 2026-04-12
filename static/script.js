const canvas = document.getElementById('hospitalCanvas');
const ctx = canvas.getContext('2d');

// Fetch the current state from the backend
async function fetchState() {
    const response = await fetch('/get_state');
    const data = await response.json();
    draw(data);
}

// Admit a new patient 
async function admitPatient() {
    const name = document.getElementById('pName').value;
    const severity = document.getElementById('pSeverity').value;
    
    if(!name) {
        alert("Please enter a patient name");
        return;
    }

    const response = await fetch('/add_patient', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name, severity: severity })
    });
    
    const result = await response.json();
    document.getElementById('statusMessage').innerText = result.message;
    document.getElementById('pName').value = "";
    
    fetchState(); // Grab the new tree data and redraw
}

// Treat patient 
async function treatPatient() {
    const response = await fetch('/treat_patient', { method: 'POST' });
    const result = await response.json();
    
    document.getElementById('statusMessage').innerText = result.message;
    fetchState(); // Grab the new tree data and redraw
}

// Drawing Logic
function draw(data) {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Wipe the canvas clean
    
    // Draw Titles
    ctx.fillStyle = "black";
    ctx.font = "bold 20px Arial";
    ctx.fillText("Waiting Room Priority Queue", 50, 40);
    ctx.fillText("Patient Records (Red-Black Tree)", 550, 40);

    // Draw the Red-Black Tree
    // Start at x=750 (right side), y=100 (top), with an initial spacing of 100px
    if (data.red_black_tree) {
        drawRBT(data.red_black_tree, 750, 100, 100);
    }
    
    // Draw the Binomial Heap on the left side
    if (data.binomial_heap) {
        drawBinomialHeap(data.binomial_heap);
    }
    console.log("Current Hospital State:", data);
}

function drawRBT(node, x, y, horizontalSpacing) {
    if (!node) return;

    // Draw lines to children first
    if (node.left) {
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x - horizontalSpacing, y + 60);
        ctx.stroke();
        drawRBT(node.left, x - horizontalSpacing, y + 60, horizontalSpacing / 2);
    }
    if (node.right) {
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + horizontalSpacing, y + 60);
        ctx.stroke();
        drawRBT(node.right, x + horizontalSpacing, y + 60, horizontalSpacing / 2);
    }

    // Draw the Node Circle
    ctx.beginPath();
    ctx.arc(x, y, 20, 0, 2 * Math.PI);
    ctx.fillStyle = node.color === "RED" ? "#e74c3c" : "#2c3e50";
    ctx.fill();
    ctx.stroke();

    // Draw the Text (severity Key inside circle, name above circle)
    ctx.fillStyle = "white";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = "bold 14px Arial";
    ctx.fillText(node.key, x, y);
    
    ctx.fillStyle = "black";
    ctx.fillText(node.name, x, y - 25);
}

function drawBinomialHeap(roots) {
    let startX = 100;
    let startY = 100;
    
    roots.forEach(root => {
        // Draw each binomial tree in the root list
        let treeWidth = drawBHNode(root, startX, startY, 60);
        startX += treeWidth + 40; // Shift right for the next tree
    });
}

function drawBHNode(node, x, y, spacing) {
    if (!node) return 0;

    let childY = y + 70;
    let totalWidth = 50; // Base width of a single node

    node.children.forEach((child, index) => {
        // Calculate child position branching down and to the right
        let childX = x - 20 + (index * spacing * 1.5) + (totalWidth / 2);
        
        // Draw connecting line
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(childX, childY);
        ctx.stroke();

        // Recursively draw child and add its width to the total
        let childWidth = drawBHNode(child, childX, childY, spacing * 0.8);
        totalWidth += childWidth;
    });

    // Draw the node circle
    ctx.beginPath();
    ctx.arc(x, y, 20, 0, 2 * Math.PI);
    ctx.fillStyle = "#3498db"; // Blue for the waiting room
    ctx.fill();
    ctx.stroke();

    // Draw the Text (severity in middle, name above)
    ctx.fillStyle = "white";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = "bold 14px Arial";
    ctx.fillText(node.severity, x, y);
    
    ctx.fillStyle = "black";
    ctx.fillText(node.name, x, y - 25);
    
    // Draw degree below the node
    ctx.fillStyle = "#7f8c8d";
    ctx.font = "10px Arial";
    ctx.fillText(`Deg: ${node.degree}`, x, y + 30); 

    return totalWidth;
}
// Load the initial empty state when the page opens
fetchState();