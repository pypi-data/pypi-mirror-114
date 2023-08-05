from localstack.utils.aws import aws_models
kRydq=super
kRydu=None
kRydo=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  kRydq(LambdaLayer,self).__init__(arn)
  self.cwd=kRydu
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.kRydo.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,kRydo,env=kRydu):
  kRydq(RDSDatabase,self).__init__(kRydo,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,kRydo,env=kRydu):
  kRydq(RDSCluster,self).__init__(kRydo,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,kRydo,env=kRydu):
  kRydq(AppSyncAPI,self).__init__(kRydo,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,kRydo,env=kRydu):
  kRydq(AmplifyApp,self).__init__(kRydo,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,kRydo,env=kRydu):
  kRydq(ElastiCacheCluster,self).__init__(kRydo,env=env)
class TransferServer(BaseComponent):
 def __init__(self,kRydo,env=kRydu):
  kRydq(TransferServer,self).__init__(kRydo,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,kRydo,env=kRydu):
  kRydq(CloudFrontDistribution,self).__init__(kRydo,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,kRydo,env=kRydu):
  kRydq(CodeCommitRepository,self).__init__(kRydo,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
