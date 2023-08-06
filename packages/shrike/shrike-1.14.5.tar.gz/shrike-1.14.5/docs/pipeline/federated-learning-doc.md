# How to write a federated learning pipeline using shrike.pipeline.federated_learning
To enjoy this doc, you should be familiar with Azure ML and know how to use `shrike` to define and submit pipelines.

## Motivation
Federated learning has become a popular technique in machine learning, as it can train an algorithm against local data in multiple decentralized edge devices or silos, without moving the data across the boundary. While users can define a federated pipeline with explicitly writing for loops, data movement, and secure aggregation, we provide an easy and structured way to do cross-silo federated learning by introducing a new class `FederatedPipelineBase` with built-in methods for the user to inherit and override.

## Caveats
1. This is an experimental feature and could change at any time.
2. The APIs are designed for federated learning inside a single workspace. As of December 2021, compliant Azure ML workspaces do not support datastores/computes in different regions.

## Prerequisites
You need to have a workspace with at least one silo defined. A silo refers to a compute and a datastore in the corresponding region.

## Federated learning workflow
We consider four fundamental building blocks: preprocess pipeline, midprocess pipeline, postprocess pipeline, training pipeline. The workflow is shown as in the diagram:
```
preprocess (orchestrator) -> training (silos) -> midprocess (orchestrator) -> training (silos) -> midprocess (orchestrator) ... many rounds -> training (silos) -> postprocess (orchestrator)

```
![image](img/fl-diagram.png)

## Configure your pipeline through a yaml file
Example: [demo_federated_learning.yaml](https://github.com/Azure/shrike/blob/main/examples/pipelines/config/experiments/demo_federated_learning.yaml)

You need to add a `federated_config` section to your pipeline yaml file:
```yaml
federated_config:
  data_transfer_component: contoso.my_organization.fl.data_transfer
  silos: 
    silo1: 
      compute: fl-wus
      inherit: [foo_config]
      params:
        dataset: test_uploaded_from_local
    silo2:
      compute: fl-eus
      datastore: fl_eus
    silo3:
      compute: fl-canada
      datastore: fl_canada
      inherit: [foo_config, bar_config]
  max_iterations: 2
  params:
    msg: "random msg"
  config_group:
    default_config:
      params:
        msg: "shared msg"
        dataset: test_csv
    foo_config:
      datastore: fl_wus
    bar_config:
      params:
        msg: "per-silo msg"
```
There are several required fields:

1. `data_transfer_component`: name of the data transfer component **registered** in your workspace.
2. `silos`: compute and datastore name (required) in the silo, and optional `params` (dict) and `inherit`. `inherit` is a list of `config_group`s to apply to this silo, and the override priority is per-silo config > `inherit` > `default_config`.

Optional parameters:

1. `max_iteration`: number of training rounds, default is 1.
2. `config_group`: configs applying to all or some silos. `default_config` will be applied to all silos, and you can also define any customized configs.

After merging, the above config yaml is simplified to:
```yaml
federated_config:
  data_transfer_component: office.smart_reply.fl.data_transfer
  max_iterations: 2
  silos:
    silo1: 
      compute: fl-wus
      datastore: fl_wus
      params:
        msg: "shared msg"
        dataset: test_uploaded_from_local
    silo2:
      compute: fl-eus
      datastore: fl_eus
      params:
        msg: "shared msg"
        dataset: test_csv
    silo3:
      compute: fl-canada
      datastore: fl_canada
      params:
        msg: "per-silo msg"
        dataset: test_csv
  params:
    msg: "random msg"
```
To use the parameters in a pipeline, you can use the dot path. For example, `config.federated_config.params.msg` will return "random msg". Note that for `train` in silo, you can refer to per-silo parameters directly. For example, `silo.params.dataset` returns "test_uploaded_from_local", "test_csv", and "test_csv" for silo1, silo2, and silo3 respectively.

## Write the Python script for your pipeline
Example: [demo_federated_learning.py](https://github.com/Azure/shrike/blob/main/examples/pipelines/experiments/demo_federated_learning.py)

Unlike a typical pipeline script, here you need to create a class inheriting from `shrike.pipeline.FederatedPipelineBase` and **implement the four required steps**: `preprocess`, `train`, `midprocess`, and `postprocess`.
```python
from shrike.pipeline import FederatedPipelineBase, StepOutput

class MyCoolPipeline(FederatedPipelineBase):
    def preprocess(self, config, input):
        # Implement your preprocess step

    def train(self, config, input, silo):
        # Implement your training step

    def midprocess(self, config, input):
        # Implement your midprocess step

    def postprocess(self, config, input):
        # Implement your postprocess step

if __name__ == "__main__":
    MyCoolPipeline.main()
```
For each step, it takes arguments: `config`: a `DictConfig` from the pipeline yaml file, `input`: a list of references to outputs from the previous step, and for `train` only, `silo` which is `config.federated_config.silos.<current_silo>`. And you can 

- use a parameter defined in the pipeline yaml file, e.g., `config.federated_config.params.param1`;
- load an input dataset, e.g., `input_data = self.dataset_load(config.federated_config.params.dataset)`
- load an output from previous step, e.g., `input[0]`

There are two ways to define a step:

1. Use a `Component`, and return a `StepOutput` consisting of the `Component` object and a list of output names. 
```python
def train(self, config, input, silo):
    train_func = self.component_load("TrainInSilo")
    input_data = self.dataset_load(silo.params.dataset)
    train_step = train_func(
        input_01=input_data, input_02=input[0], message=silo.params.msg
    )
    return StepOutput(train_step, ["results1", "results2"])
```
:warning: The outputs will be fed into the downstream step **in order**. For example, in the code snippet above, `input_02=input[0]` is using the first output from `preprocess` or `midprocess`, and in the downstream midprocess step, `results1` and `results2` from `train_step` can be referred as `input[0]` and `input[1]` respectively.

2. Use a `Pipeline`, i.e. subgraph, and return a `StepOutput` wrapping the `Pipeline` object. We do not need to specify the outputs here because the subgraph should already return a dictionary of the outputs (e.g., [subgraph.py](https://github.com/Azure/shrike/blob/main/examples/pipelines/experiments/subgraph.py)). You need to import your subgraph and specify it through `required_subgraphs()` method:
```python
from shrike.pipeline import FederatedPipelineBase, StepOutput
from subgraph import DemoSubgraph

class MyCoolPipeline(FederatedPipelineBase):
    @classmethod
    def required_subgraphs(cls):
        return {"DemoSubgraph": DemoSubgraph}
    
    def midprocess(self, config, input):
        demo_subgraph = self.subgraph_load("DemoSubgraph")
        midprocess_step = demo_subgraph(
            input_data_01=input[0], input_data_02=input[1], input_data_03=input[2]
        )
        return StepOutput(midprocess_step)
```
