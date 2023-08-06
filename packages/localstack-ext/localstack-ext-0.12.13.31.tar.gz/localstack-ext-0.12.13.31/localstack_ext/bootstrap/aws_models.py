from localstack.utils.aws import aws_models
LUBOy=super
LUBOo=None
LUBOW=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  LUBOy(LambdaLayer,self).__init__(arn)
  self.cwd=LUBOo
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.LUBOW.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,LUBOW,env=LUBOo):
  LUBOy(RDSDatabase,self).__init__(LUBOW,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,LUBOW,env=LUBOo):
  LUBOy(RDSCluster,self).__init__(LUBOW,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,LUBOW,env=LUBOo):
  LUBOy(AppSyncAPI,self).__init__(LUBOW,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,LUBOW,env=LUBOo):
  LUBOy(AmplifyApp,self).__init__(LUBOW,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,LUBOW,env=LUBOo):
  LUBOy(ElastiCacheCluster,self).__init__(LUBOW,env=env)
class TransferServer(BaseComponent):
 def __init__(self,LUBOW,env=LUBOo):
  LUBOy(TransferServer,self).__init__(LUBOW,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,LUBOW,env=LUBOo):
  LUBOy(CloudFrontDistribution,self).__init__(LUBOW,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,LUBOW,env=LUBOo):
  LUBOy(CodeCommitRepository,self).__init__(LUBOW,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
