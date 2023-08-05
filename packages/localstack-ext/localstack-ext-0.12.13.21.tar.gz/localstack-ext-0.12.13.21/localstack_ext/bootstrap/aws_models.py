from localstack.utils.aws import aws_models
sXzuD=super
sXzuC=None
sXzuO=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  sXzuD(LambdaLayer,self).__init__(arn)
  self.cwd=sXzuC
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.sXzuO.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,sXzuO,env=sXzuC):
  sXzuD(RDSDatabase,self).__init__(sXzuO,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,sXzuO,env=sXzuC):
  sXzuD(RDSCluster,self).__init__(sXzuO,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,sXzuO,env=sXzuC):
  sXzuD(AppSyncAPI,self).__init__(sXzuO,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,sXzuO,env=sXzuC):
  sXzuD(AmplifyApp,self).__init__(sXzuO,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,sXzuO,env=sXzuC):
  sXzuD(ElastiCacheCluster,self).__init__(sXzuO,env=env)
class TransferServer(BaseComponent):
 def __init__(self,sXzuO,env=sXzuC):
  sXzuD(TransferServer,self).__init__(sXzuO,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,sXzuO,env=sXzuC):
  sXzuD(CloudFrontDistribution,self).__init__(sXzuO,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,sXzuO,env=sXzuC):
  sXzuD(CodeCommitRepository,self).__init__(sXzuO,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
