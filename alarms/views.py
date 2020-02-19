from django.views.generic import TemplateView
from . import models
import json
from django.shortcuts import HttpResponse


# Alarm, ShareMe 페이지 - username 정보 받음
class Alarm(TemplateView):
    template_name = 'alarm.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data()
        context['username'] = self.request.user.user_profile.name

        return context


class ShareMe(TemplateView):
    template_name = "ShareMe.html"

    def get_context_data(self, **kwargs):
        context=super(TemplateView, self).get_context_data()
        context['username']=self.request.user.user_profile.name

        return context

    def post(self, request, **kwargs):
        ins=models.Alarm()
        data_unicode = request.body.decode('utf-8')
        data=json.loads(data_unicode) # template에서 받은 data를 load한다
        ins.message = data['message'] # template에서 받은 data를 alarm 모델에 적용
        ins.save()

        return HttpResponse('')