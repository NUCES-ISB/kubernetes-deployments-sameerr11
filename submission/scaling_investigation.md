# Scaling Investigation

## Replica Count in Deployment Files

In Kubernetes, the `replicas` field in a Deployment specification defines how many identical pods should be maintained at any given time. This is a key aspect of Kubernetes' ability to provide high availability and load balancing.

### Flask Application Deployment

In our `flask-deployment.yaml`, we have set:

```yaml
spec:
  replicas: 2
```

This means Kubernetes will maintain 2 identical pods running our Flask application. If one pod fails, Kubernetes will automatically create a new one to maintain the desired count.

### PostgreSQL Deployment

In our `postgres-deployment.yaml`, we have set:

```yaml
spec:
  replicas: 1
```

For the database, we use only 1 replica because PostgreSQL is a stateful application, and managing multiple replicas would require additional configuration for data synchronization.

## Scaling Effects

### Scaling Up

When we scale up the number of replicas:

```bash
kubectl scale deployment flask-app --replicas=5
```

Benefits:
- Increased availability: If one pod fails, others continue to serve requests
- Better load distribution: Requests are distributed across more pods
- Improved performance: Can handle more concurrent requests

### Scaling Down

When we scale down the number of replicas:

```bash
kubectl scale deployment flask-app --replicas=1
```

Effects:
- Reduced resource consumption: Fewer pods use less CPU and memory
- Single point of failure: If the only pod fails, the service becomes unavailable
- Potential performance bottleneck: All requests go to a single pod

## Min and Max Replicas

While our current deployment uses a fixed number of replicas, Kubernetes also supports automatic scaling with the Horizontal Pod Autoscaler (HPA).

With HPA, you can define:
- `minReplicas`: The minimum number of pods to maintain even during low load
- `maxReplicas`: The maximum number of pods allowed during high load

Example HPA configuration:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: flask-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flask-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

This would automatically scale the Flask application between 2 and 10 replicas based on CPU utilization, targeting 50% average utilization across all pods. 