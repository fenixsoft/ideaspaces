# 任务列表模板
# 在提案阶段自动生成

## 状态概览

- 总任务: X
- 已完成: 0
- 进行中: 0
- 待开始: X

---

## 写作任务

- [ ] 写作-引言                                        #owner: author
- [ ] 写作-[章节名称]                                  #owner: author
- [ ] 写作-总结                                        #owner: author

---

## 实验任务

- [ ] 实验-[实验名称]                                 #owner: experimenter
  - 沙箱验证: pending

---

## 校审任务

- [ ] 校审-第1轮                                      #owner: reviewer
  - 依赖: 所有写作任务完成

---

## 整合任务

- [ ] 整合发布                                        #owner: lead
  - 依赖: 校审通过