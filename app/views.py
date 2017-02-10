# -*- coding: utf-8 -*-
import urlparse
import json

from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.http import JsonResponse

from models import Sala, Debate, Usuario

from google import google, images
from google.modules.youtube_search import search

class SalaSession:
	def __init__(self):
		self.sala = None
		self.temas = []
		self.related_vids = []
		self.related_pesq = []
		self.embeds = []

	def set_sala(self, id):
		self.sala = Sala.objects.get(id=id)

	def sala_obj(self):
		if self.sala:
			obj = Sala.objects.get(id=self.sala.id)

			return obj

	def to_json(self):
		json = {
			"temas": self.temas,
			"related_vids": self.related_vids,
			"related_pesq": self.related_pesq,
			"embeds": self.embeds
		}
		if self.sala:
			json['sala'] = self.sala.to_json()

		return json

	def get_data(self, request):
		if request.session.get('sala_session'):
			data = json.loads(request.session['sala_session'])

			self.sala = self.sala_obj()
			self.temas = data['temas']
			self.related_vids = data['related_vids']
			self.related_pesq = data['related_pesq']
			self.embeds = data['embeds']

	def store_data(self, request):
		request.session['sala_session'] = json.dumps(self.to_json())


class IndexView(TemplateView):
	template_name = "index.html"

	def post(self, request, *args, **kwargs):
		ctx = self.get_context_data()
		if self.request.POST.get('dono'):
			sala = Sala(dono=self.request.POST['dono'])
			sala.nome = self.request.POST['nome']
			
			if not Usuario.objects.all().filter(nome=self.request.POST["dono"]):
				dono_usr = Usuario(nome=self.request.POST["dono"])
				dono_salas = []
				dono_salas.append(sala.id)
				
				dono_usr.salas = json.dumps(dono_salas)
				dono_usr.save()
			else:
				dono_usr = Usuario.objects.get(nome=self.request.POST["dono"])
				
				dono_salas = json.loads(dono_usr.salas)
				dono_salas.append(sala.id)
				
				dono_usr.salas = json.dumps(dono_salas)
				dono_usr.save()

			videos = self.request.POST['video'].split(",")
			embeds = []
			for v in videos:
				url_data = urlparse.urlparse(v)
				query = urlparse.parse_qs(url_data.query)
				video_id = query["v"][0]

				embeds.append("https://www.youtube.com/embed/" + video_id)

			sala.video = json.dumps(embeds)

			temas = self.request.POST['temas'].split(",")
			sala.temas = json.dumps(temas)

			membros = self.request.POST['membros'].split(",")
			for membro in membros:
				if not Usuario.objects.all().filter(nome=membro):
					membro_usr = Usuario(nome=membro)
					membro_usr.save()			
			sala.membros = json.dumps(membros)

			sala.save()

			return redirect("/" + str(sala.id))
		if self.request.POST.get('membro'):
			membro = self.request.POST['membro']
			sala = self.request.POST['sala']

			f = Sala.objects.all().filter(id=sala)
			if f:
				sala = f[0]
				membros = json.loads(sala.membros)

				for m in membros:
					if m == membro or membro == sala.dono:
						self.request.session["SALA"] = sala.id
						self.request.session["USR"] = membro
						return redirect("/" + str(sala.id))
					else:
						ctx['error_a'] = "Você não foi convidado para esta sala"
			else:
				ctx['error_a'] = "Sala não encontrada"

		return super(TemplateView, self).render_to_response(ctx)

class SalaView(TemplateView):
	template_name = "sala.html"
	get_services = ('avl', 'load_conts', 'send_cont')

	def __init__(self, *args, **kwargs):
		self.sess = SalaSession()

	def get(self, *args, **kwargs):
		ctx = self.get_context_data()
		cmd = self.request.GET.get('cmd')

		self.sess.set_sala(self.kwargs.get('pk'))
		self.sess.store_data(self.request)

		if cmd and cmd in self.get_services:
			return getattr(self, '_%s' % cmd)()

		return super(SalaView, self).get(*args, **kwargs)

	def _get_related_search(self, temas):
		temas_pesq = []

		for tema in temas:
			pesq = google.search(tema, 1)
			i = 0
			for p in pesq:
				i = i + 1
				if i < 4:
					obj = {
						"nome": p.name,
						"link": p.link,
						"desc": p.description
					}
					temas_pesq.append(obj)

		return temas_pesq

	def _get_related_vids(self, temas):
		rel_vids = []

		for tema in temas:
			yt_search = search(tema)
			i = 0
			for r in yt_search:
				i = i + 1
				if i < 3:
					obj = {
						"nome": r.name,
						"link": r.link,
						"thumb": r.thumb
					}
					rel_vids.append(obj)

		return rel_vids

	def get_context_data(self, *args, **kwargs):
		ctx = super(SalaView, self).get_context_data(*args, **kwargs)

		self.sess.get_data(self.request)
		if not self.request.session.get('sala_session'):
			self.sess.sala = Sala.objects.all().filter(id=self.kwargs.get('pk'))[0]
			self.sess.temas = json.loads(self.sess.sala.temas)
			self.sess.related_vids = self._get_related_vids(self.sess.temas)
			self.sess.related_pesq = self._get_related_search(self.sess.temas)
			self.sess.embeds = json.loads(self.sess.sala.video)

			self.sess.store_data(self.request)

			ctx = self.sess.to_json()
		else:
			self.sess.get_data(self.request)

			ctx = self.sess.to_json()
	
		if  Debate.objects.all().filter(sala=self.sess.sala_obj()):
			ctx['debates'] = Debate.objects.all().filter(sala=self.sess.sala)[0]
			ctx['conts'] = json.loads(ctx['debates'].conts)['conts']

		ctx['rel_vids'] = self.sess.related_vids

		return ctx

	def _avl(self):
		ctx = self.get_context_data()

		send = True
		avl = self.request.GET['avl']
		d = Debate.objects.all().filter(sala=self.sess.sala_obj())[0]

		conts = json.loads(d.conts)
		i = int(self.request.GET['cont'])
		c = conts['conts'][i]
			
		if c.get('usrs_aval'):
			usrs_aval = json.loads(c['usrs_aval'])
				
			for usr in usrs_aval:
				if usr == self.request.session['USR']:
					send = True
					
			usrs_aval.append(self.request.session['USR'])
				
			c['usrs_aval'] = json.dumps(usrs_aval)
		else:
			usrs_aval = [self.request.session['USR']]
			c['usrs_aval'] = json.dumps(usrs_aval)

		if avl == "apv":
			if not c.get('apv'):
				c['apv'] = 1
			else:
				c['apv'] += 1

		if avl == "rep":
			if not c.get('rep'):
				c['rep'] = 1
			else:
				c['rep'] += 1

		if c.get('apv') > c.get('rep'):
			ctx['color'] = "green"
		else:
			ctx['color'] = "red"
			
		if send == True:
			conts['conts'][i] = c
			o = Debate.objects.all().filter(sala=self.sess.sala_obj())[0]
			o.conts = json.dumps(conts)
			o.save()
			ctx['status'] = 1
			ctx['conts'] = conts['conts']

			return JsonResponse({'color': ctx['color']})
		else:
			return JsonResponse({'fail': 'Ja avaliou'})

	def _load_conts(self):
		tema = self.request.GET['update-conts']
		ctx = self.get_context_data()

		ctx['temas_pesq'] = self.sess.related_pesq
		
		d = Debate.objects.all().filter(sala=self.sess.sala_obj())[0]
		conts = json.loads(d.conts)
		res = []
		if not tema == "Todos":
			for c in conts['conts']:
				if c['tema'] == tema:
					res.append(c)
			
			ctx['conts'] = res
		else:
			ctx['conts'] = conts['conts']

		return render(self.request, "conts.html", ctx)

	def _send_cont(self):
		data = self.request.GET.get('data')
		ctx = self.get_context_data()
			
		if not Debate.objects.all().filter(sala=self.sess.sala_obj()):
			d = Debate(sala=self.sess.sala)
			obj = { 'conts': [json.loads(data)]}
			d.conts = json.dumps(obj)

			tema = json.loads(data)['tema']
			if not tema in self.sess.temas:
				self.sess.temas.append(tema)

				self.sess.sala.temas = json.dumps(self.sess.temas)
				self.sess.sala.save()

				self.sess.store_data(self.request)
				
			d.tops = "-"
			d.save()
			ctx['status'] = 1
		else:
			d = Debate.objects.all().filter(sala=self.sess.sala_obj())[0]
			obj = json.loads(d.conts)
			obj['conts'].append(json.loads(data))
			d.conts = json.dumps(obj)

			tema = json.loads(data)['tema']
			if not tema in self.sess.temas:
				self.sess.temas.append(tema)

				self.sess.sala.temas = json.dumps(self.sess.temas)
				self.sess.sala.save()
			d.save()
			ctx['status'] = 1

		return super(SalaView, self).render_to_response(ctx)