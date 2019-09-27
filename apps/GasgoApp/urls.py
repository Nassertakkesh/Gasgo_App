from django.conf.urls import url
from . import views



               
urlpatterns = [
    url(r'^$', views.index),
    url(r'^driverReg$', views.preregisterD),
    url(r'^driverRegistration$', views.registerD),
    url(r'^driverLog$', views.preLoginD),
    url(r'^driverLogin$', views.loginD),   
    url(r'^fillerReg$', views.preregisterF),
    url(r'^fillerRegistration$', views.registerF),
    url(r'^fillerLog$', views.preLoginF),
    url(r'^fillerLogin$', views.loginF),    
    url(r'^charge$', views.charge),
    url(r'^checkout2$', views.checkout2),
    url(r'^successDriver$', views.successDriver),
    url(r'^successFiller$', views.successFiller),
    url(r'^submitFillerFrom$', views.submitFillerFrom),
    url(r'^confirmation$', views.confirmation),
    url(r'^accepted$', views.accepted),
    url(r'^history$', views.History),
    url(r'^yourOrders$', views.yourOrders),
    url(r'^successDriver/accepted/(?P<id>\d+)$', views.accepted),
    url(r'^successDriver/completed/(?P<id>\d+)$', views.completed),
    
    url(r'^successDriver/cancel/(?P<id>\d+)$', views.cancel),
    url(r'^successDriver/view/(?P<id>\d+)$', views.viewPage),

    url(r'^logout$', views.logout),


    # url(r'^login$', views.login),
    # url(r'^book$', views.presuccess)

]