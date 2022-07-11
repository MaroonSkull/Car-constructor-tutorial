// настройка сервопривода, ось x
const servoMin = 45, servoMax = 135;
let servoAngle = (servoMax-servoMin)/2+servoMin;

// настройка скорости, ось y
let speedMin = -100, speedMax = 100;

// Создание очереди на кольцевом буфере для передачи запросов на бэк
let fifo = createRingBuffer(3);