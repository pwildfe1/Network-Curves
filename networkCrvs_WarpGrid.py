import rhinoscriptsyntax as rs
import math as m
import random as r

def warpCrvs(crvs,res,ratio,thres,gen):
    min=100000000000
    attPts = []
    for n in range(gen):
        for i in range(len(crvs)):
            pts = rs.DivideCurveLength(crvs[i],res)
            for j in range(len(pts)):
                for k in range(len(crvs)):
                    if i!=k:
                        param = rs.CurveClosestPoint(crvs[k],pts[j])
                        attPt = rs.EvaluateCurve(crvs[k],param)
                        if rs.Distance(attPt,pts[j])>0:
                            attPts.append(attPt)
                index = rs.PointArrayClosestPoint(attPts,pts[j])
                closeAttPt = attPts[index]
                if j==0 or j==len(pts)-1:
                    r = 0
                else:
                    r = ratio
                if rs.Distance(closeAttPt,pts[j])<thres:
                    vec = rs.VectorCreate(pts[j],closeAttPt)
                    pts[j] = rs.PointAdd(pts[j],-vec*r)
                attPts = []
            rs.DeleteObject(crvs[i])
            crvs[i] = rs.AddCurve(pts)
    return crvs

def warpCrvsAttPt(crvs,res,ratio,thres,gen,attractors,strength):
    min=100000000000
    attPts = []
    for n in range(gen):
        for i in range(len(crvs)):
            pts = rs.DivideCurveLength(crvs[i],res)
            for j in range(len(pts)):
                for k in range(len(crvs)):
                    if i!=k:
                        param = rs.CurveClosestPoint(crvs[k],pts[j])
                        attPt = rs.EvaluateCurve(crvs[k],param)
                        if rs.Distance(attPt,pts[j])>0:
                            attPts.append(attPt)
                ########### attractor Point##########
                sum = 0
                num = 0
                for k in range(len(attractors)):
                    dist = rs.Distance(attractors[k],pts[j])
                    if dist<strength:
                        sum = dist+sum
                        num = num+1
                if num>0:
                    factor = sum/num
                    val = 1-factor/strength
                else:
                    val = .5
                ########### end attractor ##########
                index = rs.PointArrayClosestPoint(attPts,pts[j])
                closeAttPt = attPts[index]
                if rs.Distance(closeAttPt,pts[j])<thres:
                    vec = rs.VectorCreate(pts[j],closeAttPt)
                    pts[j] = rs.PointAdd(pts[j],-vec*ratio*val)
                attPts = []
            rs.DeleteObject(crvs[i])
            crvs[i] = rs.AddCurve(pts)

def Main():
    crvs = rs.GetObjects("Please select curves",rs.filter.curve)
    attractors = rs.GetObjects("please select attractors",rs.filter.point)
    strength = rs.GetReal("please enter desired strength",100)
    res = rs.GetReal("Please select resolution",3)
    thres = rs.GetReal("Please select threshold",25)
    ratio = rs.GetReal("Please select ratio of snap",1.5)
    gen = rs.GetInteger("Please enter number of generations",5)
    #r.shuffle(crvs)
    rs.EnableRedraw(False)
    #crvs = warpCrvs01(crvs,res,ratio,thres)
    #thres = thresRatio*res
    crvs = warpCrvsAttPt(crvs,res,ratio,thres,gen,attractors,strength)
    rs.EnableRedraw(True)
    return crvs

Main()