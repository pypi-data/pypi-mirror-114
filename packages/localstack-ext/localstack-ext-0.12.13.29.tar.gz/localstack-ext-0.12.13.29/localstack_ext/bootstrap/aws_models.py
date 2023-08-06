from localstack.utils.aws import aws_models
BfKks=super
BfKko=None
BfKkg=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  BfKks(LambdaLayer,self).__init__(arn)
  self.cwd=BfKko
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.BfKkg.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,BfKkg,env=BfKko):
  BfKks(RDSDatabase,self).__init__(BfKkg,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,BfKkg,env=BfKko):
  BfKks(RDSCluster,self).__init__(BfKkg,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,BfKkg,env=BfKko):
  BfKks(AppSyncAPI,self).__init__(BfKkg,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,BfKkg,env=BfKko):
  BfKks(AmplifyApp,self).__init__(BfKkg,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,BfKkg,env=BfKko):
  BfKks(ElastiCacheCluster,self).__init__(BfKkg,env=env)
class TransferServer(BaseComponent):
 def __init__(self,BfKkg,env=BfKko):
  BfKks(TransferServer,self).__init__(BfKkg,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,BfKkg,env=BfKko):
  BfKks(CloudFrontDistribution,self).__init__(BfKkg,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,BfKkg,env=BfKko):
  BfKks(CodeCommitRepository,self).__init__(BfKkg,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
