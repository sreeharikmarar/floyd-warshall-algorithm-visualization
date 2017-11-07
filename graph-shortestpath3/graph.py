import wsgiref.handlers, os
import unicodedata
import cgi
import datetime
import urllib
import wsgiref.handlers


from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    def get(self):     
        html_title = 'Graph'
        html_body_text = 'All Source Shortest Path Algorithm - Floyd Warshall'

        template_values = {
            'html_title': html_title,
            'html_body_text': html_body_text,
            }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        outstr = template.render(path,template_values)
        self.response.out.write(unicode(outstr))
        
class ShortestPath:
	def GetPath (self,i,j,path,nxt,n):
        	if i>n or j>n or path[i][j] == 10000:
                	return "no path"
	        inter = nxt[i][j]
        	if inter == 0:
                	return " "
	        else:
        	        return self.GetPath(i,inter,path,nxt,n) +"%d,"%inter+ self.GetPath(inter,j,path,nxt,n)

	def GetPath2 (self,i,j,path,nxt,n):
        	if i>n or j>n or path[i][j] == 10000:
                	return "no path"
	        inter = nxt[i][j]
        	if inter == 0:
                	return " "
	        else:
        	        return self.GetPath2(i,inter,path,nxt,n) +" %d "%inter+ self.GetPath2(inter,j,path,nxt,n)

class AlgorithmWeights(webapp.RequestHandler):
    	def __init__(self, request, response):
        	self.initialize(request, response)
	def post(self):
		self.response.headers['Content-Type'] = "text/plain"
		adj_list =self.request.get_all("adj[]")  #reading list that send from jquery post
		nods = list(self.request.get_all("nods[]"))
		weight = self.request.get_all("edge_wt[]")
		dist = self.request.get_all("dist[]")

		for i in range(0, len(weight)):         #converting unicode string values of list into ascii values
			weight[i] = eval(weight[i]) 

		for i in range(0, len(dist)):         #converting unicode string values of list into ascii values
			dist[i] = eval(dist[i])


		n =int(self.request.get("length"))      #number of nodes in graph

		for i in range(1,len(adj_list)):		
			adj_list[i] = eval('['+adj_list[i]+']')	


		#construct weight matrix
		edge_weight = [[0]*n]
		for i in range(0,n-1):
			edge_weight.append([0]*n)
		count = 0
		while(count < len(weight)):
			w = weight[count]
			n1 = weight[count+1]
			n2 = weight[count+2]
			edge_weight[n1][n2] = w
			edge_weight[n2][n1] = w
			count = count+3


		#construct distance matrix
		
		


		#constructing path matrix
                global path,nxt
                path = [[0]*n]
                nxt = [[0]*n]
                for i in range(0,n-1):
                        nxt.append([0]*n)
                for i in range(1,n):
                        path.append([0]*n)
                        for j in range(1,n):
                                if i == j:
                                        path[i][j] = 0
                                else:
					for v in range(0, len(adj_list[i])):
						if adj_list[i][v] == j :
							path[i][j] = edge_weight[i][j]
					if path[i][j] == 0 :
						path[i][j] = 10000


                for k in range(1,n):
                        for i in range(1,n):
                                for j in range(1,n):
                                        if path[i][k] + path[k][j] < path[i][j]:
                                                path[i][j] = path[i][k]+path[k][j]
                                                nxt[i][j] = k

                sp = ShortestPath()

                for x in range(1,n):
                        for y in range(1,n):
                                if x != y :
                                        msg = sp.GetPath2(x,y,path,nxt,n)
                                        if msg != 'no path':
                                                display = 'Shortest path from %d to %d is :%d %s %d' %(x,y,x,msg,y)
                                        else:
                                                display = 'No path from %d to %d ' %(x,y)

					
                                        
                                        self.response.out.write(display)
                                        self.response.out.write("\n\n")
		

		    #constructing dist matrix

		
class BoxWeights(webapp.RequestHandler):
    	def __init__(self, request, response):
        	self.initialize(request, response)
	def post(self):
		self.response.headers['Content-Type'] = "text/plain"
		adj_list =self.request.get_all("adj[]")  #reading list that send from jquery post
		nods = list(self.request.get_all("nods[]"))
		weight = self.request.get_all("edge_wt[]")

		for i in range(0, len(weight)):         #converting unicode string values of list into ascii values
			weight[i] = eval(weight[i]) 

		n =int(self.request.get("length"))      #number of nodes in graph
		t1 = self.request.get("t1")
		t2 = self.request.get("t2")
		t1 = eval(t1)
		t2 = eval(t2)

		for i in range(1,len(adj_list)):		
			adj_list[i] = eval('['+adj_list[i]+']')	


		#construct weight matrix
		edge_weight = [[0]*n]
		for i in range(0,n-1):
			edge_weight.append([0]*n)
		count = 0
		while(count < len(weight)):
			w = weight[count]
			n1 = weight[count+1]
			n2 = weight[count+2]
			edge_weight[n1][n2] = w
			edge_weight[n2][n1] = w
			count = count+3

		#constructing path matrix
                global path,nxt
                path = [[0]*n]
                nxt = [[0]*n]
                for i in range(0,n-1):
                        nxt.append([0]*n)
                for i in range(1,n):
                        path.append([0]*n)
                        for j in range(1,n):
                                if i == j:
                                        path[i][j] = 0
                                else:
					for v in range(0, len(adj_list[i])):
						if adj_list[i][v] == j :
							path[i][j] = edge_weight[i][j]
					if path[i][j] == 0 :
						path[i][j] = 10000


                for k in range(1,n):
                        for i in range(1,n):
                                for j in range(1,n):
                                        if path[i][k] + path[k][j] < path[i][j]:
                                                path[i][j] = path[i][k]+path[k][j]
                                                nxt[i][j] = k

                sp = ShortestPath()
		msg = sp.GetPath(t1,t2,path,nxt,n)
		a = list(msg)
		self.response.out.write(a)

                if msg != 'no path':
                	display = t1,msg,t2
                else:
                	display = t1,t2

		
                              	
class Drawgraph(webapp.RequestHandler):
	def __init__(self, request, response):
        	self.initialize(request, response)
	def post(self):
		self.response.headers['Content-Type'] = "text/plain"
		adj_list =self.request.get_all("adj[]")  #reading list that send from jquery post
		nods = list(self.request.get_all("nods[]"))
		weight = self.request.get_all("edge_wt[]")

		for i in range(0, len(weight)):         #converting unicode string values of list into ascii values
			weight[i] = eval(weight[i]) 

		n =int(self.request.get("length"))      #number of nodes in graph
		t1 = self.request.get("t1")
		t2 = self.request.get("t2")
		t1 = eval(t1)
		t2 = eval(t2)

		for i in range(1,len(adj_list)):		
			adj_list[i] = eval('['+adj_list[i]+']')	


		#construct weight matrix
		edge_weight = [[0]*n]
		for i in range(0,n-1):
			edge_weight.append([0]*n)
		count = 0
		while(count < len(weight)):
			w = weight[count]
			n1 = weight[count+1]
			n2 = weight[count+2]
			edge_weight[n1][n2] = w
			edge_weight[n2][n1] = w
			count = count+3

		#constructing path matrix
                global path,nxt
                path = [[0]*n]
                nxt = [[0]*n]
                for i in range(0,n-1):
                        nxt.append([0]*n)
                for i in range(1,n):
                        path.append([0]*n)
                        for j in range(1,n):
                                if i == j:
                                        path[i][j] = 0
                                else:
					for v in range(0, len(adj_list[i])):
						if adj_list[i][v] == j :
							path[i][j] = edge_weight[i][j]
					if path[i][j] == 0 :
						path[i][j] = 10000


                for k in range(1,n):
                        for i in range(1,n):
                                for j in range(1,n):
                                        if path[i][k] + path[k][j] < path[i][j]:
                                                path[i][j] = path[i][k]+path[k][j]
                                                nxt[i][j] = k

                sp = ShortestPath()
		msg = sp.GetPath(t1,t2,path,nxt,n)
		
		z = list(msg)

		if z == [' ']:
			a = []
			a.insert(0,t1)
			a.insert(1,t2)
			self.response.out.write(a)

                elif msg == 'no path':
			a = 'no path'
			self.response.out.write(a)
			
                elif msg != 'no path':
                	a = eval(msg)
			b = list(a)
			c = len(b)+1
			
			b.insert(0,t1)
			b.insert(c,t2)

                	display = b
			self.response.out.write(display)
		
		else:
			self.response.out.write(' ')
		

def main():
        application = webapp.WSGIApplication(
                                     [('/', MainPage),('/byweight',AlgorithmWeights),('/byweight_bx',BoxWeights),('/draw', Drawgraph)],
                                     debug=True)
        wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
