const container = document.getElementById('circle-container');
const ballSize = 5; // Size of the balls
const numRings = 6; // Total number of concentric rings
const maxRadius = 250; // Radius for the outermost ring
const balls = [];

// Create concentric circles with random spacing
for (let ring = 1; ring <= numRings; ring++) {
    const radius = maxRadius - ring * 10;
    const numBalls = Math.floor(ring * 20 + Math.random() * 10); // Randomize number of balls

    for (let i = 0; i < numBalls; i++) {
        const angle = (2 * Math.PI / numBalls) * i + Math.random() * 0.1; // Add random angle offset
        const targetX = maxRadius + radius * Math.cos(angle);
        const targetY = maxRadius + radius * Math.sin(angle);

        const ball = document.createElement('div');
        ball.classList.add('ball');
        ball.dataset.targetX = targetX;
        ball.dataset.targetY = targetY;
        ball.style.width = `${ballSize}px`;
        ball.style.height = `${ballSize}px`;
        ball.style.left = `${targetX - ballSize / 2}px`;
        ball.style.top = `${targetY - ballSize / 2}px`;
        container.appendChild(ball);
        balls.push(ball);
    }
}

// Function to calculate distance between two points
function getDistance(x1, y1, x2, y2) {
    return Math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2);
}

// Mouse interaction with random sideways displacement
container.addEventListener('mousemove', (e) => {
    const rect = container.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    balls.forEach((ball) => {
        const ballX = parseFloat(ball.style.left) + ballSize / 2;
        const ballY = parseFloat(ball.style.top) + ballSize / 2;
        const distance = getDistance(mouseX, mouseY, ballX, ballY);

        if (distance < 250) {
            const angle = Math.atan2(ballY - mouseY, ballX - mouseX);
            const offsetX = Math.cos(angle) * (Math.random() * 50 + 50); // Randomize displacement
            const offsetY = Math.sin(angle) * (Math.random() * 50 + 50);
            ball.style.left = `${ballX + offsetX - ballSize / 2}px`;
            ball.style.top = `${ballY + offsetY - ballSize / 2}px`;
        }
    });
});

// Smooth return to circular arrangement with gravity effect
function updatePositions() {
    balls.forEach((ball) => {
        const ballX = parseFloat(ball.style.left) + ballSize / 2;
        const ballY = parseFloat(ball.style.top) + ballSize / 2;
        const targetX = parseFloat(ball.dataset.targetX);
        const targetY = parseFloat(ball.dataset.targetY);

        const dx = targetX - ballX;
        const dy = targetY - ballY;

        const moveX = dx * 0.2; // Slow down return
        const moveY = dy * 0.2;

        ball.style.left = `${ballX + moveX - ballSize / 2}px`;
        ball.style.top = `${ballY + moveY - ballSize / 2}px`;
    });

    requestAnimationFrame(updatePositions);
}

// Start the animation loop
updatePositions();
