from localstack.utils.aws import aws_models
mthvW=super
mthvN=None
mthvG=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  mthvW(LambdaLayer,self).__init__(arn)
  self.cwd=mthvN
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.mthvG.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,mthvG,env=mthvN):
  mthvW(RDSDatabase,self).__init__(mthvG,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,mthvG,env=mthvN):
  mthvW(RDSCluster,self).__init__(mthvG,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,mthvG,env=mthvN):
  mthvW(AppSyncAPI,self).__init__(mthvG,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,mthvG,env=mthvN):
  mthvW(AmplifyApp,self).__init__(mthvG,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,mthvG,env=mthvN):
  mthvW(ElastiCacheCluster,self).__init__(mthvG,env=env)
class TransferServer(BaseComponent):
 def __init__(self,mthvG,env=mthvN):
  mthvW(TransferServer,self).__init__(mthvG,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,mthvG,env=mthvN):
  mthvW(CloudFrontDistribution,self).__init__(mthvG,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,mthvG,env=mthvN):
  mthvW(CodeCommitRepository,self).__init__(mthvG,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
