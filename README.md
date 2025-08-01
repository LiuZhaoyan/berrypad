# BerryPad Markdown文本编辑器
> 利用python的tkinter创建

## tkinter库简介
Tkinter 是 Python 内置的 GUI 库，优势是?**?简单易用、跨平台（Windows/macOS/Linux）、无需额外依赖**，适合快速开发小型应用。但受限于设计定位，其特性也存在天然边界：

- **优势**：
1. 轻量级：内存占用低，启动速度快；
2. 学习成本低：基础组件（Text、Button、Menu 等）容易掌握；
3. 跨平台兼容性：无需额外配置即可在多系统运行。

- **限制**：
1. 界面定制能力弱：默认样式简陋（如按钮、滚动条风格固定），复杂布局需手动调整；
2. 性能一般：处理大文本（如万行以上代码）或高频事件（如实时语法高亮）时可能卡顿；
3. 功能扩展有限：缺乏内置的高级组件（如代码折叠、终端模拟器、调试器），需依赖第三方库或自行实现。



## 先创建一个最简单的文本编辑器
```python
    from tkinter import *
    import tkinter.filedialog as filedialog
    root=Tk("Text Editor")
    text=Text(root)
    text.grid()
    # 保存文件
    def saveas():
        global text
        t = text.get("1.0", "end-1c")
        savelocation=filedialog.asksaveasfilename()
        file1=open(savelocation, "w+")
        file1.write(t)
        file1.close()
    button=Button(root, text="Save", command=saveas)
    button.grid() 

    # 可选字体
    def FontHelvetica():
        global text
        text.config(font="Helvetica")
    def FontCourier():
        global text
        text.config(font="Courier")
    font=Menubutton(root, text="Font")
    font.grid() 
    font.menu=Menu(font, tearoff=0) 
    font["menu"]=font.menu
    Helvetica=IntVar()
    Courier=IntVar()
    font.menu.add_checkbutton(label="Courier", variable=Courier, 
    command=FontCourier)
    font.menu.add_checkbutton(label="Helvetica", variable=Helvetica,
    command=FontHelvetica) 

    root.mainloop()
```