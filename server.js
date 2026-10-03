const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
// Optional for local machine control: const robot = require('robotjs');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static('public'));

io.on('connection', (socket) => {
    console.log('A device connected:', socket.id);

    socket.on('mouse-move', (data) => {
        console.log(`Move mouse by:`, data);
        // If running locally on the host machine, use robot.moveMouse()
        // let mouse = robot.getMousePos();
        // robot.moveMouse(mouse.x + data.dx, mouse.y + data.dy);
    });

    socket.on('key-press', (data) => {
        console.log(`Key pressed:`, data.key);
        // robot.typeString(data.key);
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server running on port ${PORT}`));