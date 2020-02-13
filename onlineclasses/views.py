# onlineclasses/views.py

from django.shortcuts import render

# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, CreateView, UpdateView, View, DetailView
)
from django.core.exceptions import ObjectDoesNotExist
# from django.views.generic.edit import FormMixin
# import datetime
from django.utils import timezone
import pytz
# from django.db.models import Count, Q

from .models import *
from accounts.models import Student
from courses.models import Section
from learninglab.decorators import student_required, teacher_required
# from .forms import VoteForm

from grade.models import AttendanceInstance
from votes.models import Response, Question
import datetime

from votes.views import createAttendance

# #TODO:
# 	AttendanceInstance should be made when next video
#	Is there a need for the students to know who didn't vote yet? => 3/4 format
#	Disable not ready buttons.
#	Check if link is viable. ## CHECK URL Link. # Do it last
#	Attendance Created depending on the date?
#	Auto Download from google drive link.

@method_decorator(student_required, name='dispatch')
class VideoDetailView(CreateView):


	def get(self, request, *args, **kwargs):
		video = Video.objects.get(pk = kwargs["pk"])
		cur_student = request.user.student
		
		#messages.info(request,str(cur_student.group))

		#createVideoTracker(request,video,cur_student)
		createResponse(request,video,cur_student)

		#disable submit button if check is not successful
		cur_response = groupCheckFirstVote(request,video,cur_student)
		cur_discussion = groupCheckDiscussion(request,video,cur_student)


		return render(request,
            "onlineclasses/video_detail.html",
            {"video": video, "student": cur_student, "response":cur_response, "discussion":cur_discussion})

	def post(self, request, *args, **kwargs):

		# There is a need to block all POST if video is deactivated.

		video = Video.objects.get(pk = kwargs["pk"])
		cur_student = request.user.student
		student_response = Response.objects.filter(student=cur_student,question=video.question).first()

		# On first Vote
		if request.POST.get("first_vote") is not None:

			# If first vote is not selected.
			if request.POST.get("first_vote") is "":
				messages.warning(request,"You should select your first vote")
				return redirect("onlineclasses:detail", pk=kwargs["pk"],lecture_pk = video.lecture.pk)

			# if vote1 exist, nothing happens
			if student_response.vote1 is None:
				student_response.vote1 = request.POST.get("first_vote")
				student_response.save()
				messages.success(request,"First vote is set to" + str(student_response.vote1) +". Please start your discussion.")
			else:
				messages.warning(request,"You've already done the first vote as "+str(student_response.vote1))



		# On discussion link submit
		elif request.POST.get("discussion_link") is not None:

			# If discussion link is not submitted.
			if request.POST.get("discussion_link") is "":
				messages.warning(request,"Discisson_link does not exist")
				return redirect("onlineclasses:detail", pk=kwargs["pk"],lecture_pk = video.lecture.pk)


			# If some students in the group didn't submit vote1.
			if groupCheckFirstVote(request,video,cur_student) is False:
				messages.warning(request,"All of the group members should finish the first vote to proceed.")

			# If everybody did vote1
			else:
				updateDiscussionLink(request,video,cur_student.group,request.POST.get("discussion_link"))



		# On second vote
		elif request.POST.get("second_vote") is not None:

			# if second vote is not selected
			if request.POST.get("second_vote") is "":
				messages.warning(request,"second vote does not exist")

			# If group leader did not submit the discussion link
			if groupCheckDiscussion(request,video,cur_student) is False:
				messages.warning(request,"Discussion Link should be submitted by the group leader to proceed.")

			# If discussion link is submitted
			else:
				# if vote2 exist, nothing happens
				if student_response.vote2 is None:
					student_response.vote2 = request.POST.get("second_vote")
					student_response.save()
					messages.success(request,"Second vote is set to" + str(student_response.vote2) +".")

					# make student attendance
					createAttendance(cur_student,True)

				else:
					messages.warning(request,"You've already done the second vote as "+str(student_response.vote2))

		# On Next Video.
		elif "finish" in self.request.POST:
			return redirect("onlineclasses:list",lecture_pk = video.lecture.pk)


		#test
		# if request.POST.get("asdf") is not None:
		# 	messages.warning(request,"this is sent from asdf")



		#alert
		#messages.success(request, 'looking good!')


		return redirect("onlineclasses:detail", pk=kwargs["pk"],lecture_pk = video.lecture.pk)



class VideoListView(View):

    def get(self, request, *args, **kwargs):
        video_list = Video.objects.filter(lecture = kwargs["lecture_pk"])

        return render(request,
            "onlineclasses/video_list.html",
            {"video_list": video_list})



# Group is unique for each group!
def groupCheckFirstVote(request, video, student):

	group = student.group

	#group_members contains the student objects for a single group
	group_members=Student.objects.filter(group=group)
	pass_flag = True

	if not group_members:
		messages.warning(request,"group_members is None!")
		return

	#Count total vote
	voted = 0
	total = group_members.count()

	#Check if each student has done their first vote.
	#Some Students might not have a Response instance at all.
	for each_student in group_members:
		#messages.info(request,str(each_student))
		each_response = Response.objects.filter(student=each_student,question=video.question)
		#messages.info(request,str(each_student)+' '+str(each_response.first().vote1))

		# If there is no response yet.
		if each_response is None:
			pass_flag = False

			# add messages.warning here!

			continue

		# If there is no vote1 yet.
		try:
			each_response.first().vote1
		except:
			messages.warning(request,str(each_student)+"did not vote!")
			pass_flag = False

		# If voted, append 1
		voted += 1

			# add messages.warning here!



	return pass_flag



# def groupCheckSecondVote(lecture, group, var):
# 	if 


def groupCheckDiscussion(request, video, student):
	
	group = student.group

	link = DiscussionLink.objects.filter(group=student.group,video=video)

	pass_flag = True
	# Check if link is viable

	if not link:
		pass_flag = False

	return pass_flag



def createVideoTracker(request,video,student):
		ci = VideoTracker.objects.filter(student=student)
		#messages.info(request,"This is inside the create function with: "+str(ci))

		
		if not ci:
			vi = VideoTracker(student = student, video = video)
			vi.save()
			messages.success(request,"VideoTracker Instance created!")

		return

# Make Response if it doesn't exist
def createResponse(request,video,student):

		student_response = Response.objects.filter(student=student,question=video.question)
		
		# create new response. if not, 
		if not student_response:
			new_response = Response.objects.create(student=student,question=video.question)

			# to check
			#messages.info(request,"new response is created")
		else:
			# to check
			#essages.info(request,str(student_response)+"already exist!")
			pass

		return

def updateDiscussionLink(request,video,group,link):

	dl = DiscussionLink.objects.filter(video=video,group=group)

	if not dl:
		new_dl = DiscussionLink.objects.create(video=video,group=group,link=link)
	else:
		dl.first().link = link
		dl.first().save()