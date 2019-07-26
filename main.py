#!/usr/local/epics/modules/pythonIoc/pythonIoc
import epics
import time
from datetime import datetime
import string
import threading
import code
import math
from softioc import softioc,builder
from shutil import copyfile


firsttpc = ["CathodeVoltageReadback"]
fee = []
fee1 = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"]
fee2 = ["1","2","3","4","5","6"]
for i in fee1:
  for j in fee2:
    pv = ""
    pv += "lv_sect"+i+"_nod"+j+"_alarm"
    fee.append(pv)
tpcCheck = ["CathodeVoltageReadback","tpc_grid_leak:avrgVoltInner","tpc_grid_leak:avrgVoltOuter"]
gridleakpvs = ["tpc_grid_leak:avrgVoltInner","tpc_grid_leak:avrgVoltOuter"]
tpcnames = ["Cathode","FEE","Grid Leak Inner","Grid Leak Outer"]
tpcGG = ["tpc_grid_leak:avrgVoltInner","tpc_grid_leak:avrgVoltOuter"]
tpclabels = ["Cathode: ",""," ", " "]
ggnames = ["Grid Leak Inner", "Grid Leak Outer"]
tof = ["TOF:HV:AllSectors","TOF:HV:Standby"]
etof = ["ETOF:HV:AllSectors","ETOF:HV:Standby"]
#trigger = ["ZDC_status_TRIG","ZDCSMD_status_TRIG","UPVPD_status_TRIG","BBC_status_TRIG"]
trigZDC = ["BBCHV:09:01:vset","BBCHV:09:02:vset","BBCHV:09:03:vset","BBCHV:07:02:vset","BBCHV:07:03:vset","BBCHV:07:05:vset"]
trigZDCSMD = ["BBCHV:06:02:vset","BBCHV:06:03:vset"]
trigVPD = []
VPD13 = ["00","01","03","04","05","06","08","09","10","11","12","14","15"]
for i in VPD13:
  pv = ""
  pv += "BBCHV:13:"+i+":vset"
  trigVPD.append(pv)
VPD14 = ["00","01","03","04","05","06","08","09","10","11","13","14","15"]
for i in VPD14:
  pv = ""
  pv += "BBCHV:14:"+i+":vset"
  trigVPD.append(pv)
VPD15 = ["00","01","03","04","05","06","08","09","10","11","13","14"]
for i in VPD15:
  pv = ""
  pv += "BBCHV:15:"+i+":vset"
  trigVPD.append(pv)
trigBBC = []
BBC00 = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"]
for i in BBC00:
  pv = ""
  pv += "BBCHV:00:"+i+":vset"
  trigBBC.append(pv)
BBC02 = ["00","01","02","03","04","05","08","09","10","11","12","13","14","15"]
for i in BBC02:
  pv = ""
  pv += "BBCHV:02:"+i+":vset"
  trigBBC.append(pv)
trigBBC.append("BBCHV:03:08:vset")
trigBBC.append("BBCHV:03:10:vset")
triggernames = ["ZDC", "ZDC SMD","upVPD","BBC"]
interlocks1 = ["int_row1_alm0.SEVR","int_row1_alm1.SEVR","int_row1_alm2.SEVR","int_row1_alm3.SEVR","int_row1_alm4.SEVR","int_row1_alm5.SEVR","int_row1_alm6.SEVR","int_row1_alm7.SEVR"]
interlocks2 = ["int_row2_alm0.SEVR","int_row2_alm1.SEVR","int_row2_alm2.SEVR","int_row2_alm3.SEVR","int_row2_alm4.SEVR","int_row2_alm5.SEVR","int_row2_alm6.SEVR","int_row2_alm7.SEVR"]
interlocks3 = ["int_row3_alm0.SEVR","int_row3_alm1.SEVR","int_row3_alm2.SEVR","int_row3_alm3.SEVR","int_row3_alm4.SEVR","int_row3_alm5.SEVR","int_row3_alm6.SEVR","int_row3_alm7.SEVR"]
interlocks4 = ["int_row4_alm0.SEVR","int_row4_alm1.SEVR","int_row4_alm2.SEVR","int_row4_alm3.SEVR","int_row4_alm4.SEVR","int_row4_alm5.SEVR","int_row4_alm6.SEVR","int_row4_alm7.SEVR"]
magnet1nam = ["main Magnet","ptt West","ptt East","trim West", "trim East"]
magnet2 = ["cdev_mainMagnet2","cdev_pttWest2","cdev_pttEast2","cdev_trimWest2","cdev_trimEast2"]
magnet22 = ["MM ","pttw ","ptte ","trimw ","trime "]
weather1 = ["dew_val1","dew_val2","dew_val3"]
weathertext = ["Humidity: ", "Temperature: ", "Dew: "]
weather2 = ["RHumidity","TemperatureF","DewPointF"]
scalers1 = ["rich_1151E_val1","rich_1151E_val2","rich_1151E_val3","rich_1151E_val8"]
scalers11 = ["BBC E --> ", "BBC W --> ", "BBC And ---> ", "ZDC And ---> "]
scalers2 = ["rich_1151E_val4","rich_1151E_val5","rich_1151E_val6","rich_1151E_val7"]
scalers22 = ["Yellow Back ---> ", "Blue Back ---> ", "ZDC E ---> ","ZDC W ---> "]
scalers3 = ["rich_1151E_val9","rich_1151E_val10","rich_1151E_val11","rich_1151E_val12"]
scalers33 = ["VPD E ---> ","VPD W ---> ", "VPD E W ---> ","TOF ---> "]
scalers4 = ["rich_1151E_val13","rich_1151E_val14","rich_1151E_val15","rich_1151E_val16"]
scalers44 = ["BBC and Lumi ---> ","BBCE Large ---> ","BBCW Large ---> ", "MTD ---> "]
boards = ["00","02","04","06","08","10","12","14"]
channels = ["000","001","002","003","004","005","006","007","008","009","010","011","012","013","014","015","016","017","018","019","020","021","022","023"]
Anode = []
for i in boards:
  for j in channels:
    pv = ""
    pv += "SY4527:"+i+":"+j+":VMon"
    Anode.append(pv)
AnodeSev = []
for i in Anode:
  AnodeSev.append(i+".SEVR")
letters = ["A","B","C"]
numbers = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48"]
GG = []
for i in letters:
  for j in numbers:
    pv = ""
    pv += "GG_A_In_"+i+"_"+j
    GG.append(pv)
GGSev = []
for i in GG:
  GGSev.append(i+".SEVR")
#Interlocks, 1


class Pvs:
  def __init__(self,pvlist):
    self.pvlist = pvlist
    self.pvs = []
    for i in pvlist:
      self.pvs.append(epics.PV(i))
    #self.getpvs = []
    #for i in self.pvs:
    #  self.getpvs.append(i.get())
  
  #def printme(self):
  #  return self.getpvs

  def includetext(self,namelist):
    self.namelist = namelist
    fillstring = ""
    for idx, value in enumerate(self.pvs):
      try:
        label = namelist[idx]
        pv = value.get()
        fillstring += "<td>" + label + "%.3f </td>" % pv
      except:
        fillstring += "<td> Error </td>"
    return fillstring
  
  def tablestart(self,label):
    self.label = label
    fillstring = ""
    fillstring += """
    <head> <style>
    br, table, th, td {border: 1px solid black; border-collapse:collapse;} 
    </style></head><body><h2></h2><table style="width:100%">
    <tr><td style = 'background-color:#ABD7E5;'>
    <font color =' #A32E2E'><b>
    """
    fillstring += """
    {0} </b></font></td>
    """.format(label)

    return fillstring

  def gatingGrid(self):
    fillstring = ""
    mycheck = True
    for i in self.pvs:
      try:
        assert type(i.get()) == int
        val = i.get()
        if val == 0:
          mycheck = False
          break
      except:
        return "<td style='background-color:#FFFFFF;'> NOT CONNECTED </td>"
        break
    if mycheck:
      fillstring += "<td style='background-color:#8FED8F;'> On </td>"
    else:
      fillstring += "<td style='background-color:red;'> Off </td>"
    return fillstring 

  def interlocks(self,namelist):
    self.namelist = namelist
    fillstring = ""
    for idx,i in enumerate(self.pvs):
      try:
        if i.get() == 0:
          fillstring += "<td style='background-color:#8FED8F;'> {0} </td>".format(namelist[idx])
        else:
          fillstring += "<td style='background-color:red;'> {0} </td>".format(namelist[idx])
      except:
        fillstring += "<td style='background-color:#FFFFFF;'> NOT CONNECTED </td>"
    return fillstring

  def interlocks2(self,namelist):
    self.namelist = namelist
    fillstring = ""
    for idx,i in enumerate(self.pvs):
      try:
        if i.get() == 0:
          fillstring += "<td style='background-color:red;'> {0} </td>".format(namelist[idx])
        else:
          fillstring += "<td style='background-color:#8FED8F;'> {0} </td>".format(namelist[idx])
      except:
        fillstring += "<td style='background-color:FFFFFF;'> NOT CONNECTED </td>"
    return fillstring

  # only use this method for the object 'magnet' 
  def magnettable(self,textlist):
    self.textlist = textlist
    table = ""
    for idx, value in enumerate(self.pvs):
      try:
        val = value.get()
        val = round(val, 2)
        text = textlist[idx] + str(val)
        if (self.pvs[idx] == self.pvs[0]) & (val < 4497 or val > 4543):
          table += "<td style ='background-color:red;'> {0} </td>".format(text)
        elif (self.pvs[idx] == self.pvs[1]) & (val < 1328 or val > 1332):
          table += "<td style ='background-color:red;'> {0} </td>".format(text)
        elif (self.pvs[idx] == self.pvs[2]) & (val < 1328 or val > 1332):
          table += "<td style ='background-color:red;'> {0} </td>".format(text)
        elif (self.pvs[idx] == self.pvs[3]) & (val < 565.5 or val > 576.5):
          table += "<td style ='background-color:red;'> {0} </td>".format(text)
        elif (self.pvs[idx] == self.pvs[4]) & (val < 573 or val > 577):
          table += "<td style ='background-color:red;'> {0} </td>".format(text)
        else:
          table += """
          <td style=background-color:#8FED8F;'> {0} </td>
          """.format(text)
      except:
        table += "<td style='background-color:#FFFFFF> NOT CONNECTED </td>"
    return table

  def magnettext(self):
    table = ""
    for idx,value in enumerate(magnet.pvs):
      try:
        val = value.get()
        val = round(val, 2)
        text = self.pvlist[idx]
        if (magnet.pvs[idx] == magnet.pvs[0]) & (val < 4497 or val > 4543):
          table += "<td style ='background-color:red;'> {0} </td>".format(text)
        elif (magnet.pvs[idx] == magnet.pvs[1]) & (val < 1328 or val > 1332):
          table += "<td style ='background-color:red;'> {0} </td>".format(text)
        elif (magnet.pvs[idx] == magnet.pvs[2]) & (val < 1328 or val > 1332):
          table += "<td style ='background-color:red;'> {0} </td>".format(text)
        elif (magnet.pvs[idx] == magnet.pvs[3]) & (val < 565.5 or val > 576.5):
          table += "<td style ='background-color:red;'> {0} </td>".format(text)
        elif (magnet.pvs[idx] == magnet.pvs[4]) & (val < 573 or val > 577):
          table += "<td style ='background-color:red;'> {0} </td>".format(text)
        else:
          table += """
          <td style=background-color:#8FED8F;'> {0} </td>
          """.format(text)
      except:
          table += "<td style='background-color:#FFFFFF;'> NOT CONNECTED </td>"
    return table

  def tofnetof(self):
    fillstring = ""
    print "Checking TOF and ETOF"
    try:
      assert type(self.pvs[0].get()) == int
      if self.pvs[0].get() == 1:
        if self.pvs[1].get() == 0:
          #green
          fillstring += "<td style='background-color:#8FED8F;'> Full </td>"
        else:
          #orange
          fillstring += "<td style='background-color:#FFA500;'> Standby </td>"
      else:
        fillstring += "<td style='background-color:red;'> Off </td>"
    except:
        fillstring += "<td style='background-color:#FFFFFF;'> NOT CONNECTED </td>"
    return fillstring

  def scalers(self,namelist):
    self.namelist = namelist
    fillstring = ""
    for idx, value in enumerate(self.pvs):
      try:
        label = namelist[idx]
        pv = value.get()
        fillstring += "<td style='background-color:#8FED8F;'>" + label + "%.1f </td>" % pv
      except:
        fillstring += "<td style='background-color:#FFFFFF;'> NOT CONNECTED </td>"
    return fillstring

  def cathode(self):
    fillstring = ""
    for i in self.pvs:
      print "cathode check" +str(i.get())
      text = round(i.get(),2)
      try:
        if text < 27:
          fillstring += "<td style='background-color:red;'> {0} </td>".format(str(text))
        else:
          fillstring += "<td style='background-color:#8FED8F;'> {0} </td>".format(str(text))
      except:
        fillstring += "<td style='background-color:#FFFFFF;'> NOT CONNECTED </td>"
    return fillstring

  def FEE(self):
    fillstring = ""
    sevcheck = True
    print "Checking TPC FEEs"
    for value in self.pvs: 
      try:
        pv = value.get()
        assert type(pv) == float
        if pv == 0:
          sevcheck = False
          break
      except:
        fillstring += "<td style='background-color:#FFFFFF;'> NOT CONNECTED </td>"
        break
    if sevcheck:
      fillstring += "<td style='background-color:#8FED8F;'> ON </td>"
    else:
      fillstring += "<td style='background-color:red;'> OFF </td>"
    return fillstring
  
  def gridleak(self):
    fillstring = ""
    for idx, value in enumerate(self.pvs):
      try:
        assert type(value.get()) == float
        val = round(value.get(),3)
        if (self.pvs[idx] == self.pvs[0]) & (val > 116 or val < 114):
          fillstring += "<td style ='background-color:red;'> {0} </td>".format(str(val))
        elif (self.pvs[idx] == self.pvs[1]) & (val > 451.0 or val < 449.0):
          fillstring += "<td style='background-color:red;'> {0} </td>".format(str(val))
        else:
          fillstring += "<td style='background-color:#8FED8F;'> {0} </td>".format(str(val))
      except:
        fillstring += "<td style ='background-color:#FFFFFF;'> NOT CONNECTED </td>"
    return fillstring 

  def tpccheck(self,namelist):
    self.namelist = namelist
    fillstring = ""
    for idx,value in enumerate(self.pvs):
     try:
      assert type(value) == float
      val = value.get()
      val = round(val,3)
      text = namelist[idx] + str(val)
      if (self.pvs[idx] == self.pvs[0]) & (val < 27):
        fillstring += "<td style ='background-color:red;'> {0} </td>".format(text)
      elif (self.pvs[idx] == self.pvs[1]) & (val > 116 or val < 114):
        fillstring += "<td style ='background-color:red;'> {0} </td>".format(text)
      elif (self.pvs[idx] == self.pvs[2]) & (val > 451 or val < 449):
        fillstring += "<td style='background-color:red;'> {0} </td>".format(text)
      elif (self.pvs[idx] == self.pvs[1]) & (val == 0):
        fillstring += "<td style ='background-color:red;'> Off </td>"
      elif (self.pvs[idx] == self.pvs[1]) & (val == 1):
        fillstring += "<td style ='background-color:#8FED8F;'> On </td>"
      else:
        fillstring += "<td style = 'background-color:#8FED8F;'>{0} </td>".format(text)
     except:
      fillstring += "<td style = 'background-color:#FFFFFF;'>{0} </td>".format("NOT CONNECTED") 
    return fillstring

  #Use on severity anodes
  def anodes(self):
    sevcheck = False
    fillstring = ""
    for i in self.pvs:
      try:
        val = i.get()
        assert type(val) == int
        pv = i.get()
        if (pv == 1 or pv == 2):
          sevcheck == True
        else:
          continue
      except:
        return "<td style='background-color:#FFFFFF;'> NOT CONNECTED </td>"
    if sevcheck == False:
      fillstring += "<td style='background-color:#8FED8F;'> Anode </td>"
    else:
      fillstring += "<td style='background-color:#FF0DD0;'> Anode </td>"
    return fillstring

  #Lists using this method should only have links in strings
  #testlist should not be strings, just the text
  def includelink(self,textlist):
    self.textlist = textlist
    fillstring = ""
    for idx,link in enumerate(self.pvlist):
      try:
        fillstring += "<td> <a href={0}>".format(link)
        fillstring += "{0} </a></td>".format(textlist[idx])
      except:
        fillstring += "<td style='background-color:#FFFFFF;'> NOT CONNECTED </td>"
    return fillstring

  def trigger(self,name):
    self.name = name
    fillstring = ""
    statuscheck = True
    for value in self.pvs:
      try:
        val = i.get()
        assert type(val) == float
        if value == 0.:
          statuscheck = False
          break
      except:
        return "<td style='background-color:#FFFFFF;'> {0} NOT CONNECTED </td>".format(name)
        break
    if statuscheck:
      fillstring += "<td style='background-color:red;'> {0} </td>".format(name)
    else:
      fillstring += "<td style='background-color:#8FED8F;'> {0} </td>".format(name)
    return fillstring


magnet = Pvs(magnet2)

def main():
  print "Starting"
  t1tpc = Pvs(firsttpc)
  print "TPC Anodes and Cathode"
  feecheck = Pvs(fee)
  print "TPC FEEs"
  gridleakPV = Pvs(gridleakpvs)
  print "TPC Grid Leak"
  weatherone = Pvs(weather1)
  weathertwo = Pvs(weather2)
  print "Environment"
  intername1 = ["Pioneer System OK","Global #1 TPC Purge RACK II OK","From Gas System & Computer","Global #2 OFC HV OK","Global #3 IFC HV & Gap Gas","Water Skid OK","TPC Water OK","Gas Rm Water OK"]
  intername2 = ["Pioneer Methane Alarm","Global #1 Power to RACK II Off","Gas System Alarm","Global #2 OFC HV Off","Global #3 or Gap Gas Alarm","Water Skid Alarm","TPC Water Alarm","Gas Rm Water Alarm"]
  intername3 = ["Gas System Power On","Gas Signal to Control Rm","Gating Grid Enabled","Laser System Enabled","Anode HV Enabled","Monitor Chamber Power On","Cathode HV Enabled","Water OK Signal to Control Rm"]
  intername4 = ["Gas System Off","Gas System Alarm","Gating Grid Off","Laser System Off","Anode HV Off","Monitor Chamber Off","Cathode HV Off","Water System Alarm"]
  interlock1 = Pvs(interlocks1)
  interlock2 = Pvs(interlocks2)
  interlock3 = Pvs(interlocks3)
  interlock4 = Pvs(interlocks4)
  print "Interlocks"
  magnetnames = Pvs(magnet1nam)
  magnet = Pvs(magnet2)
  print "Magnets"
  scalersone = Pvs(scalers1)
  scalerstwo = Pvs(scalers2)
  scalersthre = Pvs(scalers3)
  scalersfo = Pvs(scalers4)
  print "Scalers"
  tof2 = Pvs(tof)
  print "TOF"
  etof2 = Pvs(etof)
  print "ETOF"
  ZDC = Pvs(trigZDC)
  print "ZDC"
  ZDCSMD = Pvs(trigZDCSMD)
  print "ZDCSMD"
  VPD = Pvs(trigVPD)
  print "VPD"
  BBC = Pvs(trigBBC)
  print "Triggers"
  tpcgg = Pvs(tpcGG)
  tpc4 = Pvs(tpcCheck)
  AnodesSev = Pvs(AnodeSev)
  linklist = ['/SlowControls2018/tpc_caen.html']
  textlist = ['Anode HV CAEN']
  anodelink = Pvs(linklist)
  GatingGridSev = Pvs(GGSev)
  cATHODE = ['Cathode']
  print "PVs assigned" 

  while True:
    time.sleep(10)
    htmlfile = open('temp.html','w')
    beginning = """
    <html><head><style>body {background-color:cornsilk;}</style>
    <link rel='stylesheet' type='text/css' href='stylesx.css'>
    <META HTTP-EQUIV='Refresh' Content='5' url='./'></head>
    """
    htmlfile.write(beginning)

    htmlfile.write(t1tpc.tablestart("TPC"))
    print "TPC Table Started"
    htmlfile.write(AnodesSev.anodes())
    htmlfile.write("<td> Cathode </td>")
    htmlfile.write("<td> FEE </td>")
    htmlfile.write("<td> Grid Leak Inner </td>")
    htmlfile.write("<td> Grid Leak Outer </td>") 
    htmlfile.write("<td> Gating Grid </td>")
    newrow = """
    </tr><tr><td style = 'background-color:#ABD7E5;'>
    <font color='#A32E2E'><b>TPC</b></font></td>
    """
    htmlfile.write(newrow)
    htmlfile.write(anodelink.includelink(textlist))
    print "Anodes written"
    htmlfile.write(t1tpc.cathode())
    print "Cathode written"
    htmlfile.write(feecheck.FEE())
    print "FEEs written"
    htmlfile.write(gridleakPV.gridleak())
    print "Grid Leak written"
    htmlfile.write(GatingGridSev.gatingGrid())
    print "Gating Grid written"
    htmlfile.write("</tr></body>")

    htmlfile.write(tof2.tablestart("TOF Status"))
    htmlfile.write(tof2.tofnetof())
    newrow = """
    </tr><tr><td style = 'background-color:#ABD7E5;'>
    <font color='#A32E2E'><b>ETOF Status</b></font></td>
    """
    htmlfile.write(newrow)
    htmlfile.write(etof2.tofnetof())
    htmlfile.write("</tr></body>")

    htmlfile.write(ZDC.tablestart("Trigger"))
    htmlfile.write(ZDC.trigger("ZDC"))
    htmlfile.write(ZDCSMD.trigger("ZDCSMD"))
    htmlfile.write(VPD.trigger("VPD"))
    htmlfile.write(BBC.trigger("BBC"))
    htmlfile.write("</tr></body>")

    htmlfile.write(interlock1.tablestart("Interlocks 1"))
    htmlfile.write(interlock1.interlocks2(intername1))
    newrow = """
    </tr><tr><td style = 'background-color:#ABD7E5;'>
    <font color='#A32E2E'><b>Interlocks 2</b></font></td>
    """ 
    htmlfile.write(newrow)
    htmlfile.write(interlock2.interlocks(intername2))
    newrow = """
    </tr><tr><td style = 'background-color:#ABD7E5;'>
    <font color='#A32E2E'><b>Interlocks 3</b></font></td>
    """
    htmlfile.write(newrow)
    htmlfile.write(interlock3.interlocks2(intername3))
    newrow = """
    </tr><tr><td style = 'background-color:#ABD7E5;'>
    <font color='#A32E2E'><b>Interlocks 4</b></font></td>
    """
    htmlfile.write(newrow)
    htmlfile.write(interlock4.interlocks(intername4))

    htmlfile.write(magnetnames.tablestart("Magnet"))
    htmlfile.write(magnetnames.magnettext())
    newrow = """
    </tr><tr><td style = 'background-color:#ABD7E5;'>
    <font color='#A32E2E'><b>Magnet Current</b></font></td>
    """
    htmlfile.write(newrow)
    htmlfile.write(magnet.magnettable(magnet22))
    htmlfile.write("</tr></body>")


    htmlfile.write(weatherone.tablestart("Weather WAH"))
    htmlfile.write(weatherone.includetext(weathertext))
    newrow = """
    </tr><tr><td style = 'background-color:#ABD7E5;'>
    <font color='#A32E2E'><b>Weather DAQ</b></font></td>
    """
    htmlfile.write(newrow)
    htmlfile.write(weathertwo.includetext(weathertext))
    htmlfile.write("</tr></body>")


    htmlfile.write(scalersone.tablestart("Scalers (Hz)"))
    htmlfile.write(scalersone.scalers(scalers11))
    newrow = """
    </tr><tr><td style = 'background-color:#ABD7E5;'>
    <font color='#A32E2E'><b>Scalers (Hz)</b></font></td>
    """
    htmlfile.write(newrow)
    htmlfile.write(scalerstwo.scalers(scalers22))
    htmlfile.write(newrow)
    htmlfile.write(scalersthre.scalers(scalers33))
    htmlfile.write(newrow)
    htmlfile.write(scalersfo.scalers(scalers44))

    htmlfile.write("</tr>")
        

    htmlfile.write("<h2></h2>")
    htmlfile.write("</table>")
    htmlfile.write("<h2></h2>")
    htmlfile.write("Last updated: " + str(datetime.now()).split(".")[0] + "\n")
    
    htmlfile.write("</html>")
    htmlfile.close()
    copyfile("/home/sysuser/iocTop/glmonitor_new/temp.html","/ceph/WWW/SlowControls2018/index.html")
#_____________________________________________________________________________

def start_monit_loop():
        t = threading.Thread(target=main)
        t.daemon = True
        t.start()



#_____________________________________________________________________________
def start_interactive():

    vars = globals()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()


start_monit_loop()
start_interactive()


