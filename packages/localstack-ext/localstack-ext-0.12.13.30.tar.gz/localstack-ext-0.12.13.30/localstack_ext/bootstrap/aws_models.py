from localstack.utils.aws import aws_models
ExdwL=super
Exdwe=None
Exdwc=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  ExdwL(LambdaLayer,self).__init__(arn)
  self.cwd=Exdwe
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.Exdwc.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,Exdwc,env=Exdwe):
  ExdwL(RDSDatabase,self).__init__(Exdwc,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,Exdwc,env=Exdwe):
  ExdwL(RDSCluster,self).__init__(Exdwc,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,Exdwc,env=Exdwe):
  ExdwL(AppSyncAPI,self).__init__(Exdwc,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,Exdwc,env=Exdwe):
  ExdwL(AmplifyApp,self).__init__(Exdwc,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,Exdwc,env=Exdwe):
  ExdwL(ElastiCacheCluster,self).__init__(Exdwc,env=env)
class TransferServer(BaseComponent):
 def __init__(self,Exdwc,env=Exdwe):
  ExdwL(TransferServer,self).__init__(Exdwc,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,Exdwc,env=Exdwe):
  ExdwL(CloudFrontDistribution,self).__init__(Exdwc,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,Exdwc,env=Exdwe):
  ExdwL(CodeCommitRepository,self).__init__(Exdwc,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
