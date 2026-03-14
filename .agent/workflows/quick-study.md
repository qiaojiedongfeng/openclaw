---
description: 快速学习项目架构 - 文件级详细认知工作流
---

# 快速学习项目架构工作流

本工作流帮助您在20小时内建立对中型项目的**文件级详细认知**,通过两阶段学习:
1. **自动扫描生成清单** - 快速建立项目文件地图
2. **交互式深度学习** - 逐个模块深入理解每个文件

---

## 📋 阶段一:自动扫描生成文件清单

### 目标
生成一个结构化的项目文件清单,包含所有核心模块的文件列表和简要说明。

### 步骤

#### 1. 识别核心模块
首先列出项目的主要源码目录:
```bash
ls -la src/
```

**识别核心模块**(通常包括):
- `agents/` - Agent相关逻辑
- `services/` - 服务层
- `models/` 或 `entities/` - 数据模型
- `api/` 或 `routes/` - API层
- `core/` 或 `lib/` - 核心库
- `controllers/` - 控制器
- `middleware/` - 中间件

**排除目录**:
- `tests/` 或 `__tests__/`
- `docs/`
- `scripts/`
- `utils/` (可选,看项目规模)
- `types/` (纯类型定义)

#### 2. 遍历每个核心模块
对每个核心模块目录,执行:

```bash
# 列出所有TypeScript/JavaScript文件
find src/agents -name "*.ts" -o -name "*.js" | grep -v ".test." | grep -v ".spec."
```

#### 3. 提取文件信息
对每个文件,提取:
- **文件路径**
- **顶部注释**(文件说明)
- **导出内容**(函数/类/常量名称)
- **主要依赖**(关键import)

使用 `view_file_outline` 工具快速获取文件结构。

#### 4. 生成清单文档
创建 `PROJECT_FILE_INVENTORY.md`,格式如下:

```markdown
# 项目文件清单

生成时间: YYYY-MM-DD HH:mm
项目路径: /path/to/project

## 📊 统计信息
- 核心模块数: X
- 核心文件数: Y
- 预计学习时间: Z 小时

---

## 模块: agents/

### agents/pi-embedded-runner/
- **run.ts** - Pi embedded agent主执行逻辑
  - 导出: `runPiEmbeddedAgent`, `AgentRunner`
  - 依赖: LLMService, ToolRegistry
  
- **config.ts** - Agent配置管理
  - 导出: `AgentConfig`, `loadConfig`
  - 依赖: ConfigLoader

### agents/agent-loop/
- **index.ts** - Agent循环控制器
  - 导出: `AgentLoop`, `LoopController`
  - 依赖: MessageHandler, StateManager

---

## 模块: services/

### services/llm/
- **llm-service.ts** - LLM调用封装
  - 导出: `LLMService`, `ChatCompletion`
  - 依赖: OpenAI, AnthropicAPI

...
```

#### 5. 输出清单
完成后,向用户展示:
- 清单文档路径
- 统计信息(模块数、文件数)
- 询问是否开始阶段二

---

## 🎓 阶段二:交互式深度学习

### 目标
按模块逐个深入学习每个文件,建立详细的功能认知。

### 学习节奏
- **单位**: 一个子模块(一个目录)
- **流程**: 逐个文件详细讲解 → 模块小结 → 下一个模块
- **时间**: 每个文件约10分钟

### 对每个文件的讲解格式(C详细版)

```
【文件 X/Y】src/agents/pi-embedded-runner/run.ts

📄 文件说明:
Pi embedded agent的主执行文件,负责agent的完整运行生命周期

📤 主要导出:
- runPiEmbeddedAgent(config: AgentConfig): Promise<void>
  主入口函数,初始化agent并启动运行循环
  
- AgentRunner class
  封装agent运行逻辑的类
  - constructor(config)
  - start(): 启动agent
  - stop(): 停止agent
  - handleMessage(msg): 处理消息

- processToolCalls(calls: ToolCall[]): Promise<ToolResult[]>
  处理工具调用结果,支持并行执行

📥 关键依赖:
- LLMService - LLM调用服务
- ToolRegistry - 工具注册表
- AgentState - Agent状态管理
- MessageQueue - 消息队列

🔄 核心流程:
1. 初始化配置和服务
2. 进入主循环:
   - 从消息队列获取消息
   - 调用LLM生成响应
   - 解析工具调用
   - 执行工具并收集结果
   - 更新状态
3. 处理退出条件

💡 关键点:
- 使用异步循环处理消息
- 支持工具并行执行
- 包含错误重试机制

---
您想要:
A. 继续下一个文件
B. 深入查看run.ts的具体实现
C. 跳过当前模块
D. 暂停学习(保存进度)
```

### 模块小结格式

```
✅ 模块小结: agents/pi-embedded-runner/

已学习文件: 3个
- run.ts - 主执行逻辑
- config.ts - 配置管理  
- types.ts - 类型定义

模块职责:
提供Pi embedded agent的完整运行环境,包括初始化、消息处理、工具调用等核心功能

模块依赖:
- services/llm - LLM调用
- services/tools - 工具执行
- core/state - 状态管理

关键收获:
1. Agent采用事件驱动的消息循环架构
2. 工具调用支持并行执行提升性能
3. 配置系统支持多环境切换

待深入的点:
- [ ] 错误重试机制的具体实现
- [ ] 状态持久化的方式

---
下一个模块: agents/agent-loop/
继续? (Y/n)
```

### 进度跟踪

在学习过程中,维护一个 `LEARNING_PROGRESS.md`:

```markdown
# 学习进度

开始时间: 2026-02-17 21:30
当前进度: 15/100 文件 (15%)
预计剩余时间: 14.2 小时

## 已完成模块
- [x] agents/pi-embedded-runner/ (3文件, 用时: 35分钟)
- [x] agents/agent-loop/ (2文件, 用时: 22分钟)

## 进行中
- [ ] services/llm/ (当前: llm-service.ts, 2/5)

## 待学习
- [ ] services/tools/
- [ ] services/state/
- [ ] core/
...

## 学习笔记
- agents模块采用统一的消息循环模式
- 所有service都实现了相同的生命周期接口
```

---

## 🎯 使用方式

### 启动工作流
```
/quick-study
```

### 工作流会询问
1. 是否使用默认核心模块列表,还是自定义?
2. 是否立即开始阶段二,还是只生成清单?

### 交互命令
在阶段二学习过程中,您可以:
- 输入 `A` 或 `next` - 继续下一个文件
- 输入 `B` 或 `deep` - 深入当前文件
- 输入 `C` 或 `skip` - 跳过当前模块
- 输入 `D` 或 `pause` - 暂停并保存进度
- 输入 `summary` - 查看当前模块小结
- 输入 `progress` - 查看整体进度

---

## ⏱️ 时间预估

### 中型项目 (100个核心文件)
- **阶段一**(自动扫描): 5-10分钟
- **阶段二**(交互学习): 15-18小时
  - 每个文件: 8-12分钟
  - 模块小结: 5分钟/模块
- **总结整理**: 2-3小时
- **总计**: 约20小时

### 小型项目 (30-50个文件)
- 总计: 5-8小时

### 大型项目 (200+个文件)
- 总计: 35-40小时
- 建议分多次完成

---

## 📝 输出产物

完成工作流后,您将拥有:

1. **PROJECT_FILE_INVENTORY.md**
   - 完整的文件清单
   - 按模块组织
   - 每个文件的导出和依赖

2. **LEARNING_PROGRESS.md**
   - 学习进度记录
   - 时间统计
   - 关键笔记

3. **MODULE_NOTES/** (可选)
   - 每个模块的详细笔记
   - 代码片段
   - 疑问和待深入的点

4. **脑海中的认知地图**
   - 知道每个文件的职责
   - 理解模块间的依赖关系
   - 能快速定位功能所在位置

---

## ✅ 成功标准

完成此工作流后,您应该能够:
- ✅ 说出项目有哪些核心模块,每个模块的职责
- ✅ 对于任意功能需求,快速定位到相关文件
- ✅ 理解每个核心文件导出的主要函数/类
- ✅ 画出模块间的依赖关系图
- ✅ 识别出项目的架构模式和设计理念
- ✅ 知道哪些地方需要进一步深入学习

---

## 💡 学习技巧

1. **做好笔记** - 记录关键发现和疑问
2. **画图辅助** - 用流程图/架构图可视化理解
3. **定期休息** - 每学习2小时休息15分钟
4. **及时总结** - 每完成一个大模块就做小结
5. **标记重点** - 标出需要深入的文件,后续专门学习
6. **关联学习** - 发现相似模式时,对比理解

---

## 🔄 后续学习

完成快速学习后,可以:
1. 使用 `/study` 工作流深入学习标记的重点文件
2. 阅读测试代码验证理解
3. 尝试修改代码加深印象
4. 查看Git历史了解演进过程
5. 绘制完整的架构图

---

## ⚠️ 注意事项

- **保持节奏** - 不要在单个文件上花费过多时间
- **先广度后深度** - 先建立全局认知,再深入细节
- **记录疑问** - 不理解的地方先记下来,不要打断节奏
- **灵活调整** - 根据实际情况调整学习速度
- **定期回顾** - 学习过程中定期回顾已学内容
