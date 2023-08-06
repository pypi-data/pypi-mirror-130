from localstack.utils.aws import aws_models
EJvSr=super
EJvSC=None
EJvSb=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  EJvSr(LambdaLayer,self).__init__(arn)
  self.cwd=EJvSC
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.EJvSb.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,EJvSb,env=EJvSC):
  EJvSr(RDSDatabase,self).__init__(EJvSb,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,EJvSb,env=EJvSC):
  EJvSr(RDSCluster,self).__init__(EJvSb,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,EJvSb,env=EJvSC):
  EJvSr(AppSyncAPI,self).__init__(EJvSb,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,EJvSb,env=EJvSC):
  EJvSr(AmplifyApp,self).__init__(EJvSb,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,EJvSb,env=EJvSC):
  EJvSr(ElastiCacheCluster,self).__init__(EJvSb,env=env)
class TransferServer(BaseComponent):
 def __init__(self,EJvSb,env=EJvSC):
  EJvSr(TransferServer,self).__init__(EJvSb,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,EJvSb,env=EJvSC):
  EJvSr(CloudFrontDistribution,self).__init__(EJvSb,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,EJvSb,env=EJvSC):
  EJvSr(CodeCommitRepository,self).__init__(EJvSb,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
