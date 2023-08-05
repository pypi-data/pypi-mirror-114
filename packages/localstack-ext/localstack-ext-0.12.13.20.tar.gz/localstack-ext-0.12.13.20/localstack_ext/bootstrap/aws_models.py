from localstack.utils.aws import aws_models
vUGJf=super
vUGJS=None
vUGJg=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  vUGJf(LambdaLayer,self).__init__(arn)
  self.cwd=vUGJS
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.vUGJg.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,vUGJg,env=vUGJS):
  vUGJf(RDSDatabase,self).__init__(vUGJg,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,vUGJg,env=vUGJS):
  vUGJf(RDSCluster,self).__init__(vUGJg,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,vUGJg,env=vUGJS):
  vUGJf(AppSyncAPI,self).__init__(vUGJg,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,vUGJg,env=vUGJS):
  vUGJf(AmplifyApp,self).__init__(vUGJg,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,vUGJg,env=vUGJS):
  vUGJf(ElastiCacheCluster,self).__init__(vUGJg,env=env)
class TransferServer(BaseComponent):
 def __init__(self,vUGJg,env=vUGJS):
  vUGJf(TransferServer,self).__init__(vUGJg,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,vUGJg,env=vUGJS):
  vUGJf(CloudFrontDistribution,self).__init__(vUGJg,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,vUGJg,env=vUGJS):
  vUGJf(CodeCommitRepository,self).__init__(vUGJg,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
