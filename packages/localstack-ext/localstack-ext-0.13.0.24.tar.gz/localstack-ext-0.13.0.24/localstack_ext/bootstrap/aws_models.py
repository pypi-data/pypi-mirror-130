from localstack.utils.aws import aws_models
cXBtl=super
cXBtI=None
cXBts=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  cXBtl(LambdaLayer,self).__init__(arn)
  self.cwd=cXBtI
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.cXBts.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,cXBts,env=cXBtI):
  cXBtl(RDSDatabase,self).__init__(cXBts,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,cXBts,env=cXBtI):
  cXBtl(RDSCluster,self).__init__(cXBts,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,cXBts,env=cXBtI):
  cXBtl(AppSyncAPI,self).__init__(cXBts,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,cXBts,env=cXBtI):
  cXBtl(AmplifyApp,self).__init__(cXBts,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,cXBts,env=cXBtI):
  cXBtl(ElastiCacheCluster,self).__init__(cXBts,env=env)
class TransferServer(BaseComponent):
 def __init__(self,cXBts,env=cXBtI):
  cXBtl(TransferServer,self).__init__(cXBts,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,cXBts,env=cXBtI):
  cXBtl(CloudFrontDistribution,self).__init__(cXBts,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,cXBts,env=cXBtI):
  cXBtl(CodeCommitRepository,self).__init__(cXBts,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
