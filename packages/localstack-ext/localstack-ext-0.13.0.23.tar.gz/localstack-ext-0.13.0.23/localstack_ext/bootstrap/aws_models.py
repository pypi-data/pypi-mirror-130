from localstack.utils.aws import aws_models
CRnDk=super
CRnDV=None
CRnDv=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  CRnDk(LambdaLayer,self).__init__(arn)
  self.cwd=CRnDV
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.CRnDv.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,CRnDv,env=CRnDV):
  CRnDk(RDSDatabase,self).__init__(CRnDv,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,CRnDv,env=CRnDV):
  CRnDk(RDSCluster,self).__init__(CRnDv,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,CRnDv,env=CRnDV):
  CRnDk(AppSyncAPI,self).__init__(CRnDv,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,CRnDv,env=CRnDV):
  CRnDk(AmplifyApp,self).__init__(CRnDv,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,CRnDv,env=CRnDV):
  CRnDk(ElastiCacheCluster,self).__init__(CRnDv,env=env)
class TransferServer(BaseComponent):
 def __init__(self,CRnDv,env=CRnDV):
  CRnDk(TransferServer,self).__init__(CRnDv,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,CRnDv,env=CRnDV):
  CRnDk(CloudFrontDistribution,self).__init__(CRnDv,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,CRnDv,env=CRnDV):
  CRnDk(CodeCommitRepository,self).__init__(CRnDv,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
