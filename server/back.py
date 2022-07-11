try:
    from flask import Flask, render_template, jsonify, request, url_for
    from time import sleep
    import RPi.GPIO as GPIO
    import multiprocessing
    import json
    import psutil
except ModuleNotFoundError:
    pass
except ImportError:
    pass

# Глобальные переменные
Ain1 = 16   # Мотор A
Ain2 = 18
PWMA = 22
Bin1 = 13   # Мотор B
Bin2 = 15
PWMB = 11
servo = 29  # Сервопривод
q = multiprocessing.Queue() # Очередь сообщений для контроллера

# Вспомогательные функции
def cpu_temperature():
    return psutil.sensors_temperatures()['cpu_thermal'][0].current
def disk_space():
    st = psutil.disk_usage(".")
    return st.free, st.total
def cpu_load() -> int:
    return int(psutil.cpu_percent())
def ram_usage() -> int:
    return int(psutil.virtual_memory().percent)

# Процедура сервера
def webapp():
    app = Flask(__name__)

    @app.route('/')
    def index():
        health = {'CPUTemp': cpu_temperature(), 'CPULoad': cpu_load(), "DiskFree": disk_space()[0], "DiskTotal": disk_space()[1], "RAMUse": ram_usage()}
        print(json.dumps(health).encode('utf-8'))
        return render_template('index.html')

    @app.route('/control', methods=['POST', 'GET'])
    def control():
        angle = int(request.args['angle'])
        speed = int(request.args['speed'])

        # Добавляем в очередь новые данные
        q.put([angle, speed])

        return str(angle)+' '+str(speed) #lol

    return app

# Моторы и серво
def controller():
    def setMotorSpeed(direction, speed):
        if direction:
            GPIO.output(Ain1,GPIO.LOW)      # реверсим направление
            GPIO.output(Ain2,GPIO.HIGH)
            GPIO.output(Bin1,GPIO.LOW)
            GPIO.output(Bin2,GPIO.HIGH)
        else:
            GPIO.output(Ain1,GPIO.HIGH)     # Пара high/low отвечает за направление вращения
            GPIO.output(Ain2,GPIO.LOW)
            GPIO.output(Bin1,GPIO.HIGH)
            GPIO.output(Bin2,GPIO.LOW)

        A.ChangeDutyCycle(speed)
        B.ChangeDutyCycle(speed)

    def setServoAngle(angle):
        dutyCycle = angle / 18. + 8./5. # Конвертируем угол 0-180 в длительность цикла
        pwm.ChangeDutyCycle(dutyCycle)

    # Настройка частот ШИМ
    pwm = GPIO.PWM(servo, 50)
    A = GPIO.PWM(PWMA, 100)
    B = GPIO.PWM(PWMB, 100)
    # Сбрасываем положение серво и скорость моторов
    A.start(0)
    B.start(0)
    pwm.start(90 / 18. + 8./5.)

    params = [90, 0]

    while True:
        if q.empty() == False:
            params = q.get()
            print('теперь обрабатываем '+str(params))

        setServoAngle(params[0])
        if params[1] >= 0:
            setMotorSpeed(True, params[1])
        else:
            setMotorSpeed(False, -params[1])

# init
if __name__ == '__main__':
    # Настройка GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    # Настройка моторов
    GPIO.setup(Ain1,GPIO.OUT)
    GPIO.setup(Ain2,GPIO.OUT)
    GPIO.setup(PWMA,GPIO.OUT)
    GPIO.setup(Bin1,GPIO.OUT)
    GPIO.setup(Bin2,GPIO.OUT)
    GPIO.setup(PWMB,GPIO.OUT)

    # Настройка серво
    GPIO.setup(servo, GPIO.OUT)

    # Создаём поток, управляющий GPIO
    qLer = multiprocessing.Process(target=controller)
    qLer.start()

    # Запуск flask-сервера в режиме debug
    web = webapp() # Можно в одну строчку
    web.run(debug=True, port=80, host='0.0.0.0', use_reloader=False)