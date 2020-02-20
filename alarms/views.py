from django.http import request
from django.views.generic import TemplateView

from group_management.models import CustomGroup
from . import models
import json
from django.shortcuts import HttpResponse, redirect, render


# Alarm, ShareMe 페이지 - username 정보 받음
class Alarm(TemplateView):
    template_name = 'alarm.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data()
        context['username'] = self.request.user.user_profile.name

        return context


# class ShareMe(TemplateView):
#     template_name = "ShareMe.html"
#
#     def get_context_data(self, **kwargs):
#         context=super(TemplateView, self).get_context_data()
#         context['username']=self.request.user.user_profile.name
#
#         return context
#
#     def post(self, request, **kwargs):
#         ins=models.Alarm()
#         data_unicode = request.body.decode('utf-8')
#         data=json.loads(data_unicode) # template에서 받은 data를 load한다
#         ins.message = data['message'] # template에서 받은 data를 alarm 모델에 적용
#         ins.save()
#
#         return HttpResponse('')

# todo 김유빈
class RequestGroup(TemplateView):
    template_name = "RequestGroup.html"

    #template setting
    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data()
        context['username'] = self.request.user.user_profile.name

        return context

    #template에서 온 수신 처리
    def post(self, request, **kwargs):

        ins = models.Alarm()  # 모든 알람 가져오기
        data_unicode = request.body.decode('utf-8')
        data = json.loads(data_unicode)  # template에서 받은 data를 load한다
        ins.message = data['message']  # template에서 받은 data를 alarm 모델에 적용
        #request_group = CustomGroup.objects.get(pk=pk)
        ins.receiver = request.user  # 그룹으로 해야하는데 ㅠㅠㅠ
        ins.save()

        return HttpResponse('')


def alarm_detail(request):
    alarms = models.Alarm(receiver=request.user)
    if alarms != None:
        return render(request, 'alarm_detail.html', {
            'alarms': alarms,
        })
    else:
        return

# delete를 안 먹음....
def alarm_delete(request):
    alarms = request.POST.get('alarms', None)
    alarms.delete()

    return redirect('alarms:alarm_detail')
