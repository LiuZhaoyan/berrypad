# BerryPad Markdown�ı��༭��
> ����python��tkinter����

## tkinter����
Tkinter �� Python ���õ� GUI �⣬������?**?�����á���ƽ̨��Windows/macOS/Linux���������������??**���ʺϿ��ٿ���С��Ӧ�á�����������ƶ�λ��������Ҳ������Ȼ�߽磺

??- **����**??��
1. ���������ڴ�ռ�õͣ������ٶȿ죻
2. ѧϰ�ɱ��ͣ����������Text��Button��Menu �ȣ��������գ�
3. ��ƽ̨�����ԣ�����������ü����ڶ�ϵͳ���С�

??- **����**??��
1. ���涨����������Ĭ����ʽ��ª���簴ť�����������̶��������Ӳ������ֶ�������
2. ����һ�㣺������ı������������ϴ��룩���Ƶ�¼�����ʵʱ�﷨������ʱ���ܿ��٣�
3. ������չ���ޣ�ȱ�����õĸ߼������������۵����ն�ģ�����������������������������������ʵ�֡�

|     ���Ĺ��ܵ�     |                       Tkinter ʵ�ַ���                     | �Ѷ� |
| :------------:| :----------------------------------------------------------: | ---: |
| �ı�������༭  | ʹ�� `tk.Text` �����֧�ֶ������롢������������ճ���Ȼ������ܡ� |   �� |
|    ʵʱԤ��    | ���� `Text` ����� `<<Modified>>` �¼������� Markdown ת������ `markdown` �⣩�������ʾ����һ `Text` �� `ScrolledText` ����С� |   �� |
|    �﷨����    | ���� `Text` ����� `tag` ���ƣ�Ϊ Markdown �﷨���� `# ����`��`**�Ӵ�**`���Զ�����ɫ/������ʽ�� |   �� |
|    ��������    | ʹ�� `PanedWindow` �� `Frame` + `grid` ���֣����ҷ������༭��/Ԥ�������� |   �� |
|    ��������    | �� `markdown2` �� `pypandoc` �⽫ Markdown ת��Ϊ HTML/PDF��ͨ�� `filedialog` ���档 |   �� |














## �ȴ���һ����򵥵��ı��༭��
```python
    from tkinter import *
    import tkinter.filedialog as filedialog
    root=Tk("Text Editor")
    text=Text(root)
    text.grid()
    # �����ļ�
    def saveas():
        global text
        t = text.get("1.0", "end-1c")
        savelocation=filedialog.asksaveasfilename()
        file1=open(savelocation, "w+")
        file1.write(t)
        file1.close()
    button=Button(root, text="Save", command=saveas)
    button.grid() 

    # ��ѡ����
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