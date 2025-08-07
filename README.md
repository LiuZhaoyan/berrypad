# berrypad
> almost depend only on **tkinter**, environment configured using **uv**

## How to run
`uv run main.py`

## :rocket: Feature

- Support for `Markdown` syntax shortcuts
- Editor Split into text area and rendering area. The rendering area can be hidden
- Almost exclusively using tkinter

## Introduction to tkinter 
Tkinter is a built-in GUI library for Python, with the advantage of being easy to use, cross-platform (Windows/macOS/Linux), and requiring no additional dependencies, making it suitable for rapid development of small applications. However, there are natural boundaries to its features due to its design position:
- **advantages**:
1. lightweight: low memory footprint, fast startup;
2. low learning costs: the basic components (Text, Button, Menu, etc.) easy to master ;
3. cross-platform compatibility: can run on multiple systems without additional configuration.

- **Limitations**:
1. weak interface customization: the default style is simple (such as buttons, scrollbars, fixed style), complex layouts need to be manually adjusted;
2. general performance: processing large text (such as more than 10,000 lines of code) or high-frequency events (such as real-time syntax highlighting) may lag;
3. limited functionality: lack of built-in advanced components (such as code folding, terminal emulator, debugger), need to rely on third-party libraries or their own implementation.


## A simplest text editor
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