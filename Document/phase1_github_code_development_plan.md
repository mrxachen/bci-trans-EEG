# 第一阶段 GitHub 项目代码开发方案（Phase I）

## 1. 目标与定位

本方案服务于第一阶段研究主线：

> **基于公开运动想象（MI）数据集，构建标准化跨设备评测基准，并开发“显式设备因子分解 + 新设备少样本快速适配”的 EEG 解码框架。**

代码工程的目标不是单纯“能跑通一个模型”，而是同时满足四个要求：

1. **科研可复现**：同一配置、同一随机种子、同一协议下，结果可复现；
2. **研究可扩展**：先支持 MI 单模态 EEG，后续无缝扩展到 SSVEP、EOG、真实设备数据；
3. **工程可维护**：模块职责清晰，避免“所有逻辑都堆进一个 notebook”；
4. **部署可衔接**：后续可以把数据接口、推理模块和适配模块迁移到真实设备与边缘环境中。

---

## 2. 设计原则

第一阶段的代码工程建议遵循以下原则：

### 2.1 Local-first，本地优先

你的主力算力是 RTX4060 笔记本，因此项目设计必须优先保证：

- 基线训练、消融实验、主协议评测都能在本地跑；
- 模型默认轻量化；
- 大规模 sweep 和大模型特征提取只作为可选增强。

### 2.2 Benchmark-first，先基准后方法

第一阶段最重要的不是先造一个复杂模型，而是先把：

- 数据接入
- 统一预处理
- 协议定义
- 评测脚本
- 强基线

全部工程化。新方法必须建立在强 benchmark 上，否则很难形成有说服力的论文。

### 2.3 Config-driven，配置驱动

所有关键实验都不应依赖“手改 Python 文件”。  
应采用 **YAML 配置驱动**：

- 数据集组合
- 预处理参数
- 模型结构
- 损失系数
- 训练参数
- 评测协议

全部通过配置管理。

### 2.4 Interface-first，先定义抽象接口

第一阶段会遇到大量异构数据源，因此必须优先定义统一接口：

- Dataset Adapter
- Preprocessor
- Channel Mapper
- Protocol Splitter
- Model Backbone
- Loss Module
- Evaluator

这样当你以后接入博睿康、NeuralScan 或借来的其他设备时，只需要新增 adapter，而不需要重写训练主流程。

### 2.5 Paper-oriented，面向论文结果组织

仓库必须天然支持输出：

- 表格
- 图像
- 配置快照
- 消融结果
- 可复现实验记录

因为第一阶段最终目标是论文，而不是只做内部 demo。

---

## 3. 推荐仓库命名与总体形式

## 3.1 仓库命名建议

建议你在 GitHub 上使用以下任一命名：

- `defeeg`
- `cross-device-eeg-mi`
- `cd-mi-benchmark`
- `defeeg-phase1`

我更推荐：

> **`defeeg`**

原因：

- 简短；
- 容易记忆；
- 后续第二阶段、第三阶段仍能复用；
- 和论文方法名 `DeFEEG` 对齐。

## 3.2 仓库形态建议

建议采用：

- **单仓库（monorepo）**
- 一个主 Python 包
- 一套统一配置系统
- 一套统一实验入口脚本
- 一套统一结果输出目录

不建议第一阶段拆成多个仓库，否则维护成本高、实验记录容易分裂。

---

## 4. 技术栈建议

## 4.1 核心语言与框架

- **Python**
- **PyTorch**：模型训练主框架
- **MNE**：EEG 读取、滤波、重参考、epoch 切片
- **NumPy / SciPy / pandas**：基础数值与元数据处理
- **scikit-learn**：传统基线、指标、统计分析
- **pyriemann**：黎曼几何基线
- **matplotlib**：论文图表输出

## 4.2 配置与实验管理

建议使用：

- **YAML**：配置文件
- 一个简单的自定义配置加载器，或使用 Hydra/OmegaConf 风格结构  
  第一阶段如果你想降低复杂度，可以先用“纯 YAML + argparse”。

## 4.3 日志与追踪

第一阶段建议至少支持：

- 本地 `logs/` 文本日志
- `results/*.json` 指标快照
- `artifacts/figures/` 图表
- `artifacts/tables/` 结果表格

可选：

- TensorBoard
- W&B（如果你愿意在线追踪）

## 4.4 测试与代码质量

建议至少加入：

- `pytest`
- `ruff` 或 `flake8`
- `black`
- `pre-commit`

这能显著降低后续维护成本。

---

## 5. 仓库总目录结构（推荐版本）

```text
defeeg/
├── README.md
├── LICENSE
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── environment.yml
├── Makefile
├── configs/
│   ├── default.yaml
│   ├── data/
│   │   ├── mi_cross_device_v1.yaml
│   │   ├── eegmmidb.yaml
│   │   ├── lee2019_mi.yaml
│   │   ├── cho2017.yaml
│   │   └── dreyer2023.yaml
│   ├── preprocess/
│   │   ├── mi_default.yaml
│   │   ├── mi_fbcsp.yaml
│   │   └── mi_virtual_grid.yaml
│   ├── protocol/
│   │   ├── within_device.yaml
│   │   ├── lodo_zero_shot.yaml
│   │   ├── lodo_few_shot.yaml
│   │   └── channel_ablation.yaml
│   ├── model/
│   │   ├── csp_lda.yaml
│   │   ├── riemann_ts_lr.yaml
│   │   ├── eegnet.yaml
│   │   ├── dann_eegnet.yaml
│   │   └── defeeg_v1.yaml
│   ├── trainer/
│   │   ├── default.yaml
│   │   ├── local_4060.yaml
│   │   └── a100_optional.yaml
│   └── experiment/
│       ├── exp_baseline_eegnet.yaml
│       ├── exp_baseline_riemann.yaml
│       ├── exp_dann.yaml
│       ├── exp_defeeg_zero_shot.yaml
│       └── exp_defeeg_few_shot.yaml
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── registry/
│       ├── datasets.csv
│       ├── subjects.csv
│       └── channels.csv
├── docs/
│   ├── architecture.md
│   ├── dataset_adapters.md
│   ├── protocols.md
│   ├── experiment_guide.md
│   └── reproduction_checklist.md
├── scripts/
│   ├── download/
│   │   ├── fetch_eegmmidb.py
│   │   ├── fetch_openbmi.py
│   │   └── fetch_public_mi.py
│   ├── preprocess/
│   │   ├── build_registry.py
│   │   ├── preprocess_dataset.py
│   │   ├── preprocess_all.py
│   │   └── export_bidslite.py
│   ├── train/
│   │   ├── train_baseline.py
│   │   ├── train_dann.py
│   │   ├── train_defeeg.py
│   │   └── adapt_few_shot.py
│   ├── eval/
│   │   ├── eval_within_device.py
│   │   ├── eval_lodo_zero_shot.py
│   │   ├── eval_lodo_few_shot.py
│   │   └── run_full_benchmark.py
│   ├── analysis/
│   │   ├── summarize_results.py
│   │   ├── plot_tables.py
│   │   ├── plot_embeddings.py
│   │   ├── plot_fewshot_curves.py
│   │   └── stats_test.py
│   └── dev/
│       ├── smoke_test.py
│       └── profile_train.py
├── src/
│   └── defeeg/
│       ├── __init__.py
│       ├── utils/
│       │   ├── seed.py
│       │   ├── io.py
│       │   ├── logging.py
│       │   ├── config.py
│       │   ├── paths.py
│       │   └── registry.py
│       ├── data/
│       │   ├── base.py
│       │   ├── schemas.py
│       │   ├── dataset_hub.py
│       │   ├── adapters/
│       │   │   ├── eegmmidb.py
│       │   │   ├── lee2019_mi.py
│       │   │   ├── cho2017.py
│       │   │   └── dreyer2023.py
│       │   ├── transforms/
│       │   │   ├── filtering.py
│       │   │   ├── rereference.py
│       │   │   ├── resample.py
│       │   │   ├── normalize.py
│       │   │   ├── epoching.py
│       │   │   └── artifact.py
│       │   ├── channels/
│       │   │   ├── montage.py
│       │   │   ├── common_subset.py
│       │   │   ├── virtual_grid.py
│       │   │   └── interpolate.py
│       │   ├── labels/
│       │   │   ├── mi_label_map.py
│       │   │   └── event_mapper.py
│       │   ├── datasets/
│       │   │   ├── epoch_dataset.py
│       │   │   ├── tensor_dataset.py
│       │   │   └── metadata_dataset.py
│       │   └── splits/
│       │       ├── within_device.py
│       │       ├── leave_one_device_out.py
│       │       └── few_shot_sampler.py
│       ├── preprocess/
│       │   ├── pipeline.py
│       │   ├── bidslite.py
│       │   └── qc.py
│       ├── baselines/
│       │   ├── csp_lda.py
│       │   ├── fbcsp.py
│       │   ├── riemann_ts.py
│       │   └── ea.py
│       ├── models/
│       │   ├── common/
│       │   │   ├── blocks.py
│       │   │   ├── adapters.py
│       │   │   ├── pooling.py
│       │   │   └── heads.py
│       │   ├── backbones/
│       │   │   ├── eegnet.py
│       │   │   ├── shallowconvnet.py
│       │   │   └── lite_encoder.py
│       │   ├── domain/
│       │   │   ├── grl.py
│       │   │   ├── dann.py
│       │   │   └── prototype.py
│       │   ├── defeeg/
│       │   │   ├── metadata_encoder.py
│       │   │   ├── feature_modulation.py
│       │   │   ├── disentangler.py
│       │   │   ├── device_head.py
│       │   │   ├── task_head.py
│       │   │   ├── fewshot_adapter.py
│       │   │   └── model.py
│       │   └── factory.py
│       ├── losses/
│       │   ├── classification.py
│       │   ├── device_adv.py
│       │   ├── orthogonal.py
│       │   ├── prototype_align.py
│       │   └── total_loss.py
│       ├── trainers/
│       │   ├── base_trainer.py
│       │   ├── baseline_trainer.py
│       │   ├── domain_trainer.py
│       │   ├── defeeg_trainer.py
│       │   └── fewshot_trainer.py
│       ├── evaluation/
│       │   ├── metrics.py
│       │   ├── evaluator.py
│       │   ├── device_report.py
│       │   ├── embedding_viz.py
│       │   └── statistical_test.py
│       └── cli/
│           ├── preprocess.py
│           ├── train.py
│           ├── eval.py
│           └── analyze.py
├── tests/
│   ├── test_config.py
│   ├── test_registry.py
│   ├── test_preprocess.py
│   ├── test_channel_mapping.py
│   ├── test_splits.py
│   ├── test_models.py
│   ├── test_losses.py
│   └── test_smoke_training.py
├── outputs/
│   ├── logs/
│   ├── runs/
│   ├── checkpoints/
│   ├── tables/
│   └── figures/
└── notebooks/
    ├── 00_data_audit.ipynb
    ├── 01_sanity_check_single_dataset.ipynb
    ├── 02_embedding_viz.ipynb
    └── 03_error_analysis.ipynb
```

---

## 6. 为什么建议用这种仓库结构

这个结构对应第一阶段的四个核心任务：

1. **数据标准化** → `src/defeeg/data`, `src/defeeg/preprocess`
2. **强基线建立** → `src/defeeg/baselines`, `scripts/train/train_baseline.py`
3. **核心方法开发** → `src/defeeg/models/defeeg`, `src/defeeg/losses`
4. **论文结果与复现** → `scripts/eval`, `scripts/analysis`, `outputs/`

它直接服务于你综述中强调的四件事：  
标准化预处理、BIDS/元数据统一、强基线、显式设备效应建模。fileciteturn0file0

---

## 7. 主包模块设计

## 7.1 `data/`：数据接入与统一抽象

这是整个项目最关键的底座。

### 目标
把不同来源的数据都转成统一抽象对象，例如：

- `RawRecording`
- `EpochRecord`
- `DatasetSample`
- `MetadataRecord`

### 建议的核心抽象

```python
class DatasetAdapter:
    def list_subjects(self) -> list[str]:
        ...
    def load_raw(self, subject_id: str):
        ...
    def load_events(self, subject_id: str):
        ...
    def get_metadata(self, subject_id: str) -> dict:
        ...
```

### 每个 adapter 应完成什么

每个数据集 adapter 只负责三件事：

1. 读取原始格式；
2. 解析事件和标签；
3. 输出统一元数据字典。

它**不要**做复杂预处理，不要在 adapter 里夹杂训练逻辑。

### 你第一阶段必须先实现的 adapter

- `eegmmidb.py`
- `lee2019_mi.py`
- `cho2017.py`
- `dreyer2023.py`

这四个正是你第一阶段主 benchmark 的起点。fileciteturn0file0

---

## 7.2 `preprocess/`：标准化预处理层

### 目标
把异构原始数据统一变成可训练的 epoch 张量。

### 建议拆分的预处理步骤

1. 读取和事件对齐
2. 工频陷波
3. 带通滤波
4. 重采样
5. 重参考
6. epoch 切片
7. 坏段/伪迹规则处理
8. 鲁棒归一化
9. 通道映射
10. 输出缓存

### 关键设计原则
**每一步都要可单独开关、可单独记录。**

不要把所有预处理写成一个黑盒函数。应采用流水线对象：

```python
class PreprocessPipeline:
    def __init__(self, steps: list):
        self.steps = steps

    def run(self, raw, events, metadata):
        data = raw
        for step in self.steps:
            data = step(data, events=events, metadata=metadata)
        return data
```

### 为什么这样重要
因为第一阶段论文一定会涉及：

- 不同预处理策略消融
- 不同参考方式对比
- 不同通道统一协议对比

如果预处理不是模块化的，后续所有实验都会非常痛苦。你的综述也明确指出，预处理选择对解码性能的影响不亚于模型选择。fileciteturn0file0

---

## 7.3 `channels/`：通道统一与空间映射层

这是“跨设备”项目特有的重要模块。

### 必做两个协议

#### 协议 A：严格公共通道
例如统一保留：

- FC3, FCz, FC4
- C3, Cz, C4
- CP3, CPz, CP4

适合做最稳的主 benchmark。

#### 协议 B：虚拟统一电极网格
将不同设备通道映射到统一 10-20/10-10 虚拟网格。

### 需要实现的类

```python
class ChannelMapper:
    def fit(self, montage_info):
        ...
    def transform(self, x, ch_names):
        ...
```

### 相关文件职责

- `common_subset.py`：公共子集映射
- `virtual_grid.py`：虚拟网格定义
- `interpolate.py`：插值逻辑
- `montage.py`：坐标模板与通道名标准化

---

## 7.4 `splits/`：协议与数据划分层

### 为什么一定要单独抽出来
很多 EEG 项目把 train/test split 写死在 notebook 里，这会导致论文不可复现。  
你第一阶段的核心就是 benchmark，因此划分协议必须成为一等公民。

### 必须支持的协议

1. `within_device.py`
2. `leave_one_device_out.py`
3. `few_shot_sampler.py`

### 协议抽象建议

```python
class Protocol:
    def build_splits(self, registry_df):
        ...
```

### 需要输出什么
协议模块必须输出：

- train / val / test 索引
- 每个样本的设备 ID
- few-shot 适配子集索引
- 统计摘要（每设备、每类别、每被试数量）

---

## 7.5 `baselines/`：传统方法与强基线层

第一阶段不建议一开始就把所有传统方法都塞进主包深处。应明确单独建立 `baselines/`。

### 第一批必须落地的基线

#### 传统
- CSP + LDA
- FBCSP + LDA
- Riemannian Tangent Space + Logistic Regression
- EA + 传统分类器

#### 深度
- EEGNet
- ShallowConvNet

#### 域适应
- EA + EEGNet
- DANN

### 设计建议
对于传统方法，最好做成 **sklearn 风格 wrapper**：

```python
class BaselineModel:
    def fit(self, X, y, metadata=None):
        ...
    def predict(self, X):
        ...
    def predict_proba(self, X):
        ...
```

这样评测器可以统一调用，不需要分别写不同脚本。

---

## 7.6 `models/defeeg/`：核心方法模块

这是第一阶段的研究主线实现区。

### 模块组成建议

#### `metadata_encoder.py`
输入设备元数据，例如：

- device_id
- sampling_rate
- reference_type
- channel_count
- hardware_filter_flags

输出一个低维 metadata embedding。

#### `feature_modulation.py`
实现 FiLM 或其他调制方式，把元数据嵌入用于特征调制。

#### `disentangler.py`
从共享特征中分出：

- `z_task`
- `z_device`

#### `device_head.py`
用于设备识别。

#### `task_head.py`
用于主任务分类。

#### `fewshot_adapter.py`
实现新设备的小参数适配器。

#### `model.py`
组装整个 DeFEEG 模型。

---

## 8. 第一阶段推荐的模型接口

建议从一开始就统一模型接口，否则脚本会非常混乱。

```python
class EEGModel(nn.Module):
    def forward(self, x, metadata=None):
        return {
            "logits": ...,
            "z_task": ...,
            "z_device": ...,
            "aux": ...
        }
```

### 统一返回字典的好处

1. 方便不同损失函数组合；
2. 方便可视化表征；
3. 方便 few-shot adapter 只取部分输出；
4. 方便后续扩展到多模态。

---

## 9. `losses/`：损失函数模块

### 推荐拆分

- `classification.py`：交叉熵/标签平滑
- `device_adv.py`：设备对抗相关损失
- `orthogonal.py`：任务/设备表征解耦损失
- `prototype_align.py`：类条件原型对齐
- `total_loss.py`：按配置聚合总损失

### 为什么不能写在 trainer 里
因为第一阶段一定要做消融：

- 去掉 `L_adv`
- 去掉 `L_proto`
- 去掉 `L_ortho`
- 只保留 `L_cls + L_dev`
- 等等

如果损失逻辑和 trainer 混在一起，会让实验矩阵很难维护。

---

## 10. `trainers/`：训练编排层

### 建议训练器拆成四类

#### `baseline_trainer.py`
负责 EEGNet、ShallowConvNet 等普通监督训练。

#### `domain_trainer.py`
负责 DANN 这类域对抗训练。

#### `defeeg_trainer.py`
负责第一阶段主方法训练。

#### `fewshot_trainer.py`
负责目标设备少样本适配。

### 基础抽象

```python
class Trainer:
    def train(self):
        ...
    def validate(self):
        ...
    def save_checkpoint(self):
        ...
```

### 关键能力

每个 trainer 至少支持：

- checkpoint 保存
- best model 选择
- early stopping
- seed 固定
- gradient clipping
- mixed precision（可选）

---

## 11. `evaluation/`：评测与结果分析层

第一阶段论文是否漂亮，很大程度上取决于这层做得好不好。

### 核心模块

#### `metrics.py`
统一计算：

- Balanced Accuracy
- Macro-F1
- Cohen’s Kappa
- confusion matrix

#### `evaluator.py`
负责接收 model 和 split，输出统一结果字典。

#### `device_report.py`
生成按设备分组的明细结果。

#### `embedding_viz.py`
生成 t-SNE/UMAP、设备着色图、类别着色图。

#### `statistical_test.py`
做配对统计检验与置信区间汇总。

### 强烈建议
所有结果都输出为统一 JSON，例如：

```json
{
  "experiment_name": "defeeg_lodo_zero_shot",
  "seed": 42,
  "protocol": "leave_one_device_out",
  "target_device": "gtec_gusbamp",
  "metrics": {
    "balanced_acc": 0.741,
    "macro_f1": 0.732,
    "kappa": 0.482
  }
}
```

这样后续 `summarize_results.py` 才能自动汇总表格。

---

## 12. `scripts/`：脚本层设计

第一阶段建议所有正式实验都通过 `scripts/` 调用，避免 notebook 成为主入口。

## 12.1 数据脚本

### `build_registry.py`
作用：

- 扫描所有数据集
- 建立统一数据注册表
- 输出设备、被试、类别、通道统计

### `preprocess_dataset.py`
作用：

- 对单个数据集执行预处理
- 便于单独调试

### `preprocess_all.py`
作用：

- 一键预处理全部主数据集
- 生成 processed cache

---

## 12.2 训练脚本

### `train_baseline.py`
训练传统/深度基线。

### `train_dann.py`
训练域对抗基线。

### `train_defeeg.py`
训练第一阶段主方法。

### `adapt_few_shot.py`
固定主干，对目标设备做少样本适配。

---

## 12.3 评测脚本

### `eval_within_device.py`
检查 sanity。

### `eval_lodo_zero_shot.py`
核心协议脚本。

### `eval_lodo_few_shot.py`
few-shot 适配协议脚本。

### `run_full_benchmark.py`
用于一键运行论文主实验矩阵。

---

## 12.4 分析脚本

### `summarize_results.py`
汇总 JSON/CSV 结果，生成总表。

### `plot_tables.py`
输出论文表格。

### `plot_embeddings.py`
输出表征图。

### `plot_fewshot_curves.py`
输出 few-shot 曲线。

### `stats_test.py`
输出统计检验结果。

---

## 13. 推荐的数据流设计

整个项目的数据流建议固定为下面这个形式：

```text
raw files
  -> dataset adapter
  -> metadata extraction
  -> preprocessing pipeline
  -> channel mapping
  -> epoch cache
  -> protocol split
  -> dataloader
  -> training / adaptation
  -> evaluation
  -> json results + figures + tables
```

### 为什么这样设计
因为你将来接入真实设备时，只需要替换：

- `dataset adapter`
- `metadata extraction`

后面的流程几乎全部可复用。

---

## 14. 配置系统设计

第一阶段配置建议分 6 层：

1. `data`
2. `preprocess`
3. `protocol`
4. `model`
5. `trainer`
6. `experiment`

### 推荐的 experiment 配置结构

```yaml
name: exp_defeeg_zero_shot
seed: 42

data:
  dataset_bundle: mi_cross_device_v1

preprocess:
  profile: mi_default

protocol:
  name: lodo_zero_shot

model:
  name: defeeg_v1

trainer:
  profile: local_4060

output:
  root: outputs/runs/exp_defeeg_zero_shot
```

### 这样做的好处
一个实验名就唯一对应一套配置快照，方便：

- 复现
- 回滚
- 论文附录补充
- 多人协作

---

## 15. 第一阶段建议的开发顺序

不要并行开太多模块。建议严格按下面顺序推进。

## 阶段 A：仓库地基（第 1 周）

### 任务
- 初始化仓库
- 建立目录结构
- 补齐 `README`, `requirements`, `pyproject`, `Makefile`
- 建立 `src/defeeg/` 主包
- 建立 YAML 配置加载器
- 建立最简单的 CLI

### 验收标准
- `python -m defeeg.cli.preprocess --help` 可以运行
- `pytest` 可以通过空测试
- 可以从配置文件读取参数

---

## 阶段 B：数据层与 registry（第 1–2 周）

### 任务
- 实现 `DatasetAdapter` 抽象
- 先接入 1 个数据集（建议 EEGMMIDB）
- 建立 registry CSV
- 输出 dataset audit 报告

### 验收标准
- 可以打印：
  - 被试数
  - 通道数
  - 采样率
  - 类别分布
  - 设备元数据

---

## 阶段 C：预处理与公共通道协议（第 2–3 周）

### 任务
- 实现默认 MI 预处理链
- 实现公共通道映射
- 输出统一 epoch cache

### 验收标准
- 四个主数据集至少有 1 个完整跑通
- 输出 shape 完全统一
- 生成 QC 图和样本摘要

---

## 阶段 D：强基线（第 3–5 周）

### 任务
- 完成 CSP + LDA
- 完成 Riemann TS + LR
- 完成 EEGNet
- 完成 within-device + zero-shot LODO 测试

### 验收标准
- 结果可以自动写入 JSON
- 可以输出第一版论文表格

---

## 阶段 E：域适应基线（第 5–6 周）

### 任务
- 完成 EA + EEGNet
- 完成 DANN
- 完成 zero-shot 对比

### 验收标准
- 能明确看出：传统 / 深度 / 域适应 三类方法的差异

---

## 阶段 F：DeFEEG v1（第 6–8 周）

### 任务
- 实现 metadata encoder
- 实现 task/device disentangler
- 实现 orthogonal loss
- 实现 device adversarial branch
- 实现 prototype alignment

### 验收标准
- 能在至少一个主协议上超过最强基线
- 或者即便不稳定提升，也能输出完整消融结论

---

## 阶段 G：few-shot adapter（第 8–9 周）

### 任务
- 实现低秩 adapter
- 实现 target-device few-shot sampler
- 画出适配曲线

### 验收标准
- 能输出 5/10/20/40 trials per class 曲线
- 能和 full fine-tuning 比较

---

## 阶段 H：收尾与论文化（第 10–12 周）

### 任务
- 固化实验配置
- 完成统计检验
- 输出最终图表
- 补齐 README 和复现实验指南

### 验收标准
- 删掉 notebook，也能通过命令行复现主结果
- 结果组织足以直接写论文

---

## 16. 建议的 Git 分支策略

第一阶段不建议太复杂。推荐：

- `main`：始终可运行
- `dev`：日常开发
- `feat/data-adapters`
- `feat/preprocess`
- `feat/baselines`
- `feat/defeeg-model`
- `feat/fewshot-adapter`
- `exp/...`：临时实验分支（可选）

### 提交规范建议

采用简洁的 commit prefix：

- `feat:`
- `fix:`
- `refactor:`
- `docs:`
- `test:`
- `exp:`

例如：

- `feat: add eegmmidb adapter`
- `feat: implement common channel mapper`
- `feat: add defeeg disentangler`
- `fix: correct event mapping for cho2017`

---

## 17. README 应该怎么写

GitHub 首屏非常重要。README 建议包含以下结构：

1. 项目简介
2. 研究问题
3. 当前阶段目标
4. 支持的数据集
5. 安装方式
6. 快速开始
7. 目录结构说明
8. 主要实验命令
9. 结果复现说明
10. 论文与引用格式
11. 后续路线图

### README 中的“快速开始”建议至少包含 4 条命令

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 构建数据注册表
python scripts/preprocess/build_registry.py

# 3. 运行一个 sanity baseline
python scripts/train/train_baseline.py --config configs/experiment/exp_baseline_eegnet.yaml

# 4. 汇总结果
python scripts/analysis/summarize_results.py --input outputs/runs
```

---

## 18. 测试策略

第一阶段的 EEG 项目很容易忽视测试，但你这个项目跨数据集、跨设备，测试非常关键。

## 18.1 必测项

### 数据层测试
- 能否正确读到样本数
- 通道名是否标准化
- 事件标签是否正确映射

### 预处理测试
- 滤波后 shape 不变
- 重采样后采样率正确
- 公共通道映射后通道顺序一致

### 协议测试
- leave-one-device-out 是否真的隔离设备
- few-shot 是否严格只取目标设备少量样本

### 模型测试
- forward 输出字段是否完整
- 损失是否可反向传播

### 训练 smoke test
- 用极小 fake 数据跑 1–2 个 epoch 不报错

## 18.2 不建议做什么
第一阶段不建议把时间花在极复杂的集成测试框架上。  
你的测试目标是“避免低级错误破坏实验”，不是构建企业级 CI 平台。

---

## 19. 结果管理与复现策略

### 19.1 每次实验必须保存

- 完整配置快照
- 随机种子
- git commit hash
- 指标 JSON
- checkpoint 路径
- 关键日志
- 生成图表

### 19.2 推荐输出目录结构

```text
outputs/runs/exp_defeeg_zero_shot/
├── config.yaml
├── metrics.json
├── train.log
├── best.ckpt
├── predictions.csv
└── figures/
```

### 19.3 为什么必须保存 git hash
因为第一阶段方法会持续修改。如果没有 git hash，后面你很可能分不清：

- 哪个结果对应哪版代码
- 哪张图对应哪组配置
- 哪次提升是偶然还是稳定

---

## 20. 论文结果表格应该如何由代码自动生成

建议从一开始就准备三类固定输出表：

### 表 1：数据集统计表
- 数据集
- 设备
- 通道数
- 采样率
- 被试数
- 类别

### 表 2：主结果表
- 方法
- within-device
- zero-shot LODO 平均
- 各目标设备结果
- few-shot 结果

### 表 3：消融表
- 去掉 metadata
- 去掉 adversarial branch
- 去掉 orthogonal loss
- 去掉 prototype alignment
- 去掉 adapter

让 `plot_tables.py` 或 `summarize_results.py` 自动生成 CSV/Markdown/LaTeX 三份输出。

---

## 21. 和未来真实设备接入的接口预留

虽然第一阶段主数据是公开数据，但代码上必须为真实设备接入留接口。

## 21.1 新增 `local_device_adapter.py`
未来你的博睿康/NeuralScan 数据只需要新增一个 adapter：

- 解析厂商原始格式
- 解析事件标记
- 输出统一 metadata

## 21.2 新增 `streaming/`（第二阶段再做）
第一阶段不一定真的实现，但目录上可以预留：

```text
src/defeeg/streaming/
    buffer.py
    online_preprocess.py
    online_infer.py
```

## 21.3 为什么值得预留
因为你的最终目标不是只做离线论文，而是后续可能要走向：

- 实时推理
- 边缘部署
- 6G 边云协同

第一阶段代码如果是纯“离线 notebook 风格”，后续迁移代价会很大。

---

## 22. 第一阶段建议的 Issue 列表

你可以在 GitHub 一开始就建这些 issues：

### Milestone 1：Project Bootstrap
- [ ] 初始化仓库和基础依赖
- [ ] 建立配置系统
- [ ] 建立 logger 和路径管理

### Milestone 2：Data Foundation
- [ ] 实现 EEGMMIDB adapter
- [ ] 实现 Lee2019_MI adapter
- [ ] 实现 Cho2017 adapter
- [ ] 实现 Dreyer2023 adapter
- [ ] 建立 dataset registry

### Milestone 3：Preprocessing
- [ ] 实现 MI 默认预处理流水线
- [ ] 实现 common subset mapper
- [ ] 实现 virtual grid mapper

### Milestone 4：Baselines
- [ ] CSP + LDA
- [ ] FBCSP + LDA
- [ ] Riemann TS + LR
- [ ] EEGNet
- [ ] DANN

### Milestone 5：DeFEEG
- [ ] metadata encoder
- [ ] feature modulation
- [ ] disentangler
- [ ] device branch
- [ ] prototype alignment
- [ ] few-shot adapter

### Milestone 6：Evaluation and Paper
- [ ] zero-shot benchmark
- [ ] few-shot curves
- [ ] ablation scripts
- [ ] result summarizer
- [ ] plotting scripts

---

## 23. 第一个可运行版本（MVP）应该长什么样

不要试图一开始就完成全部功能。  
第一版最小可运行版本建议只包含：

1. 一个数据集 adapter（EEGMMIDB）
2. 一个预处理链
3. 一个公共通道映射
4. 一个 EEGNet baseline
5. 一个 within-device 评测脚本
6. 一个结果 JSON 输出

### MVP 验收标准
你在本地运行下面这个命令能成功：

```bash
python scripts/train/train_baseline.py \
  --config configs/experiment/exp_baseline_eegnet.yaml
```

并且产生：

- `metrics.json`
- `best.ckpt`
- `train.log`

### 为什么必须先做 MVP
因为很多科研代码失败，不是败在方法，而是败在工程一开始过大过散。

---

## 24. 第一阶段不建议做的事情

为了防止工程失控，下面这些事建议暂时不要做：

1. **不要一开始上大型 foundation model 全参数微调**
2. **不要一开始支持太多范式（MI 先打穿）**
3. **不要先做在线流式系统**
4. **不要先做多模态 EEG+EOG 联合建模**
5. **不要把数据下载、预处理、训练逻辑写死在 notebook**
6. **不要为了“看起来高级”而过早引入过重的工程框架**

你的第一阶段核心是：**一个扎实的 benchmark + 一个可发表的方法 + 一套可维护的工程骨架。**

---

## 25. 第一阶段的代码开发总路线图

可以把整个 GitHub 开发路线压缩为三层：

### 第 1 层：先把“地基”搭起来
- 仓库骨架
- 数据 adapter
- 预处理流水线
- protocol split
- result logging

### 第 2 层：把“论文最需要的 baseline”做扎实
- CSP/FBCSP
- Riemann
- EEGNet
- DANN

### 第 3 层：最后做“真正的创新方法”
- Device metadata
- Disentangled representation
- Prototype alignment
- Few-shot adapter

这和你第一阶段科研路线是完全一致的，不会出现“代码路线”和“论文路线”分裂的问题。

---

## 26. 最终建议

如果把这份代码开发方案压缩成一句话，我给你的建议是：

> **把 GitHub 项目做成一个“标准化跨设备 EEG benchmark + DeFEEG 方法框架”的研究型工程仓库，而不是零散实验脚本集合。**

这样做的好处是：

- 短期可以快速出结果；
- 中期可以直接支撑论文投稿；
- 后期接真实设备、多模态和 6G 部署时，不需要推倒重来。

第一阶段真正有价值的，不只是某个模型精度提升，而是你能形成一套**可复现、可扩展、可落地**的跨设备 EEG 研究工程底座。这个工程底座本身，就是你后续持续产出论文和系统成果的基础。其设计也与你上传综述中强调的 BIDS-EEG、MNE-BIDS-Pipeline、标准化跨设备评测与显式设备建模方向一致。fileciteturn0file0

---

## 27. 下一步最合理的衔接

完成这一步后，最值得立刻继续的不是再泛泛讨论，而是直接进入：

> **把这个代码开发方案进一步细化成“首个版本的仓库初始化清单 + 每个核心文件的代码模板”。**

也就是下一步我可以继续为你输出：

- 仓库初始化命令
- `pyproject.toml` / `requirements.txt` 建议
- `README.md` 初稿
- `src/defeeg/...` 第一版文件模板
- 第一个 baseline 的开发顺序
- 第一个月可以直接执行的任务清单