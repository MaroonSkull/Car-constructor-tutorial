// настройка сервопривода, ось x
const servoMin = 70, servoMax = 110;
let servoAngle = (servoMax-servoMin)/2+servoMin;

// настройка скорости, ось y
let speedMin = -100, speedMax = 100;

// Создание очереди на кольцевом буфере для передачи запросов на бэк
let fifo = createRingBuffer(3);