# -*- coding: utf-8 -*-
import urlparse
import json

from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.http import JsonResponse

from models import Sala, Debate

from google import google, images

class IndexView(TemplateView):
	template_name = "index.html"

	def post(self, request, *args, **kwargs):
		ctx = self.get_context_data()
		if self.request.POST.get('dono'):
			sala = Sala(dono=self.request.POST['dono'])
			sala.nome = self.request.POST['nome']

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
					if m == membro:
						return redirect("/" + str(sala.id))
					else:
						ctx['error_a'] = "Você não foi convidado para esta sala"
			else:
				ctx['error_a'] = "Sala não encontrada"

		return super(TemplateView, self).render_to_response(ctx)

class SalaView(TemplateView):
	template_name = "sala.html"

	def get_context_data(self, *args, **kwargs):
		ctx = super(SalaView, self).get_context_data(*args, **kwargs)

		ctx['sala'] = Sala.objects.all().filter(id=self.kwargs.get('pk'))[0]
		if  Debate.objects.all().filter(sala=ctx['sala']):
			ctx['debates'] = Debate.objects.all().filter(sala=ctx['sala'])[0]
			ctx['conts'] = json.loads(ctx['debates'].conts)['conts']
		ctx['temas'] = json.loads(ctx['sala'].temas)
		ctx['embeds'] = json.loads(ctx['sala'].video)
		return ctx

	def get(self, *args, **kwargs):
		ctx = self.get_context_data()

		if self.request.GET.get('avl'):
			avl = self.request.GET['avl']
			d = Debate.objects.all().filter(sala=ctx['sala'])[0]

			conts = json.loads(d.conts)
			i = int(self.request.GET['cont'])
			c = conts['conts'][i]

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

			conts['conts'][i] = c
			o = Debate.objects.all().filter(sala=ctx['sala'])[0]
			o.conts = json.dumps(conts)
			o.save()
			ctx['status'] = 1
			ctx['conts'] = conts['conts']

			return JsonResponse({'color': ctx['color']})

		if self.request.GET.get('update-conts'):
			tema = self.request.GET['update-conts']
			
			json_o = []
			for t in ctx['temas']:
				pesq = google.search(t,1)
				
				objs = []
				for p in pesq:
					obj = {
						"nome": p.name,
						"link": p.link
					}
					objs.append(obj)
				json_o.append({'tema': t, 'pesq': objs})
			ctx['temas_pesq'] = json_o
			
			d = Debate.objects.all().filter(sala=ctx['sala'])[0]

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

		if self.request.GET.get('data'):
			data = self.request.GET.get('data')
			
			if not Debate.objects.all().filter(sala=ctx['sala']):
				d = Debate(sala=ctx['sala'])
				obj = { 'conts': [json.loads(data)]}
				d.conts = json.dumps(obj)

				tema = json.loads(data)['tema']
				if not tema in ctx['temas']:
					ctx['temas'].append(tema)
					ctx['sala'].temas = json.dumps(ctx['temas'])
					ctx['sala'].save()
					
				d.tops = "-"
				d.save()
				ctx['status'] = 1
			else:
				d = Debate.objects.all().filter(sala=ctx['sala'])[0]
				obj = json.loads(d.conts)
				obj['conts'].append(json.loads(data))
				d.conts = json.dumps(obj)

				tema = json.loads(data)['tema']
				if not tema in ctx['temas']:
					ctx['temas'].append(tema)
					ctx['sala'].temas = json.dumps(ctx['temas'])
					ctx['sala'].save()

				d.save()
				ctx['status'] = 1

		return super(SalaView, self).render_to_response(ctx)
