# 状态注册表

后端和 App 共用的完整状态列表。AI 输出的 stateUpdate 必须从这里选值。

## 场景 (scene)

| ID | 名称 | 有白天 | 有夜晚 |
|----|------|:------:|:------:|
| living_room | 客厅 | ✅ | ✅ |
| bedroom | 卧室 | ✅ | ✅ |
| kitchen | 厨房 | ✅ | ✅ |
| bathroom | 卫生间 | ✅ | ✅ |
| balcony | 阳台 | ✅ | ✅ |

## 时间 (time_of_day)

| ID | 名称 |
|----|------|
| day | 白天 |
| night | 夜晚 |

## 视角 (view_mode)

| ID | 说明 | 触发条件 |
|----|------|---------|
| idle | 做自己的事，不看镜头 | 默认 / 15秒无互动 |
| engaged | 看向镜头，与用户互动 | 用户发消息 |

## 动作×表情×场景×时间 完整列表

### 客厅 (living_room)

| action | expression | day | night | 说明 |
|--------|-----------|:---:|:-----:|------|
| sitting_sofa | smile | ✅ | ✅ | 坐沙发看电视微笑 |
| sitting_sofa | laugh | ✅ | ✅ | 坐沙发看电视大笑 |
| sitting_sofa | pout | ✅ | ✅ | 坐沙发嘟嘴 |
| sitting_sofa | sleepy | ✅ | | 沙发午睡 |
| snacking_sofa | smile | | ✅ | 沙发吃零食 |
| hugging_plush | shy | ✅ | ✅ | 抱玩偶害羞 |
| hugging_plush | sad | | ✅ | 抱玩偶难过 |
| typing | focused | ✅ | ✅ | 打字专注 |
| typing | smile | ✅ | | 打字微笑 |
| writing_diary | neutral | | ✅ | 写日记 |
| reading | neutral | ✅ | | 看书 |
| gaming | excited | ✅ | ✅ | 玩游戏兴奋 |
| yoga | focused | ✅ | | 做瑜伽 |
| sitting_floor | neutral | ✅ | ✅ | 地上坐着发呆 |
| sitting_floor | bored | ✅ | | 趴地上无聊 |
| phone | smile | ✅ | ✅ | 看手机 |
| stretching | sleepy | ✅ | | 伸懒腰 |
| drinking | smile | ✅ | ✅ | 喝水 |
| standing | wave | ✅ | ✅ | 挥手 |
| standing | angry | ✅ | ✅ | 生气傲娇 |

### 卧室 (bedroom)

| action | expression | day | night | 说明 |
|--------|-----------|:---:|:-----:|------|
| lying_bed | sleepy | | ✅ | 侧躺看手机 |
| lying_bed | smile | ✅ | | 趴床上 |
| sitting_bed | neutral | ✅ | ✅ | 坐床上抱枕头 |
| waking_up | sleepy | ✅ | | 起床揉眼 |
| phone_bed | smile | | ✅ | 躺着玩手机 |
| phone_bed | laugh | | ✅ | 躺着看视频笑 |
| reading_bed | neutral | | ✅ | 靠床头看书 |
| hugging_plush | shy | | ✅ | 抱玩偶入睡 |
| sleeping | sleepy | | ✅ | 睡觉 |
| listening_music | smile | ✅ | ✅ | 听音乐 |
| making_bed | neutral | ✅ | | 整理床铺 |
| dressing | shy | ✅ | | 选衣服害羞 |
| dressing | smile | ✅ | | 试衣服 |
| grooming | focused | | ✅ | 护肤 |
| grooming | smile | ✅ | ✅ | 梳头 |
| standing_window | smile | ✅ | | 看窗外 |
| standing_window | neutral | | ✅ | 看夜景 |
| sitting_bed | sad | | ✅ | 难过 |
| sitting_bed | angry | ✅ | ✅ | 傲娇 |

### 厨房 (kitchen)

| action | expression | day | night | 说明 |
|--------|-----------|:---:|:-----:|------|
| cooking | focused | ✅ | ✅ | 炒菜 |
| cooking | smile | ✅ | ✅ | 煮汤 |
| chopping | focused | ✅ | ✅ | 切菜 |
| drinking_tea | smile | ✅ | ✅ | 喝茶 |
| washing | neutral | ✅ | ✅ | 洗碗 |
| fridge | smile | ✅ | ✅ | 开冰箱 |
| fridge_icecream | excited | ✅ | ✅ | 拿冰淇淋 |
| apron | smile | ✅ | ✅ | 系围裙 |
| eating | smile | ✅ | ✅ | 吃面 |
| boiling_water | neutral | ✅ | ✅ | 烧水 |
| plating | smile | ✅ | ✅ | 装盘 |

### 卫生间 (bathroom)

| action | expression | day | night | 说明 |
|--------|-----------|:---:|:-----:|------|
| brushing | neutral | ✅ | ✅ | 刷牙 |
| washing_face | smile | ✅ | ✅ | 洗脸 |
| mirror | shy | ✅ | ✅ | 照镜子整理头发 |
| towel | shy | ✅ | ✅ | 擦头发 |
| skincare | focused | ✅ | ✅ | 护肤 |
| laundry | neutral | ✅ | ✅ | 洗衣服 |
| shower | shy | ✅ | ✅ | 洗澡 |

### 阳台 (balcony)

| action | expression | day | night | 说明 |
|--------|-----------|:---:|:-----:|------|
| sitting_chair | smile | ✅ | ✅ | 坐椅子晒太阳 |
| watering | smile | ✅ | ✅ | 浇花 |
| leaning | neutral | ✅ | ✅ | 靠栏杆看远景 |
| leaning_rain | neutral | ✅ | | 看雨 |
| telescope | excited | ✅ | ✅ | 用望远镜 |
| stargazing | smile | | ✅ | 看星星 |
| blanket | sleepy | | ✅ | 裹毯子 |
| standing_sunset | smile | ✅ | | 看夕阳 |
| hanging_clothes | neutral | ✅ | | 晾衣服 |

## 服装 (outfit)

### 在家 (home)

| ID | 描述 |
|----|------|
| H01 | 粉色大卫衣+白短裤 |
| H02 | 黑色吊带+粉色短裤 |
| H03 | 白色T恤+灰色运动裤 |
| H04 | 紫色睡裙 |
| H05 | 粉色套装睡衣 |
| H06 | 条纹长袖+牛仔短裤 |
| H07 | 黑色短款T恤+白百褶裙 |
| H08 | 浅紫针织开衫+白背心 |
| H09 | 运动内衣+运动短裤 |
| H10 | 浴巾裹身 |

### 外出 (out)

| ID | 描述 |
|----|------|
| O01 | 白衬衫+粉色A字裙 |
| O02 | 黑色连衣裙 |
| O03 | 牛仔外套+白T+牛仔裤 |
| O04 | 粉色碎花连衣裙 |
| O05 | 运动套装 |
| O06 | JK制服 |
| O07 | 白色羽绒服+围巾 |
| O08 | 格子衬衫+短裙 |
| O09 | 吊带碎花裙+草帽 |
| O10 | 西装外套+短裤 |

## 图片文件命名规则

```
背景:     bg_{scene}_{time}.png
立绘:     standing_{expression}_{outfit_id}.png
一体图:   {scene}_{action}_{expression}_{viewmode}_{time}.png

示例:
bg_living_room_day.png
standing_smile_H01.png
living_room_sitting_sofa_smile_idle_day.png
living_room_sitting_sofa_smile_engaged_night.png
```

## 统计

| 类型 | 数量 |
|------|------|
| 背景 (5场景 × 2时间) | 10 |
| 绿幕立绘 (20套 × 4表情) | 80 |
| 一体图 (66组 × ~1.5时间 × 2视角) | ~200 |
| **总计** | **~290** |
