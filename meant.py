#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import commands
import re
import os.path
import math
import time



def checkExeExists(cmd):
    status = False
    l = re.findall(r'(\S+)(\s+.+)?', cmd)

    try: 
        exe = l[0][0]
    except:
        return False 
        
    wout = commands.getstatusoutput('which ' + exe)
    exists = os.path.isfile(exe)
        
    return (wout[0] == 0 or exists)


def conTime(out):
    l = re.findall(r'([\d+]?)(\d+):(\d+.\d+) real', out)
    t = (float(l[0][1]) * 60) + float(l[0][2])
    if l[0][0] != "":
        t = (float(l[0][0]) * 3600) + t
    
    return t
    

def conUserRegex(out, userRegex):
    l = re.findall(r'' + userRegex, out)
    try:
        t = 0
        if type(l[0]) == list:            
            if len(l[0]) == 1:
                t = float(l[0][0])
            elif len(l[0]) == 2:
                t = (float(l[0][0]) * 60) + float(l[0][1])
            elif len(l[0]) == 3:
                t = (float(l[0][0]) * 3600) + (float(l[0][1]) * 60) + float(l[0][2])
            else:
                raise Exception("Bad regex")
        else:
            t = float(l[0])
            
        return t
    except:
        print >>sys.stderr, "\nLa expresión regular introducida no es válida"
        exit(1)


def sacarTiempo(cmd, unixTime, userRegex):
    while (True):  # Si el programa devuelve error vuelve a ejecutarlo
        out = commands.getstatusoutput(cmd)
        if out[0] == 0:
            if unixTime:
                t = conTime(out[1])
            else:
                t = conUserRegex(out[1], userRegex)
            break
  
    return t 


def calculaMedia(cmd, pasadas, unixTime, userRegex):
    print "Iniciando el calculo del tiempo medio..."
  
    ltiempos = []
  
    for n in range(0, pasadas):
        sys.stdout.write("  Calculando tiempo [" + str(n+1) + "]")
        sys.stdout.flush()
        t = sacarTiempo(cmd, unixTime, userRegex)
        print ":\t%4.3f s" % (t)
        ltiempos.append(t)
        
    return ltiempos


def muestraResultados(ltiempos, graph=False, graphST=False, graphName="graph.png"):
    nMuestras = len(ltiempos)
    media = sum([x for x in ltiempos]) / nMuestras
    varianza = sum([(x-media)**2 for x in ltiempos]) / len(ltiempos)
    dTipica = math.sqrt(varianza)
	
    print "Tiempo medio para", nMuestras, "ejecuciones:", media, "s"
    print "Desviación típica para", nMuestras, "ejecuciones:", dTipica, "s"
    if graph:
        draw(ltiempos, media, dTipica, graphST, graphName)


def draw(ltiempos, media, dTipica, graphST, graphName):
    import matplotlib.pyplot as plt
 
    plt.figure()
    
    # En x numero de pasadas
    x = range(1, len(ltiempos)+1)
    
    # En la recta de la media todas las y = media
    y_mean = [media for i in range(len(ltiempos))]
 
    #plot the two lines
    plt.plot(x, ltiempos, 'bo')
    plt.plot(x, y_mean, 'r')
    
    if graphST:
        y_plusST = [media+dTipica for i in range(len(ltiempos))]
        y_minusST = [media-dTipica for i in range(len(ltiempos))]
        plt.plot(x, y_plusST, 'k')
        plt.plot(x, y_minusST, 'k')
        
        legend = '\mu=' +  str(round(media, 3)) + ',\ \sigma=' + str(round(dTipica, 3))
    else:
        legend = '\mu=' +  str(round(media, 3))
    
    plt.text(1.5, media+.005, r'$' + legend + '$', bbox={'facecolor':'red', 'alpha':0.8, 'pad':5})
    plt.axis([1, len(ltiempos), min(ltiempos)-0.05, max(ltiempos)+0.05])
    plt.grid(True)

    plt.savefig(graphName)


def meant(argv):
    
    cmd = ""
    unixTime = True
    userRegex = ""
    graph = False
    graphST = False
    graphName = ""
    pasadas = 20
	
  
    # Se leen los argumentos
    i = 0
    while (i < len(argv)-1): 
        if (argv[i] == "-n"): # Pasadas
            try:
                pasadas = int(argv[i + 1])
                if (pasadas < 1):
                    raise Exception("Invalid repeat number")
                i += 1
            except:
                print >>sys.stderr, "Parámetros inválidos"
                exit(1)
                
        elif (argv[i] == "-u"): # User Regex
            try:
                userRegex = argv[i + 1]
                unixTime = False
                i += 1
            except:
                print >>sys.stderr, "Parámetros inválidos"
                exit(1)

        elif (argv[i] == "-g"): # Graph
            graph = True

            
        elif (argv[i] == "-gst"): # Graph with standard deviation
            graph = True
            graphST = True
            
        elif (argv[i] == "-gname"):
            try:
                graphName = argv[i + 1]
                if os.path.isfile(graphName):
                    raise Exception("Invalid filename for graph")
                i += 1
            except:
                print >>sys.stderr, "Parámetros inválidos"
                exit(1)

        else:
            print >>sys.stderr, "Parámetro desconocido:", argv[i]
            exit(1)
            
        i += 1
    
    # CMD
    try:
        if not checkExeExists(argv[i]):
            raise Exception("Invalid app to measure")
        if unixTime:
            cmd = "time -f \"%E real\" " + argv[i]
        else:
            cmd = argv[i]
    except:
        print >>sys.stderr, "El ejecutable a medir no existe"
        exit(1)
        
    # Nombre por defecto para el fichero con el gráfico    
    if graph and graphName == "":
        graphName = "graph_" + str(int(time.time())) + ".png"
    
    # Ejecuta el programa y calcula tiempos de ejecución    
    ltiempos = calculaMedia(cmd, pasadas, unixTime, userRegex)
    muestraResultados(ltiempos, graph, graphST, graphName)
  

# MAIN
if __name__ == '__main__':
    argc = len(sys.argv)  # Número de agumentos

    if argc < 2:
        print >>sys.stderr, "USAGE:", sys.argv[0], "[-n repeats] [-u regex] [-g|-gst] [-gname filename] 'app to measure'"
        exit(1)
        
    meant(sys.argv[1:])
