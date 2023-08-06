from datetime import datetime
sxUVM=str
sxUVc=int
sxUVz=super
sxUVu=False
sxUVP=isinstance
sxUVN=hash
sxUVb=bool
sxUVo=True
sxUVw=list
sxUVI=map
sxUVq=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:sxUVM):
  self.hash_ref:sxUVM=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:sxUVM,rel_path:sxUVM,file_name:sxUVM,size:sxUVc,service:sxUVM,region:sxUVM):
  sxUVz(StateFileRef,self).__init__(hash_ref)
  self.rel_path:sxUVM=rel_path
  self.file_name:sxUVM=file_name
  self.size:sxUVc=size
  self.service:sxUVM=service
  self.region:sxUVM=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return sxUVu
  if not sxUVP(other,StateFileRef):
   return sxUVu
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return sxUVN((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->sxUVb:
  if not other:
   return sxUVu
  if not sxUVP(other,StateFileRef):
   return sxUVu
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->sxUVb:
  for other in others:
   if self.congruent(other):
    return sxUVo
  return sxUVu
 def metadata(self)->sxUVM:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:sxUVM,state_files:Set[StateFileRef],parent_ptr:sxUVM):
  sxUVz(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:sxUVM=parent_ptr
 def state_files_info(self)->sxUVM:
  return "\n".join(sxUVw(sxUVI(lambda state_file:sxUVM(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:sxUVM,head_ptr:sxUVM,message:sxUVM,timestamp:sxUVM=sxUVM(datetime.now().timestamp()),delta_log_ptr:sxUVM=sxUVq):
  self.tail_ptr:sxUVM=tail_ptr
  self.head_ptr:sxUVM=head_ptr
  self.message:sxUVM=message
  self.timestamp:sxUVM=timestamp
  self.delta_log_ptr:sxUVM=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:sxUVM,to_node:sxUVM)->sxUVM:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:sxUVM,state_files:Set[StateFileRef],parent_ptr:sxUVM,creator:sxUVM,rid:sxUVM,revision_number:sxUVc,assoc_commit:Commit=sxUVq):
  sxUVz(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:sxUVM=creator
  self.rid:sxUVM=rid
  self.revision_number:sxUVc=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(sxUVI(lambda state_file:sxUVM(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:sxUVM,state_files:Set[StateFileRef],parent_ptr:sxUVM,creator:sxUVM,comment:sxUVM,active_revision_ptr:sxUVM,outgoing_revision_ptrs:Set[sxUVM],incoming_revision_ptr:sxUVM,version_number:sxUVc):
  sxUVz(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(sxUVI(lambda stat_file:sxUVM(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
