# **跨设备脑电（EEG）信号采集系统数据融合技术与数据集构建：研究进展、价值与可行性深度评估**

## **引言与跨设备数据融合的核心研究价值**

在当代认知神经科学、临床神经病理学以及脑机接口（Brain-Computer Interface, BCI）技术的演进历程中，脑电图（Electroencephalography, EEG）始终占据着核心地位。作为一种具备极高时间分辨率、无创且相对低成本的神经成像手段，EEG已被广泛应用于癫痫监测、睡眠分期、情绪识别以及运动意图解码等关键领域 1。然而，随着深度学习尤其是基于Transformer架构的注意力机制模型在自然语言处理和计算机视觉领域取得压倒性胜利，EEG信号解码的局限性日益凸显。视觉和语言模型之所以能够验证“缩放定律”（Scaling Laws），是因为其底层数据形式高度统一，且存在互联网规模的海量数据集支撑 3。反观EEG领域，传统的脑电实验往往受限于单一实验室、单一采集设备、单一实验范式以及几十名受试者的小样本规模，导致所训练的深度学习模型陷入严重的“数据集孤岛”效应，即在特定设备上训练的模型在面对全新的采集硬件或不同受试人群时，性能出现断崖式下跌 5。

因此，探究将不同型号的EEG采集设备所记录的异构脑电数据融合为一个具备统一表征结构的大规模数据集，不仅具备极高的工程应用价值，更是突破当前脑科学人工智能化瓶颈的必由之路。本阶段的研究重点聚焦于探明不同EEG设备型号之间底层物理架构、信号特性与空间布局的差异，并详细调研跨设备数据对齐与融合技术的前沿进展，以全面评估该构想的理论与实践可行性。

从研究价值的维度深入审视，跨设备EEG数据融合的意义远超简单的数据堆砌。首先，它是构建通用“脑电基础模型”（EEG Foundation Models, EEG-FMs）的先决条件。只有将来自数百个实验室、覆盖不同人群、利用从高精度科研设备到便携式消费级设备采集的数万小时数据汇聚一堂，才可能为数十亿参数的深层神经网络提供充足的预训练语料，从而使模型能够学习到具有高度泛化能力的跨设备、跨范式脑电时空特征 2。其次，在临床应用中，消除设备间的分布偏移（Data Shift）能够极大促进多中心联合诊断研究的开展。例如，在针对全球老龄化引发的神经认知障碍（NCDs）研究中，通过整合多源EEG数据并结合肠道微生物群、代谢组学等多组学（Multi-omics）特征，基于支持向量机（SVM）等算法的融合模型能够达到92.69%的极高诊断准确率 9。此外，国际学术界已经认识到这一战略价值，如全球大脑联盟（Global Brain Consortium, GBC）发起的EEG规范化倡议（EEG Norms Initiative），正致力于收集来自美洲、欧洲、亚洲使用各种不同设备记录的数千名受试者的静息态EEG数据，旨在制定国际化的M/EEG数据分析与质量控制标准 10。这种跨国界、跨设备的数据融合与标准化，为理解人类大脑在不同生命周期中的发展规律、预测神经退行性疾病提供了前所未有的宏观视角。

## **底层物理与硬件异构性挑战：科研级与消费级脑电设备型号详析**

要科学评估跨设备数据融合的可行性，必须首先解构阻碍数据融合的底层物理屏障。市面上主流的EEG采集设备在电极材质、参考机制、接地逻辑、前端放大器设计以及硬件滤波策略上存在着根本性的设计哲学差异。这些物理层面的不一致直接导致了多源数据的源分布（Source Distribution）存在严重的结构性偏差，若直接在数值层面拼接这些数据，将不可避免地向机器学习模型引入极其强烈的混淆变量（Confounders）。以下表格详细梳理并对比了当前神经科学界与工业界最具代表性的几款设备的硬件技术规格与特性。

| 设备品牌与代表型号 | 电极类型与系统架构 | 默认参考机制与接地逻辑 | 采样率能力与信号位深 | 硬件滤波策略与前端放大器特性 |
| :---- | :---- | :---- | :---- | :---- |
| **BioSemi ActiveTwo** | 有源湿电极 (Active Electrodes) | 无传统参考/接地，采用CMS/DRL主动闭环反馈系统 13 | 高达 16 kHz 14 / 24-bit 模数转换 15 | 纯直流(DC)耦合，无模拟高通；五阶CIC数字低通滤波 14 |
| **EGI Geodesic Net Amps** | 盐水海绵湿电极 (HydroCel) | 默认采用头顶Vertex (Cz)为物理参考电极 17 | 250 \- 1000 Hz 18 / 高精度光纤隔离 19 | ADAPT前端技术，具备高输入阻抗与4kV患者光纤隔离 19 |
| **Brain Products actiCHamp Plus** | 有源/无源电极可选 (actiCAP) | 每个放大器具备独立的REF与GND电极接口 21 | 最高达 100 kHz 22 / 24-bit (每通道独立ADC) | 极宽带宽设计 (DC至7500 Hz)，支持高频信号采集与超扫描独立接地 21 |
| **Emotiv EPOC X** | 半干态聚合物电极 (便携式) | 内置类似于BioSemi的CMS/DRL降噪机制 23 | 128 / 256 Hz 24 / 14-bit 分辨率 24 | 针对低频信号存在内部校准，受限于电池供电可能存在性能衰减 24 |
| **OpenBCI Cyton** | 模块化，支持干/湿电极 | 硬件高度自定义，支持单端或差分参考 | 200 \- 250 Hz (可拓展至1000Hz) 24 / 24-bit | 基于德州仪器(TI) ADS1299芯片，提供出色的开源底层数据访问与实时流 26 |
| **Muse S / Muse 2** | 导电银墨水扁平干电极 | 默认内部硬件参考 | 256 Hz 24 / 12-bit 分辨率 24 | 高度集成的ASIC滤波，通道极少(仅4导联)，针对消费者睡眠与冥想优化 26 |

通过对上述规格的深度剖析，我们可以清晰地识别出融合过程中必须跨越的技术鸿沟。首先是参考逻辑体系的绝对异构性。电生理学测量本质上记录的是两点之间的电位差，因此参考点的选择决定了整个拓扑图的形态。EGI Geodesic系统在设计上为了追求信号测量的对称性，默认将头顶的Cz电极作为硬件参考点，所有记录的电压波动均是相对于Cz的电位变化 17。这与BioSemi的逻辑大相径庭，BioSemi ActiveTwo系统彻底废弃了传统的接地和参考电极概念，转而采用一种名为共模感应（Common Mode Sense, CMS）的有源电极和驱动右腿（Driven Right Leg, DRL）的无源电极所组成的闭环反馈系统。该系统持续将受试者的平均电位（共模电压）驱动并钳制在尽可能接近模数转换器（ADC）内部参考电压的水平，从而赋予前端信号高达80 dB的共模抑制比（CMRR）。这种设计使得BioSemi在硬件层面记录的是完全独立的差分信号，用户必须在后期软件分析阶段手动选择诸如全脑平均（Common Average Reference, CAR）或双耳乳突平均作为数学参考 13。而Brain Products的actiCHamp系统则在设计上充分考量了多受试者交互（超扫描，Hyperscanning）的需求，其电极输入盒（如EIB64）允许为每个受试者分配完全独立的参考（REF）和物理接地（GND）电极，从而在源头上杜绝了两人共享接地所带来的电气串扰与基线漂移 21。这种在参考策略上的南辕北辙，要求数据融合管线必须具备统一的重参考（Re-referencing）映射算法，否则直接融合的特征空间将陷入逻辑混乱。

其次，硬件放大器的滤波逻辑与阻抗耐受度决定了信号的本底频谱特性。BioSemi的放大器是完全直流（DC）耦合的，摒弃了所有模拟高通滤波器，从而能够无失真地记录极低频率的慢波甚至直流偏移。其抗混叠滤波仅依赖于内部ADC的五阶级联积分梳状（CIC）数字低通滤波器，这确保了极佳的相位线性度与通道间的一致性 14。为了应对未处理皮肤上可能高达几千欧姆的接触阻抗，BioSemi将其前端输入阻抗在50 Hz时提升至极其惊人的300 MOhm，从而最大限度地免疫了工频干扰 29。相对而言，针对消费级和轻量化研究设计的Emotiv或Muse设备，其前端放大器的阻抗匹配往往无法达到科研级标准，且其内部的硬件高通滤波截止频率可能存在差异，这直接导致它们在处理低频频段（如Delta和Theta波）时，本底噪声显著增大 30。因此，跨设备数据融合在信号预处理阶段，除了重新采样，还必须应用统一且相位非失真的数字滤波器（如零相位FIR滤波器）对所有数据集的有效频带进行严格的重新对齐与裁剪 32。

## **跨设备信号质量、阻抗特性与应用范式验证的深度比较**

硬件规格的差异最终在采集到的信号质量上得到具象体现，这种质量差异是评估融合数据能否有效支撑下游任务分类边界的关键。科研界针对不同类型设备进行了大量严格的平行对照研究，尤其聚焦于科研级湿电极系统与消费级干电极系统在相同实验范式下的信噪比（SNR）与事件相关电位（ERP）表现。

传统观点认为，依赖导电膏的湿电极系统（如Brain Products和BioSemi）能够提供卓越的导电率和极低的接触阻抗，是保障信号保真度的唯一黄金标准 30。然而，伴随材料科学与主动放大技术的发展，干电极系统的信号质量已取得长足进步。研究表明，在低度至中等噪声的受控实验环境中，现代有源干电极（Active Dry Electrodes）系统虽然由于接触阻抗较高而表现出整体偏高的白噪声水平，但其在捕获宏观皮层反应的拓扑结构与时序特征上，已能够高度逼近湿电极系统 33。在视觉与听觉事件相关电位实验中，Emotiv EPOC等便携式设备能够可靠地诱发并记录下包括P100、N100、P200、N200和著名的P300在内的晚期认知成分 24。在一项测量失配负波（Mismatch Negativity, MMN）的研究中，统计分析显示干电极与湿电极记录的MMN峰值幅度在统计学上并不存在显著差异（p \= 0.911, d \= 0.02），充分证明了干电极在捕捉关键认知事件方面的有效性 35。

然而，当分析维度转移至频谱密度与高难度认知解码时，设备间的信号质量鸿沟依然存在。多项独立研究指出，在缺乏导电胶缓冲的物理条件下，多针脚干电极或银墨水扁平电极对微小的头部运动、面部肌肉收缩（肌电伪影 EMG）以及眼球运动（眼电伪影 EOG）表现出极端的敏感性 36。在高动态或长时间的脑机接口操作任务中，干电极信号在额叶和颞叶区域会涌现出大量的宽带伪影和高频肌肉干扰，且在Delta和Theta等低频频段的功率谱密度异常升高 30。针对这些挑战，传统的基于独立成分分析（ICA）的伪影剔除方法，如结合ARCI机制的SPHARA算法被引入，以有效提升干电极EEG的信噪比。实证数据表明，通过改进的空间谐波分析结合ICA，能够将干电极信号的信噪比从2.31 dB显著提升至5.56 dB，并将均方根偏差优化至可接受的范围，从而在信号层面上缩小了与科研级设备的质量差距 39。

在基于机器学习的任务解码性能上，设备差异同样引发了学术界的深刻反思。一项在DREAMER数据集（使用14导联的Emotiv设备采集）上的详尽评估揭示了消费级设备在情绪识别任务中的独特挑战。由于电极覆盖空间有限且信噪比低下，当直接应用旨在为高密度高信噪比数据设计的端到端深度卷积神经网络（如EEGNet）时，其F1分数仅为0.567。相反，当采用结合了统计学、频域以及连通性特征的领域特定特征工程（Domain-specific feature engineering），并配合传统机器学习分类器（如随机森林）时，其性能实现了高达67%的跃升（F1 \= 0.945），并在统计学上表现出极强的优越性（p \< 0.000001, Cohen's d \= 3.863） 40。在运动想象（Motor Imagery, MI）的跨设备基准测试中，受控环境下的湿电极系统在主体依赖的分类准确率上通常稳定在70%至96%之间，而干电极系统尽管存在约15%至22%的方差波动，其平均识别准确率依然能够突破71%的实用阈值 41。这些实证基准测试深刻地表明，消费级设备产生的数据并非“低质”到无法利用，只要预处理管线和特征提取算法能够针对低信噪比与空间稀疏性进行自适应优化，将这些海量的真实世界（Real-world）干电极数据融入至基于湿电极的高质量基准数据集中，不仅具有完全的可行性，更能为深度学习模型注入宝贵的对各类环境噪声的鲁棒性约束。

## **信号预处理与跨设备空间映射：物理对齐策略的技术实现**

认识到物理规格的差异与信号质量的分布特征后，实现跨设备数据融合的首要工程任务是在原始信号维度实施高度标准化的对齐策略。由于不同设备使用的蒙太奇（Montage）系统不尽相同，即使同样遵循国际10-20标准，电极的确切数量与三维坐标也存在差异（如64导联对比128导联）。为了满足诸如卷积神经网络（CNN）等对输入维度有严格限制的传统深度架构的要求，必须在头皮空间上执行极其精确的通道插值与重采样映射。

球面样条插值（Spherical Spline Interpolation, SSI）被公认为是目前解决跨设备空间不对齐问题的最优技术路径。其核心机制是将真实的测量头皮抽象为一个理想的三维单位球面 42。当试图将一个设备的通道配置（如拥有源电极位置![][image1]的数据集）映射到另一个设备的通道配置（如目标虚拟电极位置![][image2]的模板空间）时，SSI算法首先计算所有实际电极与目标电极投影在球面上的球面距离与交叉积。随后，通过求解基于逆距离加权的映射矩阵，算法能够在未布置真实电极的虚拟坐标点上，根据周围电极的电位梯度和局部曲率平滑地插值出合成信号 44。定量研究表明，相较于简单的最近邻插值（NNI）或仅考虑欧氏距离的平面样条插值（PSI），SSI由于充分顾及了颅骨几何形状与电场弥散特性，其生成的插值信号在地形图保真度与相位一致性上具有压倒性优势，被广泛用于解决不同数据集之间的通道数量与位置差异 46。

在解决空间对齐的同时，不同设备放大器的模数转换增益校准差异会导致记录到的微伏级（![][image3]）电压在绝对数值上存在极大的分布偏差。为了防止神经网络的梯度在训练初期被数值范围极大的个别数据集所主导，必须进行严谨的数据归一化（Normalization）。然而，大量实证研究发现，传统的基于均值和标准差的Z-score标准化在跨设备脑电融合中极其脆弱，因为EEG信号极易受到瞬态肌电爆发、电极脱落或眨眼引发的极端异常幅值（大数十倍于背景EEG）的污染 47。为了应对这一问题，鲁棒标准化技术（Robust Normalization）被引入融合管线。该技术舍弃了对异常值敏感的均值，转而使用数据集的中位数（Median）进行中心化，并利用四分位距（Interquartile Range, IQR，即第75百分位数与第25百分位数的差值）进行缩放分布尺度 47。实验证明，在一个或多个录音级别的滑动时间窗口内执行这种独立于通道或跨通道的鲁棒缩放策略，能够有效压缩由异常毛刺带来的数值失真，显著降低了跨记录（Cross-recording）和跨设备的信号变异性，使不同设备产生的波形特征在送入下游模型前收敛到相似的数值流形空间中 47。

## **元数据标准化与数据格式重构：BIDS 与 HED 生态系统的基石作用**

如果仅在数值和空间层面实现了对齐，融合后的多源数据集在语义和组织结构上依然是混乱的。不同实验室对于刺激事件（Triggers）、通道标签命名以及受试者元数据的记录习惯千差万别。例如，对于同样一个“左手运动想象”的事件，A实验室可能在记录文件中标记为“S 1”，而B实验室可能将其标记为“Marker\_Left\_Hand”。这种注释的不一致性构成了自动化跨数据集训练的致命壁垒。为了在语义和文件结构层面扫清融合障碍，神经影像界的两大国际标准化倡议——脑成像数据结构（Brain Imaging Data Structure, BIDS）以及分层事件描述符（Hierarchical Event Descriptors, HED）发挥了关键的基础设施作用。

BIDS-EEG规范制定了一套极其严格且机器可读的目录层级和文件命名准则 49。按照该规范，所有通过不同设备导出的私有数据格式（如BioSemi的.bdf，Brain Products的.vhdr/.eeg，EGI的.mff）均需转换为统一的、开放的文件结构。更重要的是，BIDS强制要求附带标准化的元数据文件，例如明确指定通道类型、采样率及参考方式的\_channels.tsv表格，以及通过3D数字化仪或标准模板映射生成的存储每个电极精确物理坐标的\_electrodes.tsv文件 51。这种结构化的元数据存储范式，使得自动化脚本在读取来自不同设备的数据时，能够准确无误地抽取必要的几何和电物理属性进行动态校正。

与之配套的HED标签架构，则解决了一直以来困扰多中心实验的事件语义隔离问题。HED提供了一套高度结构化的机器可读词汇库，能够精确描述实验设计中发生了什么 52。研究人员不仅可以标记单一的触发器，还能组合层级词汇，例如使用 Action/Imagine/Upper-extremity/Hand, Direction/Left 来统一且无歧义地注释来自任何实验室的左手运动想象事件。通过为BIDS数据集的\_events.tsv文件引入详尽的HED映射字典，跨国界、跨设备的异构事件被全部归一化到一个共同的概念空间内，极大地赋予了数据集之间相互印证与交叉验证的潜力 49。

在软件工程层面，这一规范已经通过诸如MNE-BIDS-Pipeline等开源自动化预处理工具链得到了完美落地 53。该管线深度集成于Python的MNE库中，通过一个简单的文本配置文件，就能针对多达数百名被试、混杂多种设备格式的庞大BIDS数据集，执行从数据读取、滤波重采样、球面空间重映射、独立成分分析（ICA）伪影剔除直到特征矩阵提取的全流程并行化批处理计算 54。这种自动化、可复现、强鲁棒的数据流水线的成熟，标志着在数据工程层面上，将不同设备采集的海量脑电信号汇聚并整编为一个标准可用数据集的可行性已经得到了坚实的工具支持。

## **模型特征级融合：域适应与黎曼流形几何对齐的高阶策略**

即便在预处理阶段穷尽了插值、重构与标准化策略，不同设备的硬件频响特性残留、局部电极空间微小错位以及不可观测的环境电气噪声，依然会使得提取到的高级特征产生不可忽视的分布偏移。这违反了传统机器学习中训练集与测试集必须满足独立同分布（i.i.d.）的假设。为跨越这一鸿沟，学术界广泛引入了迁移学习（Transfer Learning）与域适应（Domain Adaptation, DA）算法，旨在特征空间或模型权重层面实现对设备差异的“免疫” 57。

在以空间协方差特征为主的分类任务（如运动想象和BCI范式）中，基于黎曼流形（Riemannian Manifold）的几何对齐技术被证明是抑制跨设备和跨被试数据漂移最为有效的高阶算法之一 58。EEG信号在多个频带上的空间协方差矩阵（Covariance Matrices）被证实并不处于平坦的欧几里得空间内，而是驻留在一个高度弯曲的对称正定（Symmetric Positive Definite, SPD）矩阵黎曼流形上。传统基于欧氏距离的对齐算法在处理这类数据时往往会产生严重的几何畸变 59。

为解决这一问题，前沿的黎曼对齐策略设计了三个依次递进的数学变换步骤。第一步是重新居中（Re-centering），该操作在黎曼流形上计算各个设备或受试者数据分布的黎曼质心（Fréchet Mean），随后通过仿射变换将所有源数据集与目标数据集的质心平移至流形上的一个共同参考点。第二步是离散度均衡（Equalizing Dispersion），由于不同放大器的噪声本底差异，各个数据集在质心周围的散布半径不一。该步骤旨在缩放流形上协方差分布的离散程度，强迫所有分布具有相似的方差体积。第三步则是旋转校正（Rotation Correction），借助在正切空间（Tangent Space）中展开的矩阵投影，算法应用诸如相关对齐（CORAL）或普氏分析（Procrustes Analysis）等手段，修正源域特征轴与目标域特征轴之间的旋转错位，从而使异构分布在统计学方向上完美契合 5。在此理论指导下构建的端到端深度网络，如BARN-DA模型，通过最小化源域和目标域SPD矩阵在再生核希尔伯特空间（RKHS）内的黎曼最大均值差异（R-MMD）损失，迫使网络学习到了超越局部硬件限制的普适生理表征，从而在跨会话与跨主体分类精度上取得了突破性进展 6。

在处理更为复杂的非线性任务（如情绪识别与认知负荷监测）时，领域对抗神经网络（Domain-Adversarial Neural Networks, DANN）及其衍生变体（如Emo-DA模块）展示了其卓越的迁移威力 61。这类深层域适应架构通常由一个特征提取器、一个任务分类器（预测认知状态）以及一个域分类器（预测数据来源于哪种设备或哪个被试）共同组成。在反向传播训练中，通过引入梯度反转层（Gradient Reversal Layer），模型会在优化任务识别精度的同时，故意欺骗并最大化域分类器的误差。这种对抗性博弈迫使深层特征提取网络不断调整权重，直至其输出的潜在空间特征让分类器根本无法区分这是来自高精度的BioSemi系统还是含有较多噪声的Emotiv设备 62。在一项高难度的跨数据集（从科研级DREAMER迁移至SEED-VII）情绪识别实证研究中，通过联合通道拓扑映射、CORAL域适应以及TCA子空间学习的渐进式对齐技术，不仅证实了特征迁移的切实可行性，还在不利用目标域任何标签的少样本场景下，取得了极具竞争力的F1评分 40。这充分说明，在特征与模型层面进行跨设备的鲁棒迁移是具备充分算法支撑的。

## **脑电基础模型（EEG-FMs）的崛起与多设备输入自适应范式**

如果说域适应技术是在算法的后端和特征空间里被动地“修补”不同设备间的鸿沟，那么近年来引领神经计算浪潮的大规模脑电基础模型（EEG Foundation Models, EEG-FMs）则试图在架构设计的最初始阶段，从根本上解决跨设备数据集融合的底层阻碍 2。此类模型通过革新传统的序列建模假设，赋予了网络直接吞吐任意电极数量、任意采样配置且含有严重缺失值的异构EEG数据的能力 7。

传统的卷积神经网络（如广泛使用的EEGNet或Shallow ConvNet）有一个致命的前提假设：输入的EEG信号必须是被严格裁剪的固定二维张量（即固定的通道数乘以固定的时间步长）。这一约束条件使得它们在面对融合了从4通道到256通道不等的大规模多设备数据集时毫无用武之地 8。为了打破这一僵局，新一代的基础模型在自然语言处理中大获成功的Transformer架构之上，引入了极其精妙的跨尺度标记化（Tokenization）与物理嵌入（Embedding）机制。

以近期备受瞩目的BIOT（Biosignal Transformer）模型为例，它创造性地引入了一种将变长、变通道的生物信号翻译为高度统一的“句子”表征的技术范式 3。BIOT并不将所有电极作为一个庞大的矩阵输入，而是独立地将每个通道的连续时间序列切分成固定时间窗口的非重叠片段（Tokens）。随后，模型为这些零散的片段同时注入时序位置编码与通道特定标识符。通过这种设计，如果一个由Muse采集的数据集仅有4个通道，而另一个由EGI采集的数据集包含128个通道，BIOT底层庞大的自注意力网络机制（Self-Attention）依然能够动态地处理这些长短不一的“Token序列”，而无需进行强行的零填充或截断 68。

同样，为了在模型前端植入物理拓扑学的归纳偏置（Inductive Bias），诸如EEG-X与EEGPT等基础模型引入了基于大脑三维解剖位置的通道嵌入（Location-based Channel Embedding）机制 69。它们将所有可能出现的电极（无论属于10-20还是10-5系统）统一映射到一个涵盖全脑的隐式网格坐标系中。在输入阶段，任何型号设备的电极都只需寻找其在该网格中的最近几何坐标，并将该位置编码赋给对应的信号片段。更为精妙的是，另一款名为CSBrain的大型模型则采用了跨尺度时空分词（Cross-scale Spatiotemporal Tokenization, CST）与结构化稀疏注意力（SSA）架构。它依据大脑的解剖学分区（如额叶、顶叶、枕叶）对通道信号进行动态聚合，从而使得模型能够极其灵活地应对不同数据集中不断变化的电极组合和空间分辨率 71。在预训练阶段，这些基础模型往往摒弃了对昂贵标注数据的依赖，转而使用海量未标注的多设备EEG数据，通过掩码自编码器（Masked Autoencoding, MAE）机制，让模型在重构被随机遮挡的信号片段的过程中，隐式地学习到蕴藏在不同设备噪声本底之下的人类大脑普遍运行规律与动态网络连通性特征 69。

### **缩放定律的偏离与脑电评估基准的反思**

虽然脑电基础模型为跨设备融合提供了最优雅的架构解决方案，但伴随大规模融合数据集进行预训练的尝试，研究界也发现了这一领域异于文本和视觉任务的独特演化规律。为了系统评估EEG基础模型的真实效能，多项涵盖从十几到数十个庞大数据集的综合测评基准（如EEG-FM-Bench）被相继提出 72。

通过在大量不同范式（包括认知负荷、事件相关电位、情绪检测及癫痫筛查等）的严格测试中，研究者揭示了一个颇具警示意义的结论：在当前的EEG数据规模和预训练目标下，简单的增加模型参数量和预训练数据量，并不必然如同自然语言处理那般带来下游任务泛化性能的线性飞跃，即所谓的“缩放定律”在极低信噪比的EEG任务中发生了偏离 8。深入分析指出，由于脑电信号的高度非平稳性与严重的环境噪声浸染，预训练阶段用于恢复信号重构目标的损失梯度往往与下游精准分类任务所需的判别性特征梯度产生剧烈冲突（Gradient Conflicts） 72。基准测试表明，通过冻结预训练主干网络并仅仅训练最后一层分类器的线性探测（Linear Probing）方法，在跨设备验证中表现极其孱弱。为了使预训练提取的泛化表征能够在不同设备上真正发挥迁移优势，必须对模型进行深度的全参数微调（Full-parameter fine-tuning） 8。

这意味着，跨设备数据的物理融合与架构适应仅仅是迈出了第一步。未来，若要通过融合数百个型号设备产生的数据集来训练出真正无处不在、免校准且具有极强鲁棒推断能力的通用脑机接口底座模型，除了在数据广度上发力，还必须在神经生理学的底层规律上寻求突破。探索更贴合大脑电生理偶极子动力学的自监督对比学习（Contrastive Learning）目标，以及更智能的跨模态（将EEG与文本、音频结合）对齐机制，是提升下一代模型跨设备、跨被试知识迁移效率的关键命题 2。

## **结论与发展可行性总结**

综上所述，关于将不同脑电采集设备的数据融合为一个大规模数据集的构想，本报告在深入剖析硬件物理特性、信号质量对齐、元数据标准化以及前沿算法架构后得出结论：该设想不仅具备极其宏伟的科研与临床应用价值，而且在当前的技术生态下具备极高的工程实现可行性。

从底层硬件视角来看，尽管以BioSemi、EGI为代表的高精度科研设备与以Emotiv为代表的便携消费级设备在电极材质、接地闭环反馈机制以及前端硬件滤波逻辑上存在结构性差异，但科学界已经验证了只要实施针对性的降噪算法，便携式设备依然能够捕捉到足以支撑认知识别的核心时空生理特征。在数据处理层面，依托于球面样条插值（SSI）构建的统一头皮几何映射，结合中位数四分位距驱动的鲁棒归一化策略，有效地在信号层面抚平了设备间的硬性偏差。而在数据工程层面，BIDS规范与HED语义标签及MNE自动化流水线的普及，彻底清除了不同实验室私有格式相互割裂的障碍，为数据融合构建了现代化的信息高速公路。

在更为高阶的模型与算法维度，我们看到黎曼流形对齐、协方差分布离散度均衡以及对抗性域适应技术，为跨越不可消除的设备残余分布漂移提供了坚实的数学理论武器。最令人振奋的是，基于Transformer架构引入的通道位置嵌入与跨尺度时空分词技术的脑电基础模型（EEG-FMs），从根本架构上破除了卷积网络对固定输入维度的依赖，使得网络具备了海纳百川、直接吸收任意电极布局和采样率异构数据的能力。

尽管当前对脑电融合数据的规模化训练尚在探索其独特的“缩放定律”，且不可避免地遭遇低信噪比带来的特征冲突挑战，但这进一步凸显了构建高标准、大体量融合数据集的紧迫性与战略意义。随着跨国学术倡议的推进与软硬件解耦技术的成熟，跨设备脑电数据的融合必将重塑脑科学数据的基础设施形态。这不仅将极大加速免校准、高鲁棒脑机接口的工业化落地，也将为揭开人类大脑皮层动态网络机制的全景奥秘提供最强大的算料引擎支撑。

#### **Works cited**

1. A Systematic Review of Machine Learning Methods for Multimodal EEG Data in Clinical Application \- arXiv, accessed April 3, 2026, [https://arxiv.org/pdf/2501.08585](https://arxiv.org/pdf/2501.08585)  
2. Foundation Models for Cross-Domain EEG Analysis ... \- arXiv, accessed April 3, 2026, [https://arxiv.org/abs/2508.15716](https://arxiv.org/abs/2508.15716)  
3. EEG Foundation Models: A Critical Review of Current Progress and Future Directions \- arXiv, accessed April 3, 2026, [https://arxiv.org/html/2507.11783v2](https://arxiv.org/html/2507.11783v2)  
4. EEG Foundation Models: A Critical Review of Current Progress and Future Directions \- arXiv, accessed April 3, 2026, [https://arxiv.org/html/2507.11783v3](https://arxiv.org/html/2507.11783v3)  
5. Cross-Subject Motor Imagery Electroencephalogram Decoding with Domain Generalization, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12108780/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12108780/)  
6. A Band-Aware Riemannian Network with Domain Adaptation for Motor Imagery EEG Signal Decoding \- MDPI, accessed April 3, 2026, [https://www.mdpi.com/2076-3425/16/4/363](https://www.mdpi.com/2076-3425/16/4/363)  
7. Foundation Models for Cross-Domain EEG Analysis Application: A Survey \- arXiv, accessed April 3, 2026, [https://arxiv.org/html/2508.15716v2](https://arxiv.org/html/2508.15716v2)  
8. Are EEG Foundation Models Worth It? Comparative Evaluation with Traditional Decoders in Diverse BCI Tasks | OpenReview, accessed April 3, 2026, [https://openreview.net/forum?id=5Xwm8e6vbh](https://openreview.net/forum?id=5Xwm8e6vbh)  
9. The fusion of multi-omics profile and multimodal EEG data contributes to the personalized diagnostic strategy for neurocognitive disorders \- PMC, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10797890/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10797890/)  
10. Projects \- Global Brain Consortium, accessed April 3, 2026, [https://globalbrainconsortium.org/projects/](https://globalbrainconsortium.org/projects/)  
11. Global EEG Norms \- Global Brain Consortium, accessed April 3, 2026, [https://globalbrainconsortium.org/project-eegNorms/](https://globalbrainconsortium.org/project-eegNorms/)  
12. Global Brain Consortium's EEG Normative Initiative for Creating Standards for MEEG Analysis | INCF TrainingSpace, accessed April 3, 2026, [https://training.incf.org/lesson/global-brain-consortiums-eeg-normative-initiative-creating-standards-meeg-analysis](https://training.incf.org/lesson/global-brain-consortiums-eeg-normative-initiative-creating-standards-meeg-analysis)  
13. BioSemi EEG ECG EMG BSPM NEURO amplifiers systems, accessed April 3, 2026, [https://www.biosemi.com/faq/cms\&drl.htm](https://www.biosemi.com/faq/cms&drl.htm)  
14. Can we adjust the filter settings on a BioSemi system, accessed April 3, 2026, [https://www.biosemi.com/faq/adjust\_filter\_activeone.htm](https://www.biosemi.com/faq/adjust_filter_activeone.htm)  
15. Biosemi EEG ECG EMG BSPM NEURO amplifier electrodes, accessed April 3, 2026, [https://www.biosemi.com/Products\_ActiveTwo.htm](https://www.biosemi.com/Products_ActiveTwo.htm)  
16. Can we adjust the filter settings on a BioSemi system, accessed April 3, 2026, [https://www.biosemi.com/faq/adjust\_filter.htm](https://www.biosemi.com/faq/adjust_filter.htm)  
17. Geodesic Sensor Net, accessed April 3, 2026, [https://med.stanford.edu/content/dam/sm/lucasmri/documents/16\_0824\_EGI\_geodesic\_sensor\_net.pdf](https://med.stanford.edu/content/dam/sm/lucasmri/documents/16_0824_EGI_geodesic_sensor_net.pdf)  
18. User manual \- Philips, accessed April 3, 2026, [https://www.documents.philips.com/assets/20180705/845a17d2eabc4f6fbe07a914017ed58d.pdf](https://www.documents.philips.com/assets/20180705/845a17d2eabc4f6fbe07a914017ed58d.pdf)  
19. GES 400 Series \- Philips, accessed April 3, 2026, [https://www.documents.philips.com/assets/20180705/a2e417ddc1bd43b1b329a91401588dc6.pdf](https://www.documents.philips.com/assets/20180705/a2e417ddc1bd43b1b329a91401588dc6.pdf)  
20. Net Amps amplifiers \- Electrical Geodesics, Inc., accessed April 3, 2026, [https://www.egi.com/research-division/net-amps-eeg-amplifier](https://www.egi.com/research-division/net-amps-eeg-amplifier)  
21. Implementing EEG hyperscanning setups \- PMC, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6411510/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6411510/)  
22. actiCHamp series | Brain Products GmbH \> Solutions, accessed April 3, 2026, [https://www.brainproducts.com/solutions/actichamp/](https://www.brainproducts.com/solutions/actichamp/)  
23. Comparing ERPs across OpenBCI, Biosemi, Emotiv, accessed April 3, 2026, [https://openbci.com/forum/index.php?p=/discussion/1574/comparing-erps-across-openbci-biosemi-emotiv](https://openbci.com/forum/index.php?p=/discussion/1574/comparing-erps-across-openbci-biosemi-emotiv)  
24. A scoping review on the use of consumer-grade EEG devices for research \- PMC, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10917334/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10917334/)  
25. A scoping review on the use of consumer-grade EEG devices for research \- bioRxiv, accessed April 3, 2026, [https://www.biorxiv.org/content/10.1101/2022.12.04.519056v1.full.pdf](https://www.biorxiv.org/content/10.1101/2022.12.04.519056v1.full.pdf)  
26. EEG Devices You Can Actually Use: Muse vs OpenBCI vs Emotiv for AI Projects \- Sharika Zareen, accessed April 3, 2026, [https://sharikazareen.medium.com/eeg-devices-you-can-actually-use-muse-vs-openbci-vs-emotiv-for-ai-projects-c81edb32aa72](https://sharikazareen.medium.com/eeg-devices-you-can-actually-use-muse-vs-openbci-vs-emotiv-for-ai-projects-c81edb32aa72)  
27. Consumer BCI Review: 5 EEG Headsets for Developers \- NeurotechJP, accessed April 3, 2026, [https://neurotechjp.com/blog/5-bci-gadget-reviews/](https://neurotechjp.com/blog/5-bci-gadget-reviews/)  
28. Top 5 EEG Devices of 2025 \- AJProTech, accessed April 3, 2026, [https://ajprotech.com/blog/articles/top-10-eeg-devices-of-2025.html](https://ajprotech.com/blog/articles/top-10-eeg-devices-of-2025.html)  
29. BioSemiEEG ECG EMG BSPM NEURO amplifiers systems, accessed April 3, 2026, [https://www.biosemi.com/faq/compare\_specifications.htm](https://www.biosemi.com/faq/compare_specifications.htm)  
30. Comparison of EEG Signal Spectral Characteristics Obtained with Consumer- and Research-Grade Devices \- PMC, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11679099/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11679099/)  
31. Comparison between a wireless dry electrode EEG system with a conventional wired wet electrode EEG system for clinical applications \- PMC, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC7090045/](https://pmc.ncbi.nlm.nih.gov/articles/PMC7090045/)  
32. A lightweight, physics-based, sensor-fusion filter for real-time EEG denoising and improved downstream AI classification \- bioRxiv.org, accessed April 3, 2026, [https://www.biorxiv.org/content/10.1101/2025.09.24.675953v2.full.pdf](https://www.biorxiv.org/content/10.1101/2025.09.24.675953v2.full.pdf)  
33. accessed April 3, 2026, [https://sapienlabs.org/eeg-signal-quality-in-wet-versus-dry-electrodes/\#:\~:text=Overall%20the%20results%20from%20this,signature%20in%20the%20oddball%20task.](https://sapienlabs.org/eeg-signal-quality-in-wet-versus-dry-electrodes/#:~:text=Overall%20the%20results%20from%20this,signature%20in%20the%20oddball%20task.)  
34. EEG Signal Quality in Wet Versus Dry Electrodes \- Sapien Labs | Shaping the Future of Mind Health, accessed April 3, 2026, [https://sapienlabs.org/eeg-signal-quality-in-wet-versus-dry-electrodes/](https://sapienlabs.org/eeg-signal-quality-in-wet-versus-dry-electrodes/)  
35. Comparison of dry and wet electroencephalography for the assessment of cognitive evoked potentials and sensor-level connectivity \- PMC, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11576458/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11576458/)  
36. EEG Artifacts: Types, Detection, and Removal Techniques Bitbrain, accessed April 3, 2026, [https://www.bitbrain.com/blog/eeg-artifacts](https://www.bitbrain.com/blog/eeg-artifacts)  
37. (PDF) Research on Signal-to-Noise Ratio Comparison and Optimization of EEG Signals in Brain-Computer Interface Systems \- ResearchGate, accessed April 3, 2026, [https://www.researchgate.net/publication/399065399\_Research\_on\_Signal-to-Noise\_Ratio\_Comparison\_and\_Optimization\_of\_EEG\_Signals\_in\_Brain-Computer\_Interface\_Systems](https://www.researchgate.net/publication/399065399_Research_on_Signal-to-Noise_Ratio_Comparison_and_Optimization_of_EEG_Signals_in_Brain-Computer_Interface_Systems)  
38. An out-of-the-lab evaluation of dry EEG technology on a large-scale motor imagery brain-computer interface dataset \- ResearchGate, accessed April 3, 2026, [https://www.researchgate.net/publication/398802471\_An\_out-of-the-lab\_evaluation\_of\_dry\_EEG\_technology\_on\_a\_large-scale\_motor\_imagery\_brain-computer\_interface\_dataset](https://www.researchgate.net/publication/398802471_An_out-of-the-lab_evaluation_of_dry_EEG_technology_on_a_large-scale_motor_imagery_brain-computer_interface_dataset)  
39. Combination of spatial and temporal de-noising and artifact reduction techniques in multi-channel dry EEG \- PMC, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12247144/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12247144/)  
40. Traditional Machine Learning Outperforms EEGNet for Consumer-Grade EEG Emotion Recognition: A Comprehensive Evaluation with Cross-Dataset Validation \- PMC, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12693886/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12693886/)  
41. Recent Advances in Portable Dry Electrode EEG: Architecture and Applications in Brain-Computer Interfaces \- MDPI, accessed April 3, 2026, [https://www.mdpi.com/1424-8220/25/16/5215](https://www.mdpi.com/1424-8220/25/16/5215)  
42. Repairing bad channels — MNE 0.14.1 documentation, accessed April 3, 2026, [https://www.nmr.mgh.harvard.edu/mne/0.14/manual/channel\_interpolation.html](https://www.nmr.mgh.harvard.edu/mne/0.14/manual/channel_interpolation.html)  
43. Spherical spline interpolation to use subject data on template head model \- MNE Forum, accessed April 3, 2026, [https://mne.discourse.group/t/spherical-spline-interpolation-to-use-subject-data-on-template-head-model/7566](https://mne.discourse.group/t/spherical-spline-interpolation-to-use-subject-data-on-template-head-model/7566)  
44. (PDF) Channel interpolation in TMS-EEG: A quantitative study towards an accurate topographical representation \- ResearchGate, accessed April 3, 2026, [https://www.researchgate.net/publication/309324491\_Channel\_interpolation\_in\_TMS-EEG\_A\_quantitative\_study\_towards\_an\_accurate\_topographical\_representation](https://www.researchgate.net/publication/309324491_Channel_interpolation_in_TMS-EEG_A_quantitative_study_towards_an_accurate_topographical_representation)  
45. Interpolate bad channels for MEG/EEG channels — MNE 1.1.1 documentation, accessed April 3, 2026, [https://mne.tools/1.1/auto\_examples/preprocessing/interpolate\_bad\_channels.html](https://mne.tools/1.1/auto_examples/preprocessing/interpolate_bad_channels.html)  
46. Assigning channel weights using an attention mechanism: an EEG interpolation algorithm, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10552919/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10552919/)  
47. Data Normalization Strategies for EEG Deep Learning \- arXiv, accessed April 3, 2026, [https://arxiv.org/pdf/2506.22455](https://arxiv.org/pdf/2506.22455)  
48. How Sensitive are EEG Results to Preprocessing Methods: A Benchmarking Study | bioRxiv, accessed April 3, 2026, [https://www.biorxiv.org/content/10.1101/2020.01.20.913327v1.full-text](https://www.biorxiv.org/content/10.1101/2020.01.20.913327v1.full-text)  
49. (PDF) EEG-BIDS, an extension to the brain imaging data structure for electroencephalography \- ResearchGate, accessed April 3, 2026, [https://www.researchgate.net/publication/334012709\_EEG-BIDS\_an\_extension\_to\_the\_brain\_imaging\_data\_structure\_for\_electroencephalography](https://www.researchgate.net/publication/334012709_EEG-BIDS_an_extension_to_the_brain_imaging_data_structure_for_electroencephalography)  
50. Capturing the nature of events and event context using hierarchical event descriptors (HED) \- PMC, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC8925904/](https://pmc.ncbi.nlm.nih.gov/articles/PMC8925904/)  
51. BIDS organization for multimodal data acquired simultaneously \- Neurostars, accessed April 3, 2026, [https://neurostars.org/t/bids-organization-for-multimodal-data-acquired-simultaneously/24206](https://neurostars.org/t/bids-organization-for-multimodal-data-acquired-simultaneously/24206)  
52. HED resources \- Hierarchical Event Descriptor (HED), accessed April 3, 2026, [https://www.hedtags.org/hed-resources/](https://www.hedtags.org/hed-resources/)  
53. MNE-BIDS-Pipeline, accessed April 3, 2026, [https://mne.tools/mne-bids-pipeline/](https://mne.tools/mne-bids-pipeline/)  
54. PyLossless: A non-destructive EEG processing pipeline | bioRxiv, accessed April 3, 2026, [https://www.biorxiv.org/content/10.1101/2024.01.12.575323v1.full-text](https://www.biorxiv.org/content/10.1101/2024.01.12.575323v1.full-text)  
55. mne-tools/mne-bids-pipeline: Automatically process entire electrophysiological datasets using MNE-Python. \- GitHub, accessed April 3, 2026, [https://github.com/mne-tools/mne-bids-pipeline](https://github.com/mne-tools/mne-bids-pipeline)  
56. Harmonizing and aligning M/EEG datasets with covariance-based techniques to enhance predictive regression modeling \- PMC, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12007539/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12007539/)  
57. A Review on Signal Processing Approaches to Reduce Calibration Time in EEG-Based Brain–Computer Interface \- PMC, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC8417074/](https://pmc.ncbi.nlm.nih.gov/articles/PMC8417074/)  
58. Label-Based Alignment Multi-Source Domain Adaptation for Cross-Subject EEG Fatigue Mental State Evaluation \- Frontiers, accessed April 3, 2026, [https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2021.706270/full](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2021.706270/full)  
59. Riemannian Geometry-Based EEG Approaches: A Literature Review \- arXiv, accessed April 3, 2026, [https://arxiv.org/html/2407.20250v1](https://arxiv.org/html/2407.20250v1)  
60. A dual alignment-based multi-source domain adaptation framework for motor imagery EEG classification \- PMC, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC9402410/](https://pmc.ncbi.nlm.nih.gov/articles/PMC9402410/)  
61. Domain adaptation spatial feature perception neural network for cross-subject EEG emotion recognition \- Frontiers, accessed April 3, 2026, [https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2024.1471634/full](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2024.1471634/full)  
62. Hybrid transfer learning strategy for cross-subject EEG emotion recognition \- PMC \- NIH, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10687359/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10687359/)  
63. Toward cross-subject and cross-session generalization in EEG-based emotion recognition: Systematic review, taxonomy, and methods This work has been published on Neurocomputing journal. Please refer to the final version of the paper on \\urlhttps://doi.org/10.1016/j.neucom.2024.128354. Old title "Machine Learning Strategies \- arXiv, accessed April 3, 2026, [https://arxiv.org/html/2212.08744v3](https://arxiv.org/html/2212.08744v3)  
64. Domain Adaptation Techniques for EEG-Based Emotion Recognition: A Comparative Study on Two Public Datasets \- IEEE Xplore, accessed April 3, 2026, [https://ieeexplore.ieee.org/document/8337789/](https://ieeexplore.ieee.org/document/8337789/)  
65. Multi-source deep domain adaptation ensemble framework for cross-dataset motor imagery EEG transfer learning \- PubMed, accessed April 3, 2026, [https://pubmed.ncbi.nlm.nih.gov/38772402/](https://pubmed.ncbi.nlm.nih.gov/38772402/)  
66. A Simple Review of EEG Foundation Models: Datasets, Advancements and Future Perspectives \- arXiv, accessed April 3, 2026, [https://arxiv.org/html/2504.20069v1](https://arxiv.org/html/2504.20069v1)  
67. ycq091044/BIOT: BIOT \- A framework for pretraining biosignals at scale. Large EEG pre-trained models. \- GitHub, accessed April 3, 2026, [https://github.com/ycq091044/BIOT](https://github.com/ycq091044/BIOT)  
68. BIOT: Biosignal Transformer for Cross-data Learning in the Wild, accessed April 3, 2026, [https://papers.neurips.cc/paper\_files/paper/2023/file/f6b30f3e2dd9cb53bbf2024402d02295-Paper-Conference.pdf](https://papers.neurips.cc/paper_files/paper/2023/file/f6b30f3e2dd9cb53bbf2024402d02295-Paper-Conference.pdf)  
69. EEG-X: Device-Agnostic and Noise-Robust Foundation Model for EEG | OpenReview, accessed April 3, 2026, [https://openreview.net/forum?id=pJlXo9TlW1](https://openreview.net/forum?id=pJlXo9TlW1)  
70. Large Cognition Model: Towards Pretrained Electroencephalography (EEG) Foundation Model \- arXiv, accessed April 3, 2026, [https://arxiv.org/html/2502.17464v1](https://arxiv.org/html/2502.17464v1)  
71. CSBrain: A Cross-scale Spatiotemporal Brain Foundation Model for ..., accessed April 3, 2026, [https://openreview.net/forum?id=agcXjEHmyW](https://openreview.net/forum?id=agcXjEHmyW)  
72. EEG-FM-Bench: A Comprehensive Benchmark for the Systematic Evaluation and Diagnostic Analyses of EEG Foundation Models \- arXiv, accessed April 3, 2026, [https://arxiv.org/html/2508.17742v2](https://arxiv.org/html/2508.17742v2)  
73. Dingkun0817/EEG-FM-Benchmark: Fair and comprehensive benchmarking for open source EEG foundation models. \- GitHub, accessed April 3, 2026, [https://github.com/Dingkun0817/EEG-FM-Benchmark](https://github.com/Dingkun0817/EEG-FM-Benchmark)  
74. Cross-modality fusion with EEG and text for enhanced emotion detection in English writing, accessed April 3, 2026, [https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2024.1529880/full](https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2024.1529880/full)  
75. Neural networks and foundation models: two strategies for EEG-to-fMRI prediction \- PMC, accessed April 3, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12753390/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12753390/)  
76. Neural Networks and Foundation Models: Two Strategies for EEG-to-fMRI Prediction, accessed April 3, 2026, [https://www.biorxiv.org/content/10.1101/2025.05.06.652346v1.full](https://www.biorxiv.org/content/10.1101/2025.05.06.652346v1.full)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAYCAYAAAD3Va0xAAAA5ElEQVR4Xu2ToQoCQRCGf5ugxWS3CYJZ0GY2C76CD2HxBYwi+BLar5vFZNUgKAgGizpzs+vuzq2H9eA++OF2/mFmGOaAkuKzIr2VKkEGcPQ81iO0QxLSCZI4Da2UPumpgzEupB4k+aU8Zg1plkuNtDDfY8hUHWen3EkjFcvQIk3MdxNSaPZ1hTMkL5c5qeG97a4s7HFOLtyFu/nwrrjQwLx52r+m2ekgpNANsqu98qIkcIv2OcDt6hpacbhrVwchk9gD3CovQx1y2b/ge+JCQ21Y+BdYwnXckNpBhmBvqqqNkqLyATshM0FECYPbAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAZCAYAAADe1WXtAAABL0lEQVR4Xu2SMUsDQRCFn6ASIWJjI/EPWFukCVZaaqGllTZJn0Kwtw+BWIj+Axv7EAJWYu0PUATBxsrSJO9lbr3dzXn7A7wPHne3b2ZvZneAigrHKjWNVEYPYWw3tEMeqQnSm77BYj5jo4gv6hWWsBx5jg51Bou5iLwFlqh7aghL2ArtOQNYq8/UO7Ud2ovsUi3qErbpfmhjgzrI3uUrLskp1aDasKTj0J5X6I6k6KeFqCWhir+pW89bgZ2l2IFtWsvtv/nInpvUC2wSHCPvvY/0dPyiCxJ1agybAqEL1FyKddjPXAGlqKUj7/sKNq9r1IO3rhhVKT+JWlKFjkNY8hPV9NbH2bqKKOWE+onWNH9KjudQa8nzvEYeqDbdJroste84p+6Qx95Qe55f8e+ZAUdpQ7lf2E8cAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAZCAYAAADAHFVeAAABbklEQVR4Xu2UvS9EURDFj6BQiRAVIVSiUIiODh2tyKo0FDQaEVH6LxS0otVvtBKdqCSvE4VGQiTiY07mTfbu2beLTVZC9pec4p2ZeXPfvXMf0KbNX2bd9CE6r8oAtpMYdVcd/hmdqLxoRGLBATy+poFmiGZDGsh5NG2q2SwP8GbzGoA3mVNTWTXtqWn0q2GU4c12xe8y3YhXCIvfxJs0vYtHzuD5R+IvmFbEq6EPXlxOPK6SL71MvIBfpPnkXp4LKcGLlxNv1vRq2ki8gGfFL+bZkW7TKYq3vAZuB+/DWOLF6mcSL5g2PZme82du3Usl3BiO6qF4GbwZt1MZMF3D4x2mW9NomtAIFnG16nEbSZb4wQk858LUI7G6TMGLeEYBr0AMQK9pK4kFO/CcoutSlxiOY/gKechZ7l3Bz2M4z01Zgud8aygCjnbZNGhaRKWY/8Bx+JcVwbx9Nb9CR76lsFk68i1jAt7s1+Dt/198ArdTUK7IuGJ+AAAAAElFTkSuQmCC>