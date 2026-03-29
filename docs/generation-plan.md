# 图片生成计划

## 生成规则

- 每张一体图（人物+背景）都需要 idle 和 engaged 两个版本
- idle：小爱在做自己的事，视线看向场景内物体
- engaged：小爱看向镜头/屏幕外，与用户互动
- 背景图（空房间）每个场景一张，用于叠加绿幕立绘
- 绿幕立绘用于通用站姿等不依赖家具的动作

## 一、空房间背景（5 张）

| ID | 文件名 | prompt 关键词 |
|----|--------|-------------|
| BG01 | bg_living_room.png | cozy living room, sofa, TV, desk, pink white theme, afternoon light |
| BG02 | bg_bedroom.png | cozy bedroom, bed with purple sheets, wardrobe, vanity table, night lamp, warm light |
| BG03 | bg_kitchen.png | small kitchen, white tiles, stove, fridge, pink apron hanging, warm light |
| BG04 | bg_bathroom.png | clean bathroom, mirror, sink, shower area, white tiles, soft light |
| BG05 | bg_balcony.png | balcony with plants, small table and chairs, city view, sunset sky |

## 二、绿幕立绘 — 在家服装（10 套 × 常用动作）

### 在家服装列表

| 编号 | 服装描述 | prompt 关键词 |
|------|---------|-------------|
| H01 | 粉色大卫衣+白短裤 | oversized pastel pink hoodie, white shorts, barefoot |
| H02 | 黑色吊带+粉色短裤 | black camisole, pink shorts, barefoot |
| H03 | 白色T恤+灰色运动裤 | white t-shirt, grey sweatpants, barefoot |
| H04 | 紫色睡裙 | purple nightgown, knee length, barefoot |
| H05 | 粉色套装睡衣 | pink pajama set, button-up top and pants, barefoot |
| H06 | 条纹长袖+牛仔短裤 | striped long sleeve shirt, denim shorts, barefoot |
| H07 | 黑色短款T恤+百褶裙 | black crop top, white pleated mini skirt, barefoot |
| H08 | 浅紫针织开衫+白背心 | lavender cardigan over white tank top, shorts, barefoot |
| H09 | 运动内衣+运动短裤 | sports bra, athletic shorts, barefoot |
| H10 | 浴巾裹身 | wrapped in pink towel, wet hair, barefoot |

### 在家绿幕立绘（每套衣服 × 4 个表情 = 40 张）

动作：standing（站立）
表情：smile, neutral, shy, sleepy

| 文件名格式 | 说明 |
|-----------|------|
| standing_smile_H01.png | 粉卫衣站立微笑 |
| standing_neutral_H01.png | 粉卫衣站立自然 |
| standing_shy_H01.png | 粉卫衣站立害羞 |
| standing_sleepy_H01.png | 粉卫衣站立困倦 |
| ... 每套衣服同理 ... |

## 三、绿幕立绘 — 外出服装（10 套 × 4 表情 = 40 张）

| 编号 | 服装描述 | prompt 关键词 |
|------|---------|-------------|
| O01 | 白衬衫+粉色A字裙 | white blouse, pink A-line mini skirt, white mary janes |
| O02 | 黑色连衣裙 | black sleeveless dress, knee length, heeled sandals |
| O03 | 牛仔外套+白T+牛仔裤 | denim jacket, white t-shirt, blue jeans, sneakers |
| O04 | 粉色碎花连衣裙 | pink floral sundress, straw hat, sandals |
| O05 | 运动套装 | pink tracksuit, white sneakers |
| O06 | JK制服 | sailor uniform, navy blue skirt, white top, red ribbon |
| O07 | 白色羽绒服+围巾 | white puffy jacket, pink scarf, boots, winter |
| O08 | 格子衬衫+短裙 | plaid shirt tied at waist, black mini skirt, boots |
| O09 | 吊带碎花裙+草帽 | floral spaghetti strap dress, sun hat, summer |
| O10 | 西装外套+短裤 | oversized blazer, shorts, heels, cool style |

## 四、一体图 — 客厅场景（12 张 × 2 视角 = 24 张）

| ID | 动作 | 表情 | idle 视线 | engaged 视线 |
|----|------|------|----------|-------------|
| LR01 | sitting_sofa | smile | 看电视 | 看向镜头微笑 |
| LR02 | sitting_sofa | laugh | 看电视笑 | 看向镜头大笑 |
| LR03 | typing | focused | 看电脑屏幕 | 抬头看向镜头 |
| LR04 | typing | smile | 看电脑屏幕 | 抬头看向镜头微笑 |
| LR05 | reading | neutral | 看书 | 抬头看向镜头 |
| LR06 | gaming | excited | 看电视拿手柄 | 看向镜头兴奋 |
| LR07 | phone | smile | 看手机 | 抬头看向镜头 |
| LR08 | sitting_floor | neutral | 盘腿坐地上发呆 | 看向镜头 |
| LR09 | stretching | sleepy | 伸懒腰 | 看向镜头揉眼 |
| LR10 | drinking | smile | 喝水看窗外 | 看向镜头举杯 |
| LR11 | hugging_plush | shy | 抱玩偶看电视 | 抱玩偶看向镜头 |
| LR12 | standing | wave | — | 挥手看向镜头 |

## 五、一体图 — 卧室场景（10 张 × 2 = 20 张）

| ID | 动作 | 表情 | idle | engaged |
|----|------|------|------|---------|
| BR01 | lying_bed | sleepy | 侧躺看手机 | 抬头看向镜头 |
| BR02 | lying_bed | smile | 趴在床上 | 看向镜头微笑 |
| BR03 | sitting_bed | neutral | 坐床上抱枕头 | 看向镜头 |
| BR04 | waking_up | sleepy | 坐起来揉眼 | 看向镜头 |
| BR05 | dressing | shy | 对着衣柜选衣服 | 回头看向镜头害羞 |
| BR06 | grooming | focused | 梳妆台化妆 | 从镜子里看向镜头 |
| BR07 | phone_bed | smile | 躺着玩手机 | 看向镜头 |
| BR08 | reading_bed | neutral | 靠床头看书 | 看向镜头 |
| BR09 | hugging_plush | shy | 抱玩偶入睡 | 睁眼看向镜头 |
| BR10 | standing | smile | 站在窗边看外面 | 转身看向镜头 |

## 六、一体图 — 厨房场景（6 张 × 2 = 12 张）

| ID | 动作 | 表情 | idle | engaged |
|----|------|------|------|---------|
| KT01 | cooking | focused | 炒菜 | 回头看向镜头 |
| KT02 | chopping | focused | 切菜 | 抬头看向镜头 |
| KT03 | drinking_tea | smile | 端茶看窗外 | 看向镜头 |
| KT04 | washing | neutral | 洗碗 | 回头看向镜头 |
| KT05 | fridge | smile | 开冰箱找东西 | 回头看向镜头 |
| KT06 | apron | smile | 系围裙 | 看向镜头 |

## 七、一体图 — 卫生间场景（4 张 × 2 = 8 张）

| ID | 动作 | 表情 | idle | engaged |
|----|------|------|------|---------|
| BT01 | grooming | neutral | 刷牙 | 从镜子看向镜头 |
| BT02 | grooming | smile | 洗脸 | 从镜子看向镜头 |
| BT03 | mirror | shy | 照镜子整理头发 | 从镜子看向镜头 |
| BT04 | towel | shy | 擦头发 | 看向镜头害羞 |

## 八、一体图 — 阳台场景（6 张 × 2 = 12 张）

| ID | 动作 | 表情 | idle | engaged |
|----|------|------|------|---------|
| BL01 | sitting_chair | smile | 坐椅子晒太阳闭眼 | 睁眼看向镜头 |
| BL02 | watering | smile | 浇花 | 回头看向镜头 |
| BL03 | leaning | neutral | 靠栏杆看远景 | 转头看向镜头 |
| BL04 | telescope | excited | 用望远镜 | 放下望远镜看向镜头 |
| BL05 | blanket | sleepy | 裹毯子坐着 | 看向镜头 |
| BL06 | standing | smile | 站着看夕阳 | 转身看向镜头 |

## 汇总

| 类型 | 数量 |
|------|------|
| 空房间背景 | 5 |
| 绿幕立绘（在家 10 套 × 4 表情） | 40 |
| 绿幕立绘（外出 10 套 × 4 表情） | 40 |
| 一体图（5 场景共 38 组 × 2 视角） | 76 |
| **总计** | **~161 张** |

## 生成命令

```bash
# 全部生成（按顺序）
python scripts/batch_generate.py all

# 或分步生成
python scripts/batch_generate.py bg           # 先生成背景
python scripts/batch_generate.py sprite_home  # 在家立绘
python scripts/batch_generate.py sprite_out   # 外出立绘
python scripts/batch_generate.py scene_lr     # 客厅一体图
python scripts/batch_generate.py scene_br     # 卧室一体图
python scripts/batch_generate.py scene_kt     # 厨房一体图
python scripts/batch_generate.py scene_bt     # 卫生间一体图
python scripts/batch_generate.py scene_bl     # 阳台一体图
```

已生成的图片会自动跳过，可以中断后继续。
