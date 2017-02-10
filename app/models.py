# -*- coding: utf-8 -*-

from django.db import models

class Sala(models.Model):
	dono = models.CharField(max_length=1500)
	nome = models.CharField(max_length=1500)
	temas = models.CharField(max_length=3500)
	video = models.CharField(max_length=1500)
	membros = models.CharField(max_length=1500)

	def to_json(self):
		json = {
			"id": self.id,
			"dono": self.dono,
			"nome": self.nome,
			"temas": self.temas,
			"video": self.video,
			"membros": self.membros
		}

		return json

class Debate(models.Model):
	sala = models.ForeignKey(Sala)
	tops = models.CharField(max_length=1000)
	conts = models.TextField(max_length=10000000)

class Usuario(models.Model):
	nome = models.CharField(max_length=300)
	salas = models.CharField(
		max_length=400,
		blank=True
	)
