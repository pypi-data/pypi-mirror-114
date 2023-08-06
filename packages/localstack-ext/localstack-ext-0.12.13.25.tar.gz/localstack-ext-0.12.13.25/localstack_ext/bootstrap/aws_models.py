from localstack.utils.aws import aws_models
QtMhG=super
QtMhR=None
QtMhg=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  QtMhG(LambdaLayer,self).__init__(arn)
  self.cwd=QtMhR
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.QtMhg.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,QtMhg,env=QtMhR):
  QtMhG(RDSDatabase,self).__init__(QtMhg,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,QtMhg,env=QtMhR):
  QtMhG(RDSCluster,self).__init__(QtMhg,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,QtMhg,env=QtMhR):
  QtMhG(AppSyncAPI,self).__init__(QtMhg,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,QtMhg,env=QtMhR):
  QtMhG(AmplifyApp,self).__init__(QtMhg,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,QtMhg,env=QtMhR):
  QtMhG(ElastiCacheCluster,self).__init__(QtMhg,env=env)
class TransferServer(BaseComponent):
 def __init__(self,QtMhg,env=QtMhR):
  QtMhG(TransferServer,self).__init__(QtMhg,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,QtMhg,env=QtMhR):
  QtMhG(CloudFrontDistribution,self).__init__(QtMhg,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,QtMhg,env=QtMhR):
  QtMhG(CodeCommitRepository,self).__init__(QtMhg,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
