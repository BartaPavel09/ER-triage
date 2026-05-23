// Grab both canvases
const heapCanvas = document.getElementById('heapCanvas');
const heapCtx = heapCanvas.getContext('2d');

const rbtCanvas = document.getElementById('rbtCanvas');
const rbtCtx = rbtCanvas.getContext('2d');

// API Calls
async function fetchState() {
    const response = await fetch('/get_state');
    const data = await response.json();
    draw(data);
}

async function admitPatient() {
    const name = document.getElementById('pName').value;
    const severity = document.getElementById('pSeverity').value;
    
    if(!name) { alert("Please enter a patient name"); return; }

    const response = await fetch('/add_patient', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name, severity: severity })
    });
    
    const result = await response.json();
    document.getElementById('statusMessage').innerText = result.message;
    document.getElementById('pName').value = "";
    fetchState(); 
}

async function treatPatient() {
    const response = await fetch('/treat_patient', { method: 'POST' });
    const result = await response.json();
    document.getElementById('statusMessage').innerText = result.message;
    fetchState(); 
}

async function removePatient() {
    const name = document.getElementById('manageName').value;
    const severity = document.getElementById('currentSev').value;
    
    if(!name || !severity) { alert("Please enter name and current severity"); return; }

    const response = await fetch('/delete_patient', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name, severity: severity })
    });
    
    const result = await response.json();
    document.getElementById('statusMessage').innerText = result.message;
    fetchState();
}

async function changeSeverity() {
    const name = document.getElementById('manageName').value;
    const oldSev = document.getElementById('currentSev').value;
    const newSev = document.getElementById('newSev').value;
    
    if(!name || !oldSev || !newSev) { alert("Please fill all fields"); return; }

    const response = await fetch('/update_severity', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name, oldSeverity: oldSev, newSeverity: newSev })
    });
    
    const result = await response.json();
    document.getElementById('statusMessage').innerText = result.message;
    if (result.status === "success") {
        document.getElementById('currentSev').value = newSev;
    }
    fetchState();
}

async function resetHospital() {
    const response = await fetch('/reset', { method: 'POST' });
    const result = await response.json();
    document.getElementById('statusMessage').innerText = result.message;
    fetchState(); 
}

function getDepth(node) {
    if (!node) return 0;
    return 1 + Math.max(getDepth(node.left), getDepth(node.right));
}

// Main drawing function
function draw(data) {
    // Wipe BOTH canvases clean
    heapCtx.clearRect(0, 0, heapCanvas.width, heapCanvas.height);
    rbtCtx.clearRect(0, 0, rbtCanvas.width, rbtCanvas.height);

    if (data.redBlackTree) {
        let rbtDepth = getDepth(data.redBlackTree);

        // Mathematically calculate the bottom nodes are always spaced apart safely
        let baseSpacing = 40 * Math.pow(2, Math.max(0, rbtDepth - 2));

        // Expand canvas to fit the full tree before drawing
        rbtCanvas.width  = Math.max(2500, baseSpacing * 4 + 200);
        rbtCanvas.height = Math.max(500,  rbtDepth * 80 + 80);

        // Center root horizontally in the (possibly enlarged) canvas
        let rootStartX = rbtCanvas.width / 2;

        drawRBT(data.redBlackTree, rootStartX, 40, baseSpacing);
    }

    // Draw the Binomial Heap
    if (data.binomialHeap) {
        drawBinomialHeap(data.binomialHeap);
    }
}

// Red-Black Tree drawing logic
const RBT_LEVEL_HEIGHT = 80;

function drawRBT(node, x, y, horizontalSpacing) {
    if (!node) return;

    if (node.left) {
        rbtCtx.beginPath();
        rbtCtx.moveTo(x, y);
        rbtCtx.lineTo(x - horizontalSpacing, y + RBT_LEVEL_HEIGHT);
        rbtCtx.stroke();
        drawRBT(node.left, x - horizontalSpacing, y + RBT_LEVEL_HEIGHT, horizontalSpacing / 2);
    }
    if (node.right) {
        rbtCtx.beginPath();
        rbtCtx.moveTo(x, y);
        rbtCtx.lineTo(x + horizontalSpacing, y + RBT_LEVEL_HEIGHT);
        rbtCtx.stroke();
        drawRBT(node.right, x + horizontalSpacing, y + RBT_LEVEL_HEIGHT, horizontalSpacing / 2);
    }

    rbtCtx.beginPath();
    rbtCtx.arc(x, y, 20, 0, 2 * Math.PI);
    rbtCtx.fillStyle = node.color === "RED" ? "#e74c3c" : "#2c3e50";
    rbtCtx.fill();
    rbtCtx.stroke();

    rbtCtx.fillStyle = "white";
    rbtCtx.textAlign = "center";
    rbtCtx.textBaseline = "middle";
    rbtCtx.font = "bold 14px Arial";
    rbtCtx.fillText(node.key, x, y);
    
    rbtCtx.fillStyle = "black";
    rbtCtx.fillText(node.name, x, y - 25);
}

// Binomial Heap drawing logic
const minNodeWidth = 80;

function getTreeWidth(node) {
    if (!node) return 0;
    if (!node.children || node.children.length === 0) return minNodeWidth;
    let totalWidth = 0;
    node.children.forEach(child => { totalWidth += getTreeWidth(child); });
    return totalWidth;
}

function drawBinomialHeap(roots) {
    let startX = 50; 
    let startY = 50;
    
    roots.forEach(root => {
        let treeWidth = getTreeWidth(root); 
        let rootCenterX = startX + (treeWidth / 2); 
        drawBHNode(root, rootCenterX, startY);
        startX += treeWidth + 40; 
    });
}

function drawBHNode(node, x, y) {
    if (!node) return;
    let childY = y + 80;

    if (node.children && node.children.length > 0) {
        let totalChildrenWidth = getTreeWidth(node);
        let currentX = x - (totalChildrenWidth / 2);

        node.children.forEach(child => {
            let childWidth = getTreeWidth(child);
            let childCenterX = currentX + (childWidth / 2);

            heapCtx.beginPath();
            heapCtx.moveTo(x, y + 20); 
            heapCtx.lineTo(childCenterX, childY - 20); 
            heapCtx.stroke();

            drawBHNode(child, childCenterX, childY);
            currentX += childWidth; 
        });
    }

    heapCtx.beginPath();
    heapCtx.arc(x, y, 22, 0, 2 * Math.PI);
    heapCtx.fillStyle = "#3498db"; 
    heapCtx.fill();
    heapCtx.stroke();

    heapCtx.fillStyle = "white";
    heapCtx.textAlign = "center";
    heapCtx.textBaseline = "middle";
    heapCtx.font = "bold 14px Arial";
    heapCtx.fillText(node.severity, x, y);
    
    heapCtx.fillStyle = "black";
    heapCtx.fillText(node.name, x, y - 30);
    
    heapCtx.fillStyle = "#7f8c8d";
    heapCtx.font = "12px Arial";
    heapCtx.fillText(`Deg: ${node.degree}`, x, y + 35); 
}

// Initial load
fetchState();