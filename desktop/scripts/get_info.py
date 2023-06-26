MATRIX_IP = '192.168.50.77'


import config
import requests
def get_info(matrix_ip):
	request = f'http://{matrix_ip}/api?function=getInfo'
	info = []
	for data in requests.get(request).text.split(';'):
		info.append(data.split(':'))
	return info


if __name__ == '__main__':
	print(get_info(MATRIX_IP))