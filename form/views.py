from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import models
import csv, copy

def home(request):
	cityList = []
	count = 0
	with open('world-cities.csv', newline = '', encoding = 'utf-8') as file02:
		fileRead = csv.reader(file02, delimiter = ',')
		for row in fileRead:
			if count == 0:
				count += 1
			else:
				cityList.append(row[0] + ', ' + row[1])
	request.session['user'] = None
	if request.method == 'POST':
		fullname = request.POST['fullname']
		email = request.POST['email']
		location = request.POST['location']
		type = request.POST['schoolType']
		print(request.POST)
		p = models.account.objects.create(fullname=fullname, email=email, location=location)
		if type == 'Undergraduate':
			return redirect('schools/')
		if type == 'Postgraduate':
			return redirect('postgraduate/')
		if type == 'Professional':
			return redirect('professional/')
	context = {'cityList': cityList}
	return render(request, 'school.html', context)

def schools(request):
	numChoices = []
	currentUser = models.account.objects.last()
	# if request.method == 'POST':
	# 	if 'numChoicesSubmit' in request.POST:
	# 		for i in range(int(request.POST['numChoices'])):
	# 			numChoices.append(i + 1)
	# 	elif 'selectedUnis' in request.POST:
	# 		for i in range(len(request.POST) - 2):
	# 			try:
	# 				models.School.objects.get(title=request.POST['schoolChoice-' + str(i + 1)])
	# 			except:
	# 				s = models.School.objects.create(title=request.POST['schoolChoice-' + str(i + 1)])
	# 				s.save()
	# 				currentUser.schools.add(s)
	# 				currentUser.save()
	# 			else:
	# 				currentUser.schools.add(models.School.objects.get(title=request.POST['schoolChoice-' + str(i + 1)]))
	# 		return redirect('deadlines')
	if request.method == 'POST':
		for i in range(4):
			try:
				models.School.objects.get(title=request.POST['myLink' + str(i + 1)])
			except:
				s = models.School.objects.create(title=request.POST['myLink' + str(i + 1)])
				s.save()
				currentUser.schools.add(s)
				currentUser.save()
			else:
				currentUser.schools.add(models.School.objects.get(title=request.POST['schoolChoice-' + str(i + 1)]))
		return redirect('deadlines')

	uniList = []
	with open('world-universities.csv', newline = '', encoding = 'utf-8') as file:
		fileRead = csv.reader(file, delimiter=',')
		for row in fileRead:
			if row[0] == 'US':
				uniList.append(row[1])
	context = {'uniList': uniList,
	  'numUnis': numChoices}
	return render(request, 'home.html', context)

def postgrad(request):
	uniList = []
	with open('world-universities.csv', newline = '', encoding = 'utf-8') as file:
		fileRead = csv.reader(file, delimiter=',')
		for row in fileRead:
			if row[0] == 'US':
				uniList.append(row[1])
	context = {'uniList': uniList}
	return render(request, 'postgrad.html', context)

def professional(request):
	return render(request, 'professional.html')

def deadlines(request):
	if request.method == 'POST':
		return redirect('home')
	currentUser = models.account.objects.last()
	context = []
	for school in currentUser.schools.all():
		with open('world-universities.csv', newline='', encoding='utf-8') as file:
			fileRead = csv.reader(file, delimiter=',')
			for row in fileRead:
				if row[1] == school.title:
					s = {'school': row[1], 'earlyD': row[3], 'earlyA': row[4], 'regular': row[5]}
					l = copy.deepcopy(s)
					context.append(l)
			file.close()
	contextSend = {'content': context}
	return render(request, 'deadlines.html', contextSend)
