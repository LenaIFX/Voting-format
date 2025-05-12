from django.contrib import admin
from django.http import HttpResponse
from .models import UserInfo, UserAnswer
import pandas as pd

@admin.action(description="Export to Excel")
def export_to_excel(modeladmin, request, queryset):
    user_data = []
    for user in queryset:
        answers = UserAnswer.objects.filter(user=user)
        for answer in answers:
            user_data.append({
                'Username': user.username,
                'Role in SC': user.role_in_sc,
                'Years Working': user.years_working,
                'Date': user.date,
                'Time': user.time,
                'Graph Number': answer.graph_number,
                'Impact Value': answer.impact_value,
                'Probability Value': answer.probability_value,
            })
    df = pd.DataFrame(user_data)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="survey_data.xlsx"'
    df.to_excel(response, index=False)
    return response

class UserInfoAdmin(admin.ModelAdmin):
    actions = [export_to_excel]

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(UserAnswer)