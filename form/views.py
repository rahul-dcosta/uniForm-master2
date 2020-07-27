from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import models
import csv, copy, re

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
		SAT = request.POST['SAT']
		ACT = request.POST['ACT']
		TOEFL = request.POST['TOEFL']
		IELTS = request.POST['IELTS']
		p = models.account.objects.create(fullname=fullname, email=email, location=location, takeACT=ACT, takeSAT=SAT, takeIELTS=IELTS,takeTOEFL=TOEFL)
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
	selectedSchools = []
	if request.method == 'POST':
		for i in request.POST:
			if re.search("selectedSchool-.", i) != None:
				try:
					s = models.School.objects.get(title=request.POST[i])
				except:
					models.School.objects.create(title=request.POST[i])
					s = models.School.objects.get(title=request.POST[i])
					currentUser.schools.add(s)
				else:
					currentUser.schools.add(s)
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
		with open('us-universities.csv', newline='', encoding='utf-8') as file:
			fileRead = csv.reader(file, delimiter='|')
			for row in fileRead:
				print(row[1])
				if row[0] == school.title:
					s = {'school': row[0], 'earlyD': row[1], 'earlyA': row[2], 'regular': row[3]}
					l = copy.deepcopy(s)
					context.append(l)
					break
			file.close()

	contextSend = {'content': context}
	print(context)
	return render(request, 'deadlines.html', contextSend)
