from subprocess import check_output


def get_ip():
	ips = check_output(['hostname', '--all-ip-addresses'])
	return ips.decode('utf-8').split(' \n')[0]