#! /usr/bin/python

import sys

def read_input(file):
	'''
		read input train file
		return a list contaions all sessions
	'''
	while True:
		session = read_session(file)
		if not session:
			break
		yield session

def read_session(file):
	'''
		read a session from file
	'''
	line = file.readline().rstrip()
	session = []
	while line and line != '':
		session.append(line)
		line = file.readline().rstrip()
	return session


def main():
	sessions = read_input(sys.stdin)

	with open('train_sessions','w') as f_res:
		for one_session in sessions:
			f_res.write(','.join(one_session)+'\n')
		

if __name__=='__main__':
	main()
