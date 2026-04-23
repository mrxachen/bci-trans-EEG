# 跨设备脑电数据融合：可行性、方法与战略机遇

**将不同采集设备获取的脑电（EEG）数据融合为统一数据集，在聚合层面的神经特征上目前已具备条件可行性，但在细粒度脑机接口应用层面仍是一个未解决的挑战。** 该领域比功能磁共振成像（fMRI）的数据协调工作滞后约八年——ComBat统计协调方法首次应用于EEG是在2024年。然而，2023–2025年间EEG基础模型（LaBraM、REVE、CBraMod、BIOT、EEGPT）的集中涌现，已经开辟了一条切实可行的设备无关化脑电处理路径。对于电信研究机构而言，这是一个时机恰当的战略窗口：跨设备EEG融合处于巨大未满足科学需求、中国积极推进的国家脑机接口政策布局，以及运营商独具的基础设施优势（云计算、边缘部署、联邦学习）三者的交汇点上。

---

## 一、设备差异客观存在但可控——约占总信号方差的9%

对跨设备EEG效应最严谨的量化研究来自Ratti等人（2017）[1]，该研究在六种标准范式下对EEG数据方差进行了分解。**被试间差异在总方差中占主导地位，约为32%**，设备/系统差异约占**9%**，而会话间（session-to-session）变异仅约1%。当样本量约为16名被试时，设备方差的量级已与每位被试的个体方差相当——这意味着任何跨系统汇集数据的研究都不可忽视设备效应。

关键发现是：**研究级系统之间可统计互换**（在各范式间无显著均值差异），而消费级和干电极系统会引入系统性偏差，在至少一半的测试范式中产生显著差异值[1]。2024年发表的一项消费级与研究级设备频谱特征对比研究[2]证实了这一不对称性：PSBD Headband Pro在alpha频段与Brain Products研究级放大器的相关性可达r=0.9，而**Muse的信号质量最差**，对齐度极低。

这些设备效应的技术根源贯穿信号链的每一层：

**通道配置差异**：电极数量从1个（NeuroSky MindWave）到280个（BioSemi ActiveTwo）[3]不等，电极布局遵循互不兼容的标准——10-20系统、扩展10-10系统、EGI的等距测地线放置（使用数字标识符），以及Emotiv的14通道专有配置[4]等。

**采样率差异**：跨越两个数量级，从128 Hz（Emotiv蓝牙传输）[4]到16,384 Hz（BioSemi ActiveTwo）[3]，重采样时需要谨慎的抗混叠处理。

**ADC分辨率差异**：从12位（NeuroSky）到24位（BioSemi、Brain Products、g.tec、OpenBCI的ADS1299），形成不同的噪声底和动态范围。

**参考电极方案根本不兼容**：BioSemi采用独特的CMS/DRL有源参考系统，必须进行事后重参考[3]；临床系统使用连接乳突或Cz参考；平均参考对于不完整头皮覆盖在数学上是近似的。

**AC与DC耦合**造成不可调和的频率限制——Emotiv EPOC X的AC耦合和0.2–45 Hz带宽[4]永久性地丢失了DC漂移和gamma频段活动，而DC耦合的研究级系统则保留了这些信息。

**噪声特性**相差一个数量级：BioSemi在2048 Hz采样下的输入噪声为0.8 µVRMS，共模抑制比（CMRR）>90 dB[3]；而消费级设备表现出干电极伪迹污染导致的低频功率显著升高[2]。

这些差异虽然并非微不足道，但遵循可预测的物理原理，这使得系统性校正在理论上是可行的。

---

## 二、基础模型自2023年以来彻底改变了技术格局

跨设备EEG处理领域最重大的进展，是**EEG基础模型**的出现——在异构多设备数据集上进行大规模自监督预训练的神经网络，能够学习设备不变的表征。这种方法通过在预训练阶段学会抽象掉设备特异性特征，从根本上绕过了许多传统协调难题。

**BENDR**（Kostas等，2021）[5]开创了这一方向，将wav2vec 2.0架构适配到EEG上，在Temple University Hospital语料库约1,500小时数据上进行预训练，验证了跨硬件迁移能力。但此后该领域加速发展：

**LaBraM**（蒋、赵、鲁；ICLR 2024 Spotlight，上海交通大学）[6]引入了通道-分片分词（channel-patch tokenization）——将每个EEG通道独立分割为时间片段——天然适应不同电极数量。该模型在BioSemi、BrainAmp、BCI2000、g.tec等约20个数据集上预训练约2,500小时，在异常检测、事件分类、情绪识别和步态预测等任务上取得了最优结果，参数规模从580万到3.69亿。

**BIOT**（Yang、Westover、Sun；NeurIPS 2023，UIUC/哈佛）[7]采取了不同策略：通道级分词，将所有信号重采样至200 Hz，每个通道编码为独立token并附加可学习的通道嵌入——天然支持不匹配的通道数、可变长度和跨设备的缺失值。

**CBraMod**（王、赵、罗等；ICLR 2025，浙江大学）[8]引入交叉注意力Transformer，分别建模空间和时间依赖关系，采用非对称条件位置编码，在约9,000小时数据上预训练，在10个下游BCI任务中达到最优性能。

**REVE**（El Ouahidi等；NeurIPS 2025，IMT Atlantique/蒙特利尔大学）[9]代表了**迄今最先进的跨设备方案**，引入了**4D位置编码**——将每个电极映射到其三维空间坐标加时间位置，使用傅里叶嵌入编码。这使得在不重新训练的情况下实现真正的跨配置迁移成为可能——系统通过查询标准坐标数据库即可处理任意电极排列。该模型在约25,000名被试、约60,000小时数据上预训练，平均性能超越先前模型约2.5%，线性探测（linear probing）场景下提升可达17%。

2024–2025年间还涌现了多个模型：**EEGPT**（NeurIPS 2024）[10]采用基于掩码的双重自监督学习；**Large Cognition Model（LCM）**[11]引入可学习的通道映射矩阵；**BrainOmni**[12]作为首个EEG/MEG统一基础模型；以及被描述为"设备无关且噪声鲁棒"的EEG-X等。

| 模型 | 年份/会议 | 预训练规模 | 跨设备策略 | 机构 |
|------|----------|-----------|-----------|------|
| BENDR | 2021, Frontiers | ~1,500小时 | 固定19通道输入 | 多伦多/Vector |
| BIOT | 2023, NeurIPS | 多数据集 | 通道级分词，200 Hz重采样 | UIUC/哈佛 |
| LaBraM | 2024, ICLR | ~2,500小时，~20个数据集 | 通道-分片分词 | 上海交通大学 |
| CBraMod | 2025, ICLR | ~9,000小时 | 条件位置编码 | 浙江大学 |
| REVE | 2025, NeurIPS | ~60,000小时，~25,000名被试 | 4D傅里叶位置编码 | IMT Atlantique/蒙特利尔 |

---

## 三、统计协调与域适应方法发挥互补作用

除基础模型外，另外两类方法在处理流程的不同层面解决跨设备EEG融合问题。

### 3.1 统计协调方法

统计协调方法直接校正批次效应。具有里程碑意义的**HarMNqEEG**项目（Li、Valdes-Sosa等，2022）[13]基于**12种不同EEG设备、9个国家、1,564名被试**的数据，利用交叉功率谱张量上的黎曼几何与加性混合效应模型，建立了全生命周期标准化定量EEG。这一全球脑联盟（Global Brain Consortium）主导的计划证明，协调后的黎曼z分数提高了脑发育障碍的诊断准确率，建立了迄今最全面的多设备EEG常模数据库。

Jaramillo-Jimenez等人（2024）[14]首次系统比较了ComBat变体在EEG中的应用，在5个独立数据集（n=374）的汇集静息态EEG上测试了neuroCombat、neuroHarmonize、OPNested-GMM和HarmonizR。结果表明，**HarmonizR和OPNested-GMM ComBat在有效减少传感器空间频谱特征的批次效应的同时，最好地保留了与年龄相关的生物学关联**。这项工作将ComBat——最初源自基因组学[15]，后应用于神经影像[16]——引入EEG领域，较其fMRI版本晚了大约八年。

### 3.2 域适应与迁移学习

**欧几里得对齐（Euclidean Alignment, EA）**由华中科技大学吴冬蕊团队（2020）提出[17]，至今仍是最广泛采用的实用方法——一种简单而有效的技术，通过将不同被试或设备的EEG协方差矩阵对齐到公共参考空间来实现迁移。EA是NeurIPS 2021 BEETL（脑电迁移学习基准）竞赛获胜方案的核心。**跨设备表征一致性框架（CDRC）**（Zhang等，2025）[18]直接针对跨设备EEG，采用双分支Transformer嵌入的自监督对比预训练。此外，对抗域适应（DANN）、最大均值差异（MMD）和黎曼对齐（RA）等也提供了可选工具。

### 3.3 空间协调

对于不同通道配置间的空间协调，**球面样条插值**（Perrin等，1989）[19]仍是标准方法，而较新的**RESIT**（参考电极标准化插值技术，2021）误差降低了2.39%–33.5%。一项基于CNN的方法[20]在5,144小时、1,385名被试数据上训练后，可将4或14通道上采样重建为21通道EEG，经认证神经电生理学家判断，其质量与真实记录无法区分。

---

## 四、五个关键研究空白定义了机遇空间

文献分析揭示了若干明确界定的研究空白，使跨设备EEG融合成为一个高价值研究方向：

### 4.1 缺乏"旅行被试"（traveling-subject）EEG数据集

在fMRI领域，让同一批被试在多台扫描仪上采集是量化设备效应和验证协调方法的金标准。**EEG领域尚无等价物**。创建一个50+被试、在5–8种设备类型上执行相同范式的数据集将是一项里程碑式的贡献——且在技术上完全可行。

### 4.2 EEG协调方法比fMRI滞后约八年

fMRI领域已有ComBat（2017–2018适配）[16]、旅行被试方法（2019）、完善的评估框架和SMA协调方法。EEG的首个ComBat应用出现在2024年[14]，且尚无共识性协调框架。EEG面临更严峻的组合复杂性（数十家设备厂商 vs. 三家主要MRI供应商；1–256通道 vs. 标准化体素网格），但神经影像的方法体系提供了清晰的蓝图。

### 4.3 基础模型未显式建模设备效应

当前的基础模型（LaBraM[6]、CBraMod[8]、REVE[9]）通过灵活的分词机制处理通道配置差异，但将设备身份视为隐式因素。没有模型显式建模或去除设备特异性噪声特性、放大器传递函数或电极阻抗特征。**设备条件化训练或设备对抗训练**是一个尚未探索但具有明确理论动机的扩展方向。

### 4.4 缺乏标准化的跨设备评估基准

BCI竞赛（BCI Competition IV、OpenBMI）和基准测试平台（MOABB）[21]在每个数据集中使用单一设备。虽然MOABB涵盖了使用不同硬件录制的36个数据集，但没有专门的"跨设备"评估模式来隔离设备迁移性能。建立一个类似GLUE的跨设备EEG基准将大幅加速进展。

### 4.5 消费级到研究级的桥梁缺失

已有超过916项研究使用了消费级EEG设备[22]，其中Emotiv占67.7%，NeuroSky占24.6%。然而，目前没有经过验证的方法能够将消费级（1–16通道、干电极、AC耦合）与研究级（64–256通道、湿电极、DC耦合）数据进行有效融合。这一空白阻碍了最具影响力的应用：利用海量消费级EEG数据来改进研究和临床模型。

---

## 五、中国国家脑机接口政策布局创造独特战略窗口

中国的BCI政策环境近年来大幅升温。2024年1月，七部门将脑机接口列为"未来产业"十大旗舰创新产品之一[23][24]。2024年7月，工信部宣布计划成立**脑机接口标准化技术委员会**，覆盖脑信息获取、预处理、编解码和数据通信[23]。2025年8月，六部门联合发布国家指导方针，目标是到2027年实现关键突破，到2030年建立行业标准并培育具有全球竞争力的BCI企业[24][25]。中国**首个BCI医疗器械行业标准**——《脑机接口技术医疗器械术语》——于2026年1月1日生效[26]。2025年12月还宣布了**116亿元人民币的脑科学基金**[25]。

中国研究团队在直接相关领域处于世界领先地位。**吴冬蕊**（华中科技大学）[17]率先提出欧几里得对齐方法，并在中国BCI竞赛（2019–2024）中获得9项全国冠军。**鲁柏良**（上海交通大学）[6]开发了LaBraM，这是EEG基础模型首次登上ICLR Spotlight。**高小榕**（清华大学）[27]领导跨设备SSVEP-BCI迁移学习研究。**潘纲**（浙江大学）[8]创建了CBraMod（ICLR 2025）。**Pedro Valdes-Sosa**（电子科技大学）[28]领导了跨国HarMNqEEG协调项目。

在国际层面，关键的EEG数据标准已趋成熟：**BIDS-EEG**（2019）[29]提供标准化元数据和文件组织格式，目前OpenNeuro上已有60+个EEG数据集[30]。**HED**（层级事件描述符）标准化了事件标注。**MOABB**[21]在36个数据集上对30个机器学习流水线进行基准测试。**全球脑联盟**[28]和**国际脑计划**协调多国合作。然而，尚无单一的通用标准存在，而中国积极构建国家标准体系的做法有可能在碎片化的国际格局中实现弯道超车。

---

## 六、跨设备EEG融合的可行技术路线图

对于进入该领域的电信研究机构，以下分阶段方案可最大化科学影响力与战略定位：

**第一阶段——数据基础设施与基准建设（第1–6个月）。** 采用BIDS-EEG作为标准格式。构建旅行被试EEG数据集：50+被试在5–8种设备（BioSemi、Brain Products、g.tec、Emotiv、Muse、OpenBCI）上执行相同范式（静息态、运动想象、P300、SSVEP）。实施标准化预处理流水线：统一重参考（平均参考或REST）、0.5–45 Hz带通滤波、250 Hz重采样、球面样条空间插值到标准10-20位置、基于ICA的伪迹去除。仅此数据集本身就将是一项里程碑式的贡献。

**第二阶段——协调方法开发（第4–12个月）。** 利用旅行被试数据集适配并验证ComBat变体。开发设备对抗训练方法：设计带有设备分类对抗分支的神经网络，迫使网络学习设备不变表征。构建可学习的通道映射网络，扩展LCM[11]的方案。系统量化设备效应，发表跨范式的设备-被试-会话方差分解成果。

**第三阶段——显式设备建模的基础模型（第6–18个月）。** 扩展LaBraM/REVE架构，加入设备类型嵌入层、设备对抗预训练目标和灵活的通道-分片编码。目标为10,000+小时的多设备数据。创建覆盖异常检测、MI分类、情绪识别和睡眠分期的跨设备评估基准。

**第四阶段——联邦跨设备框架（第12–24个月）。** 开发面向EEG设备异构性的联邦学习方案，设计设备特异性的局部特征提取器和共享语义表征——充分利用电信行业已有的联邦学习基础设施。实现跨医院、跨设备的隐私保护EEG模型训练。

**第五阶段——平台化部署（第18–30个月）。** 部署"BCI即服务（BCI-as-a-Service）"：研究者上传任意设备的EEG数据，即可获得协调后的数据集、跨设备模型推理和标准化质量指标。优化5G/6G网络下的边缘推理以支持实时应用。

---

## 七、结论

跨设备EEG数据融合正从理论上的不可能转变为实践中的现实，其主要驱动力来自于能从大规模异构数据集中学习设备不变表征的基础模型。该领域已到达拐点：计算工具已就绪（Transformer架构、自监督学习、灵活的位置编码），数据基础设施日趋成熟（BIDS-EEG[29]、MOABB[21]、OpenNeuro[30]），科学动机也十分明确（约9%的设备方差不可忽视[1]，而跨设备数据汇集是将EEG训练数据扩大10–100倍的唯一可行路径）。

最具即时影响力的贡献将是创建首个旅行被试多设备EEG数据集，以及建立标准化的跨设备评估基准——两者均可在6–12个月内实现，且鉴于已识别的研究空白，必将引起广泛关注。电信研究机构在这一问题上拥有独特优势：用于大规模模型训练和部署的云/边缘基础设施，用于隐私保护多医院协作的联邦学习能力，以及面向实时BCI应用的5G/6G网络。在中国脑机接口标准化技术委员会组建和116亿元脑科学新增资金的背景下，2026–2030年的窗口期代表了在跨设备EEG协调领域进行平台级布局的最佳时机。

---

## 参考文献

[1] Ratti E, Waninger S, Tenke C, et al. Systems, Subjects, Sessions: To What Extent Do These Factors Influence EEG Data? *Frontiers in Human Neuroscience*, 2017, 11: 150. https://www.frontiersin.org/articles/10.3389/fnhum.2017.00150

[2] Comparison of EEG Signal Spectral Characteristics Obtained with Consumer- and Research-Grade Devices. *Sensors*, 2024, 24(24): 8108. https://www.mdpi.com/1424-8220/24/24/8108

[3] BioSemi ActiveTwo Specifications. https://www.biosemi.com/activetwo_full_specs.htm

[4] EMOTIV EPOC X Technical Specifications. https://emotiv.gitbook.io/epoc-x-user-manual/introduction/technical-specifications

[5] Kostas D, Aroca-Ouellette S, Bhatt UP. BENDR: Using Transformers and a Contrastive Self-Supervised Learning Task to Learn From Massive Amounts of EEG Data. *Frontiers in Human Neuroscience*, 2021. https://www.semanticscholar.org/paper/BENDR-Kostas-Aroca-Ouellette/c008f0f47bde9c224d5cdbc63988033995fa87c4

[6] Jiang W, Zhao L, Lu BL. Large Brain Model for Learning Generic Representations with Tremendous EEG Data in BCI. *ICLR 2024 (Spotlight)*. https://arxiv.org/abs/2405.18765

[7] Yang C, Westover MB, Sun J. BIOT: Biosignal Transformer for Cross-data Learning in the Wild. *NeurIPS 2023*. https://neurips.cc/virtual/2023/poster/71117

[8] Wang J, Zhao L, Luo Y, et al. CBraMod: A Criss-Cross Brain Foundation Model for EEG Decoding. *ICLR 2025*. https://arxiv.org/abs/2412.07236

[9] El Ouahidi H, et al. REVE: A Foundation Model for EEG Adapting to Any Setup with Large-Scale Pretraining on 25,000 Subjects. *NeurIPS 2025*. https://www.emergentmind.com/papers/2510.21585

[10] EEGPT: Pretrained Transformer for Universal and Reliable Representation of EEG Signals. *NeurIPS 2024*. https://proceedings.neurips.cc/paper_files/paper/2024/hash/4540d267eeec4e5dbd9dae9448f0b739-Abstract-Conference.html

[11] Large Cognition Model: Towards Pretrained Electroencephalography (EEG) Foundation Model. *arXiv*, 2025. https://arxiv.org/html/2502.17464

[12] BrainOmni: A Brain Foundation Model for Unified EEG and MEG Signals. *arXiv*, 2025. https://arxiv.org/html/2505.18185v1

[13] Li M, Valdes-Sosa PA, et al. Harmonized-Multinational qEEG Norms (HarMNqEEG). *NeuroImage*, 2022. https://pubmed.ncbi.nlm.nih.gov/35398285/

[14] Jaramillo-Jimenez A, et al. ComBat Models for Harmonization of Resting-State EEG Features in Multisite Studies. *Clinical Neurophysiology*, 2024. https://pubmed.ncbi.nlm.nih.gov/39369552/

[15] Johnson WE, Li C, Rabinovic A. Adjusting Batch Effects in Microarray Expression Data Using Empirical Bayes Methods. *Biostatistics*, 2007, 8(1): 118–127.

[16] Fortin JP, et al. Harmonization of Multi-Site Diffusion Tensor Imaging Data. *NeuroImage*, 2017; Fortin JP, et al. Harmonization of Cortical Thickness Measurements across Scanners and Sites. *NeuroImage*, 2018.

[17] He H, Wu D. Transfer Learning for Brain-Computer Interfaces: A Euclidean Space Data Alignment Approach. *IEEE Transactions on Biomedical Engineering*, 2020. 另见: Revisiting Euclidean Alignment for Transfer Learning in EEG-Based Brain-Computer Interfaces. https://arxiv.org/html/2502.09203

[18] Zhang Y, et al. Self-Supervised Contrastive Pre-Training for EEG-Based Recognition via Cross Device Representation Consistency. *IEEE Transactions on Biomedical Engineering*, 2025. https://pubmed.ncbi.nlm.nih.gov/41052170/

[19] Perrin F, Pernier J, Bertrand O, et al. Spherical Splines for Scalp Potential and Current Density Mapping. *Electroencephalography and Clinical Neurophysiology*, 1989, 72(2): 184–187.

[20] Shin Y, et al. Virtual EEG-Electrodes: Convolutional Neural Networks as a Method for Upsampling or Restoring Channels. *Journal of Neuroscience Methods*, 2021. https://www.sciencedirect.com/science/article/pii/S0165027021000613

[21] Chevallier S, et al. The Largest EEG-Based BCI Reproducibility Study for Open Science: The MOABB Benchmark. *arXiv*, 2024. https://arxiv.org/abs/2404.15319

[22] Sabio J, et al. A Scoping Review on the Use of Consumer-Grade EEG Devices for Research. *PLOS ONE*, 2024. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0291186

[23] China is Racing to Set the Standards for Pioneering Brain-Machine Interface Research. *South China Morning Post*, 2024. https://www.scmp.com/news/china/politics/article/3268906

[24] China's Brain-Computer Interface Industry: Investing in the Future. *China Briefing*, 2024. https://www.china-briefing.com/news/chinas-brain-computer-interface-industry-tapping-into-the-future-of-human-machine-integration/

[25] China's Brain-Computer Interface Industry Is Racing Ahead. *TechCrunch*, 2026. https://techcrunch.com/2026/02/22/chinas-brain-computer-interface-industry-is-racing-ahead/

[26] China Issues First Industry Standard for Brain-Computer Interface Medical Devices. *TechNode*, 2025. https://technode.com/2025/09/17/china-issues-first-industry-standard-for-brain-computer-interface-medical-devices/

[27] Gao Xiaorong, Department of Biomedical Engineering, Tsinghua University. Google Scholar: https://scholar.google.com/citations?user=8HR2SA0AAAAJ

[28] Global Brain Consortium. https://globalbrainconsortium.org/

[29] Pernet CR, et al. EEG-BIDS, an Extension to the Brain Imaging Data Structure for Electroencephalography. *Scientific Data*, 2019, 6: 103. https://www.nature.com/articles/s41597-019-0104-8

[30] Markiewicz CJ, et al. The OpenNeuro Resource for Sharing of Neuroscience Data. *eLife*, 2021. https://elifesciences.org/articles/71774
