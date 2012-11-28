# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
     (r'^$', views.index),
     (r'^anual/$', views.anual),
     (r'^simples/$', views.simples),
     (r'^ajustes/$', views.ajustes),
     (r'^despesas/$', views.lista_despesas),
     url(r'^vendas_por_mesa/$', views.view_relatorio, kwargs={ "titulo": "Vendas", "tablemakers": [views.vendas_por_mesa] }),
     url(r'^vendas_por_categoria/$', views.view_relatorio, kwargs={ "titulo": "Vendas", "tablemakers": [views.vendas_por_categoria] }),
     url(r'^vendas_por_cidade/$', views.view_relatorio, kwargs={ "titulo": "Vendas", "tablemakers": [views.vendas_por_cidade] }),
     url(r'^vendas_por_dia_da_semana/$', views.view_relatorio, kwargs={ "titulo": "Vendas", "tablemakers": [views.vendas_por_dia_da_semana] }),
     url(r'^vendas/$', views.view_relatorio, kwargs={ "titulo": "Vendas",
                                                      "tablemakers": [views.vendas_por_mesa, views.vendas_por_categoria,
                                                                      views.vendas_por_dia_da_semana, views.vendas_por_cidade]
                                                     }),
     url(r'^pgtos_por_bandeira/$', views.view_relatorio, kwargs={ "titulo": "Pagamentos com cartão", "tablemakers": [views.pgtos_por_bandeira] }),
     url(r'^despesas_por_categoria/$', views.view_relatorio, kwargs={ "titulo": "Despesas", "tablemakers": [views.despesas_por_categoria] }),
     url(r'^movbancarias_por_categoria/$', views.view_relatorio, kwargs={ "titulo": u"Movimentações bancárias", "tablemakers": [views.movbancarias_por_categoria] }),
)