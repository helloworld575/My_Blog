# 博客系统

## 项目介绍及说明

这是跟着《跟老齐学Django》一步步做下来博客管理系统的版本一，每章均分了一个分支。

#### 主要的功能实现有：
1. 用户管理
2. 博客栏目，文章及标签管理
3. 图片上传及管理

#### 主要技术实现有：
1. 借用django自带登录登出
2. 借用外包实现图片压缩显示（sorl.thumbnail）
3. 使用sqlite作为主数据库，并使用redis记录点赞，查看浏览人数，点赞人数，并借此实现评论数最多/点赞数最多等方式的推荐
4. 实现图片的上传及保存
5. 自定义超级管理员后台
6. 调用json传参
7. 分页管理
8. url传参
9. 调用slug解决中文url传参问题
10. 实现文章点赞功能
11. 实现头像上传管理功能（借用外包）
12. 图片的瀑布流显示

## 运行环境
python 3.6.3
django 1.11.7
awesome_slugify(解决中文url)
pillow 4.3.0
redis 2.10.6
sorl_thumbnail 12.4.1

### 借用外包：
1. markdown编辑器：https:github.com/pandao
2. 弹出框：https://github.com/qiwsir/DjangoPracticeProject 的layer
### 联系方式
###### 李志琛
###### 电话：18845897065
###### 邮箱：zhichenli6@gmail.com
