import logging
Kdmyf=bool
Kdmyx=hasattr
KdmyS=set
KdmyC=True
KdmyN=False
KdmyJ=isinstance
KdmyA=dict
Kdmys=getattr
Kdmyn=None
KdmyV=str
Kdmyu=Exception
KdmyH=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
API_STATES_DIR="api_states"
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[Kdmyf,Set]:
 if Kdmyx(obj,"__dict__"):
  visited=visited or KdmyS()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return KdmyC,visited
  visited.add(wrapper)
 return KdmyN,visited
def get_object_dict(obj):
 if KdmyJ(obj,KdmyA):
  return obj
 obj_dict=Kdmys(obj,"__dict__",Kdmyn)
 return obj_dict
def is_composite_type(obj):
 return KdmyJ(obj,(KdmyA,OrderedDict))or Kdmyx(obj,"__dict__")
def api_states_traverse(api_states_path:KdmyV,side_effect:Callable[...,Kdmyn],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except Kdmyu as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with KdmyH(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except Kdmyu as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
def persist_object(obj,state_file):
 with KdmyH(state_file,"wb")as f:
  result=f.write(dill.dumps(obj))
  return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)
