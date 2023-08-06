import contextlib
SiCxN=None
SiCxg=isinstance
SiCxf=list
SiCxX=all
SiCxK=dict
SiCxk=tuple
SiCxQ=set
SiCxl=True
SiCxe=type
SiCxJ=Exception
SiCxL=str
SiCxI=getattr
SiCxU=len
SiCxo=range
SiCxq=map
SiCxE=bool
SiCxp=False
SiCxP=open
import inspect
import json
import logging
import os
import pickle
import sqlite3
from typing import Any,Dict,Set,Type
from localstack.utils.common import ArbitraryAccessObj
from moto.s3.models import FakeBucket
from moto.sqs.models import Queue
from localstack_ext.bootstrap.state_utils import(check_already_visited,get_object_dict,is_composite_type)
LOG=logging.getLogger(__name__)
DDB_PREDEF_TABLES=("dm","cf","sm","ss","tr","us")
def _merge_helper_three_way(current,injecting,common_ancestor,visited:Set=SiCxN):
 if SiCxg(current,SiCxf)and SiCxg(injecting,SiCxf):
  current.extend(injecting)
  return
 if(not is_composite_type(current)or not is_composite_type(injecting)or not is_composite_type(common_ancestor)):
  return
 cycle,visited=check_already_visited(injecting,visited)
 if cycle:
  return
 cur_dict=get_object_dict(current)
 inj_dict=get_object_dict(injecting)
 ancestor_dict=get_object_dict(common_ancestor)
 for key in cur_dict.keys()&inj_dict.keys()&ancestor_dict.keys():
  if SiCxX(SiCxg(d.get(key),SiCxK)for d in(cur_dict,inj_dict,ancestor_dict)):
   cur_dict[key]=inj_dict[key]=ancestor_dict[key]=_merge_helper_three_way(cur_dict[key],inj_dict[key],ancestor_dict[key])
 for d in cur_dict,inj_dict,ancestor_dict:
  for k,v in d.items():
   if SiCxg(v,SiCxK):
    d[k]=SiCxk(v.items())
 set_cur,set_inj,set_ancestor=(SiCxQ((k,pickle.dumps(v))for k,v in d.items())for d in(cur_dict,inj_dict,ancestor_dict))
 for k in SiCxQ(k for k,_ in set_cur^set_ancestor)&SiCxQ(k for k,_ in set_inj^set_ancestor):
  if cur_dict.get(k)!=inj_dict.get(k)or(k in cur_dict)^(k in inj_dict):
   LOG.debug("Found update-update conflict")
   cur_dict[k]=inj_dict[k]
 d=SiCxK(set_cur&set_inj&set_ancestor|set_cur-set_ancestor|set_inj-set_ancestor)
 for k,v in d.items():
  v=pickle.loads(v)
  if SiCxg(v,SiCxk):
   d[k]=SiCxK(v)
  else:
   d[k]=v
 return d
def _merge_helper(current,injecting,merge_strategy=SiCxN,visited:Set=SiCxN):
 if SiCxg(current,SiCxf)and SiCxg(injecting,SiCxf):
  current.extend(injecting)
  return
 if not is_composite_type(current)or not is_composite_type(injecting):
  return
 cycle,visited=check_already_visited(injecting,visited)
 if cycle:
  return
 cur_dict=get_object_dict(current)
 inj_dict=get_object_dict(injecting)
 for field_name,inj_field_value in inj_dict.items():
  cur_field_value=cur_dict.get(field_name)
  if cur_field_value is not SiCxN:
   if is_composite_type(cur_field_value):
    _merge_helper(cur_field_value,inj_field_value,merge_strategy=merge_strategy,visited=visited)
   elif cur_field_value!=inj_field_value:
    LOG.debug("Overwriting existing value with new state: '%s' <> '%s'"%(cur_field_value,inj_field_value))
    cur_dict[field_name]=inj_field_value
  else:
   cur_dict[field_name]=inj_field_value
 return cur_dict
def merge_object_state(current,injecting,common_ancestor=SiCxN,merge_strategy=SiCxN):
 if not current or not injecting:
  return current
 is_special_case=handle_special_case(current,injecting)
 if is_special_case:
  return current
 if common_ancestor:
  _merge_helper_three_way(current,injecting,common_ancestor)
 else:
  _merge_helper(current,injecting)
 add_missing_attributes(current)
 return current
def handle_special_case(current,injecting):
 if SiCxg(injecting,Queue):
  current.queues[injecting.name]=injecting
  return SiCxl
 elif SiCxg(injecting,FakeBucket):
  current["global"].buckets[injecting.name]=injecting
  return SiCxl
def add_missing_attributes(obj:Any,safe:SiCxE=SiCxl,visited:Set=SiCxN):
 try:
  obj_dict=get_object_dict(obj)
  if obj_dict is SiCxN:
   return
  cycle,visited=check_already_visited(obj,visited)
  if cycle:
   return
  for attr_value in obj_dict.values():
   add_missing_attributes(attr_value,safe=safe,visited=visited)
  class_inst_attrs=infer_class_attributes(SiCxe(obj))
  for key,value in class_inst_attrs.items():
   if key not in obj_dict:
    LOG.debug("Add missing attribute '%s' to state object of type %s"%(key,SiCxe(obj)))
    obj_dict[key]=value
 except SiCxJ as e:
  if not safe:
   raise
  LOG.warning("Unable to add missing attributes to persistence state object %s: %s",(obj,e))
def infer_class_attributes(clazz:Type)->Dict[SiCxL,Any]:
 if clazz in[SiCxf,SiCxK]or not inspect.isclass(clazz)or clazz.__name__=="function":
  return{}
 constructor=SiCxI(clazz,"__init__",SiCxN)
 if not constructor:
  return{}
 try:
  sig_args=inspect.getfullargspec(constructor)
  def get_default_arg_value(arg_name,arg_index=-1):
   arg_defaults=sig_args.defaults or[]
   num_non_default_args=SiCxU(sig_args.args or[])-SiCxU(arg_defaults)
   offset=arg_index-num_non_default_args
   if offset in SiCxo(SiCxU(arg_defaults)):
    return arg_defaults[offset]
   kwargs_defaults=sig_args.kwonlydefaults or{}
   if arg_name in kwargs_defaults:
    return kwargs_defaults[arg_name]
   return ArbitraryAccessObj()
  args=[]
  kwargs={}
  for arg_idx in SiCxo(1,SiCxU(sig_args.args)):
   args.append(get_default_arg_value(sig_args.args[arg_idx],arg_index=arg_idx))
  for arg in sig_args.kwonlyargs:
   kwargs[arg]=get_default_arg_value(arg)
  instance=clazz(*args,**kwargs)
  result=SiCxK(instance.__dict__)
  return result
 except SiCxJ:
  return{}
def merge_sqllite_dbs(file_dest:SiCxL,file_src:SiCxL)->SiCxN:
 def _merge_table(table_name:SiCxL,cursor_a,cursor_b)->SiCxN:
  tmp_table_name=f"'{table_name}_new'"
  table_name=f"'{table_name}'"
  select_query=f"SELECT * FROM {table_name}"
  if table_name=="'cf'":
   return
  schema=SiCxk(SiCxq(lambda x:x[1],cursor_b.execute(f"PRAGMA table_info({table_name})")))
  params=f"({('?,' * len(schema))[:-1]})"
  insert_str=f"INSERT INTO {tmp_table_name} {str(schema)} values {params}"
  if table_name=="'dm'":
   excl_tables=(SiCxL(SiCxf(SiCxq(lambda x:x[0],cursor_a.execute(f"SELECT TableName FROM {table_name}")))).replace("[","(",1).replace("]",")",1))
   select_query+=f"AS O_T WHERE O_T.TableName NOT IN {excl_tables}"
  cursor_a.execute(f"CREATE TABLE IF NOT EXISTS {tmp_table_name} AS SELECT * FROM {table_name}")
  for row in cursor_b.execute(select_query):
   cursor_a.execute(insert_str,row)
  cursor_a.execute(f"DROP TABLE IF EXISTS {table_name}")
  cursor_a.execute(f"ALTER TABLE {tmp_table_name} RENAME TO {table_name}")
 with contextlib.closing(sqlite3.connect(file_dest))as db_src,contextlib.closing(sqlite3.connect(file_src))as db_target:
  cursor_dest=db_src.cursor()
  cursor_src=db_target.cursor()
  table_names=SiCxf(SiCxq(lambda x:x[0],cursor_dest.execute("SELECT name FROM sqlite_master WHERE type='table'")))
  for current_table in table_names:
   try:
    _merge_table(current_table,cursor_dest,cursor_src)
   except sqlite3.OperationalError as e:
    LOG.warning(f"Failed to merge table {current_table}: {e}")
    cursor_dest.execute(f"DROP TABLE IF EXISTS '{current_table}'")
    db_src.rollback()
    return
  db_src.commit()
  LOG.debug(f"Successfully merged db at {file_src} into {file_dest}")
def merge_kinesis_state(path_dest:SiCxL,path_src:SiCxL)->SiCxE:
 state_file="kinesis-data.json"
 datadir_statefile=os.path.join(path_dest,state_file)
 tmp_dir_statefile=os.path.join(path_src,state_file)
 if not os.path.isfile(datadir_statefile):
  LOG.info(f"Could not find statefile in path destination {path_dest}")
  return SiCxp
 if not os.path.isfile(tmp_dir_statefile):
  LOG.info(f"Could not find statefile in path source {path_src}")
  return SiCxp
 with SiCxP(datadir_statefile)as datadir_kinesis_file,SiCxP(tmp_dir_statefile)as tmp_dir_kinesis_file:
  datadir_kinesis_json=json.load(datadir_kinesis_file)
  tmp_dir_kinesis_json=json.load(tmp_dir_kinesis_file)
  datadir_streams=datadir_kinesis_json.get("streams",[])
  tmp_dir_streams=tmp_dir_kinesis_json.get("streams",[])
  if SiCxU(tmp_dir_streams)>0:
   datadir_stream_names=datadir_streams.keys()
   for stream in tmp_dir_streams:
    if stream not in datadir_stream_names:
     datadir_streams[stream]=tmp_dir_streams.get(stream)
     LOG.debug(f"Copied state from stream {stream}")
   with SiCxP(datadir_statefile,"w")as mutated_datadir_kinesis_file:
    mutated_datadir_kinesis_file.write(json.dumps(datadir_kinesis_json))
   return SiCxl
 return SiCxp
# Created by pyminifier (https://github.com/liftoff/pyminifier)
