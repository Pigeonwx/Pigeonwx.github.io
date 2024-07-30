

### RESNET-18

#### ResNet-18 的结构

ResNet-18 包含 18 层，具体包括：

1. **卷积层和池化层（Conv1）**
   - 1 层（7x7 卷积，stride=2）+ 1 层（3x3 最大池化，stride=2）
2. **残差块（Residual Blocks）**
   - **Conv2_x**: 2 个残差块，每个残差块包含 2 个 3x3 卷积层
   - **Conv3_x**: 2 个残差块，每个残差块包含 2 个 3x3 卷积层
   - **Conv4_x**: 2 个残差块，每个残差块包含 2 个 3x3 卷积层
   - **Conv5_x**: 2 个残差块，每个残差块包含 2 个 3x3 卷积层
3. **平均池化层（Average Pooling）**
   - 1 层
4. **全连接层（Fully Connected Layer）**
   - 1 层
