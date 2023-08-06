from localstack.utils.aws import aws_models
DGXYV=super
DGXYH=None
DGXYE=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  DGXYV(LambdaLayer,self).__init__(arn)
  self.cwd=DGXYH
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.DGXYE.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,DGXYE,env=DGXYH):
  DGXYV(RDSDatabase,self).__init__(DGXYE,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,DGXYE,env=DGXYH):
  DGXYV(RDSCluster,self).__init__(DGXYE,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,DGXYE,env=DGXYH):
  DGXYV(AppSyncAPI,self).__init__(DGXYE,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,DGXYE,env=DGXYH):
  DGXYV(AmplifyApp,self).__init__(DGXYE,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,DGXYE,env=DGXYH):
  DGXYV(ElastiCacheCluster,self).__init__(DGXYE,env=env)
class TransferServer(BaseComponent):
 def __init__(self,DGXYE,env=DGXYH):
  DGXYV(TransferServer,self).__init__(DGXYE,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,DGXYE,env=DGXYH):
  DGXYV(CloudFrontDistribution,self).__init__(DGXYE,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,DGXYE,env=DGXYH):
  DGXYV(CodeCommitRepository,self).__init__(DGXYE,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
