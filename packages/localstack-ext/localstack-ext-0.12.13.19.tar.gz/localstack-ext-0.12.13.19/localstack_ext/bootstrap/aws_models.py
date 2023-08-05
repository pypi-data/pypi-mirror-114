from localstack.utils.aws import aws_models
JsbQx=super
JsbQY=None
JsbQV=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  JsbQx(LambdaLayer,self).__init__(arn)
  self.cwd=JsbQY
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.JsbQV.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,JsbQV,env=JsbQY):
  JsbQx(RDSDatabase,self).__init__(JsbQV,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,JsbQV,env=JsbQY):
  JsbQx(RDSCluster,self).__init__(JsbQV,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,JsbQV,env=JsbQY):
  JsbQx(AppSyncAPI,self).__init__(JsbQV,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,JsbQV,env=JsbQY):
  JsbQx(AmplifyApp,self).__init__(JsbQV,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,JsbQV,env=JsbQY):
  JsbQx(ElastiCacheCluster,self).__init__(JsbQV,env=env)
class TransferServer(BaseComponent):
 def __init__(self,JsbQV,env=JsbQY):
  JsbQx(TransferServer,self).__init__(JsbQV,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,JsbQV,env=JsbQY):
  JsbQx(CloudFrontDistribution,self).__init__(JsbQV,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,JsbQV,env=JsbQY):
  JsbQx(CodeCommitRepository,self).__init__(JsbQV,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
