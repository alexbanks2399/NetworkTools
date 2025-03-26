import socket,csv,subprocess,datetime,os,traceback,sys

start_time = datetime.datetime.now()
print(f"Start time: {start_time}")
directory = os.getcwd()

class Ping:
    def write_output(csv_file_path, csv_data):
        csv_file = open(csv_file_path, "a", newline="")
        with csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(csv_data)

    def ping(fqdn):
        ping_time = datetime.datetime.now()
        print(f"Looking up {fqdn}")
        ip = socket.gethostbyname(fqdn)
        print(f"Trying to ping {ip}")
        response = subprocess.Popen(['ping.exe',ip], stdout = subprocess.PIPE).communicate()[0]
        response = response.decode()

        if 'bytes=32' in response:
            status = 'Up'
        elif 'destination host unreachable' in response:
            status = 'Unreachable'
        else:
            status = 'Down'
            ip = 'Not Found'
        # if status == 'Down':
        #     ip = 'Not Found'

        Ping.write_output(fr"{directory}\Ping output.csv", [[fqdn, ip, status, ping_time]])

devices = open(fr"{directory}\Devices.txt")
device_list = []
for line in devices:
    line = line.rstrip()
    device_list.append(line)

device_count = 0

for fqdn in device_list:
    device_count = device_count + 1
    device_start_time = datetime.datetime.now()

    try:
        Ping.ping(fqdn)

    except socket.gaierror as err:
        exception_line_number = traceback.extract_tb(sys.exc_info()[2])[-1].lineno
        print(f"An error occurred, writing to Issues.csv")
        Ping.write_output(fr"{directory}\Issues.csv", 
                            [[fqdn,
                            device_start_time,
                            err,
                            exception_line_number,"DNS lookup error"]])

    except Exception as err:
        exception_line_number = traceback.extract_tb(sys.exc_info()[2])[-1].lineno
        print(f"An error occurred, writing to Issues.csv")
        Ping.write_output(fr"{directory}\Issues.csv", 
                             [[fqdn,
                               device_start_time,
                               err,
                               exception_line_number,"Raised out of function"]])

    device_end_time = datetime.datetime.now()
    time_so_far = device_end_time - start_time
    avg_time_per_device = time_so_far / device_count
    device_time_taken = device_end_time - device_start_time
    
    print(f"Devices so far: {device_count}")
    print(f"Time so far: {time_so_far}")
    print(f"Time for device: {device_time_taken}")
    print(f"Average time so far: {avg_time_per_device}\n")

end_time = datetime.datetime.now()
time_taken = end_time - start_time
end_avg_time = time_taken / device_count
print(f"Time taken: {time_taken}")
print(f"Average time per device: {end_avg_time}")
