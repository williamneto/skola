# -*- coding: utf-8 -*-

from django.db import models

class Sala(models.Model):
	dono = models.CharField(max_length=1500)
	nome = models.CharField(max_length=1500)
	temas = models.CharField(max_length=3500)
	video = models.CharField(max_length=1500)
	membros = models.CharField(max_length=1500)

class Debate(models.Model):
	sala = models.ForeignKey(Sala)
	tops = models.CharField(max_length=1000)
	conts = models.TextField(max_length=10000000)