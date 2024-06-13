"""
URL configuration for matrixpollingserver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from api import views as apiviews
from gui import views as guiviews
from fm import views as fmviews
from django.urls import path

urlpatterns = [
    path('api', apiviews.index),
    path('api/request', apiviews.makeRequest),
    path('api/poll', apiviews.poll),
    path('api/reg_user', apiviews.regUser),
    path('api/set_user_pass', apiviews.setUserPass),
    path('api/new_user_session', apiviews.newUserSession),
    path('api/reg_matrix', apiviews.regMatrix),
    path('api/delete_matrix', apiviews.deleteMatrix),
    path('api/exit_current_session', apiviews.exitCurrentSession),
    path('api/exit_all_sessions', apiviews.exitAllSessions),
    path('api/new_matrix_session', apiviews.newMatrixSession),
    path('api/exit_current_matrix_session', apiviews.exitCurrentMatrixSession),
    path('api/exit_all_matrix_sessions', apiviews.exitAllMatrixSessions),
    path('api/get_all_matrixes', apiviews.getAllMatrixes),
    path('fm/get_file', fmviews.getFile),
    path('matrix_control/<str:matrix_id>/<str:url>', guiviews.matrixControl)
]
