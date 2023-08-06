from datetime import datetime
cPvxd=str
cPvxE=int
cPvxm=super
cPvxp=False
cPvxb=isinstance
cPvxV=hash
cPvxI=bool
cPvxD=True
cPvxJ=list
cPvxq=map
cPvxQ=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:cPvxd):
  self.hash_ref:cPvxd=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:cPvxd,rel_path:cPvxd,file_name:cPvxd,size:cPvxE,service:cPvxd,region:cPvxd):
  cPvxm(StateFileRef,self).__init__(hash_ref)
  self.rel_path:cPvxd=rel_path
  self.file_name:cPvxd=file_name
  self.size:cPvxE=size
  self.service:cPvxd=service
  self.region:cPvxd=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return cPvxp
  if not cPvxb(other,StateFileRef):
   return cPvxp
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return cPvxV((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->cPvxI:
  if not other:
   return cPvxp
  if not cPvxb(other,StateFileRef):
   return cPvxp
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->cPvxI:
  for other in others:
   if self.congruent(other):
    return cPvxD
  return cPvxp
 def metadata(self)->cPvxd:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:cPvxd,state_files:Set[StateFileRef],parent_ptr:cPvxd):
  cPvxm(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:cPvxd=parent_ptr
 def state_files_info(self)->cPvxd:
  return "\n".join(cPvxJ(cPvxq(lambda state_file:cPvxd(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:cPvxd,head_ptr:cPvxd,message:cPvxd,timestamp:cPvxd=cPvxd(datetime.now().timestamp()),delta_log_ptr:cPvxd=cPvxQ):
  self.tail_ptr:cPvxd=tail_ptr
  self.head_ptr:cPvxd=head_ptr
  self.message:cPvxd=message
  self.timestamp:cPvxd=timestamp
  self.delta_log_ptr:cPvxd=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:cPvxd,to_node:cPvxd)->cPvxd:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:cPvxd,state_files:Set[StateFileRef],parent_ptr:cPvxd,creator:cPvxd,rid:cPvxd,revision_number:cPvxE,assoc_commit:Commit=cPvxQ):
  cPvxm(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:cPvxd=creator
  self.rid:cPvxd=rid
  self.revision_number:cPvxE=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(cPvxq(lambda state_file:cPvxd(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:cPvxd,state_files:Set[StateFileRef],parent_ptr:cPvxd,creator:cPvxd,comment:cPvxd,active_revision_ptr:cPvxd,outgoing_revision_ptrs:Set[cPvxd],incoming_revision_ptr:cPvxd,version_number:cPvxE):
  cPvxm(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(cPvxq(lambda stat_file:cPvxd(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
