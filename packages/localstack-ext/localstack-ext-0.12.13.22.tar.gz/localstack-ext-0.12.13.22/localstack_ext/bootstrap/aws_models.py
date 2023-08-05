from localstack.utils.aws import aws_models
CzuKV=super
CzuKj=None
CzuKS=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  CzuKV(LambdaLayer,self).__init__(arn)
  self.cwd=CzuKj
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.CzuKS.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,CzuKS,env=CzuKj):
  CzuKV(RDSDatabase,self).__init__(CzuKS,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,CzuKS,env=CzuKj):
  CzuKV(RDSCluster,self).__init__(CzuKS,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,CzuKS,env=CzuKj):
  CzuKV(AppSyncAPI,self).__init__(CzuKS,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,CzuKS,env=CzuKj):
  CzuKV(AmplifyApp,self).__init__(CzuKS,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,CzuKS,env=CzuKj):
  CzuKV(ElastiCacheCluster,self).__init__(CzuKS,env=env)
class TransferServer(BaseComponent):
 def __init__(self,CzuKS,env=CzuKj):
  CzuKV(TransferServer,self).__init__(CzuKS,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,CzuKS,env=CzuKj):
  CzuKV(CloudFrontDistribution,self).__init__(CzuKS,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,CzuKS,env=CzuKj):
  CzuKV(CodeCommitRepository,self).__init__(CzuKS,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
