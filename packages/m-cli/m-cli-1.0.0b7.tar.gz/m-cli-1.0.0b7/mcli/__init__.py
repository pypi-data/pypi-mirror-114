# -*- coding: utf-8 -*-
import importlib.util as f;Z=f.spec_from_file_location;v=f.module_from_spec;import json as json;z=json.load;import os as O;A=O.path.join;m=O.path.expanduser;b=O.path.exists;C=O.mkdir;import requests as W;T=W.get;p=W.exceptions.ConnectionError
def main():
 L=s();I=Z("code",L);e=v(I);I.loader.exec_module(e);c=e.cf()
 try:
  c.up();y=e.cm(c).ge();y()
 except Exception as g:
  raise g
def J(r):
 with open(r,"r")as l:
  l.readline();return l.readline().strip()[2:]
def s():
 def U(E):
  try:
   return T(c["_url"]+E,headers={"Accept":"application/json","Authorization":"Bearer {0}".format(c["_token"])})
  except p:
   return
 j=A(m("~"),".mcli")
 if not b(j):
  C(j)
 r=A(j,".c.py");c=None
 with open(A(j,"conf.json"),"r")as l:
  c=z(l)
 if b(r):
  D=U("/@mclicode-version")
  if not D or D.status_code!=200:
   return r
  if D.json()["v"]==J(r):
   return r
 h=U("/@mclicode")
 if not h or h.status_code!=200:
  return r
 with open(r,"w")as l:
  l.write(h.json()["r"])
 return r
