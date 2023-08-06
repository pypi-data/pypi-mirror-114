# What's PyKit

# road map

## v0.0.1

- ddd
- error
- database
- cmd

# DDD 说明
## ValueObject
## Entity
## DomainService
## Repository
## ApplicationService

# gRPC的处理

GrpcApplicationServer
XXGrpcServicer
XXApplicationService

GrpcApplicationServer 抽象了gRPC的应用服务器，负责管理gRPC进程的生命周期、gRPC的路由调度等。
XXGrpcServicer 符合gRPC规则的业务服务的gRPC处理器，gRPC会将请求路由到对应的方法中，进而执行业务代码。
XXApplicationService DDD 中的 ApplicationService的子类。
ApplicationService 的返回error或者是抛出异常决定了grpc的response处理逻辑。


```python

class XXGrpcServicer(xx_pb2_grpc.XXServicer):
    def __init__(self):
        self.application_service

    @grpc_execute        
    def usecase(self):
        self.application_service.usecase()
```