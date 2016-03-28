import rhinoscriptsyntax as rs
import math as m

def spineJoin(crvs,rad,res,thres):
    sets = []
    old = []
    for i in range(len(crvs)):
        sects = []
        val = 0
        oldVal = 20
        pts = rs.DivideCurveLength(crvs[i],res)
        for j in range(len(pts)):
            param = rs.CurveClosestPoint(crvs[i],pts[j])
            tangents = rs.CurveTangent(crvs[i],param)
            plane = rs.PlaneFromNormal(pts[j],tangents)
            sect = rs.AddCircle(plane,rad)
            old.append(sect)
            for k in range(len(crvs)):
                if i!=k:
                    param = rs.CurveClosestPoint(crvs[k],pts[j])
                    attPt = rs.EvaluateCurve(crvs[k],param)
                    dist = rs.Distance(attPt,pts[j])
                    sectPts = rs.DivideCurve(sect,10)
                    if dist<rad*2:
                        for n in range(len(sectPts)):
                            attDist = rs.Distance(attPt,sectPts[n])
                            if attDist<rad and attDist!=0:
                                val = attDist/rad
                                vec = rs.VectorCreate(attPt,sectPts[n])*(1-val)
                                sectPts[n] = rs.PointAdd(sectPts[n],vec)
                    if abs(oldVal-val)>.2 or j==len(pts)-1 or j==0:
                        oldVal = val
                        sectPts.append(sectPts[0])
                        sects.append(rs.AddCurve(sectPts))
                    #rs.DeleteObject(sect)
        #sets.append(sects)
        rs.AddSweep1(crvs[i],sects)
        rs.DeleteObjects(old)
        sects = []
    return sets


def varyPipe(crv,attPt,rad,thres):
    set = []
    pts = rs.DivideCurve(crv,100)
    for j in range(len(pts)):
        param = rs.CurveClosestPoint(crv,pts[j])
        tangents = rs.CurveTangent(crv,param)
        plane = rs.PlaneFromNormal(pts[j],tangents)
        dist = rs.Distance(pts[j],attPt)
        if dist<thres:
            val = rad + rad*(1-dist/thres)
        else:
            val = rad
        sect = rs.AddCircle(plane,val)
        set.append(sect)
    srf = rs.AddSweep1(crv,set)
    rs.DeleteObjects(sect)
    return srf

def Main():
    spines = rs.GetObjects("Please select spines",rs.filter.curve)
    radius = rs.GetReal("Please enter desired spine radius",15)
    thres = rs.GetReal("Please enter merging distance",radius*5)
    vines = []
    thres = 300
    for i in range(len(spines)):
        vines.append(varyPipe(spines[i],rs.CurveMidPoint(spines[i]),radius,thres))
    return vines

Main()