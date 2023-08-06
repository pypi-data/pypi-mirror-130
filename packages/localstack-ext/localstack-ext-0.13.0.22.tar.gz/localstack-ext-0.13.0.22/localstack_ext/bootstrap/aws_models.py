from localstack.utils.aws import aws_models
EdoGC=super
EdoGj=None
EdoGy=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  EdoGC(LambdaLayer,self).__init__(arn)
  self.cwd=EdoGj
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.EdoGy.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,EdoGy,env=EdoGj):
  EdoGC(RDSDatabase,self).__init__(EdoGy,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,EdoGy,env=EdoGj):
  EdoGC(RDSCluster,self).__init__(EdoGy,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,EdoGy,env=EdoGj):
  EdoGC(AppSyncAPI,self).__init__(EdoGy,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,EdoGy,env=EdoGj):
  EdoGC(AmplifyApp,self).__init__(EdoGy,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,EdoGy,env=EdoGj):
  EdoGC(ElastiCacheCluster,self).__init__(EdoGy,env=env)
class TransferServer(BaseComponent):
 def __init__(self,EdoGy,env=EdoGj):
  EdoGC(TransferServer,self).__init__(EdoGy,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,EdoGy,env=EdoGj):
  EdoGC(CloudFrontDistribution,self).__init__(EdoGy,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,EdoGy,env=EdoGj):
  EdoGC(CodeCommitRepository,self).__init__(EdoGy,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
