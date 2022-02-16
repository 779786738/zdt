import socket
import time
import json
# from Data import Data, Session
import _thread
import pickle


class Data:
    def __init__(self, host, data_dict):
        self.ip = host

        self.robot_id = data_dict['robotID']
        self.cabinet_id = data_dict['controlCabinetID']

        self.current_fluctuation_1 = data_dict['data']['currentFluctuation']['joint_1']
        self.current_fluctuation_2 = data_dict['data']['currentFluctuation']['joint_2']
        self.current_fluctuation_3 = data_dict['data']['currentFluctuation']['joint_3']
        self.current_fluctuation_4 = data_dict['data']['currentFluctuation']['joint_4']
        self.current_fluctuation_5 = data_dict['data']['currentFluctuation']['joint_5']
        self.current_fluctuation_6 = data_dict['data']['currentFluctuation']['joint_6']

        self.paused = data_dict['data']['paused']
        self.task_mode = int(data_dict['data']['task_mode'])
        self.drag_status = data_dict['data']['drag_status']

        self.ins_average_power_1 = data_dict['data']['insAveragePower']['joint_1']
        self.ins_average_power_2 = data_dict['data']['insAveragePower']['joint_2']
        self.ins_average_power_3 = data_dict['data']['insAveragePower']['joint_3']
        self.ins_average_power_4 = data_dict['data']['insAveragePower']['joint_4']
        self.ins_average_power_5 = data_dict['data']['insAveragePower']['joint_5']
        self.ins_average_power_6 = data_dict['data']['insAveragePower']['joint_6']

        self.cur_running_circles_1 = data_dict['data']['curRunningCircles']['joint_1']
        self.cur_running_circles_2 = data_dict['data']['curRunningCircles']['joint_2']
        self.cur_running_circles_3 = data_dict['data']['curRunningCircles']['joint_3']
        self.cur_running_circles_4 = data_dict['data']['curRunningCircles']['joint_4']
        self.cur_running_circles_5 = data_dict['data']['curRunningCircles']['joint_5']
        self.cur_running_circles_6 = data_dict['data']['curRunningCircles']['joint_6']

        self.joint_1_actual_position = data_dict['data']['joint_actual_position'][0]
        self.joint_2_actual_position = data_dict['data']['joint_actual_position'][1]
        self.joint_3_actual_position = data_dict['data']['joint_actual_position'][2]
        self.joint_4_actual_position = data_dict['data']['joint_actual_position'][3]
        self.joint_5_actual_position = data_dict['data']['joint_actual_position'][4]
        self.joint_6_actual_position = data_dict['data']['joint_actual_position'][5]

        self.inst_voltage_1 = data_dict['data']['instVoltage']['joint_1']
        self.inst_voltage_2 = data_dict['data']['instVoltage']['joint_2']
        self.inst_voltage_3 = data_dict['data']['instVoltage']['joint_3']
        self.inst_voltage_4 = data_dict['data']['instVoltage']['joint_4']
        self.inst_voltage_5 = data_dict['data']['instVoltage']['joint_5']
        self.inst_voltage_6 = data_dict['data']['instVoltage']['joint_6']

        self.sum_running_time = data_dict['data']['sumRunningTime']
        self.emergency_stop = data_dict['data']['emergency_stop']
        self.powered_on = data_dict['data']['powered_on']
        self.task_state = data_dict['data']['task_state']
        self.interp_state = data_dict['data']['interp_state']
        self.protective_stop = data_dict['data']['protective_stop']

        self.actual_position_1 = data_dict['data']['actual_position'][0]
        self.actual_position_2 = data_dict['data']['actual_position'][1]
        self.actual_position_3 = data_dict['data']['actual_position'][2]
        self.actual_position_4 = data_dict['data']['actual_position'][3]
        self.actual_position_5 = data_dict['data']['actual_position'][4]
        self.actual_position_6 = data_dict['data']['actual_position'][5]

        self.rapid_rate = data_dict['data']['rapidrate']
        self.enabled = data_dict['data']['enabled']
        self.error_code = data_dict['data']['errcode']
        self.inpos = data_dict['data']['inpos']

        self.inst_temperature_1 = data_dict['data']['instTemperature']['joint_1']
        self.inst_temperature_2 = data_dict['data']['instTemperature']['joint_2']
        self.inst_temperature_3 = data_dict['data']['instTemperature']['joint_3']
        self.inst_temperature_4 = data_dict['data']['instTemperature']['joint_4']
        self.inst_temperature_5 = data_dict['data']['instTemperature']['joint_5']
        self.inst_temperature_6 = data_dict['data']['instTemperature']['joint_6']

        self.cur_running_time = data_dict['data']['curRunningTime']

        self.sum_running_circles_1 = data_dict['data']['sumRunningCircles']['joint_1']
        self.sum_running_circles_2 = data_dict['data']['sumRunningCircles']['joint_2']
        self.sum_running_circles_3 = data_dict['data']['sumRunningCircles']['joint_3']
        self.sum_running_circles_4 = data_dict['data']['sumRunningCircles']['joint_4']
        self.sum_running_circles_5 = data_dict['data']['sumRunningCircles']['joint_5']
        self.sum_running_circles_6 = data_dict['data']['sumRunningCircles']['joint_6']

        self.rtc = data_dict['rtc']


def to_Data(data_dict, host):
    data = Data()

    # data.robot_ip = host

    return data


def get_host_set(port):
    '''
    监听54545端口号，
    接收udp报文，
    返回报文的源地址集合
    :return:
    '''
    print('get_robot')
    host_list = list()
    robot_list = []
    # 创建socket对象
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = ("0.0.0.0", port)
    # 绑定端口号
    s.bind(address)
    # 设置超时异常时间
    s.settimeout(3)

    start_time = time.time()
    # 设计抓取时间间隔
    time_interval = 1.3
    while time.time() < start_time + time_interval:

        try:
            # receive_data表示接受到的传来的数据,是bytes类型
            # client  表示传来数据的客户端的身份信息，客户端的ip和端口，元组
            receive_data, client = s.recvfrom(2048)
            receive_data = receive_data.decode('utf8').split(';')
            print("来自客户端%s,发送的:%s" % (client, receive_data))  # 打印接收的内容
            # client[0] 表示用户ip
            if client[0] in host_list:
                continue
            else:
                host_list.append(client[0])
                item = [client[0], *receive_data]
                robot_list.append(item)

        except socket.timeout:  # 如果3秒钟没有接收数据进行提示（打印 "time out"）
            print("time out")
    s.close()

    return robot_list


def get_data_from_tcp(host, port):
    print(host, '尝试连接')
    s = socket.socket()
    address = (host, port)
    # 建立tcp连接
    try:
        s.connect(address)
    except Exception as e:
        # 该host无法连接
        print(host + ' 该host无法连接')
        print(e)
        return False
    print(address, ' 连接成功')
    nan_str = s.recv(4)
    length = s.recv(4)
    len_int = 0
    # print(length)
    for i in length:
        len_int *= 256
        len_int += i

    res = s.recv(len_int)
    s.close()
    res = res.decode(errors='ignore')
    res = res[res.index('{'):]
    # print(res)

    try:
        res = json.loads(res)
    except Exception as e:
        print(res)
        print('解析数据错误')
        print(e)
        return False

    data = Data(host, res)

    return data


def demo(host_set):
    port = 10003
    for host in host_set:
        try:
            _thread.start_new_thread(get_data_from_tcp, (host, port))
            # get_data_from_tcp(host, port)
        except Exception as e:
            # print('线程启动失败')
            print(e)
        # _thread.start_new_thread(get_data_from_tcp, (host, port))

    time_start = time.time()
    while time_start + 1 > time.time():
        pass
    print('end!!!!!')


def predict(df):
    model_name = 'svm_pipe_01.pickle'

    columns = ['protective_stop', 'task_state', 'rapid_rate', 'sum_running_time', 'ins_average_power_2',
               'sum_running_circles_2', 'joint_2_actual_position', 'current_fluctuation_2', 'inst_temperature_2', 'inst_voltage_2'
               ]

    path = '.\\utils\\'+model_name

    with open(path, 'rb') as f:
        model = pickle.load(f)
    test_x = df[columns]
    y_hat = model.predict(test_x)
    return y_hat

if __name__ == '__main__':
    # print(host_set)
    robot_list = get_host_set(54545)
    for robot in robot_list:
        print(robot)

    # while True:
    #     host_set = get_host_set(54545)
    # demo(host_set)
